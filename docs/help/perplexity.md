---
title: Perplexity
area: connections
summary: Your Perplexity conversations, Task results and a heads-up when credits run low.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
---
## What it reads

Your recent Perplexity conversations, the results each time one of your Perplexity Tasks runs, and your credit balance. When a conversation ends in something to do, or a Task brings news, The Machine can make a to-do of it. When your credits drop to 2 or less, it tells you once, and again only after you topped up and they ran low again.

It reads through the OpenClaw browser you are signed in to Perplexity in, about once an hour, between 7:00 and 22:00. The first read goes back a week.

## What it can do

Nothing. It only reads. It never asks Perplexity anything, and never changes, renames or deletes a conversation or a Task.

## Connect it

1. Sign in to Perplexity once in the OpenClaw browser: open https://www.perplexity.ai/ there and sign in.
2. In the dashboard, open **Connections**, then **Other**, and pick Perplexity. On a hosted Machine, the setup page has it too, under **More sources**. On your own computer, you can also run `assistant connect perplexity`.

Perplexity has no way to sign in an app to read your conversations, so it uses the signed-in browser. You don't need a key.

## Remove it

In the dashboard: **Connections**, open Perplexity, **Details**, then **Disconnect**. To end the browser's access too, sign out of Perplexity in the OpenClaw browser.
