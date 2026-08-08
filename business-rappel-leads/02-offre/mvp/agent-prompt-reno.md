# Prompt agent vocal — Rénovation énergétique / isolation

Même structure que [agent-prompt-pac.md](agent-prompt-pac.md). Remplacer le bloc questions par :

1. Code postal / ville
2. Propriétaire ?
3. Type de travaux : isolation, menuiseries, ventilation, rénovation globale, autre ?
4. Logement : maison / appartement ?
5. Délai : immédiat, <3 mois, plus tard ?
6. Aides déjà en cours (MaPrimeRénov’ / autre) ?
7. Créneau RDV parmi {{calendar_slots}}

Qualification OK si : dans zone, propriétaire, délai ≤ 3 mois, projet concret.
