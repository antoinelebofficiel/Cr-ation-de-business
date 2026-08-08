# État liste ICP

## Livré
- Sheet **200 lignes** (`icp-sheet.csv`)
- Machine de remplissage Ad Library + Maps (`process-liste.md`)
- Seeds recherchées (entreprises / sources publiques)
- Slots géographiques pré-créés pour atteindre 200 fiches score ≥ 3

## À faire avant saturation d’appels
Chaque matin : convertir 40 lignes `A_RECHERCHER` → `A_APPELER` avec score ≥ 3 + téléphone.

Commandes :
```bash
python3 business-rappel-leads/tools/score_and_filter.py
python3 business-rappel-leads/tools/validate_kit.py
```

## Règle
Ne jamais appeler un slot non enrichi. Score ≥ 3 + téléphone obligatoire.
