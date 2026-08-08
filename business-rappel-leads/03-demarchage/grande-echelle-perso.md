# Grande échelle + personnalisation

Pas l’un ou l’autre. **Les deux.**  
Perso = variables vraies. Échelle = machine de touches + file énorme.

## Principe
```
HOOK (30s) → SÉQUENCE multi-touch → CALL close
```
- L’email/SMS **ouvrent et relancent**
- Le **téléphone encaise**
- Aucun canal “générique spray” sans `hook`

## Ce que “grande échelle” veut dire ici
| Phase | File active | Touches / sem | Appels / sem |
|---|---|---|---|
| Août (facteur) | 300–500 fiches | 800–1 200 | ~245 |
| Dès mi-sept | 1 000+ | 2 500+ | 450–550 |
| Post-20k | 2 000+ | 4 000+ | 350 toi + setter |

Grande échelle ≠ 10 000 mails identiques.  
= **beaucoup de prospects × séquence courte × 1 hook chacun**.

---

## Variables de personnalisation (token system)

Minimum viable sur chaque fiche :
| Token | Exemple | Obligatoire |
|---|---|---|
| `{{hook}}` | « devis gratuit PAC », « 4 créas actives » | **OUI** |
| `{{ville}}` | Lyon | OUI |
| `{{vertical}}` | pac_clim | OUI |
| `{{prenom}}` | si connu | non |
| `{{entreprise}}` | Optihome | OUI |

Règle : **pas de touche sortante si `hook` vide** (sauf fallback « pubs PAC/clim » max 20 % des envois).

---

## Séquence 7 jours (grande échelle)

| Jour | Canal | But |
|---|---|---|
| J0 | **Call** #1 | Décrocher / douleur |
| J0 | SMS si non-joint | Pose créneau |
| J1 | Call #2 | Relance |
| J2 | Email 5 lignes | Preuve + 2 créneaux |
| J3 | Call #3 | Close attempt |
| J5 | SMS court | Dernier push créneau |
| J7 | Call #4 ou kill | `KO` / recycle dans 45j |

**Cadence août (soir)** : tu fais surtout J0 call+SMS le soir ; emails J2 en micro-bloc 20 min ; relances call sur WE.

**Cadence mi-sept** : blocs call matin/aprem + emails automatisés / semi-auto + SMS.

---

## Machine de hooks à l’échelle

### Usine matinale (ou pauses)
Objectif : **40–80 nouveaux hooks/jour** (août) → **150/jour** dès mi-sept.

Pipeline :
1. Ad Library mot-clé (PAC, clim, MaPrimeRénov…)
2. Page active → site → tél
3. `hook` = 6–10 mots (angle crea / ville / multi-créas)
4. Score ≥3
5. Statut `A_APPELER` + date `sequence_start` vide

Outils OK : Sheet d’abord. Plus tard Make/n8n pour :
- append fiche
- envoyer email J2
- reminder SMS J5  
**Le dial reste humain** (ou setter).

### Batching anti-TDAH
| Bloc | Durée | Output |
|---|---|---|
| Hooks | 45 min | 40 fiches hookées |
| Dial | 75–240 min | appels |
| Relances écrites | 20 min | SMS/emails J1–J5 |
| Debrief | 10 min | 1 correction |

Jamais “je personnalise pendant que j’appelle”.  
**Chargeur plein → gâchette.**

---

## Templates échelle (toujours 1 hook)

### Call (J0)
« {{prenom}}, vous poussez {{hook}} en ce moment. Lead à 10h : rappel en combien de temps ? »

### SMS J0
« {{prenom}} — vu vos pubs {{hook}}. On rappelle vos leads en <5 min + RDV agenda. 12 min auj. 18h30 ou demain 9h ? »

### Email J2
Objet : `{{hook}}` → leads rappelés <5 min

> {{prenom}},  
> Vous tournez des pubs sur {{hook}} ({{ville}}).  
> On rappelle ces leads en <5 min, on qualifie, on pose le RDV.  
> Essai 14 jours — setup 48h.  
> Créneau : demain 9h ou 18h ?  
> {{ton_prenom}} — {{tel}}

### SMS J5
« Dernier message {{prenom}} : vos leads {{hook}}. 12 min demain 9h15 ou je vous retire de la liste ? »

---

## Organisation “grande échelle” humaine

### Jusqu’à 10 clients (août)
Toi seul :
- Hooks + calls + SMS
- Emails en batch 20 min
- **Pas** d’agence, pas de setter

### Dès 10 clients + mi-sept
| Rôle | Job |
|---|---|
| Toi | Close + démos + deals score 5 |
| Setter (option) | J0–J3 calls + pose démos |
| Automatisation | Emails J2 / SMS J5 / logging |

Setter KPI : démos posées / jour, pas “appels pour appels”.

---

## Stack minimale pour scaler sans te noyer

**Maintenant**
- Google Sheet (`hook`, `sequence_step`, `last_touch`, `next_touch`)
- Téléphone + SMS
- Gmail / Superhuman-like + templates
- Ad Library

**Dès 5–10 clients**
- Instantly / Lemlist / Emailalto **seulement** pour J2/J5 email (B2B, domaines warmed)
- Aircall / Twilio dialer si volume
- n8n : avance `sequence_step`

Interdit avant 10 clients : construire le “CRM parfait”.

---

## Colonnes Sheet (échelle)

Ajoute :
- `hook`, `hook_type` (déjà)
- `sequence_step` : 0–7 ou `DONE` / `KO`
- `last_touch_at`
- `next_touch_at`
- `touches_count`

Vue du jour :
1. `next_touch_at <= today` ET score ≥3
2. Priorité : call steps > SMS > email

---

## Maths (pourquoi ça scale)

Hypothèses réalistes perso+volume :
- 1 000 touches écrites / sem + 245 calls (août)
- 2–4 % réponse utile écrite + fort taux sur call sniper
- Objectif toujours : **démo → close**, pas vanity opens

Si email ouvre mais 0 démo → kill copy, **augmente les calls**, ne double pas les envois.

---

## Garde-fous légaux (rapide)
- B2B installateurs : OK sous RGPD + opposition = stop
- Pas de particuliers
- Email : lien désinscription / stop clair
- Pas de scrape douteux de 06 perso en masse

---

## Scoreboard “grande échelle”

| Signal | Vert | Rouge |
|---|---|---|
| % fiches avec hook | ≥90 % | <70 % |
| Appels / sem | ≥245 (août) / ≥450 (mi-sept) | Sous quota |
| Démos / sem | ≥5 (août) / ≥12 (mi-sept) | <3 |
| Perso ressentie (tu cites le hook) | chaque décroché | script générique |

---

## Phrase de discipline
> On industrialise la **personnalisation courte**, pas le spam.  
> On industrialise le **calendrier de touches**, pas le blabla.  
> Le volume pousse des hooks. Les hooks poussent des décrochés. Les décrochés poussent des closes.

Page quotidienne reste [../LOUP.md](../LOUP.md).  
Celle-ci = quand tu passes la seconde : **usine**.
