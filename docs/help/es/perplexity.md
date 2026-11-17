---
title: Perplexity
area: connections
summary: Tus conversaciones de Perplexity, resultados de Tasks y un aviso cuando quedan pocos créditos.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## Qué lee

Tus conversaciones recientes de Perplexity, los resultados cada vez que se ejecuta una de tus Tasks de Perplexity y tu saldo de créditos. Cuando una conversación termina en algo por hacer, o una Task trae novedades, The Machine puede convertirlo en una tarea. Cuando tus créditos bajan a 2 o menos, te avisa una vez, y de nuevo solo después de recargar y volver a bajar.

Lee a través del navegador de OpenClaw en el que tienes sesión iniciada en Perplexity, más o menos una vez por hora, entre las 7:00 y las 22:00. La primera lectura abarca una semana atrás.

## Qué puede hacer

Nada. Solo lee. Nunca le pregunta nada a Perplexity, ni cambia, renombra o borra una conversación o una Task.

## Conectarlo

1. Inicia sesión una vez en Perplexity en el navegador de OpenClaw: abre allí https://www.perplexity.ai/ e inicia sesión.
2. En el panel, abre **Conexiones** y luego **Otras**. Después, elige **Perplexity**. Si usas una Machine alojada, también encontrarás esta opción en la página de configuración, en **Más fuentes**. En tu propio ordenador, también puedes ejecutar `assistant connect perplexity`.

Perplexity no ofrece una forma de autorizar una app para leer tus conversaciones, así que usa el navegador con la sesión iniciada. No necesitas ninguna clave.

## Desconectarlo

En el panel: abre **Conexiones**, selecciona Perplexity y ve a **Detalles**. Después, selecciona **Desconectar**. Para quitar también el acceso del navegador, cierra la sesión de Perplexity en el navegador de OpenClaw.
