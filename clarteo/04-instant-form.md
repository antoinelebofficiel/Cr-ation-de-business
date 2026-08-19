# Instant Form — vitrines uniquement

Un formulaire. Commerces / locaux pro. **Pas de particulier.**

Politique de confidentialité : page `site/politique.html` en ligne, URL dans Meta. Sans URL, le formulaire ne passe pas.

La source à coller : `site/machine.html` onglet Instant Form.

---

## Formulaire A — Vitrines

Nom interne : `Clartéo Vitrines 48h`
Intro :
> Vitrines de commerce — Lorient et 40 km.
> On vous rappelle en 5 minutes. Première intervention sous 48 h, sans engagement.

Écran 1 — questions custom (obligatoires) :

1. **Ville du local** — Lorient / Lanester / Ploemeur / Guidel / Quéven / Caudan / Hennebont / Larmor-Plage / Port-Louis / Auray / Autre (56, < 40 km)
2. **Nombre de baies** — 1 à 3 / 4 à 8 / 9 ou plus / Je ne sais pas
3. **Situation actuelle** — Personne ne s’en occupe / Prestataire irrégulier / Je compare / Urgent (ouverture / contrôle)

Coupé volontairement : « Vous êtes particulier / bureau / commerce ». Ça achetait des leads hors offre.

Écran 2 — prérempli Facebook : Prénom, Nom, **Téléphone**, E-mail
Écran 3 — consentement rappel tél / WhatsApp (obligatoire)

Thank you :
**Titre :** Décrochez. On appelle dans les 5 minutes.
**Texte :** Si vous ratez l’appel, rappelez le numéro qui s’affiche. On cale le passage sous 48 h.
**Bouton :** Appeler maintenant → mobile business.

Routing : tout le monde = script vitrines. Un bureau qui veut des vitres = même script. Sols/bureaux = upsell après preuve.

---

## Formulaire B — Ménage

**PARKÉ.** Ne pas lancer. Ne pas budgéter.

---

## Zapier / Make

Déclencheur : nouveau lead Instant Form A.

Action 1 — WhatsApp vers **ton** numéro, < 30 secondes :

```
CLARTEO LEAD VITRINES
{prenom} {nom}
{tel}
{ville} | {baies} | {situation}
Il y a {timestamp}
RAPPELER MAINTENANT
```

Action 2 — Google Sheet `leads-clarteo`.
Action 3 — Si pas de statut « joint » dans 7 min : 2ᵉ ping `LEAD NON TRAITÉ {prenom} {tel}`.

## Message auto au lead (60 s)

```
{prenom}, c’est Clartéo (vitrines autour de Lorient).
On vous appelle dans la minute au {tel}.
Décrochez — on cale le créneau sous 48h.
```
