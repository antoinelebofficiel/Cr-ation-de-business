import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'

export default function Systeme() {
  return (
    <>
      <Nav cta="/appliquer" />
      <main className="wrap section">
        <p className="kicker">Cockpit interne · Premier retour</p>
        <h1>La cible 100–200 k€ tient. Le modèle “je filme tout seul” la tue.</h1>
        <p className="lead">
          L’agence existe maintenant : marque, offre, site, qualification, scripts,
          maths. Zéro euro encaissé. La suite se joue uniquement sur la vente et la
          capacité de production. Tu vends. D’autres filment et montent.
        </p>

        <div className="warn" style={{ marginTop: 32 }}>
          <strong>Prémisse corrigée.</strong> 100 à 200 k€ en 90 jours avec des clips à
          800–1 500 € est mathématiquement mort : il faudrait 80 à 150 clients et une
          usine. Le seul chemin : 4 à 8 contrats à 6 500–14 500 € / mois, acompte jour 0,
          3 équipes freelance prêtes avant le 3ᵉ close. Tes forces (cold call, cold
          email, ads Facebook, conversion) portent ce modèle. Tes faiblesses (ops,
          perfectionnisme, TDAH sur le long terme) interdisent que tu sois cadreur,
          monteur ou community.
        </div>

        <h2 style={{ marginTop: 72 }}>1. Ce qui s’est passé</h2>
        <div className="steps">
          <div className="step">
            <em>A</em>
            <div>
              <h3>Le repo était vide</h3>
              <p className="muted">
                Notes personnelles, pas de marque, pas d’offre chiffrée, pas de tunnel,
                pas de liste, pas d’équipe. Une idée de format, zéro business.
              </p>
            </div>
          </div>
          <div className="step">
            <em>B</em>
            <div>
              <h3>Le produit a été recadré</h3>
              <p className="muted">
                Format retenu : journée terrain → 12 clips 30–45s → 1 YouTube → épisode
                du média <em>Une journée avec</em>. L’offre Empire ajoute 3 000 € d’ads
                (ton levier Facebook, déjà prouvé sur le nettoyage).
              </p>
            </div>
          </div>
          <div className="step">
            <em>C</em>
            <div>
              <h3>La contrainte réelle est la production</h3>
              <p className="muted">
                Tu closes plus vite que tu livres si tu restes derrière la caméra. Un
                client Empire = 2 jours de tournage + 20 montages. À 6 clients, le mois
                explose. D’où le plafond : 8 fondateurs / trimestre, et des freelances
                payés au forfait.
              </p>
            </div>
          </div>
          <div className="step">
            <em>D</em>
            <div>
              <h3>Une clé API Google traîne dans le fichier `cle` sur main</h3>
              <p className="muted">
                Elle est déjà publique dans GitHub. Révoque-la dans Google Cloud.
                Nouvelle clé uniquement en variable d’environnement. Le fichier est
                désormais ignoré.
              </p>
            </div>
          </div>
        </div>

        <h2 style={{ marginTop: 72 }}>2. Maths : comment on touche 150 k€</h2>
        <p className="muted">
          Confiance : 70 % si tu fais 80 conversations qualifiées / semaine et que 3
          crews existent au jour 10. Ça tombe à 20 % si tu filmes toi-même ou si tu
          baisses le ticket “pour signer plus facilement”.
        </p>
        <table className="table">
          <thead>
            <tr>
              <th>Mois</th>
              <th>Contrats actifs</th>
              <th>Mix</th>
              <th>CA encaissé</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>3</td>
              <td>2 Pilote + 1 Saison + 3 × 2 500 € setup</td>
              <td>29 000 €</td>
            </tr>
            <tr>
              <td>2</td>
              <td>6</td>
              <td>2 Pilote + 3 Saison + 1 Empire + 3 setups</td>
              <td>60 500 €</td>
            </tr>
            <tr>
              <td>3</td>
              <td>8</td>
              <td>2 Pilote + 4 Saison + 2 Empire + 2 setups</td>
              <td>71 500 €</td>
            </tr>
            <tr>
              <td>Total</td>
              <td>8 max</td>
              <td>Plafond volontaire</td>
              <td>161 000 €</td>
            </tr>
          </tbody>
        </table>
        <p>
          200 k€ exige 2 Empire de plus ou un ticket Saison à 10 500 € dès le mois 2,
          après les 3 premiers cas. Marge visée : 55–65 % si cadreur 500 €/jour, monteur
          250 €/clip, pub Empire refacturée au réel.
        </p>
        <div className="okbox">
          <strong>Coût d’un client Saison.</strong> Tournage 500 € + 12 × 250 € de
          montage = 3 500 €. Reste 5 000 € avant ton temps de vente et la plateforme.
          Un Empire : 1 000 € tournage + 5 000 € montage + 3 000 € ads = 9 000 €. Reste
          5 500 €. Tu refuses tout ce qui descend sous 4 000 € de marge brute.
        </div>

        <h2 style={{ marginTop: 72 }}>3. Comment rendre le projet hors catégorie</h2>
        <div className="card-grid">
          <article className="card">
            <h3>Le média est le produit</h3>
            <p className="muted">
              Les fondateurs achètent une place dans <em>Une journée avec</em>, comme une
              saison. Les clips sont le bonus qu’ils gardent. La rareté (8 places) crée
              le prix.
            </p>
          </article>
          <article className="card">
            <h3>Tu vends un rythme commercial</h3>
            <p className="muted">
              12 preuves filmées + ads sur le meilleur clip. Le client mesure les DM et
              les RDV, pas les vues. Ton historique Facebook ads devient l’arme que les
              videastes n’ont pas.
            </p>
          </article>
          <article className="card">
            <h3>Saison 1 = munition</h3>
            <p className="muted">
              Les 3 Pilotes paient 6 500 €. Ils ne sont pas gratuits. Leur footage
              devient tes pubs et tes extraits de close. Prix relevé ensuite, jamais
              baissé.
            </p>
          </article>
        </div>

        <h2 style={{ marginTop: 72 }}>4. Plan 90 jours</h2>
        <h3>Heures 0–72</h3>
        <ol>
          <li>Révoquer la clé Google du fichier `cle`.</li>
          <li>Mettre le site en ligne et le formulaire en notification email.</li>
          <li>
            Lister 120 fondateurs FR, CA visible ou estimé &gt; 300 k€, visage utile à
            la vente : BTP, industrie, formation, cabinets, cliniques, SaaS B2B.
          </li>
          <li>
            Recruter 3 binômes cadreur+monteur (Malt, groupes FB, écoles). Test payé :
            1 clip 45s, 200 €. Garder ceux qui livrent en 48h.
          </li>
          <li>Ouvrir un compte pub (Budget test 30 €/jour dès le 1er cas filmé).</li>
        </ol>
        <h3>Jours 4–21 — closer</h3>
        <p>
          80 conversations / semaine. Mix : 40 cold calls, 30 cold emails
          personnalisés, 10 inbound (site + LinkedIn). Objectif : 3 Pilotes signés,
          acomptes encaissés, 3 dates de tournage posées.
        </p>
        <h3>Jours 22–45 — preuve</h3>
        <p>
          Tourner les 3. Livrer en 14 jours. Couper 15 extraits pour tes propres ads et
          tes messages. Passer Saison à 8 500 €. Ouvrir Empire aux 2 qui veulent des
          RDV mesurables.
        </p>
        <h3>Jours 46–90 — échelle</h3>
        <p>
          5 closes de plus. Plafond 8. Lancer le YouTube PREUVE avec les 3 premiers
          portraits. Chaque nouvel épisode = 1 asset de prospection. Stopper toute
          nouvelle vente si un montage a plus de 5 jours de retard.
        </p>

        <h2 style={{ marginTop: 72 }}>5. Scoreboard quotidien</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Métrique</th>
              <th>Plancher</th>
              <th>Signal d’alarme</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Appels / messages personnalisés</td>
              <td>40 / jour</td>
              <td>&lt; 20 deux jours de suite</td>
            </tr>
            <tr>
              <td>Conversations réelles</td>
              <td>12 / jour</td>
              <td>Liste pourrie ou angle faible</td>
            </tr>
            <tr>
              <td>RDV de close</td>
              <td>8 / semaine</td>
              <td>Revoir le script, pas le prix</td>
            </tr>
            <tr>
              <td>Contrats signés</td>
              <td>1 / semaine sur 8 semaines</td>
              <td>Si 0 à J21 : 3 jours de calls uniquement</td>
            </tr>
            <tr>
              <td>Clips en retard</td>
              <td>0</td>
              <td>Stop vente, tu change de monteur</td>
            </tr>
          </tbody>
        </table>

        <h2 style={{ marginTop: 72 }}>6. Scripts</h2>
        <p className="kicker">Cold call · 28 secondes</p>
        <div className="script">{`[Prénom], Antoine de PREUVE. Je filme le quotidien de fondateurs dans [métier] et je leur sors 12 clips de 45 secondes plus une YouTube par mois. Ça leur amène des RDV parce que le prospect a déjà passé 8 minutes avec eux avant l’appel. Je vous prends 12 minutes cette semaine pour voir si votre visage doit être sur le marché. Mardi 9h ou mercredi 18h ?`}</div>
        <p className="kicker" style={{ marginTop: 28 }}>
          Cold email
        </p>
        <div className="script">{`Objet : 12 preuves filmées pour [Société]

[Prénom],
J’ai regardé [détail précis : avis Google, chantier, keynote, offre].
Votre offre se vend à la confiance. Aujourd’hui un inconnu qui vous cherche tombe sur un site. Demain il peut tomber sur 12 moments où on vous voit décider.
PREUVE : 1 journée sur site, 12 clips 30-45s, 1 YouTube, une place dans le média Une journée avec.
8 fondateurs ce trimestre. 6 500 € / mois sur 90 jours pour les 3 premiers.
12 minutes : [lien calendrier]
Antoine`}</div>
        <p className="kicker" style={{ marginTop: 28 }}>
          Close
        </p>
        <div className="script">{`Vous achetez 90 jours. Setup 2 500 € aujourd’hui, premier mois à la signature. On filme dans les 10 jours. 12 clips en 14 jours après le tournage. Si les 12 ne sont pas livrés, le mois suivant est offert.
Vous mesurez les messages et les RDV, pas les vues.
On signe le mandat. Je bloque le crew.`}</div>

        <h2 style={{ marginTop: 72 }}>7. Comment agir maintenant</h2>
        <div className="okbox">
          <p>
            <strong>Aujourd’hui.</strong> 40 noms dans un tableur : nom, tel, email,
            angle en une ligne. Premier bloc de 20 appels avant 13h. Premier bloc de 20
            emails avant 18h.
          </p>
          <p>
            <strong>Demain.</strong> 3 messages Malt : “Cadreur journée entreprise, 500
            €, dispo J+7. Envoyez un extrait 30s.” Idem monteurs 250 €/clip, 48h.
          </p>
          <p>
            <strong>Après-demain.</strong> Relance des 20 qui n’ont pas répondu. 8
            nouveaux appels. Si 1 RDV : closer sur Pilote, encaisser le setup.
          </p>
          <p>
            <strong>Ça marche quand</strong> tu as 1 acompte avant J10, 3 contrats avant
            J21, 12 clips publiés d’un client avant J45, et 0 jour où tu as tourné
            toi-même.
          </p>
        </div>
      </main>
      <Footer />
    </>
  )
}
