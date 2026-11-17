---
title: Perplexity
area: connections
summary: Le tue conversazioni Perplexity, i risultati dei Task e un avviso quando i crediti stanno finendo.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## Cosa legge

Le tue conversazioni recenti su Perplexity, i risultati ogni volta che uno dei tuoi Task di Perplexity viene eseguito e il saldo dei crediti. Quando una conversazione finisce con qualcosa da fare, o un Task porta novità, The Machine può crearne un’attività. Quando i crediti scendono a 2 o meno, te lo dice una volta, e di nuovo solo dopo che hai ricaricato e sono scesi ancora.

Legge tramite il browser OpenClaw in cui hai effettuato l’accesso a Perplexity, circa una volta all’ora, tra le 7:00 e le 22:00. La prima lettura risale a una settimana prima.

## Cosa può fare

Niente. Legge soltanto. Non chiede mai nulla a Perplexity e non modifica, rinomina o elimina mai una conversazione o un Task.

## Connettilo

1. Accedi una volta a Perplexity nel browser OpenClaw: apri lì https://www.perplexity.ai/ ed effettua l’accesso.
2. Nella dashboard, apri **Connessioni**, poi **Altro** e scegli Perplexity. Su una Machine ospitata, trovi la configurazione anche nella pagina di setup, sotto **Altre fonti**. Sul tuo computer puoi anche eseguire `assistant connect perplexity`.

Perplexity non offre un modo per autorizzare un’app a leggere le tue conversazioni, quindi usa il browser in cui hai effettuato l’accesso. Non serve nessuna chiave.

## Rimuovilo

Nella dashboard: apri **Connessioni**, seleziona Perplexity, poi **Dettagli** e **Disconnetti**. Per togliere anche l’accesso del browser, esci da Perplexity nel browser OpenClaw.
