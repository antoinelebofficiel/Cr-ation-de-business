# Prompt agent vocal — Solaire / photovoltaïque

Même structure que [agent-prompt-pac.md](agent-prompt-pac.md). Remplacer le bloc questions par :

1. Code postal / ville
2. Propriétaire ?
3. Type de toiture / orientation connue ?
4. Facture électricité mensuelle approx. (ordre de grandeur) ?
5. Délai : immédiat, <3 mois, plus tard ?
6. A déjà un devis solaire ?
7. Créneau RDV parmi {{calendar_slots}}

Qualification OK si : dans zone, propriétaire, délai ≤ 3 mois.
