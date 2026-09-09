import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Acquisition() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Acquisition · machine</p>
        <h1>Tu n’écris plus de mails. Une séquence envoie 200/jour. Tu appelles ceux qui ouvrent.</h1>
        <p className="lead">
          Stack : Sales Navigator + Dropcontact + Instantly + Calendly. Coût ~200 €/mois.
          Toi : 1 h de liste le lundi, 60 appels/jour sur les chauds. Le reste est un
          robot.
        </p>
        <p>
          <Link href="/demain" className="btn">
            Allumer ça demain
          </Link>
        </p>

        <h2>1. Une recherche LinkedIn, figée</h2>
        <div className="script">{`Titre : Fondateur OU CEO OU Gérant OU Président
Secteur : construction OU industrie OU formation OU santé OU logiciel
Géo : France
Effectif : 10–200
Mots-clés exclus : freelance, coach, influenceur`}</div>
        <p>Tu ne changes plus cette recherche pendant 30 jours. 300 nouveaux profils chaque lundi.</p>

        <h2>2. Enrichir, une fois par semaine</h2>
        <p>
          Export Sales Nav → Dropcontact ou Apollo → email + téléphone. Tu pousses le
          CSV dans Instantly. Lundi 10h, c’est fini. Pas de chasse de noms le mardi.
        </p>

        <h2>3. Séquence Instantly — 5 mails, 12 jours, 200/jour</h2>
        <div className="script">{`J0 — Objet : 24 clips pour {{company}}
{{firstName}}, j’ai vu {{angle}}. Votre vente repose sur le visage du dirigeant. On filme une journée, vous sortez 24 clips de 45s + une YouTube en 14 jours. 3 900 €/mois, 90 jours. 12 min : {{calendar}}
Antoine · PREUVE

J2 — Objet : Re
Je relance une fois. Si le visage ne doit pas être sur le marché, ignorez. Sinon le créneau est là : {{calendar}}

J5 — Objet : 14 jours
Mécanique : 1 jour chez vous → 24 clips templates + 1 YouTube. Si les 24 ne partent pas en 14 jours, le mois suivant est offert. {{calendar}}

J8 — Objet : 2 tournages
On ouvre 2 dates cette semaine. {{ville}} ou à 2h. {{calendar}}

J12 — Objet : Je ferme le dossier
Je sors {{company}} de la liste. Répondez « plus tard » si vous voulez rester dans le pipe.`}</div>
        <p className="muted">
          Personnalisation : 1 champ {'{{angle}}'} (avis Google, chantier, offre), pas un
          roman. Instantly envoie. Tu ne touches pas à la boîte.
        </p>

        <h2>4. Liste d’appels = les chauds uniquement</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Signal Instantly</th>
              <th>Action le matin</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>A répondu</td>
              <td>Appel dans l’heure, close</td>
            </tr>
            <tr>
              <td>A cliqué le calendrier</td>
              <td>Appel le jour même</td>
            </tr>
            <tr>
              <td>A ouvert 2 fois ou plus</td>
              <td>Appel, script court</td>
            </tr>
            <tr>
              <td>Rien</td>
              <td>Le robot continue. Tu n’appelles pas.</td>
            </tr>
          </tbody>
        </table>
        <p>
          60 appels/jour sur cette liste. S’il n’y a que 15 chauds, tu ajoutes 20
          baleines (CA visible, même recherche) au cold call. Jamais 40 appels au
          hasard.
        </p>

        <h2>5. Script d’appel — 20 secondes</h2>
        <div className="script">{`[Prénom], Antoine, PREUVE. Vous avez ouvert le mail sur les 24 clips. On filme une journée, 3 900 €/mois. 12 minutes jeudi 9h ou vendredi 18h ?`}</div>

        <h2>6. Close — une phrase</h2>
        <div className="script">{`90 jours. 1 500 € aujourd’hui, 3 900 € du premier mois à la signature. 24 clips en 14 jours après le tournage, sinon mois offert. Je bloque le cadreur.`}</div>

        <h2>7. Volumes qui tiennent 150 k€</h2>
        <table className="table">
          <thead>
            <tr>
              <th></th>
              <th>Semaine</th>
              <th>90 jours</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Nouveaux dans Instantly</td>
              <td>300</td>
              <td>3 600</td>
            </tr>
            <tr>
              <td>Mails envoyés (robot)</td>
              <td>1 000</td>
              <td>12 000</td>
            </tr>
            <tr>
              <td>Appels (toi)</td>
              <td>300</td>
              <td>3 600</td>
            </tr>
            <tr>
              <td>RDV</td>
              <td>8</td>
              <td>100</td>
            </tr>
            <tr>
              <td>Closes à 3 900 €</td>
              <td>1–2</td>
              <td>12–14 clients actifs</td>
            </tr>
          </tbody>
        </table>
        <p>
          5 clients M1, 10 M2, 14 M3 = 27 000 + 46 500 + 60 600 ={' '}
          <strong>134 100 €</strong>. 200 k€ si 4 passent en Moteur + Ads.
        </p>

        <h2>8. Ads — seulement après le 1er tournage</h2>
        <p>
          30 €/jour, 2 extraits du client 1, ciblage fondateurs 25–55 France. Destination
          : Calendly. Ça nourrit la liste d’appels. Avant le 1er cas filmé, les ads
          sont du théâtre.
        </p>
      </main>
      <Footer />
    </>
  )
}
