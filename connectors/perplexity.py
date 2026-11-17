"""Perplexity: your recent conversations (threads), the results of your Perplexity Tasks (scheduled searches), and a
heads-up when your credits run low, for the account signed in to the OpenClaw browser.

Perplexity has no OAuth and no API that reads a person's threads, Tasks or credit balance (its API only answers new
questions, with a key billed per request). So this reads the way linkedin.py and x.py do: the same requests
perplexity.ai's own pages make, from one tab of the signed-in OpenClaw browser parked on perplexity.ai/robots.txt. No
key, no cookies leaving the browser, nothing asked, sent, renamed or deleted. Sign in once in that browser
(`openclaw browser --browser-profile openclaw open https://www.perplexity.ai/`). One account:

    {"id": "me-perplexity", "service": "perplexity", "transport": "perplexity-web", "boundary": "work:Acme",
     "poll_seconds": 3600}

Optional: "credits_low" (the balance at or under which it tells you, default 2), "active_hours": [7, 22] (local
time), "browser_profile" / "browser_cdp" (a browser of its own; else PERPLEXITY_BROWSER_PROFILE / _CDP, else
"openclaw"). Reviews decide which conversations end in a to-do; this only stores them.
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READ_HOURS = (7, 22)
KINDS = {'perplexity.thread': 'Perplexity', 'perplexity.task': 'Perplexity Task', 'perplexity.credits': 'Perplexity credits'}
# How each kind reads in the message viewer and the app its link opens in (docs/adding-a-source.md, "How a message reads")
VIEWS = {'perplexity.thread': 'chat', 'perplexity.task': 'card', 'perplexity.credits': 'notification'}
APP = 'Perplexity'
SITE = 'https://www.perplexity.ai'
NEUTRAL_URL = SITE + '/robots.txt'
CREDITS_LOW = 2.0
SETUP = {'label': 'Perplexity', 'what': 'Your Perplexity conversations, Task results and low-credit alerts.',
         'account': {'id': 'me-perplexity', 'service': 'perplexity', 'transport': 'perplexity-web', 'boundary': 'work', 'poll_seconds': 3600},
         'browser': 'perplexity',
         'browser_env': {'browser_profile': 'PERPLEXITY_BROWSER_PROFILE', 'browser_cdp': 'PERPLEXITY_BROWSER_CDP'},
         'hints': {'perplexity_signed_out': 'the browser it reads with is not signed in to Perplexity; sign in there, then connect again',
                   'perplexity_browser_busy': 'the shared browser is busy; it reads again soon'},
         'no_oauth': 'Perplexity offers no OAuth and no API for reading threads, Tasks or credits, so it reads through the signed-in browser.',
         'note': "Sign in to Perplexity once in The Machine's browser first: https://www.perplexity.ai/"}

# Runs in the perplexity.ai tab: the web app's own read requests (GET or list queries only), shaped into plain rows.
READ_JS = r'''async () => {
  const since = __SINCE__;
  const get = async (path, body) => {
    const r = await fetch(path, body ? {method: 'POST', credentials: 'include', headers: {'content-type': 'application/json'}, body: JSON.stringify(body)}
                                     : {credentials: 'include'});
    if (r.status === 401 || r.status === 403) throw new Error('signed out');
    if (!r.ok) return null;
    try { return await r.json(); } catch (e) { return null; }
  };
  const me = await get('/api/auth/session');
  if (!me || !me.user) return {signed_out: true};
  const secs = v => typeof v === 'number' ? (v > 1e12 ? Math.floor(v / 1000) : Math.floor(v)) : (v ? Math.floor(Date.parse(v) / 1000) : 0);
  const text = e => String(e && (e.answer_text || e.answer || e.text || '') || '');
  const list = await get('/rest/thread/list_ask_threads?version=2.18&source=default', {limit: 20, offset: 0, ascending: false, search_term: ''}) || [];
  const threads = [];
  for (const t of (Array.isArray(list) ? list : list.threads || [])) {
    const at = secs(t.last_query_datetime || t.updated_datetime || t.created_datetime);
    if (!t.slug || at < since) continue;
    const full = await get('/rest/thread/' + encodeURIComponent(t.slug) + '?version=2.18&source=default&limit=20');
    const entries = (full && (full.entries || full.thread)) || [];
    threads.push({id: String(t.uuid || t.slug), slug: String(t.slug), title: String(t.title || t.query_str || ''), at,
      turns: entries.map(e => ({q: String(e.query_str || ''), a: text(e), at: secs(e.updated_datetime || e.entry_updated_datetime)}))});
  }
  const tasks = [];
  const runs = await get('/rest/tasks/list?version=2.18&source=default') || [];
  for (const t of (Array.isArray(runs) ? runs : runs.tasks || [])) {
    const at = secs(t.last_run_datetime || t.last_run_at || t.updated_datetime);
    if (!t.uuid && !t.id || at < since) continue;
    tasks.push({id: String(t.uuid || t.id), title: String(t.title || t.query || ''), at, schedule: String(t.schedule_text || t.schedule || ''),
      slug: String(t.last_thread_slug || t.thread_slug || ''), text: text(t.last_result || t)});
  }
  const s = await get('/rest/user/settings?version=2.18&source=default') || {};
  const c = s.api_credits || s.credits || {};
  const balance = typeof c === 'number' ? c : (c.balance ?? c.remaining ?? null);
  return {threads, tasks, credits: typeof balance === 'number' ? {balance, currency: String(c.currency || '')} : null};
}'''


class Source:
    """One read in one tab of the shared browser, under its lease; the tab is always closed again."""

    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        env = {**os.environ, **{var: account[f] for f, var in SETUP['browser_env'].items() if account.get(f)}}
        self.profile, self.cdp = env.get('PERPLEXITY_BROWSER_PROFILE') or 'openclaw', env.get('PERPLEXITY_BROWSER_CDP') or ''

    def oc(self, *args, timeout=120):
        done = subprocess.run(['openclaw', 'browser', '--browser-profile', self.profile, *args], capture_output=True, text=True, timeout=timeout)
        if done.returncode:
            raise RuntimeError('browser_command_failed ' + (done.stderr or done.stdout)[:300])
        return done.stdout

    def lease(self, action, owner):
        script = Path(self.config.get('browser_lease_script') or ROOT / 'integrations/browser-lease.py').expanduser()
        extra = [] if action == 'release' else ['--minutes', '10']
        return subprocess.run([sys.executable, str(script), action, '--owner', owner, *extra], capture_output=True, text=True, timeout=30)

    def evaluate(self, js):
        """The script's JSON value from a fresh perplexity.ai tab."""
        SourceError = self.helpers.SourceError
        owner = 'perplexity-' + uuid.uuid4().hex[:8]
        try:
            claim = self.lease('claim', owner)
        except (OSError, subprocess.SubprocessError):
            raise SourceError('perplexity_browser_busy', retry_after=600) from None
        if claim.returncode:
            raise SourceError('perplexity_browser_busy', retry_after=600)
        target = None
        try:
            if self.cdp:
                sys.path.insert(0, str(ROOT / 'integrations'))
                import browser_cdp
                target = browser_cdp.open_background_tab(self.cdp, NEUTRAL_URL)
                return browser_cdp.evaluate(self.cdp, target, js, 90000)
            receipt = self.oc('open', '--label', owner, NEUTRAL_URL + '#the-machine-' + owner)
            found = re.search(r'^(?:id|tab):\s*(\S+)', receipt, re.M)
            if not found:
                raise RuntimeError('browser_command_failed no_tab_receipt')
            target = found[1]
            out = self.oc('evaluate', '--target-id', target, '--timeout-ms', '90000', '--fn', js, timeout=150)
            return json.loads(out[out.find('{'):])
        except subprocess.TimeoutExpired:
            raise SourceError('perplexity_browser_stalled', retry_after=900) from None
        except ValueError:
            raise SourceError('perplexity_invalid_json') from None
        except Exception as error:
            text = str(error).lower()
            if 'signed out' in text:
                raise SourceError('perplexity_signed_out', retry_after=3600) from None
            code = self.helpers.browser_read_failure('perplexity', text)
            if code.endswith('_browser_unreachable'):
                self.helpers.recover_browser(self.profile, own_cdp=bool(self.cdp), config=self.config)
                raise SourceError(code, retry_after=300) from None
            raise SourceError(code, retry_after=900) from None
        finally:
            try:
                if target and self.cdp:
                    browser_cdp.close_tab(self.cdp, target)
                elif target:
                    self.oc('close', target, timeout=90)
            except Exception:
                pass  # the browser's own tab cleanup takes it later
            try:
                self.lease('release', owner)
            except (OSError, subprocess.SubprocessError):
                pass  # the ten-minute lease runs out by itself

    def read(self, since):
        data = self.evaluate(READ_JS.replace('__SINCE__', str(int(since))))
        if not isinstance(data, dict):
            raise self.helpers.SourceError('perplexity_invalid_page')
        if data.get('signed_out'):
            raise self.helpers.SourceError('perplexity_signed_out', retry_after=3600)
        if not isinstance(data.get('threads'), list) or not isinstance(data.get('tasks'), list):
            raise self.helpers.SourceError('perplexity_invalid_page')
        return data


def _hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _when(raw, helpers):
    at = raw.get('at')
    if isinstance(at, bool) or not isinstance(at, (int, float)) or at <= 0:
        raise helpers.SourceError('perplexity_invalid_item')
    return helpers.iso(at)


def _link(slug):
    return SITE + '/search/' + re.sub(r'[^A-Za-z0-9._-]', '', slug) if slug else SITE + '/library'


def thread_event(account, raw, helpers):
    if not isinstance(raw.get('id'), str) or not raw['id'] or not isinstance(raw.get('turns'), list):
        raise helpers.SourceError('perplexity_invalid_item')
    turns = [t for t in raw['turns'] if isinstance(t, dict)]
    body = '\n\n'.join(('You: ' + str(t.get('q') or '').strip() + '\n\nPerplexity: ' + str(t.get('a') or '').strip()).strip()
                       for t in turns)
    title = str(raw.get('title') or (turns[0].get('q') if turns else '') or 'Perplexity conversation').strip()
    metadata = {'conversation_id': _hash('thread:' + raw['id']), 'chat_name': title[:200], 'from_me': True, 'from': 'You',
                'sender_display': 'You', 'turns': len(turns), 'source_url': _link(raw.get('slug') or ''),
                'truncated': len(body) > 40000}
    return {'account_id': account['id'], 'source_id': _hash('thread:' + raw['id']), 'kind': 'perplexity.thread',
            'occurred_at': _when(raw, helpers), 'title': title[:1000], 'body': body[:40000], 'metadata': metadata, 'deleted': False}


def task_event(account, raw, helpers):
    if not isinstance(raw.get('id'), str) or not raw['id']:
        raise helpers.SourceError('perplexity_invalid_item')
    title = str(raw.get('title') or 'Perplexity Task').strip()
    occurred = _when(raw, helpers)
    metadata = {'task_id': _hash('task:' + raw['id']), 'schedule': str(raw.get('schedule') or '')[:200],
                'sender_display': 'Perplexity', 'source_url': _link(raw.get('slug') or '')}
    # one event per run: each run of a Task is its own reminder
    return {'account_id': account['id'], 'source_id': _hash('task:' + raw['id'] + ':' + occurred), 'kind': 'perplexity.task',
            'occurred_at': occurred, 'title': title[:1000], 'body': str(raw.get('text') or '')[:40000], 'metadata': metadata,
            'deleted': False}


def credits_event(account, credits, state, threshold, helpers):
    """One alert per drop under the threshold; it goes again only after the balance came back up."""
    balance = credits.get('balance') if isinstance(credits, dict) else None
    if isinstance(balance, bool) or not isinstance(balance, (int, float)):
        return None
    if balance > threshold:
        state.pop('credits_low_since', None)
        return None
    since = state.setdefault('credits_low_since', helpers.now())
    currency = str(credits.get('currency') or '').strip()
    amount = ('{:.2f} {}'.format(balance, currency)).strip()
    return {'account_id': account['id'], 'source_id': _hash('credits-low:' + account['id'] + ':' + since), 'kind': 'perplexity.credits',
            'occurred_at': since, 'title': 'Perplexity credits are running low',
            'body': 'Balance left: ' + amount + '. Top up at ' + SITE + '/account/api/billing',
            'metadata': {'balance': balance, 'sender_display': 'Perplexity', 'source_url': SITE + '/account/api/billing'}, 'deleted': False}


def check(config, account, helpers, source=None):
    """A real read of the last day, without storing anything."""
    (source or Source(config, account, helpers)).read(dt.datetime.fromisoformat(helpers.now()).timestamp() - 86400)


def sync(store, config, account, helpers, source=None):
    current = dt.datetime.fromisoformat(helpers.now())
    start, end = account.get('active_hours', READ_HOURS)
    if not start <= current.astimezone(helpers.local_tz()).hour < end:
        return {'mode': 'incremental', 'events': 0}
    state = store.checkpoint(account['id']) or {}
    first = (current - dt.timedelta(days=int(config.get('bootstrap_days', 7)))).timestamp()
    since = max(0, state['read_until'] - 3600) if state.get('read_until') else first
    data = (source or Source(config, account, helpers)).read(since)
    skipped = helpers.Skips('perplexity_invalid_item')
    found = [e for e, _ in skipped.every(data['threads'], lambda raw: thread_event(account, raw, helpers))]
    found += [e for e, _ in skipped.every(data['tasks'], lambda raw: task_event(account, raw, helpers))]
    skipped.check()
    low = credits_event(account, data.get('credits'), state, float(account.get('credits_low', CREDITS_LOW)), helpers)
    if low:
        found.append(low)
    found = list({e['source_id']: e for e in found}.values())
    state.update(mode='incremental', read_until=int(current.timestamp()))
    skipped.note(state)
    store.commit_page(account['id'], state, found)
    return {'mode': 'incremental', 'events': len(found), 'skipped': sum(skipped.values())}
