# Remplir les slots ICP

## Méthode
1. Ouvre [icp-sheet.csv](icp-sheet.csv)
2. Prends les lignes `A_RECHERCHER`
3. Remplace `slot_*` par un vrai commerce Maps
4. Remplis : `nom`, `type`, `adresse`, `telephone`, signaux score, `hook`
5. Passe `statut` → `A_APPELER` si score ≥3 + tél

## Hook = 1 fait visible
Exemples :
- `vitrine angle rue République traces pluie`
- `baies sud pollen + doigts`
- `devanture optique reflets matin`
- `terrasse + vitrine resto soir`

Sans hook → tu appelles quand même, mais le close est plus faible.

## Cadence
40 slots / jour jusqu’à file ≥120 appelables.
