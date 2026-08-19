# Site Clartéo

Landing vitrines + landing ménage. Statique, zéro build.

`index.html` = Google / bouche-à-oreille. **Jamais une pub Meta.**

## Meta Ads — URL exactes

Chaque pub a **la même phrase** en overlay et en H1 (`?a=`).

### Machine A — vitrines
| Pub | Destination |
|---|---|
| 2 secondes. Il est déjà parti. | `vitres.html?a=2s` |
| Vitrines nickel. Dès 48 h. | `vitres.html?a=48h` |
| Payez le passage. Pas un contrat. | `vitres.html?a=contrat` |
| Votre pub, c’est la vitrine. | `vitres.html?a=pub` |

### Machine B — ménage
| Pub | Destination |
|---|---|
| 2 heures de week-end. Rendu. | `menage.html?a=samedi` |
| Les vitres, on sait. | `menage.html?a=vitres` |
| Un jour fixe. C’est fait. | `menage.html?a=jourfixe` |

Pixel : `pixelId` dans `js/config.js`. Event `Lead` au submit + sur `merci.html`.

## Deux campagnes, pas une

1. **Instant Form** (volume, CPL bas) — même copy que la pub.
2. **Landing** (leads plus chauds, retargeting, preuve) — URLs ci-dessus.

On juge au **contrat signé**, pas au CPL.

## Local

`ouvrir.bat` (Windows) ou `python serveur.py` — IPv4 + IPv6, port **8000**.

Dans Cursor : onglet **Ports** → Forward 8000, puis l’URL générée (pas Chrome hors Cursor sur `127.0.0.1`).

## Config

```js
tel: "0612345678",
telDisplay: "06 12 34 56 78",
wa: "33612345678",
pixelId: "123456789",
```
