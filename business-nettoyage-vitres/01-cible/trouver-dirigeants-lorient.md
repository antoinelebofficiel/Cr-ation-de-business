# Trouver les dirigeants — Lorient (mail + call)

Objectif : constituer une file **prête à attaquer**, moitié enrichie email, moitié téléphone.

Quota Phase 0 : **40 fiches/jour**  
- **20 track MAIL** (email dirigeant ou nominatif trouvé)  
- **20 track CALL** (tél décideur / standard + nom dirigeant)

Fichier de travail : [dirigeants-lorient.csv](dirigeants-lorient.csv)

---

## Qui tu cherches (pas le mauvais contact)

| Priorité | Titre | Quand |
|---|---|---|
| 1 | **Gérant / Président / DG** (Pappers) | PME, SARL, SAS locales |
| 2 | **Gérant de magasin / franchisé** | Enseignes, showrooms, retail |
| 3 | **Responsable magasin / adjoint** | Si siège gère le budget |
| 4 | Office manager / services généraux | Bureaux, multi-sites |

**Règle :** dirigeant légal (Pappers) ≠ toujours décideur ops.  
Croise toujours avec **qui paie l’entretien / le marketing** selon ton offre.

---

## Pipeline commun (30–40 min)

### Étape 1 — Lister les entreprises (15 min)
Sources **gratuites** (ordre) :

1. **Google Maps** — requêtes zone Lorient / Lanester / Ploemeur / Guidel  
   Ex. : `optique Lorient`, `agence immobilière Lorient`, `cuisine Lorient`, `garage Lorient`, `SARL Lorient`
2. **Pappers** — [pappers.fr](https://www.pappers.fr)  
   - Recherche entreprises : ville / CP `56100`, `56600`…  
   - Ou [recherche dirigeants](https://www.pappers.fr/recherche-dirigeants) + filtre département **56**
3. **Societe.com** / **Annuaire des entreprises** (data.gouv / annuaire-entreprises.data.gouv.fr)
4. **Pages Jaunes** + site de l’entreprise (mentions légales)

Pour chaque fiche note tout de suite :
`nom entreprise` · `ville` · `SIREN si dispo` · `source`

### Étape 2 — Identifier le dirigeant (2 min / fiche)
Sur **Pappers** → fiche entreprise → bloc **Dirigeants** :
- Nom + prénom  
- Fonction (gérant, président…)  
- Mandat en cours ?

Vérif rapide **LinkedIn** : “[Prénom Nom] [Entreprise] Lorient”  
- Toujours en poste ? → OK  
- Parti / holding pure ? → cherche le **dirigeant ops** local (magasin)

### Étape 3 — Split MAIL vs CALL (règle dure)

| Si tu trouves… | Track | Action |
|---|---|---|
| Email **nominatif** (`prenom.nom@`, `prenom@`) | **MAIL** | Séquence cold email |
| Seulement `contact@` / `info@` **+** tél | **CALL** (mail = touche 2 optionnelle) | Appel / SMS prioritaire |
| Tél mobile gérant | **CALL** | Meilleur canal |
| Rien sous 3 min | Skip ou `A_ENRICHIR` | Ne stagne pas |

---

## PARTIE 1 — Track MAIL (dirigeants)

### Où trouver l’email
Ordre de recherche (chrono max **2 min**) :
1. Site → **Mentions légales** / Contact / équipe  
2. Pattern classique testé via Hunter / VoilaNorbert / Apollo :  
   `prenom.nom@domaine` · `prenom@domaine` · `p.nom@domaine`  
3. LinkedIn (parfois email / site perso)  
4. Signature PDF devis / plaquette si publique  

**Pas d’email nominatif = pas de track MAIL prioritaire.**  
`contact@` seul → bascule CALL.

### Colonnes obligatoires track MAIL
`prenom` `nom` `fonction` `email` `domaine` `hook` `statut_mail`

### Statuts mail
`A_ENVOYER` · `J0_SENT` · `J3_BUMP` · `J7_BREAK` · `REPLY` · `STOP` · `BOUNCE`

### Séquence (rappel)
- J0 : hook + CTA (passage / offre)  
- J3 : bump 2 lignes  
- J7 : breakup  
Voir logique copy dans les scripts démarchage / cold email.

### Quota mail / jour
- Début (domaine neuf) : **20–30** envois max  
- Après warm-up : **40–50**  
Bounce >3 % → freine.

---

## PARTIE 2 — Track CALL (dirigeants)

### Où trouver le téléphone
1. **Google Maps** / fiche établissement (souvent le meilleur pour retail)  
2. Site → Contact  
3. Pages Jaunes  
4. Mentions légales (parfois)  
5. Standard + “je cherche M./Mme [Nom Pappers]”

### Script gatekeeper (10 sec)
> « Bonjour, Antoine Bauché — je souhaiterais parler à [Prénom Nom], [gérant/président]. C’est à quel sujet ? → [1 phrase offre]. Vous me le passez ? »

Mobile direct :
> « [Prénom], Antoine Bauché — 40 secondes sur [sujet]. »

### Colonnes obligatoires track CALL
`prenom` `nom` `fonction` `telephone` `tel_type` (mobile/standard) `hook` `statut_call`

### Statuts call
`A_APPELER` · `JOINT` · `RAPPEL_J1` · `SMS_SENT` · `CLOSE` · `KO_*`

### Quota call
- Micro-fenêtres : **20–25** appels (8h–9h / 11h–12h / 14h30–16h30)  
- Soir commerces fermés : **SMS** sur la file CALL, pas d’appel magasin 17h30–19h  
- Samedi : gros volume CALL

### Non-décroché → SMS (dans la minute)
> [Entreprise] — Antoine Bauché. Pour [hook court]. [CTA binaire]. Stop = stop.

---

## Routine quotidienne Lorient (exemple)

| Bloc | Durée | Output |
|---|---|---|
| Chargeur Maps + Pappers | 25 min | 40 entreprises brutes |
| Enrichissement dirigeant | 20 min | Nom + fonction sur 40 |
| Split + email/tél | 20 min | 20 MAIL prêts + 20 CALL prêts |
| FIRE mail (soir OK) | 20–30 min | 20 envois J0 |
| FIRE call (créneau jour/sam) | 40 min | 20–30 appels + SMS |

---

## Outils (stack minimal)

| Besoin | Gratuit / freemium | Payant si scale |
|---|---|---|
| Identité légale | Pappers, annuaire-entreprises.data.gouv.fr | Pappers Pro |
| Liste locale | Maps, Pages Jaunes | — |
| Email | Site + Hunter free credits | Instantly / Smartlead + Hunter |
| Tél | Maps, site | — |
| CRM | Google Sheet = [dirigeants-lorient.csv](dirigeants-lorient.csv) | Plus tard |

Pas besoin de base à 200 €/mois en Phase 0.

---

## Compliance (rappel)
- **B2B** mail/call : OK avec identité claire + stop honoré  
- **B2C particuliers** : pas de cold email / cold call — ads / opt-in seulement  
- Source de chaque contact notée (`Maps`, `Pappers`, `site`)  
- Pas de liste achetée douteuse

---

## DoD “file prête”
- [ ] 40 lignes avec **nom dirigeant**  
- [ ] 20 avec **email nominatif** → track MAIL  
- [ ] 20 avec **téléphone** → track CALL  
- [ ] Hook rempli sur chaque ligne  
- [ ] Aucune fiche >3 min d’enrichissement sans décision MAIL/CALL/SKIP
