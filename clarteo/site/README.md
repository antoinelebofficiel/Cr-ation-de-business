# Site Clartéo

Landing vitrines = **seule destination Meta**. Statique, zéro build.

`index.html` = Google / bouche-à-oreille. **Jamais une pub Meta.**
`machine.html` = outil interne (noindex). **Jamais une pub Meta.**
`menage.html` = parkée. Pas de budget.

## Outil de conversion

Ouvre `machine.html` : 10 angles coller-dans-Meta, Instant Form, script d’appel, upsell bureaux, règles kill/scale. Source unique : `js/ads.js`.

## Meta Ads — URL exactes

Chaque pub a **la même phrase** en overlay et en H1 (`?a=`).

| Overlay | Destination |
|---|---|
| 2 secondes. Il est déjà parti. | `vitres.html?a=2s` |
| Vitrines nickel. Dès 48 h. | `vitres.html?a=48h` |
| Payez le passage. Pas un contrat. | `vitres.html?a=contrat` |
| Vous tenez le commerce. On tient la vitrine. | `vitres.html?a=gerant` |
| Il devait passer mardi. | `vitres.html?a=fantome` |
| Lorient • Lanester • Ploemeur • Auray | `vitres.html?a=local` |
| Même vitrine. 12 minutes. | `vitres.html?a=demo` |
| Votre pub, c’est la vitrine. | `vitres.html?a=pub` |
| D’abord le résultat. Ensuite le contrat. | `vitres.html?a=mecanisme` |
| Qui passe cette semaine ? | `vitres.html?a=question` |

Pixel : `pixelId` dans `js/config.js`. Events : `PageView`, `ViewContent` (angle), `Lead` au submit + `merci.html`.

## Deux chemins, une offre

1. **Instant Form** (volume) — mêmes phrases.
2. **Landing** (qualité, retargeting) — URLs ci-dessus.

On juge au **contrat vitrines signé**, pas au CPL. Bureaux = upsell après preuve.

## Local

`ouvrir.bat` ou `python serveur.py` — port **8000**.

## Config

```js
tel: "0612345678",
telDisplay: "06 12 34 56 78",
wa: "33612345678",
pixelId: "123456789",
```
