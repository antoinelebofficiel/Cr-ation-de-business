# Remplir les 185 slots A_RECHERCHER

Les lignes `SLOT-xxx` dans [icp-sheet.csv](icp-sheet.csv) sont des **emplacements géographiques**. Remplace le nom `[À TROUVER]...` par une vraie entreprise.

## Méthode (5 min / fiche)
1. Ouvre Ad Library + Maps avec `mots_cles_ad_library` + `ville`
2. Choisis **1** entreprise qui matche l’ICP
3. Remplis : `nom`, `site`, `telephone`, flags, `score`
4. Passe `statut` à `A_APPELER` si score ≥ 3, sinon `KO_AUTRE` ou laisse `A_ENRICHIR`
5. Note dans `notes` la preuve pubs (ex. « 3 créas actives Ad Library 26/07 »)

## Priorité de remplissage
1. Toutes les villes sur vertical `pac_clim`
2. Puis `reno`
3. Puis `solaire`

## Objectif
200 lignes avec **score numérique ≥ 3** et téléphone renseigné avant de saturationner les appels Phase 0.
Les 15 `SEED-*` sont déjà amorcées ; vérifie leurs pubs Ad Library avant le 1er appel.
