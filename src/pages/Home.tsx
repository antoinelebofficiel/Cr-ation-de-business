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
          Vous filmez votre journée avec un protocole de 40 plans. L’usine sort 24
          clips et une YouTube. 3 400 €/mois. Un humain côté PREUVE : le closer.
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
            <b>1</b>
            <span>Humain côté PREUVE</span>
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
              Vous filmez votre journée avec un protocole. L’usine en tire 24 clips pour
              Instagram, TikTok, LinkedIn, une pièce YouTube, et un épisode du média PREUVE.
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
                <h3>Protocole 40 plans</h3>
                <p className="muted">
                  Loom de 9 minutes. Vous filmez votre journée, iPhone + cravate. Les
                  40 plans sont écrits avant que vous appuyiez sur rec.
                </p>
              </div>
            </div>
            <div className="step">
              <em>02</em>
              <div>
                <h3>Dépôt des rushes</h3>
                <p className="muted">
                  Un dossier Drive s’ouvre à la signature. Vous déposez. L’usine
                  transcrit et coupe.
                </p>
              </div>
            </div>
            <div className="step">
              <em>03</em>
              <div>
                <h3>24 clips + 1 YouTube en 14 jours</h3>
                <p className="muted">
                  5 templates, sous-titres, hook 1,2 s. QA humaine 45 minutes. Huit
                  coupes LinkedIn.
                </p>
              </div>
            </div>
            <div className="step">
              <em>04</em>
              <div>
                <h3>Publication automatique</h3>
                <p className="muted">
                  24 slots sur vos comptes, 4 extraits sur le média PREUVE. Ads en
                  option.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="offre">
        <div className="wrap">
          <p className="kicker">Offre</p>
          <h2>Usine par défaut. Terrain seulement groupé.</h2>
          <p className="muted">990 € de setup. 90 jours. Vous filmez, ou 4 dates la même semaine.</p>
          <div className="card-grid" style={{ marginTop: 32 }}>
            <article className="card featured">
              <span className="tag">Défaut · 0 cadreur</span>
              <h3>Usine</h3>
              <div className="price">3 400 €</div>
              <p className="muted">/ mois</p>
              <ul>
                <li>Vous filmez, protocole 40 plans</li>
                <li>24 clips 30–45s + 8 LinkedIn</li>
                <li>1 YouTube</li>
                <li>Publication auto + média PREUVE</li>
              </ul>
            </article>
            <article className="card">
              <span className="tag">4 clients / ville / semaine</span>
              <h3>Terrain</h3>
              <div className="price">4 900 €</div>
              <p className="muted">/ mois</p>
              <ul>
                <li>1 cadreur, journée groupée</li>
                <li>Même usine derrière</li>
                <li>Interdit pour un client isolé</li>
              </ul>
            </article>
            <article className="card">
              <span className="tag">Refus</span>
              <h3>Hors cadre</h3>
              <div className="price" style={{ fontSize: 28 }}>
                Non
              </div>
              <p className="muted">pas négociable</p>
              <ul>
                <li>CA &lt; 400 k€</li>
                <li>Refus du protocole</li>
                <li>Mois sans engagement</li>
                <li>Monteur dédié</li>
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
