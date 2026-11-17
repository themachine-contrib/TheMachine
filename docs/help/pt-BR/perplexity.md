---
title: Perplexity
area: connections
summary: Suas conversas do Perplexity, resultados de Tasks e um aviso quando os créditos estão acabando.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## O que ela lê

Suas conversas recentes do Perplexity, os resultados toda vez que uma das suas Tasks do Perplexity é executada e seu saldo de créditos. Quando uma conversa termina em algo a fazer, ou uma Task traz novidades, a The Machine pode transformar isso em uma tarefa. Quando seus créditos caem para 2 ou menos, ela avisa uma vez, e de novo só depois que você recarregar e eles caírem outra vez.

Ela lê pelo navegador do OpenClaw em que você entrou no Perplexity, mais ou menos uma vez por hora, entre 7:00 e 22:00. A primeira leitura volta uma semana.

## O que ela pode fazer

Nada. Ela só lê. Nunca pergunta nada ao Perplexity e nunca altera, renomeia ou apaga uma conversa ou uma Task.

## Conectar

1. Entre uma vez no Perplexity pelo navegador do OpenClaw: abra https://www.perplexity.ai/ nele e faça login.
2. No painel, abra **Conexões**, depois **Outras** e selecione Perplexity. Em uma Machine hospedada, a página de configuração também tem essa opção, em **Mais fontes**. No seu computador, você também pode executar `assistant connect perplexity`.

O Perplexity não oferece um jeito de autorizar um app a ler suas conversas, então ela usa o navegador conectado. Você não precisa de nenhuma chave.

## Remover

No painel: abra o Perplexity em **Conexões**, selecione **Detalhes** e depois **Desconectar**. Para tirar também o acesso do navegador, saia do Perplexity no navegador do OpenClaw.
