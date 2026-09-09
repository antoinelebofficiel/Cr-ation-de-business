import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Plan() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Business plan · PREUVE · 90 jours</p>
        <h1>1 humain. Le client filme. Le logiciel coupe. Instantly amène les RDV.</h1>
        <p className="lead">
          Système : <Link href="/machine">/machine</Link>. Acquisition :{' '}
          <Link href="/acquisition">/acquisition</Link>.
        </p>
        <p>
          <Link href="/demain" className="btn">
            To-do de demain
          </Link>
        </p>

        <div className="kpi">
          <div>
            <b>140 k€</b>
            <span className="muted"> CA Usine J1–J90</span>
          </div>
          <div>
            <b>55–65 %</b>
            <span className="muted"> marge brute visée</span>
          </div>
          <div>
            <b>1–2 closes / sem.</b>
            <span className="muted"> rythme minimum</span>
          </div>
        </div>

        <h2>1. Offre</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Prix</th>
              <th>Qui</th>
              <th>Livrable</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Usine</td>
              <td>3 400 €/mois + 990 € setup</td>
              <td>Défaut. Le client filme.</td>
              <td>24 clips, 8 LinkedIn, 1 YouTube</td>
            </tr>
            <tr>
              <td>Terrain</td>
              <td>4 900 €/mois + 990 €</td>
              <td>4 clients, même ville, même semaine</td>
              <td>1 cadreur forfait, puis la même usine</td>
            </tr>
          </tbody>
        </table>
        <p>
          Engagement 90 jours. 1 500 € le jour J. Premier mois à la signature. 24
          clips en 14 jours après tournage, sinon mois suivant offert.
        </p>

        <h2>2. Client</h2>
        <p>
          Fondateur France, CA estimé ≥ 400 k€ : BTP, industrie, formation, cabinet,
          clinique, SaaS B2B, agence chère.
        </p>
        <p className="muted">
          Refus : CA &lt; 400 k€, refus caméra, « 3 Reels », illégal.
        </p>

        <h2>3. Pourquoi Usine à 3 400 €</h2>
        <p>
          Le client fournit la matière. Ton coût variable ≈ 0. 3 400 € pour 24 clips =
          142 €/clip côté lui, ~3 300 € de marge côté toi après outils. Recruter un
          monteur détruit le modèle.
        </p>

        <h2>4. Acquisition — robot + appels chauds</h2>
        <p>
          Processus entier sur <Link href="/acquisition">/acquisition</Link> : Sales
          Nav → Dropcontact → Instantly 200 mails/jour → tu appelles ouvertures et
          clics. 300 nouveaux lundi. 60 appels/jour. 8 RDV/semaine. 1–2 closes.
        </p>

        <h2>5. Production</h2>
        <p>
          Zéro monteur. Templates + IA + 45 min de QA. Cadreur uniquement en Terrain
          groupé (500 € / 4 clients = 125 €). Détail : /machine.
        </p>
        <div className="okbox">
          Coût Usine : ~20 € d’outils alloués. Marge ≈ 3 300 €.
          <br />
          Kill : recruter. Kill : Terrain pour 1 client isolé.
        </div>

        <h2>6. Prévisionnel 90 jours</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Mois</th>
              <th>Actifs</th>
              <th>Mix</th>
              <th>CA</th>
              <th>Coûts prod+ads</th>
              <th>Marge</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>5</td>
              <td>5 Moteurs + 5 setups</td>
              <td>27 000 €</td>
              <td>~6 000 €</td>
              <td>~21 000 €</td>
            </tr>
            <tr>
              <td>2</td>
              <td>10</td>
              <td>10 Moteurs + 5 setups</td>
              <td>46 500 €</td>
              <td>~12 000 €</td>
              <td>~34 500 €</td>
            </tr>
            <tr>
              <td>3</td>
              <td>14</td>
              <td>14 Moteurs + 4 setups</td>
              <td>60 600 €</td>
              <td>~17 000 €</td>
              <td>~43 600 €</td>
            </tr>
            <tr>
              <td>Total</td>
              <td>14 max</td>
              <td></td>
              <td>134 100 €</td>
              <td>~35 000 €</td>
              <td>~99 000 €</td>
            </tr>
          </tbody>
        </table>
        <p className="muted">
          200 k€ = 18 Usine + 6 Terrain groupés, toujours sans salariat.
        </p>

        <h2>7. Structure légale et cash</h2>
        <ul>
          <li>Facture au nom de ta structure actuelle dès le 1er setup.</li>
          <li>Acompte 1 500 € avant de bloquer un cadreur.</li>
          <li>Pas de tournage sans solde du 1er mois encaissé.</li>
          <li>Freelances payés après livraison validée, pas avant.</li>
          <li>Compte ads séparé, budget Ads refacturé au réel.</li>
        </ul>

        <h2>8. Risques et seuils d’arrêt</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Risque</th>
              <th>Seuil</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>0 RDV à J7</td>
              <td>&lt; 8 RDV posés</td>
              <td>3 jours calls only, script du cockpit</td>
            </tr>
            <tr>
              <td>0 close à J21</td>
              <td>0 acompte</td>
              <td>Vérifier Instantly + 60 appels/jour sur les chauds, pas de baisse</td>
            </tr>
            <tr>
              <td>Retard montage</td>
              <td>&gt; 5 jours</td>
              <td>Stop vente, change de monteur le jour même</td>
            </tr>
            <tr>
              <td>Tu tournes</td>
              <td>1 journée caméra</td>
              <td>Échec ops. Annule le shoot, envoie le freelance</td>
            </tr>
            <tr>
              <td>Tréso</td>
              <td>Setup non payé</td>
              <td>Pas de date de tournage</td>
            </tr>
          </tbody>
        </table>

        <h2>9. Jalons</h2>
        <div className="steps">
          <div className="step">
            <em>J1</em>
            <div>
              <h3>Demain — machine allumée</h3>
              <p className="muted">
                Stack payée, 300 leads dans Instantly, 40 appels, 6 Malt. Détail :{' '}
                <Link href="/demain">/demain</Link>.
              </p>
            </div>
          </div>
          <div className="step">
            <em>J10</em>
            <div>
              <h3>1er acompte</h3>
              <p className="muted">Setup 1 500 € + 1er mois. Date de tournage posée. Crew briefé.</p>
            </div>
          </div>
          <div className="step">
            <em>J21</em>
            <div>
              <h3>5 Moteurs signés</h3>
              <p className="muted">5 dates. Liste crews validée (test 200 € déjà fait).</p>
            </div>
          </div>
          <div className="step">
            <em>J45</em>
            <div>
              <h3>12 clips d’un client en ligne</h3>
              <p className="muted">Tes pubs tournent. Saison passe à 8 500 € sans négocier.</p>
            </div>
          </div>
          <div className="step">
            <em>J90</em>
            <div>
              <h3>8 actifs, média lancé</h3>
              <p className="muted">3 portraits YouTube PREUVE publics. File d’attente pour le trimestre 2.</p>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
