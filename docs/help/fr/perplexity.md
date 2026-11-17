---
title: Perplexity
area: connections
summary: Vos conversations Perplexity, les résultats de vos Tasks et une alerte quand les crédits baissent.
covers: connector:perplexity
code: connectors/perplexity.py
site: More sources
translated: ae347f8303c191ae
---
## Ce qu’elle lit

Vos conversations Perplexity récentes, les résultats à chaque exécution d’une de vos Tasks Perplexity, et votre solde de crédits. Quand une conversation se termine par quelque chose à faire, ou qu’une Task apporte du nouveau, The Machine peut en faire une tâche. Quand vos crédits tombent à 2 ou moins, elle vous prévient une fois, puis à nouveau seulement après une recharge suivie d’une nouvelle baisse.

Elle lit via le navigateur OpenClaw dans lequel vous êtes connecté à Perplexity, environ une fois par heure, entre 7 h et 22 h. La première lecture remonte d’une semaine.

## Ce qu’elle peut faire

Rien. Elle se contente de lire. Elle ne pose jamais de question à Perplexity et ne modifie, ne renomme ni ne supprime jamais une conversation ou une Task.

## Connecter Perplexity

1. Connectez-vous une fois à Perplexity dans le navigateur OpenClaw : ouvrez-y https://www.perplexity.ai/ et connectez-vous.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **Autres**, et choisissez **Perplexity**. Sur une Machine hébergée, la page de configuration propose aussi cette option, sous **Plus de sources**. Sur votre propre ordinateur, vous pouvez aussi exécuter `assistant connect perplexity`.

Perplexity ne permet pas d’autoriser une app à lire vos conversations : elle utilise donc le navigateur connecté. Aucune clé n’est nécessaire.

## Supprimer la connexion

Dans le tableau de bord : ouvrez Perplexity depuis **Connexions**, puis **Détails**, et enfin **Déconnecter**. Pour retirer aussi l’accès du navigateur, déconnectez-vous de Perplexity dans le navigateur OpenClaw.
