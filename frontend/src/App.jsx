import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import PersonaDashboard from './pages/PersonaDashboard'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<PersonaDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
