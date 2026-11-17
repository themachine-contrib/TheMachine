---
title: Perplexity
area: connections
summary: 你的 Perplexity 对话、任务结果，以及额度不足时的提醒。
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## 读取的内容

你最近的 Perplexity 对话、每次 Perplexity 任务（Tasks）运行的结果，以及你的额度余额。当一段对话以待办的事结束，或某个任务带来新消息时，The Machine 可以把它变成待办。额度降到 2 或更少时，会提醒你一次；只有在你充值后再次变少时才会再次提醒。

它通过你已登录 Perplexity 的 OpenClaw 浏览器读取，大约每小时一次，时间在 7:00 到 22:00 之间。第一次读取会回溯一周。

## 可以执行的操作

什么也不做。它只读取。它从不向 Perplexity 提问，也从不修改、重命名或删除对话或任务。

## 连接

1. 在 OpenClaw 浏览器中登录一次 Perplexity：在那里打开 https://www.perplexity.ai/ 并登录。
2. 在控制面板中，打开 **连接**，然后选择 **其他**，再选择 Perplexity。在托管版 Machine 上，也可以在设置页面的 **更多来源** 下找到它。在自己的电脑上，也可以运行 `assistant connect perplexity`。

Perplexity 没有让应用登录来读取你对话的方式，所以它使用已登录的浏览器。你不需要任何密钥。

## 移除

在控制面板中，打开 **连接**，选择 Perplexity，再打开 **详情**，然后选择 **断开连接**。如果还要结束浏览器的访问，请在 OpenClaw 浏览器中退出 Perplexity。
