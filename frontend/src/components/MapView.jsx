import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, Circle } from 'react-leaflet'
import { useEffect, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Distinct colors for each route
const routeColors = [
  '#667eea', // Purple
  '#f093fb', // Pink
  '#4facfe', // Blue
  '#43e97b', // Green
  '#fa709a'  // Coral
]

// Custom icons for different POI types
const createCustomIcon = (color, type) => {
  const icons = {
    poi: '🏛️',
    restaurant: '🍽️',
    hotel: '🏨',
    park: '🌳',
    viewpoint: '👁️',
    museum: '🏛️'
  }
  
  const icon = icons[type] || '📍'
  
  return L.divIcon({
    className: 'custom-poi-marker',
    html: `<div style="
      background: ${color};
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    ">${icon}</div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  })
}

function MapUpdater({ routes }) {
  const map = useMap()
  
  useEffect(() => {
    if (routes.length > 0) {
      const bounds = []
      routes.forEach(route => {
        bounds.push([route.start.lat, route.start.lon])
        bounds.push([route.end.lat, route.end.lon])
        if (route.geometry) {
          route.geometry.forEach(coord => bounds.push([coord[1], coord[0]]))
        }
      })
      if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] })
      }
    }
  }, [routes, map])
  
  return null
}

function MapView({ routes, selectedRoute, onSelectRoute }) {
  const defaultCenter = [37.0902, -95.7129]
  const defaultZoom = 4
  const [hoveredRoute, setHoveredRoute] = useState(null)

  return (
    <MapContainer
      center={defaultCenter}
      zoom={defaultZoom}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MapUpdater routes={routes} />
      
      {routes.map((route, index) => {
        const isSelected = selectedRoute?.id === route.id
        const isHovered = hoveredRoute === route.id
        const color = routeColors[index % routeColors.length]
        const opacity = isSelected ? 1 : (isHovered ? 0.7 : 0.5)
        const weight = isSelected ? 6 : (isHovered ? 4 : 3)
        
        // Get route path
        const positions = route.geometry 
          ? route.geometry.map(coord => [coord[1], coord[0]])
          : [
              [route.start.lat, route.start.lon],
              ...route.waypoints.map(wp => [wp.lat, wp.lon]),
              [route.end.lat, route.end.lon]
            ]
        
        return (
          <div key={route.id}>
            {/* Route line */}
            <Polyline
              positions={positions}
              color={color}
              weight={weight}
              opacity={opacity}
              eventHandlers={{
                click: () => onSelectRoute(route),
                mouseover: () => setHoveredRoute(route.id),
                mouseout: () => setHoveredRoute(null)
              }}
            >
              <Popup>
                <div style={{ minWidth: '200px' }}>
                  <h3 style={{ margin: '0 0 10px 0', color: color }}>
                    Route {index + 1}: {route.variant_type}
                  </h3>
                  <p><strong>Distance:</strong> {route.distance_km.toFixed(1)} km</p>
                  <p><strong>Duration:</strong> {route.duration_hours.toFixed(1)} hours</p>
                  <p><strong>POIs:</strong> {route.poi_count || 0}</p>
                  <p><strong>Restaurants:</strong> {route.dining_count || 0}</p>
                  <p><strong>Hotels:</strong> {route.lodging_count || 0}</p>
                  <button 
                    onClick={() => onSelectRoute(route)}
                    style={{
                      background: color,
                      color: 'white',
                      border: 'none',
                      padding: '8px 16px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      marginTop: '10px'
                    }}
                  >
                    View Details
                  </button>
                </div>
              </Popup>
            </Polyline>
            
            {/* Start marker */}
            <Marker position={[route.start.lat, route.start.lon]}>
              <Popup>
                <strong>Start</strong><br/>
                {route.start.name}
              </Popup>
            </Marker>
            
            {/* End marker */}
            <Marker position={[route.end.lat, route.end.lon]}>
              <Popup>
                <strong>End</strong><br/>
                {route.end.name}
              </Popup>
            </Marker>
            
            {/* Show POIs, restaurants, and hotels for selected route */}
            {isSelected && (
              <>
                {/* POIs */}
                {route.poi_list?.map((poi, idx) => (
                  <Marker
                    key={`poi-${idx}`}
                    position={[poi.lat, poi.lon]}
                    icon={createCustomIcon(color, poi.type)}
                  >
                    <Popup>
                      <div style={{ minWidth: '180px' }}>
                        <h4 style={{ margin: '0 0 8px 0', color: color }}>
                          {poi.name}
                        </h4>
                        <p style={{ margin: '4px 0' }}>
                          <strong>Type:</strong> {poi.type}
                        </p>
                        {poi.rating && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Rating:</strong> {'⭐'.repeat(Math.floor(poi.rating))} {poi.rating}
                          </p>
                        )}
                        {poi.description && (
                          <p style={{ margin: '4px 0', fontSize: '12px', color: '#666' }}>
                            {poi.description}
                          </p>
                        )}
                      </div>
                    </Popup>
                  </Marker>
                ))}
                
                {/* Restaurants */}
                {route.dining_list?.map((restaurant, idx) => (
                  <Marker
                    key={`dining-${idx}`}
                    position={[restaurant.lat, restaurant.lon]}
                    icon={createCustomIcon(color, 'restaurant')}
                  >
                    <Popup>
                      <div style={{ minWidth: '180px' }}>
                        <h4 style={{ margin: '0 0 8px 0', color: color }}>
                          🍽️ {restaurant.name}
                        </h4>
                        <p style={{ margin: '4px 0' }}>
                          <strong>Type:</strong> {restaurant.type}
                        </p>
                        {restaurant.cuisine && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Cuisine:</strong> {restaurant.cuisine}
                          </p>
                        )}
                        {restaurant.rating && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Rating:</strong> {'⭐'.repeat(Math.floor(restaurant.rating))} {restaurant.rating}
                          </p>
                        )}
                        {restaurant.price_level && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Price:</strong> {'$'.repeat(restaurant.price_level)}
                          </p>
                        )}
                      </div>
                    </Popup>
                  </Marker>
                ))}
                
                {/* Hotels */}
                {route.lodging_list?.map((hotel, idx) => (
                  <Marker
                    key={`lodging-${idx}`}
                    position={[hotel.lat, hotel.lon]}
                    icon={createCustomIcon(color, 'hotel')}
                  >
                    <Popup>
                      <div style={{ minWidth: '180px' }}>
                        <h4 style={{ margin: '0 0 8px 0', color: color }}>
                          🏨 {hotel.name}
                        </h4>
                        <p style={{ margin: '4px 0' }}>
                          <strong>Type:</strong> {hotel.type}
                        </p>
                        {hotel.rating && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Rating:</strong> {'⭐'.repeat(Math.floor(hotel.rating))} {hotel.rating}
                          </p>
                        )}
                        {hotel.price_level && (
                          <p style={{ margin: '4px 0' }}>
                            <strong>Price:</strong> {'$'.repeat(hotel.price_level)}
                          </p>
                        )}
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </>
            )}
          </div>
        )
      })}
    </MapContainer>
  )
}

export default MapView

// Made with Bob - Improved version with better visibility and interactivity