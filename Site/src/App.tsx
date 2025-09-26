import './App.css'
import Jobs from './Pages/Jobs'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Detail from './Pages/Detail'
import ErrorBoundary from './components/ErrorBoundary'
import Admin from './Pages/Admin'

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Jobs />} />
          <Route path="/detail" element={<Detail />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
