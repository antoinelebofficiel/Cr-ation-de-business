# Instant Forms + notif WhatsApp

Deux formulaires. Jamais un seul fourre-tout.

Politique de confidentialité : collez le texte de `09-politique-confidentialite.md` dans une page Notion publique et mettez l’URL dans Meta. Sans URL, le formulaire ne passe pas.

---

## Formulaire A — Vitrines

Nom interne : `Clartéo Vitrines 48h`
Intro :
> Vitrines de commerce — Lorient et 40 km.
> On vous rappelle en 5 minutes. Première intervention sous 48 h, sans engagement.

Écran 1 — questions custom (obligatoires) :

1. **Vous êtes** (choix unique)
   - Commerce / magasin / resto / café
   - Bureau / local pro
   - Particulier (vitres maison)
   - Autre

2. **Ville du local** (choix unique)
   - Lorient
   - Lanester
   - Ploemeur
   - Guidel
   - Quéven
   - Caudan
   - Hennebont
   - Larmor-Plage
   - Port-Louis
   - Auray
   - Autre (56, < 40 km)

3. **Nombre de vitrines / baies**
   - 1 à 3
   - 4 à 8
   - 9 ou plus / enseigne / hauteur

4. **Situation actuelle**
   - Personne n’en s’occupe
   - Prestataire irrégulier
   - Déjà un prestataire, je compare
   - C’est urgent (événement / contrôle / ouverture)

Écran 2 — prérempli Facebook :
- Prénom
- Nom
- Téléphone (prioritaire)
- E-mail

Écran 3 — consentement :
> J’accepte d’être rappelé par téléphone / WhatsApp au sujet de ma demande Clartéo. [obligatoire]

Thank you screen :
**Titre :** Décrochez. On appelle dans les 5 minutes.
**Texte :** Si vous ratez l’appel, rappelez le numéro qui s’affiche. On cale le passage sous 48 h.
**Bouton :** Appeler maintenant → votre mobile business.

Routing :
- « Particulier » → message auto WhatsApp machine B + tu ne vends pas du 49 € vitrine commerce. Tu bascules ménage/vitres maison.
- Reste → script A.

---

## Formulaire B — Ménage

Nom interne : `Clartéo Menage 48h`
Intro :
> Ménage et vitres — Lorient et 40 km.
> Rappel en 5 minutes. Première vacation sous 48 h.

1. **Type de lieu** : Appartement / Maison / Bureau / Commerce
2. **Ville** : même liste que A
3. **Besoin** : Ménage ponctuel / Récurrent / Vitres seulement / Ménage + vitres
4. **Surface approx.** : < 50 m² / 50–90 / 90–130 / 130+
5. Prénom + téléphone + consentement

Thank you : identique (décrochez).

---

## Zapier / Make (branchement 10X)

Déclencheur : nouveau lead Instant Form (A ou B).

Action 1 — WhatsApp Business Cloud ou Twilio vers **ton** numéro, < 30 secondes :

```
CLARTEO LEAD {A|B}
{prenom} {nom}
{tel}
{ville} | {q1} | {q2} | {q3}
Il y a {timestamp}
RAPPELER MAINTENANT
```

Action 2 — Google Sheet `leads-clarteo` (une ligne).
Action 3 — Si pas de statut « joint » dans 7 min : 2ᵉ ping WhatsApp `LEAD NON TRAITÉ {prenom} {tel}`.

Le 2ᵉ ping est non négociable. L’action moyenne laisse le lead refroidir.

---

## Message auto au lead (WhatsApp, 60 secondes après le form)

```
{prenom}, c’est Clartéo (vitrines / ménage autour de Lorient).
On vous appelle dans la minute au {tel}.
Décrochez — on cale le créneau sous 48h.
```

Ça sauve les leads qui ont mis un numéro mais qui ont le téléphone en silencieux : ils voient le WhatsApp.
