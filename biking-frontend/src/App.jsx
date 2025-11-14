import { useState } from 'react'
import TripDurationChart from './components/TripDurationChart'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Biking Data Analyzer</h1>
      </header>
      <main>
        <TripDurationChart />
      </main>
    </div>
  )
}

export default App

