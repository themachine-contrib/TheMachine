---
title: Perplexity
area: connections
summary: Je Perplexity-gesprekken, resultaten van taken en een seintje als je tegoed opraakt.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## Wat er wordt gelezen

Je recente Perplexity-gesprekken, de resultaten telkens als een van je Perplexity-taken (Tasks) draait, en je tegoed. Eindigt een gesprek in iets om te doen, of brengt een taak nieuws, dan kan The Machine er een to-do van maken. Zakt je tegoed tot 2 of minder, dan laat hij het je één keer weten, en pas opnieuw nadat je hebt bijgeladen en het weer laag staat.

Hij leest via de OpenClaw-browser waarin je bij Perplexity bent aangemeld, ongeveer één keer per uur, tussen 7:00 en 22:00. De eerste keer leest hij een week terug.

## Wat ermee kan

Niets. Hij leest alleen. Hij vraagt Perplexity nooit iets, en wijzigt, hernoemt of verwijdert nooit een gesprek of een taak.

## Koppelen

1. Meld je één keer aan bij Perplexity in de OpenClaw-browser: open daar https://www.perplexity.ai/ en meld je aan.
2. Open in het dashboard **Koppelingen**, dan **Andere**, en kies Perplexity. Op een gehoste Machine staat deze optie ook op de instelpagina, onder **Meer bronnen**. Op je eigen computer kun je ook `assistant connect perplexity` uitvoeren.

Perplexity heeft geen manier om een app aan te melden die je gesprekken leest, dus gebruikt hij de aangemelde browser. Je hebt geen sleutel nodig.

## Verwijderen

Open in het dashboard Perplexity via **Koppelingen**, kies **Details** en vervolgens **Ontkoppelen**. Wil je ook de toegang van de browser beëindigen, meld je dan af bij Perplexity in de OpenClaw-browser.
