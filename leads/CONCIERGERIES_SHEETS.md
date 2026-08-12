# Conciergeries Bretagne — CRM Google Sheets

## Fichiers
- `leads/crm_conciergeries_bretagne.csv` — **à importer dans Sheets** (colonnes CRM)
- `leads/conciergeries_bretagne_100.csv` — top 100 (email unique + détail Places)
- `leads/conciergeries_bretagne_all.csv` — 204 fiches scrapées (131 emails)

Colonnes CRM : `nom`, `email`, `telephone`, `adresse`, `ville_zone`, `site`, `maps`, `note`, `nb_avis`, `statut_crm`, `date_ajout`, …

## Import Google Sheets (30 secondes)
1. Ouvre https://sheets.new
2. **Fichier → Importer → Téléverser** → `crm_conciergeries_bretagne.csv`
3. Séparateur : **virgule** · **Remplacer la feuille**
4. Renomme l’onglet `Conciergeries Bretagne`

## Sync auto depuis GitHub
Dans A1 d’une feuille vide :
```
=IMPORTDATA("https://raw.githubusercontent.com/antoinelebofficiel/Cr-ation-de-business/cursor/conciergeries-bretagne-9069/leads/crm_conciergeries_bretagne.csv")
```

## Push API (optionnel)
```bash
# .env
GOOGLE_SERVICE_ACCOUNT_JSON=./service-account.json
GOOGLE_SHEET_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

python conciergeries_bretagne.py --from-csv leads/conciergeries_bretagne_100.csv --no-email --push-sheets
```
Partage la Sheet avec l’email du service account en **Éditeur**.

## Relancer le scrape
```bash
python conciergeries_bretagne.py --limit 100 --out leads/conciergeries_bretagne_100.csv
```

**Note :** Google Places ne fournit pas d’emails. Les mails sont extraits des sites (accueil / page contact).
