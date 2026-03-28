import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import Journey from './pages/Journey'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/onboard" element={<Onboarding />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/journey/:journeyId" element={<Journey />} />
    </Routes>
  )
}

export default App
