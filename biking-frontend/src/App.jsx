import { Routes, Route, Navigate } from 'react-router-dom'
import NavigationBar from './components/NavigationBar'
import TripDurationChart from './components/TripDurationChart'
import TripHourRangeChart from './components/TripHourRangeChart'
import './App.css'

function App() {
  return (
    <div className="App">
      <NavigationBar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/trip-duration" replace />} />
          <Route path="/trip-duration" element={<TripDurationChart />} />
          <Route path="/hour-range" element={<TripHourRangeChart />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

