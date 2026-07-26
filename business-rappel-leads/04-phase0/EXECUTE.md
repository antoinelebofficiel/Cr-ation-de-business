# Exécution Phase 0 (humain au téléphone)

Le kit est prêt. Cette phase se **joue au décroché**.

## Setup (avant appels)
1. `python3 business-rappel-leads/tools/validate_kit.py`
2. Importer `01-cible/icp-sheet.csv` dans Google Sheets
3. Remplir 40 fiches score ≥ 3 (Ad Library) — `fill-slots.md`
4. `python3 business-rappel-leads/tools/score_and_filter.py` → ouvre `queue-a-appeler.csv`
5. Brancher MVP (prompt + n8n) jusqu’à démo live OK

## Boucle quotidienne
1. Suivre `../03-demarchage/daily-ritual.md`
2. Logger chaque appel dans `call-log-100.csv`
3. Logger les totaux dans `daily-tracker.csv`
4. Close selon `../03-demarchage/close-14j.md`

## Definition of Done Phase 0
- [ ] 100 lignes `call-log-100.csv` datées
- [ ] Scorecard J7 remplie
- [ ] 1 close payant **ou** ≥8 démos douleur
- [ ] Décision go P1 / change vertical / kill

## Interdit
Reporter les appels pour « améliorer le produit » avant le 1er close.
