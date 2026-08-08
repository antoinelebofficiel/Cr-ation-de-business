# Machine de liste ICP — Rappel leads <5 min

## Objectif quotidien
40 nouvelles fiches **score ≥ 3**, prêtes à appeler.

Fichier de travail : [icp-sheet.csv](icp-sheet.csv) (importer dans Google Sheets).

## ICP
- Vertical : `pac_clim` (priorité) → `reno` → `solaire`
- Dépense ads estimée ≥ 1 500 €/mois (proxy : pubs Meta actives + landing devis)
- Reçoit des leads formulaire / appel / WhatsApp
- Décideur : gérant, resp. commercial, resp. marketing

## Anti-ICP
- Artisan solo sans pub
- Pas de landing lead
- Demande « une IA pour faire joli »
- Siège corporate non décisionnaire local (sauf franchise/partenaire local)

## Pipeline matin (30 min)

### 1. Meta Ad Library (20 min)
URL : https://www.facebook.com/ads/library/

Filtres :
- Pays : France
- Category : All ads
- Status : Active ads
- Mots-clés (tour à tour) :
  - `pompe à chaleur`
  - `climatisation`
  - `devis gratuit`
  - `MaPrimeRénov`
  - `isolation`
  - `panneaux solaires`

Pour chaque pub active pertinente :
1. Noter la Page
2. Ouvrir le site / WhatsApp / formulaire
3. Extraire téléphone (site, mentions légales, Pages Jaunes)
4. Remplir une ligne CSV / Sheet
5. Scorer immédiatement

### 2. Google Maps (10 min)
Requêtes :
- `installateur pompe à chaleur [ville]`
- `clim réversible [ville]`
- `rénovation énergétique [ville]`

Villes prioritaires : 50k+ hab. (slots déjà pré-créés dans le CSV).

Vérifier : site avec « devis », nombre d’avis, zone multi-villes.

### 3. Enrichissement
- Téléphone standard + mobile gérant si dispo
- LinkedIn gérant (pour relance post-appel uniquement)
- Email générique `contact@` si trouvé

## Scoring (0–5) — appeler seulement ≥ 3

| Signal | Points |
|---|---|
| Pubs Meta/Google actives visibles | +2 |
| Landing / formulaire lead | +1 |
| >20 avis Google | +1 |
| Multi-villes / flotte / plusieurs équipes | +1 |

Règle dure : **score < 3 = ne pas appeler**.

## Statuts Sheet
- `A_RECHERCHER` — slot géographique à remplir
- `A_ENRICHIR` — nom trouvé, manque tel/score
- `A_APPELER` — score ≥ 3, jamais joint
- `RAPPEL_J1` / `RAPPEL_J3` — non décroché, SMS envoyé
- `DEMO` — démo planifiée
- `ESSAI` — close 14 jours
- `CLIENT` — abonnement actif
- `KO_DOULEUR` — pas de douleur rappel
- `KO_BUDGET` — douleur OK, pas de budget
- `KO_AUTRE` — hors ICP / refus net
- `A_QUALIFIER` — réseau/plateforme (tester si acheteur réel)

## Colonnes obligatoires
Voir header de `icp-sheet.csv`.

## Quota Phase 0
- J1 : remplir / vérifier **40** fiches score ≥ 3
- J2–J7 : +40/jour jusqu’à épuisement des slots, en priorité `pac_clim`

## Import Google Sheets
1. Créer une Sheet vide
2. Fichier → Importer → `icp-sheet.csv`
3. Ajouter filtre sur `score` et `statut`
4. Vue « À appeler aujourd’hui » : `statut = A_APPELER` ET `score >= 3`
