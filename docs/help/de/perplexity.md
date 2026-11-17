---
title: Perplexity
area: connections
summary: Deine Perplexity-Unterhaltungen, Task-Ergebnisse und ein Hinweis, wenn das Guthaben knapp wird.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## Was gelesen wird

Deine letzten Perplexity-Unterhaltungen, die Ergebnisse jedes Mal, wenn einer deiner Perplexity-Tasks läuft, und dein Guthaben. Endet eine Unterhaltung mit etwas zu erledigen oder bringt ein Task Neuigkeiten, kann The Machine daraus eine Aufgabe machen. Fällt dein Guthaben auf 2 oder weniger, sagt sie es dir einmal, und erst wieder, nachdem du aufgeladen hast und es erneut knapp wird.

Sie liest über den OpenClaw-Browser, in dem du bei Perplexity angemeldet bist, etwa einmal pro Stunde zwischen 7:00 und 22:00. Beim ersten Mal liest sie eine Woche zurück.

## Was möglich ist

Nichts. Sie liest nur. Sie fragt Perplexity nie etwas und ändert, benennt oder löscht nie eine Unterhaltung oder einen Task.

## Verbindung herstellen

1. Melde dich einmal im OpenClaw-Browser bei Perplexity an: Öffne dort https://www.perplexity.ai/ und melde dich an.
2. Öffne im Dashboard **Verbindungen** und dann **Andere**. Wähle Perplexity aus. Auf einer gehosteten Machine findest du die Einrichtung auch unter **Weitere Quellen**. Auf deinem eigenen Computer kannst du auch `assistant connect perplexity` ausführen.

Perplexity bietet keine Möglichkeit, eine App zum Lesen deiner Unterhaltungen anzumelden, deshalb nutzt sie den angemeldeten Browser. Du brauchst keinen Schlüssel.

## Verbindung entfernen

Im Dashboard: Öffne **Verbindungen**, wähle Perplexity und dann **Details** und **Trennen**. Um auch den Zugriff des Browsers zu beenden, melde dich im OpenClaw-Browser bei Perplexity ab.
