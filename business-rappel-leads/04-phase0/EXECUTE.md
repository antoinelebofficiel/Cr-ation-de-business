# Exécution Phase 0 — adaptée facteur

Contrainte : **facteur jusqu’à mi-septembre** → Phase 0 en **régime A** (20 appels/soir), puis bascule **régime B**.

## Setup (avant / pendant les soirs)
1. `python3 business-rappel-leads/tools/validate_kit.py`
2. Importer `01-cible/icp-sheet.csv` dans Google Sheets
3. Remplir fiches score ≥ 3 (15/jour en A) — `fill-slots.md`
4. `python3 business-rappel-leads/tools/score_and_filter.py`
5. Brancher MVP jusqu’à démo live OK **avant** d’exploser le volume B

## Boucle quotidienne
- Suivre `../03-demarchage/daily-ritual.md` (**A** puis **B**)
- Logger dans `call-log-100.csv` + `daily-tracker.csv`
- Close : `../03-demarchage/close-14j.md`

## Definition of Done Phase 0
- [ ] ≥100 appels cumulés (peuvent s’étaler sur régime A + début B)
- [ ] Scorecard remplie
- [ ] 1 close payant **ou** ≥8 démos douleur
- [ ] Décision go / change vertical / kill
- [ ] Bascule mi-sept : file `A_APPELER` ≥ 3 jours d’avance

## Calendrier réaliste
| Fenêtre | Objectif Phase 0 |
|---|---|
| Jusqu’à mi-sept | MVP + ~100–200 appels A + 1er close si possible |
| Semaine de bascule | Atteindre DoD Phase 0 si pas déjà fait, puis scale B |

## Interdit
Reporter les appels du soir pour “parfaire le produit” sans démo montrable.
