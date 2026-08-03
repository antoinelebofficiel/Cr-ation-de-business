# Machine de liste ICP — Clean&Pro commerces

## Objectif quotidien
40 nouvelles fiches **score ≥ 3**, prêtes à appeler.

Fichier : [icp-sheet.csv](icp-sheet.csv)

## ICP
- Type : commerce vitrine, resto/café baies, agence, bureau entrée vitrée, syndic
- Zone : agglo verrouillée ([STATUS.md](STATUS.md))
- Décideur : gérant, responsable magasin, office manager, syndic

## Anti-ICP
- Pas de vitrine / peu de verre
- Franchise nationale (décision siège) sauf gérant local autonome
- Trop loin (>25 min prestataire)
- Déjà sous contrat national type multi-sites (sauf si local insatisfait)

## Pipeline matin (30–40 min)

### 1. Google Maps (25 min)
Requêtes (tour à tour, zone verrouillée) :
- `optique [quartier]`
- `agence immobilière [quartier]`
- `boulangerie [quartier]`
- `salon de coiffure [quartier]`
- `restaurant [quartier]`
- `magasin vêtements [quartier]`
- `pharmacie [quartier]`
- `banque agence [quartier]`
- `coworking [quartier]`
- `syndic de copropriété [ville]`

Pour chaque résultat pertinent :
1. Street View / photos → y a-t-il une **vraie vitrine** ?
2. Téléphone
3. Horaires (matin = meilleur créneau appel avant ouverture clients)
4. Remplir une ligne CSV
5. Scorer immédiatement

### 2. Balade / photos (optionnel 1×/sem, 45 min)
Rue passante → noter 20 commerces + photos vitrines sales / traces → hooks call ultra-concrets.

### 3. Enrichissement
- Tél + éventuellement Instagram commerce (relance visuelle)
- Email `contact@` si site
- Nom gérant si Google / LinkedIn local

## Scoring (0–5) — appeler seulement ≥ 3

| Signal | Points |
|---|---|
| Grande vitrine / baies visibles | +2 |
| Rue passante / zone commerciale | +1 |
| Traces / saleté visibles (Street View ou photo) | +1 |
| >15 avis Google OU enseigne soignée | +1 |

Règle dure : **score < 3 = ne pas appeler**.

## Statuts Sheet
- `A_RECHERCHER` — slot à remplir
- `A_ENRICHIR` — nom trouvé, manque tel
- `A_APPELER` — score ≥3, jamais joint
- `RAPPEL_J1` / `RAPPEL_J3` — non décroché, SMS envoyé
- `VISITE` — 1er passage planifié
- `CONTRAT` — contrat actif
- `ONESHOT` — intervention ponctuelle encaissée
- `KO_INTERNE` — géré en interne / salarié
- `KO_CONTRAT` — déjà prestataire satisfait
- `KO_BUDGET` — prix refus
- `KO_AUTRE` — hors ICP / refus net

## Colonnes obligatoires
Voir header de `icp-sheet.csv`.

## Quota Phase 0
- J1 : **40** fiches score ≥3 dans la zone
- J2–J7 : +40/jour, priorité rues passantes

## Import Google Sheets
1. Sheet vide → Importer `icp-sheet.csv`
2. Filtre `score` + `statut`
3. Vue jour : `statut = A_APPELER` ET `score >= 3`
