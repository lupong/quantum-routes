import { useState } from 'react'
import './RouteForm.css'

const EXAMPLE_LOCATIONS = {
  houston: { lat: 29.7604, lon: -95.3698, name: 'Houston, TX' },
  denver: { lat: 39.7392, lon: -104.9903, name: 'Denver, CO' },
  sanfrancisco: { lat: 37.7749, lon: -122.4194, name: 'San Francisco, CA' },
  newyork: { lat: 40.7128, lon: -74.0060, name: 'New York, NY' },
  chicago: { lat: 41.8781, lon: -87.6298, name: 'Chicago, IL' },
  seattle: { lat: 47.6062, lon: -122.3321, name: 'Seattle, WA' }
}

function RouteForm({ onSubmit, onLoadExample, loading }) {
  const [formData, setFormData] = useState({
    startLat: 29.7604,
    startLon: -95.3698,
    endLat: 39.7392,
    endLon: -104.9903,
    preferences: {
      scenic: 0.4,
      dining: 0.2,
      lodging: 0.2,
      poi: 0.2
    },
    numRoutes: 3,
    useQuantum: true
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handlePreferenceChange = (key, value) => {
    setFormData(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: parseFloat(value)
      }
    }))
  }

  const setLocation = (field, location) => {
    if (field === 'start') {
      setFormData(prev => ({
        ...prev,
        startLat: location.lat,
        startLon: location.lon
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        endLat: location.lat,
        endLon: location.lon
      }))
    }
  }

  return (
    <div className="route-form">
      <h2>🗺️ Plan Your Route</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Start Location</h3>
          <div className="location-quick-select">
            {Object.entries(EXAMPLE_LOCATIONS).map(([key, loc]) => (
              <button
                key={key}
                type="button"
                className="location-btn"
                onClick={() => setLocation('start', loc)}
              >
                {loc.name}
              </button>
            ))}
          </div>
          <div className="form-row">
            <input
              type="number"
              step="0.0001"
              value={formData.startLat}
              onChange={(e) => setFormData({...formData, startLat: parseFloat(e.target.value)})}
              placeholder="Latitude"
            />
            <input
              type="number"
              step="0.0001"
              value={formData.startLon}
              onChange={(e) => setFormData({...formData, startLon: parseFloat(e.target.value)})}
              placeholder="Longitude"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>End Location</h3>
          <div className="location-quick-select">
            {Object.entries(EXAMPLE_LOCATIONS).map(([key, loc]) => (
              <button
                key={key}
                type="button"
                className="location-btn"
                onClick={() => setLocation('end', loc)}
              >
                {loc.name}
              </button>
            ))}
          </div>
          <div className="form-row">
            <input
              type="number"
              step="0.0001"
              value={formData.endLat}
              onChange={(e) => setFormData({...formData, endLat: parseFloat(e.target.value)})}
              placeholder="Latitude"
            />
            <input
              type="number"
              step="0.0001"
              value={formData.endLon}
              onChange={(e) => setFormData({...formData, endLon: parseFloat(e.target.value)})}
              placeholder="Longitude"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>Optimization Preferences</h3>
          <div className="preference-slider">
            <label>
              🏞️ Scenic Value: {(formData.preferences.scenic * 100).toFixed(0)}%
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={formData.preferences.scenic}
                onChange={(e) => handlePreferenceChange('scenic', e.target.value)}
              />
            </label>
          </div>
          <div className="preference-slider">
            <label>
              🍽️ Dining Options: {(formData.preferences.dining * 100).toFixed(0)}%
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={formData.preferences.dining}
                onChange={(e) => handlePreferenceChange('dining', e.target.value)}
              />
            </label>
          </div>
          <div className="preference-slider">
            <label>
              🏨 Lodging: {(formData.preferences.lodging * 100).toFixed(0)}%
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={formData.preferences.lodging}
                onChange={(e) => handlePreferenceChange('lodging', e.target.value)}
              />
            </label>
          </div>
          <div className="preference-slider">
            <label>
              📍 Points of Interest: {(formData.preferences.poi * 100).toFixed(0)}%
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={formData.preferences.poi}
                onChange={(e) => handlePreferenceChange('poi', e.target.value)}
              />
            </label>
          </div>
        </div>

        <div className="form-section">
          <label>
            Number of Routes:
            <input
              type="number"
              min="1"
              max="5"
              value={formData.numRoutes}
              onChange={(e) => setFormData({...formData, numRoutes: parseInt(e.target.value)})}
            />
          </label>
        </div>

        <div className="form-section">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={formData.useQuantum}
              onChange={(e) => setFormData({...formData, useQuantum: e.target.checked})}
            />
            ⚛️ Use Quantum Optimization
          </label>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? '🔄 Optimizing...' : '🚀 Find Routes'}
          </button>
          <button 
            type="button" 
            className="btn-secondary" 
            onClick={onLoadExample}
            disabled={loading}
          >
            📍 Load Example
          </button>
        </div>
      </form>
    </div>
  )
}

export default RouteForm

// Made with Bob
