"""Perplexity tests (connectors/perplexity.py): the browser read is canned; no browser, no live calls. It stores
threads and Task runs once, tells about low credits once per drop, and fails with safe labels."""
import datetime as dt
import json
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
from unittest.mock import patch

from connectors import perplexity
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors
import sources

NOW = '2026-11-16T12:00:00+00:00'
AT = int(dt.datetime(2026, 11, 16, 9, 0, tzinfo=dt.timezone.utc).timestamp())
ACCOUNT = dict(perplexity.SETUP['account'])


def page(balance=10.0):
    return {'threads': [{'id': 'fixture-thread-1', 'slug': 'plan-the-offsite-abc123', 'title': 'Plan the offsite', 'at': AT,
                         'turns': [{'q': 'Venues near the station?', 'a': 'Three options. **Book** before Friday.', 'at': AT}]}],
            'tasks': [{'id': 'fixture-task-1', 'title': 'Weekly market news', 'at': AT, 'schedule': 'Every Monday',
                       'slug': 'weekly-market-news-def456', 'text': 'Two new competitors launched.'}],
            'credits': {'balance': balance, 'currency': 'USD'}}


class FakeSource:
    def __init__(self, *pages):
        self.pages, self.calls = list(pages), []

    def read(self, since):
        self.calls.append(since)
        item = self.pages.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class PerplexityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        base = machine_sources_connectors.CONNECTOR_HELPERS
        self.helpers = types.SimpleNamespace(SourceError=sources.SourceError, Skips=base.Skips, iso=base.iso, now=lambda: NOW,
                                             local_tz=lambda: dt.timezone.utc, browser_read_failure=base.browser_read_failure,
                                             recover_browser=lambda *a, **k: False)

    def sync(self, *pages):
        source = FakeSource(*pages)
        result = perplexity.sync(self.store, {}, ACCOUNT, self.helpers, source)
        return result, source

    def test_threads_and_task_runs_are_stored_once(self):
        result, source = self.sync(page())
        self.assertEqual(result['events'], 2)
        events = {e['kind']: e for e in self.store.events([ACCOUNT['id']])}
        thread, task = events['perplexity.thread'], events['perplexity.task']
        self.assertEqual(thread['title'], 'Plan the offsite')
        self.assertIn('You: Venues near the station?', thread['body'])
        self.assertEqual(thread['metadata']['source_url'], 'https://www.perplexity.ai/search/plan-the-offsite-abc123')
        self.assertNotIn('fixture-thread-1', thread['source_id'] + thread['metadata']['conversation_id'])
        self.assertEqual(task['title'], 'Weekly market news')
        self.assertEqual(task['metadata']['schedule'], 'Every Monday')
        self.assertNotIn('perplexity.credits', events)
        # the first read goes back bootstrap_days; the next from the last read, with an hour's overlap
        self.assertEqual(source.calls[0], dt.datetime.fromisoformat(NOW).timestamp() - 7 * 86400)
        _, again = self.sync(page())
        self.assertEqual(len(self.store.events([ACCOUNT['id']])), 2)
        self.assertEqual(again.calls[0], dt.datetime.fromisoformat(NOW).timestamp() - 3600)

    def test_a_new_run_of_a_task_is_a_new_reminder(self):
        self.sync(page())
        later = page()
        later['tasks'][0].update(at=AT + 7 * 86400, text='One more launched.')
        self.sync(later)
        self.assertEqual(len([e for e in self.store.events([ACCOUNT['id']]) if e['kind'] == 'perplexity.task']), 2)

    def test_low_credits_tell_once_per_drop(self):
        self.sync(page(balance=1.5))
        low = [e for e in self.store.events([ACCOUNT['id']]) if e['kind'] == 'perplexity.credits']
        self.assertEqual(len(low), 1)
        self.assertIn('1.50 USD', low[0]['body'])
        self.sync(page(balance=1.2))
        self.assertEqual(len([e for e in self.store.events([ACCOUNT['id']]) if e['kind'] == 'perplexity.credits']), 1)
        self.sync(page(balance=20))
        self.assertNotIn('credits_low_since', self.store.checkpoint(ACCOUNT['id']))

    def test_odd_rows_are_skipped_not_fatal(self):
        bad = page()
        bad['threads'].append({'id': 'x', 'at': 'yesterday', 'turns': []})
        result, _ = self.sync(bad)
        self.assertEqual(result['skipped'], 1)
        self.assertEqual(result['events'], 2)

    def test_failures_keep_the_checkpoint(self):
        self.sync(page())
        state = self.store.checkpoint(ACCOUNT['id'])
        with self.assertRaises(sources.SourceError) as caught:
            self.sync(sources.SourceError('perplexity_signed_out'))
        self.assertEqual(str(caught.exception), 'perplexity_signed_out')
        self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)

    def test_no_reads_outside_active_hours(self):
        account = {**ACCOUNT, 'active_hours': [0, 1]}
        source = FakeSource(page())
        self.assertEqual(perplexity.sync(self.store, {}, account, self.helpers, source)['events'], 0)
        self.assertEqual(source.calls, [])

    def test_check_reads_without_storing(self):
        source = FakeSource(page())
        self.assertIsNone(perplexity.check({}, ACCOUNT, self.helpers, source))
        self.assertEqual(self.store.events([ACCOUNT['id']]), [])
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))


class BrowserReadTests(unittest.TestCase):
    """The browser read: only the lease, open, evaluate and close; signed out and busy as safe labels."""

    def setUp(self):
        base = machine_sources_connectors.CONNECTOR_HELPERS
        self.helpers = types.SimpleNamespace(SourceError=sources.SourceError, browser_read_failure=base.browser_read_failure,
                                             recover_browser=lambda *a, **k: False)
        self.commands = []

    def run_with(self, evaluate_out, claim=0):
        def fake(args, **kwargs):
            self.commands.append(args)
            if 'claim' in args:
                return subprocess.CompletedProcess(args, claim, '', '')
            if 'open' in args:
                return subprocess.CompletedProcess(args, 0, 'id: TAB1\n', '')
            if 'evaluate' in args:
                return subprocess.CompletedProcess(args, 0, json.dumps(evaluate_out), '')
            return subprocess.CompletedProcess(args, 0, '', '')
        with patch.object(perplexity.subprocess, 'run', side_effect=fake), patch.dict(perplexity.os.environ, {}, clear=False):
            perplexity.os.environ.pop('PERPLEXITY_BROWSER_CDP', None)
            return perplexity.Source({}, ACCOUNT, self.helpers).read(0)

    def test_reads_in_a_tab_it_closes(self):
        data = self.run_with(page())
        self.assertEqual(data['threads'][0]['slug'], 'plan-the-offsite-abc123')
        verbs = [next(v for v in ('claim', 'open', 'evaluate', 'close', 'release') if v in c) for c in self.commands]
        self.assertEqual(verbs, ['claim', 'open', 'evaluate', 'close', 'release'])
        script = next(c for c in self.commands if 'evaluate' in c)[-1]
        for write in ('DELETE', 'PUT', 'PATCH', '/delete', '/update', '/create'):
            self.assertNotIn(write, script)

    def test_signed_out_and_busy_are_safe_labels(self):
        with self.assertRaises(sources.SourceError) as caught:
            self.run_with({'signed_out': True})
        self.assertEqual(str(caught.exception), 'perplexity_signed_out')
        with self.assertRaises(sources.SourceError) as caught:
            self.run_with(page(), claim=3)
        self.assertEqual(str(caught.exception), 'perplexity_browser_busy')
        with self.assertRaises(sources.SourceError) as caught:
            self.run_with({'threads': 'nope', 'tasks': []})
        self.assertEqual(str(caught.exception), 'perplexity_invalid_page')


if __name__ == '__main__':
    unittest.main()
