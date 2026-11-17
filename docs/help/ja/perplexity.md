---
title: Perplexity
area: connections
summary: Perplexity の会話、タスクの結果、クレジットが減ったときのお知らせ。
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## 読み取る内容

最近の Perplexity の会話、Perplexity のタスク（Tasks）が実行されるたびの結果、クレジット残高を読み取ります。会話がやるべきことで終わったときや、タスクが新しい情報を届けたときは、The Machine がそれを ToDo にできます。クレジットが 2 以下になると一度お知らせし、チャージしてから再び減るまで次のお知らせはしません。

Perplexity にサインインしている OpenClaw のブラウザを通して、7:00 から 22:00 の間に、だいたい 1 時間に 1 回読み取ります。最初の読み取りでは 1 週間前までさかのぼります。

## できること

何もしません。読み取るだけです。Perplexity に質問することはなく、会話やタスクを変更、名前変更、削除することもありません。

## 接続する

1. OpenClaw のブラウザで Perplexity に一度サインインします。そのブラウザで https://www.perplexity.ai/ を開いてサインインしてください。
2. ダッシュボードで**接続**を開き、**その他**から Perplexity を選びます。ホスト型のMachineでは、セットアップページの**その他のソース**からも選べます。自分のコンピューターでは、`assistant connect perplexity`を実行する方法もあります。

Perplexity には会話を読み取るアプリにサインインを許可する仕組みがないため、サインイン済みのブラウザを使います。キーは必要ありません。

## 削除する

ダッシュボードで Perplexity を開き、**詳細**から**接続を解除**を選びます。ブラウザのアクセスも終わらせるには、OpenClaw のブラウザで Perplexity からサインアウトしてください。
