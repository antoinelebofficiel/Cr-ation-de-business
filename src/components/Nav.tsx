import { Link } from '../lib/router'

export function Nav({ cta = '/appliquer' }: { cta?: string }) {
  return (
    <div className="wrap">
      <nav className="nav">
        <Link href="/" className="brand">
          PREUVE
        </Link>
        <div className="nav-links">
          <a href="/#offre">Offre</a>
          <a href="/#methode">Méthode</a>
          <Link href="/systeme">Système</Link>
          <Link href={cta} className="btn">
            Candidater
          </Link>
        </div>
      </nav>
    </div>
  )
}
