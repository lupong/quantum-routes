import './RouteList.css'

function RouteList({ routes, selectedRoute, onSelectRoute }) {
  if (routes.length === 0) return null

  return (
    <div className="route-list">
      <h3>📋 Optimized Routes</h3>
      {routes.map((route, index) => (
        <div
          key={route.id}
          className={`route-card ${selectedRoute?.id === route.id ? 'selected' : ''}`}
          onClick={() => onSelectRoute(route)}
        >
          <div className="route-header">
            <span className="route-number">Route {index + 1}</span>
            {route.quantum_optimized && <span className="quantum-badge">⚛️</span>}
          </div>
          
          <div className="route-stats">
            <div className="stat">
              <span className="stat-label">Distance</span>
              <span className="stat-value">{route.distance_km.toFixed(0)} km</span>
            </div>
            <div className="stat">
              <span className="stat-label">Duration</span>
              <span className="stat-value">{route.duration_hours.toFixed(1)} hrs</span>
            </div>
          </div>

          <div className="route-scores">
            <div className="score-bar">
              <span>🏞️ Scenic</span>
              <div className="bar">
                <div className="fill" style={{width: `${route.scenic_score * 100}%`}}></div>
              </div>
            </div>
            <div className="score-bar">
              <span>📍 POI</span>
              <div className="bar">
                <div className="fill" style={{width: `${route.poi_score * 100}%`}}></div>
              </div>
            </div>
            <div className="score-bar">
              <span>🍽️ Dining</span>
              <div className="bar">
                <div className="fill" style={{width: `${route.dining_score * 100}%`}}></div>
              </div>
            </div>
            <div className="score-bar">
              <span>🏨 Lodging</span>
              <div className="bar">
                <div className="fill" style={{width: `${route.lodging_score * 100}%`}}></div>
              </div>
            </div>
          </div>

          <div className="route-highlights">
            <div className="highlight">
              <strong>{route.poi_count}</strong> POIs
            </div>
            <div className="highlight">
              <strong>{route.dining_count}</strong> Restaurants
            </div>
            <div className="highlight">
              <strong>{route.lodging_count}</strong> Hotels
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RouteList
