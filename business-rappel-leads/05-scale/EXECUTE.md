# Exécution scale 20 clients

## Entrée
Phase 0 validée (1 close ou ≥8 démos douleur).

## Boucle
1. 60 appels/jour (`daily-ritual.md`)
2. Chaque close → ligne dans `client-roster-20.csv` + onboarding 48h
3. Suivre MRR dans `daily-tracker.csv` colonne `mrr_cumule_eur`
4. Upsells seulement après J+14 (`upsells.md`)

## Jalons
| Jalon | Preuve |
|---|---|
| 3 clients | 3 lignes CLIENT/ESSAI avec `mrr_eur` |
| 10 clients | MRR ≥ 8–10k |
| 20 clients | MRR ≥ 19,8k ou CA mois ≥ 20k |

## Definition of Done
- [ ] 20 lignes roster remplies (statut ESSAI ou CLIENT)
- [ ] Somme `mrr_eur` ≥ 19800 **ou** CA encaissé mois calendaire ≥ 20000
- [ ] Churn 30j < 15%
