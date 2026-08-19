# Site Clartéo

Statique. Zéro build.

| Fichier | Rôle |
|---|---|
| `index.html` | Google / bouche-à-oreille. **Jamais une pub Meta.** |
| `vitres.html?a=48h\|2s\|contrat` | **Seule destination ads.** Message match via `js/ads.js`. |
| `politique.html` | URL obligatoire dans l’Instant Form Meta. |
| `machine.html` | Outil interne. noindex. **Jamais une pub.** |

Pack ads : `../lancer-meta/`.

Pixel, tél, WhatsApp : `js/config.js`. Events : PageView, ViewContent, Lead.

Local : `ouvrir.bat` / `ouvrir.sh` — port **8000**.
