import { usePath } from './lib/path'
import Acquisition from './pages/Acquisition'
import Appliquer from './pages/Appliquer'
import Demain from './pages/Demain'
import Home from './pages/Home'
import Merci from './pages/Merci'
import Plan from './pages/Plan'
import Systeme from './pages/Systeme'

export default function App() {
  const path = usePath()

  if (path === '/appliquer') return <Appliquer />
  if (path === '/merci') return <Merci />
  if (path === '/systeme') return <Systeme />
  if (path === '/plan') return <Plan />
  if (path === '/demain') return <Demain />
  if (path === '/acquisition') return <Acquisition />
  return <Home />
}
