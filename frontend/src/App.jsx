import { useState } from 'react'
import axios from 'axios'
import MapView from './components/MapView'
import RouteForm from './components/RouteForm'
import RouteList from './components/RouteList'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedRoute, setSelectedRoute] = useState(null)
  const [quantumUsed, setQuantumUsed] = useState(false)

  const handleOptimizeRoutes = async (formData) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post(`${API_BASE}/api/routes/optimize`, {
        start_lat: formData.startLat,
        start_lon: formData.startLon,
        end_lat: formData.endLat,
        end_lon: formData.endLon,
        preferences: formData.preferences,
        num_routes: formData.numRoutes,
        use_quantum: formData.useQuantum
      })
      
      setRoutes(response.data.routes)
      setQuantumUsed(response.data.quantum_used)
      if (response.data.routes.length > 0) {
        setSelectedRoute(response.data.routes[0])
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to optimize routes')
      console.error('Route optimization error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLoadExample = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.get(`${API_BASE}/api/routes/example`)
      setRoutes(response.data.routes)
      setQuantumUsed(response.data.quantum_used)
      if (response.data.routes.length > 0) {
        setSelectedRoute(response.data.routes[0])
      }
    } catch (err) {
      setError('Failed to load example routes')
      console.error('Example load error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🗺️⚛️ Quantum Scenic Route Optimizer</h1>
        <p>Find optimal scenic routes using quantum computing</p>
        {quantumUsed && (
          <div className="quantum-badge">✨ Quantum Optimized</div>
        )}
      </header>
      
      <div className="app-content">
        <aside className="sidebar">
          <RouteForm 
            onSubmit={handleOptimizeRoutes}
            onLoadExample={handleLoadExample}
            loading={loading}
          />
          
          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}
          
          {routes.length > 0 && (
            <RouteList 
              routes={routes}
              selectedRoute={selectedRoute}
              onSelectRoute={setSelectedRoute}
            />
          )}
        </aside>
        
        <main className="map-container">
          <MapView 
            routes={routes}
            selectedRoute={selectedRoute}
            onSelectRoute={setSelectedRoute}
          />
        </main>
      </div>
    </div>
  )
}

export default App

// Made with Bob
