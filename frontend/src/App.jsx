import { Routes, Route } from 'react-router'
import Layout from './components/Layout'
import LandingPage from './components/LandingPage'
import Debugger from './components/Debugger'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LandingPage />} />
      </Route>
      <Route path="/debug" element={<Debugger />} />
    </Routes>
  )
}

export default App


