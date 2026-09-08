import { Footer } from '../components/Footer'
import { Nav } from '../components/Nav'
import { Link } from '../lib/router'

export default function Merci() {
  return (
    <>
      <Nav />
      <main className="wrap section">
        <p className="kicker">Dossier reçu</p>
        <h1>On vous rappelle si le profil tient.</h1>
        <p className="lead">
          Si votre CA dépasse 200 k€ et que vous acceptez d’être filmé, vous aurez un
          créneau d’appel. Préparez votre offre, votre prix moyen, et 3 clients que vous
          voulez attirer.
        </p>
        <p style={{ marginTop: 28 }}>
          <Link href="/" className="btn">
            Retour
          </Link>
        </p>
      </main>
      <Footer />
    </>
  )
}
