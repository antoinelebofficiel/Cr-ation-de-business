import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Demain() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Mercredi 9 septembre 2026 · J1</p>
        <h1>Demain tu allumes le robot. Tu n’écris pas 30 mails à la main.</h1>
        <p className="lead">
          Fin de journée = Sales Nav + Instantly + Dropcontact payés, 300 leads dans
          la séquence, 200 mails partent tout seuls, 40 appels sur les premiers
          téléphones, 6 Malt envoyés. Détail machine :{' '}
          <Link href="/acquisition">/acquisition</Link>.
        </p>
        <p>
          <Link href="/plan" className="btn ghost">
            Business plan
          </Link>
        </p>

        <div className="warn" style={{ marginTop: 28 }}>
          Téléphone en mode avion hors blocs d’appels. Pas de montage, pas de logo, pas
          de YouTube. Le site PREUVE existe déjà. Tu vends.
        </div>

        <h2>Avant 8h15 — setup (15 min)</h2>
        <ul className="todo">
          <li>
            <time>08:00</time>
            <div>
              <strong>Payer la stack</strong>
              LinkedIn Sales Navigator, Instantly, Dropcontact. Calendly avec 8
              créneaux de 12 min. ~200 €/mois. Sans ça tu restes artisan.
            </div>
          </li>
          <li>
            <time>08:10</time>
            <div>
              <strong>Calendrier</strong>
              8 créneaux de 12 min sur les 5 prochains jours (deux le matin, un le
              soir). Lien prêt à envoyer par SMS.
            </div>
          </li>
        </ul>

        <h2>8h15–9h00 — hygiène + 20 premiers noms</h2>
        <ul className="todo">
          <li>
            <time>08:15</time>
            <div>
              <strong>Révoquer la clé du fichier `cle`</strong>
              Google Cloud → Credentials → clé AIza… → Delete. 5 minutes. Ensuite tu
              n’y touches plus.
            </div>
          </li>
          <li>
            <time>08:25</time>
            <div>
              <strong>20 fondateurs</strong>
              Sources : Societe.com / Pappers / LinkedIn / avis Google. Filtres : BTP,
              industrie, formation, cabinet, clinique, agence &gt; 5 personnes, ville
              où tu peux envoyer un cadreur sous 10 jours. Angle écrit AVANT l’appel
              (chantier, avis, keynote, offre).
            </div>
          </li>
        </ul>

        <h2>9h00–11h30 — bloc call 1 (non négociable)</h2>
        <ul className="todo">
          <li>
            <time>09:00</time>
            <div>
              <strong>20 appels</strong>
              Script : « [Prénom], Antoine de PREUVE. Je filme le quotidien de
              fondateurs dans [métier] et je leur sors 12 clips de 45 secondes plus une
              YouTube par mois. Ça leur amène des RDV. 12 minutes cette semaine : mardi
              9h ou mercredi 18h ? »
            </div>
          </li>
          <li>
            <time>11:00</time>
            <div>
              <strong>Score à noter</strong>
              Décrochés / conversations / RDV. Objectif du bloc : 8 conversations, 2
              RDV. Si 0 conversation : tes numéros sont nuls, tu changes de source à
              14h, tu ne changes pas le prix.
            </div>
          </li>
        </ul>

        <h2>11h30–12h30 — crews</h2>
        <ul className="todo">
          <li>
            <time>11:30</time>
            <div>
              <strong>3 messages Malt / groupes cadreurs</strong>
              « Cadreur journée entreprise, lumière naturelle, son cravate, 500 €
              jour, dispo sous 10 jours, Île-de-France ou [ta ville]. Envoyez un extrait
              30s. Test payé 200 € si le style tient. »
            </div>
          </li>
          <li>
            <time>12:00</time>
            <div>
              <strong>3 messages monteurs</strong>
              « Montage Reels 30–45s, hook 1,2s, sous-titres, 250 €/clip, livré 48h.
              Envoyez 2 extraits. Test : 1 clip 200 €. »
            </div>
          </li>
        </ul>

        <h2>13h30–15h00 — 30 mails</h2>
        <ul className="todo">
          <li>
            <time>13:30</time>
            <div>
              <strong>Contrôle Instantly</strong>
              200 mails doivent déjà être partis ou en file. Tu n’écris rien. Tu
              appelles ceux qui ont ouvert. Séquence : /acquisition.
            </div>
          </li>
        </ul>

        <h2>15h00–17h00 — bloc call 2</h2>
        <ul className="todo">
          <li>
            <time>15:00</time>
            <div>
              <strong>20 appels de plus</strong>
              Même script. Tu ajoutes 20 noms au tableur si la liste est sèche. Total
              journée : 40 appels, 120 lignes minimum en fin de journée.
            </div>
          </li>
          <li>
            <time>16:45</time>
            <div>
              <strong>SMS aux décrochés tièdes</strong>
              « [Prénom], Antoine. Je vous envoie le créneau 12 min : [lien]. 8 places
              ce trimestre. »
            </div>
          </li>
        </ul>

        <h2>17h00–18h30 — close si RDV, sinon relances</h2>
        <ul className="todo">
          <li>
            <time>17:00</time>
            <div>
              <strong>Si un RDV tombe demain ou après-demain</strong>
              Prépare : prix Pilote, setup 2 500 €, IBAN, contrat 1 page (90 j, 12
              clips / 14 j, mois offert si retard). Close : « On signe, je bloque le
              crew. »
            </div>
          </li>
          <li>
            <time>17:30</time>
            <div>
              <strong>Si 0 RDV</strong>
              Relance vocale des 10 qui ont dit « rappelez-moi ». Tu ne finis pas sans
              8 prochaines actions datées dans le tableur.
            </div>
          </li>
        </ul>

        <h2>18h30–19h00 — revue</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Case</th>
              <th>Plancher</th>
              <th>Si en dessous</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Lignes tableur</td>
              <td>120</td>
              <td>Encore 30 noms avant de couper</td>
            </tr>
            <tr>
              <td>Appels</td>
              <td>40</td>
              <td>Le manque se rattrape jeudi 8h–11h, pas “la semaine prochaine”</td>
            </tr>
            <tr>
              <td>Mails</td>
              <td>30</td>
              <td>Tu les envoies à 19h, pas demain</td>
            </tr>
            <tr>
              <td>Conversations</td>
              <td>8</td>
              <td>Numéros ou métier faux → change de verticale jeudi</td>
            </tr>
            <tr>
              <td>RDV posés</td>
              <td>2</td>
              <td>OK si 8 relances datées. Mort si tu as “réfléchi”</td>
            </tr>
            <tr>
              <td>Crews contactés</td>
              <td>6 messages</td>
              <td>Sans ça, un close J3 te casse</td>
            </tr>
          </tbody>
        </table>

        <div className="okbox">
          <strong>Interdit demain.</strong> Tourner un essai. Refaire le site. Baisser
          le prix. Offrir un pilote gratuit. Recruter un associé. Lancer le YouTube.
          <br />
          <strong>Autorisé.</strong> Appeler, écrire, closer, staffer.
        </div>
      </main>
      <Footer />
    </>
  )
}
