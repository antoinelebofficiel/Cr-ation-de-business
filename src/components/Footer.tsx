import { Link } from '../lib/router'

export function Footer() {
  return (
    <footer className="wrap footer">
      <div>PREUVE · Une journée avec · 8 places / trimestre</div>
      <div>
        <a href="mailto:antoinebch.pro@gmail.com">antoinebch.pro@gmail.com</a>
        {' · '}
        <Link href="/systeme">Cockpit interne</Link>
      </div>
    </footer>
  )
}
