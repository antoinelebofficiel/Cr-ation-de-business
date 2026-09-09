import { ApplyForm } from '../components/ApplyForm'
import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Home() {
  return (
    <>
      <Nav />
      <header className="wrap hero">
        <p className="kicker">Média · Clips · YouTube</p>
        <h1>On filme votre journée. Le marché apprend votre nom.</h1>
        <p className="lead">
          PREUVE produit le quotidien des fondateurs : 24 clips de 30 à 45 secondes, une
          vidéo YouTube, une présence dans le média <em>Une journée avec</em>. 3 900 €
          par mois. Un jour de tournage, un calendrier de 30 jours.
        </p>
        <div className="hero-actions">
          <Link href="/appliquer" className="btn">
            Demander une date
          </Link>
          <a href="#offre" className="btn ghost">
            Voir les tarifs
          </a>
        </div>
        <div className="stats">
          <div className="stat">
            <b>30–45s</b>
            <span>Format qui arrête le scroll</span>
          </div>
          <div className="stat">
            <b>24</b>
            <span>Clips livrés chaque mois</span>
          </div>
          <div className="stat">
            <b>8–12 min</b>
            <span>Portrait YouTube par tournage</span>
          </div>
          <div className="stat">
            <b>12</b>
            <span>Clients max en parallèle</span>
          </div>
        </div>
      </header>

      <section className="section">
        <div className="wrap grid-2">
          <div>
            <p className="kicker">Le vrai produit</p>
            <h2>Une saison dans un média de fondateurs, plus la matière pour vos comptes.</h2>
          </div>
          <div>
            <p>
              Un cadreur passe une journée dans votre entreprise. On capte le terrain, les
              décisions, l’équipe, le produit, le rythme. On en tire 24 clips pour Instagram,
              TikTok, LinkedIn, une pièce YouTube, et un épisode du média PREUVE.
            </p>
            <p className="muted">
              L’option Ads met 2 500 € derrière les 2 meilleurs clips. Le contenu ouvre
              des conversations commerciales.
            </p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap grid-2">
          <div>
            <p className="kicker">Pourquoi ça marche</p>
            <h2>Le fondateur invisible perd des deals contre le fondateur filmé.</h2>
          </div>
          <div>
            <p>
              Vos prospects vous googlenent. Ils tombent sur un site et un LinkedIn plat. Le
              concurrent a 40 clips où on le voit décider, livrer, recadrer, vendre. Ils
              choisissent celui qu’ils ont déjà “rencontré”.
            </p>
            <p>
              Les agences vidéo vendent des rushes. PREUVE vend un rythme : un jour de
              capture, un calendrier de 30 jours, une autorité qui s’empile.
            </p>
          </div>
        </div>
      </section>

      <section className="section" id="methode">
        <div className="wrap">
          <p className="kicker">Méthode</p>
          <h2>Quatre mouvements. Zéro flou.</h2>
          <div className="steps">
            <div className="step">
              <em>01</em>
              <div>
                <h3>Brief de 40 minutes</h3>
                <p className="muted">
                  Offre, client idéal, objections, preuves à filmer. On écrit les 12 angles
                  avant d’allumer la caméra.
                </p>
              </div>
            </div>
            <div className="step">
              <em>02</em>
              <div>
                <h3>Tournage d’une journée</h3>
                <p className="muted">
                  7h–18h sur site. Caméra-épaule, son cravate, lumière naturelle. Vous
                  travaillez. On documente.
                </p>
              </div>
            </div>
            <div className="step">
              <em>03</em>
              <div>
                <h3>24 clips + 1 YouTube en 14 jours</h3>
                <p className="muted">
                  5 templates de montage, sous-titres, hook en 1,2 seconde. Huit coupes
                  LinkedIn en plus. Le YouTube tient 8 à 12 minutes.
                </p>
              </div>
            </div>
            <div className="step">
              <em>04</em>
              <div>
                <h3>Publication et, si Empire, ads</h3>
                <p className="muted">
                  Calendrier fourni. Sur Empire, 3 000 € d’ads sur le clip le plus fort.
                  Objectif : messages privés et prises de rendez-vous.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="offre">
        <div className="wrap">
          <p className="kicker">Offre</p>
          <h2>Une offre. Tu la vends telle quelle.</h2>
          <p className="muted">1 500 € de setup. 90 jours. 24 clips, pas 12.</p>
          <div className="card-grid" style={{ marginTop: 32 }}>
            <article className="card featured">
              <span className="tag">Offre unique</span>
              <h3>Moteur</h3>
              <div className="price">3 900 €</div>
              <p className="muted">/ mois</p>
              <ul>
                <li>1 journée de tournage</li>
                <li>24 clips 30–45s</li>
                <li>8 coupes LinkedIn</li>
                <li>1 YouTube 8–12 min</li>
                <li>Calendrier 30 jours + épisode média</li>
              </ul>
            </article>
            <article className="card">
              <span className="tag">Option dès le 2ᵉ mois</span>
              <h3>Moteur + Ads</h3>
              <div className="price">6 400 €</div>
              <p className="muted">/ mois</p>
              <ul>
                <li>Tout le Moteur</li>
                <li>2 500 € d’ads sur les 2 meilleurs clips</li>
                <li>Revue hebdo des DM et RDV</li>
              </ul>
            </article>
            <article className="card">
              <span className="tag">Ce que tu refuses</span>
              <h3>Hors cadre</h3>
              <div className="price" style={{ fontSize: 28 }}>
                Non
              </div>
              <p className="muted">pas négociable</p>
              <ul>
                <li>CA estimé &lt; 400 k€</li>
                <li>« 3 Reels à 800 € »</li>
                <li>Mois sans engagement</li>
                <li>Tu filmes toi-même</li>
              </ul>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap grid-2">
          <div>
            <p className="kicker">Pour qui</p>
            <h2>Fondateurs à 400 k€ et plus, qui vendent de la confiance.</h2>
            <p>
              BTP, industrie, cabinets, formation, SaaS B2B, cliniques, agences qui
              facturent cher. Le visage du dirigeant doit peser dans la décision d’achat.
            </p>
          </div>
          <div>
            <p className="kicker">Refusés</p>
            <ul>
              <li>CA sous 400 k€ : le ticket casse votre trésorerie</li>
              <li>Refus d’être à l’image</li>
              <li>Demande de “juste 3 Reels à 800 €”</li>
              <li>Produit illégal ou flou</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section faq">
        <div className="wrap">
          <p className="kicker">Questions</p>
          <h2>Ce que les fondateurs demandent avant de signer.</h2>
          <details>
            <summary>Vous garantissez les vues ?</summary>
            <p>
              Non.               On garantit 24 clips publiables en 14 jours après tournage, un
              YouTube, et sur Moteur + Ads une mise en ads de 2 500 €. Les vues dépendent de
              l’offre et de l’audience. Les rendez-vous se mesurent dans vos messages.
            </p>
          </details>
          <details>
            <summary>Je n’ai pas le temps.</summary>
            <p>
              Vous travaillez normalement. Le brief prend 40 minutes. Le tournage suit
              votre journée. La publication peut être déléguée à votre community ou à
              nous sur Empire.
            </p>
          </details>
          <details>
            <summary>Et si le rendu est mauvais ?</summary>
            <p>
              Une vague de retakes gratuite si un clip est inutilisable (son mort, visage
              flou, angle raté). Si les 24 clips ne partent pas en 14 jours, le mois
              suivant est offert.
            </p>
          </details>
        </div>
      </section>

      <section className="section" id="candidater">
        <div className="wrap">
          <p className="kicker">Candidature</p>
          <h2>Dossiers incomplets ignorés. CA sous 400 k€ ignoré.</h2>
          <ApplyForm />
        </div>
      </section>

      <Footer />
      <div className="sticky-cta">
        <Link href="/appliquer" className="btn">
          Candidater
        </Link>
      </div>
    </>
  )
}
