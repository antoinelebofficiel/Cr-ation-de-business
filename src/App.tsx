import { usePath } from './lib/path'
import Appliquer from './pages/Appliquer'
import Home from './pages/Home'
import Merci from './pages/Merci'
import Systeme from './pages/Systeme'

export default function App() {
  const path = usePath()

  if (path === '/appliquer') return <Appliquer />
  if (path === '/merci') return <Merci />
  if (path === '/systeme') return <Systeme />
  return <Home />
}
