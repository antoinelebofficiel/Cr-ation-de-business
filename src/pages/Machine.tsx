import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Machine() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Système · 1 humain</p>
        <h1>Toi. Zéro monteur. Zéro cadreur en staff. Le client filme. Le logiciel coupe.</h1>
        <p className="lead">
          Un entrepreneur systémique refuse de recruter pour livrer. Il vend un
          protocole + une usine. L’humain ne touche que le close et 45 minutes de QA
          par client.
        </p>
        <p>
          <Link href="/acquisition" className="btn">
            Le robot d’acquisition
          </Link>
        </p>

        <h2>1. Headcount autorisé</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Rôle</th>
              <th>Qui</th>
              <th>Temps</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Vente + QA + média</td>
              <td>Toi</td>
              <td>100 %</td>
            </tr>
            <tr>
              <td>Cadreur</td>
              <td>1 freelance, 1 semaine / mois max</td>
              <td>Uniquement offre Terrain, 4 clients la même ville</td>
            </tr>
            <tr>
              <td>Monteur</td>
              <td>Interdit</td>
              <td>Templates + IA + ta QA</td>
            </tr>
            <tr>
              <td>Community, commercial, stagiaire</td>
              <td>Interdit jusqu’à 20 clients</td>
              <td>—</td>
            </tr>
          </tbody>
        </table>

        <h2>2. Offre calée sur le système</h2>
        <table className="table">
          <thead>
            <tr>
              <th></th>
              <th>Usine</th>
              <th>Terrain</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Prix</td>
              <td>3 400 €/mois + 990 € setup</td>
              <td>4 900 €/mois + 990 €</td>
            </tr>
            <tr>
              <td>Qui filme</td>
              <td>Le fondateur, iPhone + cravate, protocole 40 plans</td>
              <td>1 cadreur, semaine groupée, 4 clients / ville</td>
            </tr>
            <tr>
              <td>Livrable</td>
              <td>24 clips + 8 LinkedIn + 1 YouTube</td>
              <td>Idem</td>
            </tr>
            <tr>
              <td>Ton temps / client / mois</td>
              <td>20 min brief Loom + 45 min QA</td>
              <td>+ 0 (le cadreur est forfait 500 € × 4 = 125 €/client)</td>
            </tr>
          </tbody>
        </table>
        <p>
          Tu vends <strong>Usine</strong> par défaut. Terrain seulement si le client
          refuse de se filmer et qu’il y a 3 autres dates dans un rayon de 2h la même
          semaine. Sinon tu perds le levier.
        </p>

        <h2>3. Tuyauterie (aucun humain dans le tuyau)</h2>
        <div className="steps">
          <div className="step">
            <em>01</em>
            <div>
              <h3>Stripe + Calendly</h3>
              <p className="muted">
                Close → lien de paiement 990 € + 3 400 €. Pas de date d’onboarding
                sans paiement.
              </p>
            </div>
          </div>
          <div className="step">
            <em>02</em>
            <div>
              <h3>Protocole 40 plans (Loom de 9 min, figé)</h3>
              <p className="muted">
                Lever, décision, équipe, produit, client, objection, chiffre, trajet,
                échec, close. Il tourne sa journée. Dossier Drive déjà créé par Zapier
                à la vente.
              </p>
            </div>
          </div>
          <div className="step">
            <em>03</em>
            <div>
              <h3>Dépôt des rushes → n8n</h3>
              <p className="muted">
                Whisper transcrit. Claude sort 24 hooks. Captions / Submagic / CapCut
                template applique les 5 formats. Fichiers nommés, prêts.
              </p>
            </div>
          </div>
          <div className="step">
            <em>04</em>
            <div>
              <h3>QA 45 min (toi)</h3>
              <p className="muted">
                Tu tues 4 clips, tu gardes 24, tu corriges 3 hooks. Si tu passes 2h,
                le protocole client est mauvais, tu ne recrutes pas un monteur.
              </p>
            </div>
          </div>
          <div className="step">
            <em>05</em>
            <div>
              <h3>Late / Upload-Post</h3>
              <p className="muted">
                24 slots sur ses comptes + les 4 meilleurs sur PREUVE. Zéro community.
              </p>
            </div>
          </div>
        </div>

        <h2>4. Stack à payer (≈ 280 €/mois)</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Outil</th>
              <th>Job</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Sales Nav + Instantly + Dropcontact</td>
              <td>Acquisition, déjà défini</td>
            </tr>
            <tr>
              <td>Stripe + Calendly</td>
              <td>Encaisser, booker</td>
            </tr>
            <tr>
              <td>Drive + Zapier/n8n</td>
              <td>Dossier auto, transcription, hooks</td>
            </tr>
            <tr>
              <td>Captions ou Submagic + 5 templates CapCut</td>
              <td>Coupe + sous-titres</td>
            </tr>
            <tr>
              <td>Late</td>
              <td>Publication</td>
            </tr>
          </tbody>
        </table>

        <h2>5. Capacité d’un seul corps</h2>
        <p>
          18 clients Usine = 18 × 45 min QA = 13,5 h/mois. Close : 8 RDV/sem. Il
          reste de la semaine. Le plafond n’est plus le calendrier cadreur. C’est
          tes 8 RDV.
        </p>
        <p>
          6 + 12 + 18 clients à 3 400 € + setups 990 € ≈ <strong>140 k€ / 90 j</strong>.
          200 k€ = 6 Terrain groupés ou 8 Usine de plus, toujours sans recruter.
        </p>

        <h2>6. Règles non négociables</h2>
        <ul>
          <li>Pas de monteur « le temps de démarrer ».</li>
          <li>Pas de tournage solo pour faire plaisir.</li>
          <li>Pas de Terrain pour 1 client isolé.</li>
          <li>Si la QA dépasse 45 min, tu durcis le protocole, tu n’ajoutes pas de main-d’œuvre.</li>
          <li>Le média PREUVE republie les 4 meilleurs clips : l’inbound remplace Instantly à partir de 40 épisodes.</li>
        </ul>
      </main>
      <Footer />
    </>
  )
}
