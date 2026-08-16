# Site Clartéo

Landing vitrines + landing ménage. Statique, zéro build.

## Fichiers

| URL | Rôle |
|---|---|
| `index.html` | Choix des deux offres |
| `vitres.html` | Machine A — pubs Facebook vitrines |
| `menage.html` | Machine B — pubs ménage |
| `politique.html` | URL à coller dans l’Instant Form Meta |
| `mentions.html` | Mentions légales |

## Avant mise en ligne

Ouvrir `js/config.js` :

```js
tel: "0612345678",
telDisplay: "06 12 34 56 78",
wa: "33612345678",
```

Sans `wa`, le formulaire ouvre un e-mail vers `email`.

## Déploiement (10 minutes)

1. [Netlify Drop](https://app.netlify.com/drop) : glisser le dossier `site/`.
2. Ou Cloudflare Pages / GitHub Pages (dossier `clarteo/site`).
3. Coller l’URL `https://VOTRE-DOMAINE/politique.html` dans Meta Instant Form.

Ads : trafic vitrines → `vitres.html` ; ménage → `menage.html`. Ne pas envoyer les deux avatars sur `index.html`.
