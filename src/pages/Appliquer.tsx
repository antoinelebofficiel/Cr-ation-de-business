import { ApplyForm } from '../components/ApplyForm'
import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'

export default function Appliquer() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Candidature</p>
        <h1>Une place. Un fondateur. Un trimestre.</h1>
        <p className="lead">
          Réponse sous 24 heures ouvrées. Appel de 20 minutes ensuite. Signature et
          acompte de 2 500 € pour bloquer la date de tournage.
        </p>
        <div style={{ marginTop: 36 }}>
          <ApplyForm />
        </div>
      </main>
      <Footer />
    </>
  )
}
