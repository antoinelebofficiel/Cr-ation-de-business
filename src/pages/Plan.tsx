import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Plan() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Business plan · PREUVE · 90 jours</p>
        <h1>Vendre 8 places de média-fondateur. Encaisser 161 k€. Livrer sans que tu tournes.</h1>
        <p className="lead">
          PREUVE filme une journée d’un fondateur, livre 12 clips de 30–45 secondes, une
          YouTube, et un épisode du média <em>Une journée avec</em>. Toi : vente et
          close. Freelances : caméra et montage. Plafond : 8 clients.
        </p>
        <p>
          <Link href="/demain" className="btn">
            To-do de demain
          </Link>
        </p>

        <div className="kpi">
          <div>
            <b>170 500 €</b>
            <span className="muted"> CA cible J1–J90</span>
          </div>
          <div>
            <b>55–65 %</b>
            <span className="muted"> marge brute visée</span>
          </div>
          <div>
            <b>1 close / sem.</b>
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
              <td>Pilote</td>
              <td>6 500 €/mois × 90 j + 2 500 € setup</td>
              <td>3 premiers seulement</td>
              <td>1 jour, 12 clips, 1 YouTube, Saison 1 du média</td>
            </tr>
            <tr>
              <td>Saison</td>
              <td>8 500 €/mois + setup</td>
              <td>Standard dès le 4ᵉ</td>
              <td>Idem + versions LinkedIn + calendrier 30 j</td>
            </tr>
            <tr>
              <td>Empire</td>
              <td>14 500 €/mois + setup</td>
              <td>Fondateur qui veut des RDV mesurés</td>
              <td>2 jours, 20 clips, 2 YouTube, 3 000 € d’ads</td>
            </tr>
          </tbody>
        </table>
        <p>
          Engagement 90 jours. Acompte setup le jour de la signature. Premier mois
          prélevé à la signature. Garantie : 12 clips publiables 14 jours après le
          tournage, sinon mois suivant offert.
        </p>

        <h2>2. Client</h2>
        <p>
          Fondateur, France, CA déclaré ou estimé ≥ 200 k€, offre vendue à la
          confiance : BTP, industrie, formation, cabinet, clinique, SaaS B2B, agence
          chère. Le visage du dirigeant pèse dans le deal.
        </p>
        <p className="muted">
          Refus automatique : CA &lt; 200 k€, refus d’être à l’image, demande de 3
          Reels à 800 €, activité illégale.
        </p>

        <h2>3. Pourquoi le prix tient</h2>
        <p>
          Un client à 8 500 €/mois qui signe un seul contrat de 4 000 € grâce aux
          clips a déjà payé le trimestre. Tu vends des conversations commerciales
          filmées, avec un calendrier, plus une place rare dans un média (8 / trimestre).
        </p>
        <p>
          Ton avantage : cold call + cold email + ads Facebook déjà prouvés sur le
          nettoyage. Les videastes n’ont pas la distribution. Empire emballe les ads
          dans le contrat.
        </p>

        <h2>4. Acquisition — 80 conversations / semaine</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Canal</th>
              <th>Volume</th>
              <th>Job</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Cold call</td>
              <td>40 / jour</td>
              <td>Prendre le RDV de 12 minutes</td>
            </tr>
            <tr>
              <td>Cold email perso</td>
              <td>30 / jour</td>
              <td>Même angle, preuve + rareté</td>
            </tr>
            <tr>
              <td>LinkedIn / site</td>
              <td>10 inbound / sem. dès J21</td>
              <td>Relance sous 1 heure</td>
            </tr>
            <tr>
              <td>Ads (après 1er cas filmé)</td>
              <td>30 €/jour</td>
              <td>Extraits du client 1 vers fondateurs similaires</td>
            </tr>
          </tbody>
        </table>
        <p>
          Entonnoir à tenir : 200 touches → 12 conversations → 8 RDV/sem → 1 close/sem
          × 8 semaines = 8 contrats. Taux de close visé sur RDV : 12–15 %. Si tu es
          sous 8 %, tu changes l’angle, pas le prix.
        </p>

        <h2>5. Production</h2>
        <p>
          3 binômes cadreur + monteur freelance. Cadreur 500 €/jour. Monteur 250 €/clip,
          livré en 48 h. Toi jamais derrière la caméra. Stop vente si un clip a plus de
          5 jours de retard.
        </p>
        <div className="okbox">
          Coût Saison : 500 + 12 × 250 = 3 500 € → marge ~5 000 €.
          <br />
          Coût Empire : 1 000 + 5 000 + 3 000 ads = 9 000 € → marge ~5 500 €.
          <br />
          Kill : toute offre qui descend sous 4 000 € de marge brute.
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
              <td>3</td>
              <td>2 Pilote + 1 Saison + 3 setups</td>
              <td>29 000 €</td>
              <td>~10 500 €</td>
              <td>~18 500 €</td>
            </tr>
            <tr>
              <td>2</td>
              <td>6</td>
              <td>+3 Saison + 1 Empire + 3 setups</td>
              <td>60 500 €</td>
              <td>~23 500 €</td>
              <td>~37 000 €</td>
            </tr>
            <tr>
              <td>3</td>
              <td>8</td>
              <td>2 Pilote + 4 Saison + 2 Empire + 2 setups</td>
              <td>81 000 €</td>
              <td>~32 000 €</td>
              <td>~49 000 €</td>
            </tr>
            <tr>
              <td>Total</td>
              <td>8 max</td>
              <td></td>
              <td>170 500 €</td>
              <td>~66 000 €</td>
              <td>~104 500 €</td>
            </tr>
          </tbody>
        </table>
        <p className="muted">
          200 k€ = +2 Empire au trimestre, ou Saison à 10 500 € dès le mois 2 après 3
          cas filmés. Confiance 70 % si 80 conversations/sem et 3 crews au jour 10. 20 %
          si tu filmes toi-même ou si tu casses le prix.
        </p>

        <h2>7. Structure légale et cash</h2>
        <ul>
          <li>Facture au nom de ta structure actuelle dès le 1er setup.</li>
          <li>Acompte 2 500 € avant de bloquer un cadreur.</li>
          <li>Pas de tournage sans solde du 1er mois encaissé.</li>
          <li>Freelances payés après livraison validée, pas avant.</li>
          <li>Compte ads séparé, budget Empire refacturé au réel.</li>
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
              <td>Pilote à 6 500 € uniquement, 40 appels/jour, pas de baisse</td>
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
                120 noms, 40 appels, 30 mails, 3 Malt cadreurs, 3 Malt monteurs, clé
                Google révoquée. Détail heure par heure sur <Link href="/demain">/demain</Link>.
              </p>
            </div>
          </div>
          <div className="step">
            <em>J10</em>
            <div>
              <h3>1er acompte</h3>
              <p className="muted">Setup 2 500 € + 1er mois. Date de tournage posée. Crew briefé.</p>
            </div>
          </div>
          <div className="step">
            <em>J21</em>
            <div>
              <h3>3 Pilotes signés</h3>
              <p className="muted">3 dates. Liste crews validée (test 200 € déjà fait).</p>
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
