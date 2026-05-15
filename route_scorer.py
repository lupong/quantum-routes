"""
Route Scoring System
Scores routes based on scenic value, POI, dining, and lodging
Uses OSRM for real routing and Overpass API for POI data
"""
import requests
import random
from typing import List, Dict, Tuple
import math


class RouteScorer:
    """Scores routes based on multiple criteria using real data sources"""
    
    def __init__(self):
        # OSRM public server (can be self-hosted for production)
        self.osrm_base = "http://router.project-osrm.org"
        # Overpass API for OpenStreetMap POI data
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
        self.poi_types = ['park', 'viewpoint', 'museum', 'attraction', 'waterfall', 'monument']
        self.dining_types = ['restaurant', 'cafe', 'fast_food', 'bar']
        self.lodging_types = ['hotel', 'motel', 'guest_house', 'hostel', 'camp_site']
    
    def generate_candidate_routes(
        self, 
        start: Tuple[float, float], 
        end: Tuple[float, float],
        num_routes: int = 5
    ) -> List[Dict]:
        """
        Generate candidate routes using OSRM with different routing preferences
        
        Args:
            start: (lat, lon) tuple
            end: (lat, lon) tuple
            num_routes: Number of candidate routes to generate
        
        Returns:
            List of route dictionaries with real routing data
        """
        routes = []
        
        # Get main route from OSRM
        main_route = self._get_osrm_route(start, end)
        if not main_route:
            print("Warning: OSRM request failed, using fallback")
            return self._generate_fallback_routes(start, end, num_routes)
        
        routes.append(main_route)
        
        # Generate alternative routes by adding waypoints
        for i in range(1, num_routes):
            alt_route = self._get_alternative_route(start, end, i)
            if alt_route:
                routes.append(alt_route)
        
        # Score all routes with POI data
        for route in routes:
            self._score_route_with_real_data(route)
        
        return routes
    
    def _get_osrm_route(
        self, 
        start: Tuple[float, float], 
        end: Tuple[float, float],
        waypoints: List[Tuple[float, float]] = None
    ) -> Dict:
        """Get route from OSRM routing engine"""
        try:
            # Build coordinates string: lon,lat format for OSRM
            coords = f"{start[1]},{start[0]}"
            
            if waypoints:
                for wp in waypoints:
                    coords += f";{wp[1]},{wp[0]}"
            
            coords += f";{end[1]},{end[0]}"
            
            # Request route with geometry and steps
            url = f"{self.osrm_base}/route/v1/driving/{coords}"
            params = {
                'overview': 'full',
                'geometries': 'geojson',
                'steps': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] != 'Ok' or not data['routes']:
                return None
            
            route_data = data['routes'][0]
            
            # Extract waypoints from geometry
            geometry = route_data['geometry']['coordinates']
            waypoint_indices = list(range(0, len(geometry), max(1, len(geometry) // 10)))
            
            route = {
                'id': f'route_osrm_{hash(coords) % 10000}',
                'start': {'lat': start[0], 'lon': start[1], 'name': 'Start'},
                'end': {'lat': end[0], 'lon': end[1], 'name': 'End'},
                'waypoints': [
                    {'lat': geometry[i][1], 'lon': geometry[i][0], 'name': f'Point {j}'}
                    for j, i in enumerate(waypoint_indices)
                ],
                'geometry': geometry,  # Full route geometry
                'distance_km': route_data['distance'] / 1000,
                'duration_hours': route_data['duration'] / 3600,
                'variant_type': 'direct' if not waypoints else 'scenic'
            }
            
            return route
            
        except Exception as e:
            print(f"OSRM request failed: {e}")
            return None
    
    def _get_alternative_route(
        self, 
        start: Tuple[float, float], 
        end: Tuple[float, float],
        variant: int
    ) -> Dict:
        """Generate alternative route by adding intermediate waypoints"""
        # Calculate midpoint with offset for variation
        lat_mid = (start[0] + end[0]) / 2
        lon_mid = (start[1] + end[1]) / 2
        
        # Add perpendicular offset to create alternative route
        lat_diff = end[0] - start[0]
        lon_diff = end[1] - start[1]
        
        # Perpendicular direction
        offset_factor = 0.2 * (1 if variant % 2 == 0 else -1)
        waypoint = (
            lat_mid - lon_diff * offset_factor,
            lon_mid + lat_diff * offset_factor
        )
        
        return self._get_osrm_route(start, end, [waypoint])
    
    def _generate_fallback_routes(
        self, 
        start: Tuple[float, float], 
        end: Tuple[float, float],
        num_routes: int
    ) -> List[Dict]:
        """Fallback route generation if OSRM fails"""
        routes = []
        lat_diff = end[0] - start[0]
        lon_diff = end[1] - start[1]
        distance = math.sqrt(lat_diff**2 + lon_diff**2) * 111
        
        for i in range(num_routes):
            num_waypoints = random.randint(3, 6)
            waypoints = []
            
            for j in range(num_waypoints):
                progress = (j + 1) / (num_waypoints + 1)
                offset = (i - 2) * 0.1
                
                lat = start[0] + lat_diff * progress + random.uniform(-0.3, 0.3) * offset
                lon = start[1] + lon_diff * progress + random.uniform(-0.3, 0.3) * offset
                waypoints.append({'lat': lat, 'lon': lon, 'name': f'Waypoint {j+1}'})
            
            route = {
                'id': f'route_fallback_{i}',
                'start': {'lat': start[0], 'lon': start[1], 'name': 'Start'},
                'end': {'lat': end[0], 'lon': end[1], 'name': 'End'},
                'waypoints': waypoints,
                'distance_km': distance * (1 + random.uniform(-0.1, 0.2)),
                'duration_hours': distance / 80 * (1 + random.uniform(-0.1, 0.2)),
                'variant_type': ['scenic', 'fast', 'balanced'][i % 3]
            }
            routes.append(route)
        
        return routes
    
    def _score_route_with_real_data(self, route: Dict) -> None:
        """Score route using real POI data from Overpass API"""
        # Get bounding box for route
        all_points = [route['start']] + route['waypoints'] + [route['end']]
        lats = [p['lat'] for p in all_points]
        lons = [p['lon'] for p in all_points]
        
        bbox = (min(lats) - 0.1, min(lons) - 0.1, max(lats) + 0.1, max(lons) + 0.1)
        
        # Query POIs from Overpass API
        pois = self._query_overpass_pois(bbox)
        dining = self._query_overpass_amenities(bbox, ['restaurant', 'cafe', 'fast_food'])
        lodging = self._query_overpass_amenities(bbox, ['hotel', 'motel', 'guest_house', 'hostel'])
        
        # Calculate scores based on real data
        distance = route['distance_km']
        
        route['poi_count'] = len(pois)
        route['poi_list'] = pois[:20]  # Limit to top 20
        route['poi_score'] = min(1.0, len(pois) / max(10, distance / 50))
        
        route['dining_count'] = len(dining)
        route['dining_list'] = dining[:15]
        route['dining_score'] = min(1.0, len(dining) / max(5, distance / 100))
        
        route['lodging_count'] = len(lodging)
        route['lodging_list'] = lodging[:10]
        route['lodging_score'] = min(1.0, len(lodging) / max(2, distance / 200))
        
        # Scenic score based on natural features
        natural_pois = [p for p in pois if p['type'] in ['park', 'viewpoint', 'waterfall', 'nature_reserve']]
        route['scenic_score'] = min(1.0, len(natural_pois) / max(5, distance / 100))
        
        route['overall_score'] = (
            route['scenic_score'] * 0.3 +
            route['poi_score'] * 0.3 +
            route['dining_score'] * 0.2 +
            route['lodging_score'] * 0.2
        )
    
    def _query_overpass_pois(self, bbox: Tuple[float, float, float, float]) -> List[Dict]:
        """Query POIs from Overpass API"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["tourism"~"attraction|viewpoint|museum|artwork"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
              node["natural"~"peak|waterfall|spring"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
              node["leisure"~"park|nature_reserve"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
            );
            out body;
            """
            
            response = requests.post(self.overpass_url, data={'data': query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            pois = []
            for element in data.get('elements', []):
                if 'lat' in element and 'lon' in element:
                    tags = element.get('tags', {})
                    poi = {
                        'name': tags.get('name', 'Unnamed POI'),
                        'type': tags.get('tourism') or tags.get('natural') or tags.get('leisure', 'attraction'),
                        'lat': element['lat'],
                        'lon': element['lon'],
                        'description': tags.get('description', ''),
                        'rating': 4.0  # Default rating
                    }
                    pois.append(poi)
            
            return pois
            
        except Exception as e:
            print(f"Overpass POI query failed: {e}")
            # Fallback: Generate mock POIs for demo purposes
            return self._generate_mock_pois(bbox)
    
    def _query_overpass_amenities(
        self, 
        bbox: Tuple[float, float, float, float],
        amenity_types: List[str]
    ) -> List[Dict]:
        """Query amenities (dining/lodging) from Overpass API"""
        try:
            amenity_filter = '|'.join(amenity_types)
            query = f"""
            [out:json][timeout:25];
            node["amenity"~"{amenity_filter}"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
            out body;
            """
            
            response = requests.post(self.overpass_url, data={'data': query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            amenities = []
            for element in data.get('elements', []):
                if 'lat' in element and 'lon' in element:
                    tags = element.get('tags', {})
                    amenity = {
                        'name': tags.get('name', f"Unnamed {tags.get('amenity', 'place')}"),
                        'type': tags.get('amenity', 'unknown'),
                        'lat': element['lat'],
                        'lon': element['lon'],
                        'rating': 4.0,
                        'cuisine': tags.get('cuisine', 'Various') if 'restaurant' in amenity_types else None,
                        'price_level': 2
                    }
                    amenities.append(amenity)
            
            return amenities
            
        except Exception as e:
            print(f"Overpass amenity query failed: {e}")
            # Fallback: Generate mock amenities for demo purposes
            return self._generate_mock_amenities(bbox, amenity_types)
    
    def get_route_summary(self, route: Dict) -> str:
        """Generate a human-readable summary of the route"""
        summary = f"""
Route: {route['variant_type'].title()} Route
Distance: {route['distance_km']:.1f} km
Duration: {route['duration_hours']:.1f} hours
Overall Score: {route['overall_score']:.2f}

Highlights:
- {route['poi_count']} points of interest
- {route['dining_count']} dining options
- {route['lodging_count']} lodging options
- Scenic rating: {route['scenic_score']:.2f}/1.0

Top POIs:
"""
        for poi in route['poi_list'][:3]:
            summary += f"  • {poi['name']} ({poi['type']})\n"
        
        return summary.strip()
    
    def _generate_mock_pois(self, bbox: Tuple[float, float, float, float]) -> List[Dict]:
        """Generate mock POIs when Overpass API is unavailable"""
        mock_poi_names = [
            ("Grand Canyon Viewpoint", "viewpoint"),
            ("Historic Downtown", "attraction"),
            ("State Park", "park"),
            ("Natural Springs", "spring"),
            ("Mountain Peak Trail", "peak"),
            ("Scenic Overlook", "viewpoint"),
            ("Art Museum", "museum"),
            ("Botanical Gardens", "park"),
            ("Waterfall Trail", "waterfall"),
            ("Historic Monument", "attraction"),
            ("Nature Reserve", "nature_reserve"),
            ("Sculpture Garden", "artwork"),
            ("Observation Tower", "viewpoint"),
            ("Wildlife Sanctuary", "nature_reserve"),
            ("Heritage Site", "attraction")
        ]
        
        pois = []
        num_pois = random.randint(8, 15)
        
        for i in range(num_pois):
            name, poi_type = random.choice(mock_poi_names)
            lat = random.uniform(bbox[0], bbox[2])
            lon = random.uniform(bbox[1], bbox[3])
            
            pois.append({
                'name': f"{name} #{i+1}",
                'type': poi_type,
                'lat': lat,
                'lon': lon,
                'description': f"A beautiful {poi_type} along your route",
                'rating': round(random.uniform(3.5, 5.0), 1)
            })
        
        return pois
    
    def _generate_mock_amenities(
        self,
        bbox: Tuple[float, float, float, float],
        amenity_types: List[str]
    ) -> List[Dict]:
        """Generate mock amenities when Overpass API is unavailable"""
        mock_restaurants = [
            "The Roadside Diner", "Mountain View Cafe", "Highway Grill",
            "Sunset Restaurant", "Local Bistro", "Family Restaurant",
            "Quick Stop Cafe", "Scenic Eatery", "Traveler's Rest"
        ]
        
        mock_hotels = [
            "Comfort Inn", "Roadside Motel", "Mountain Lodge",
            "Highway Hotel", "Traveler's Inn", "Rest Stop Motel",
            "Scenic View Hotel", "Journey's End Inn"
        ]
        
        amenities = []
        num_amenities = random.randint(6, 12)
        
        for i in range(num_amenities):
            lat = random.uniform(bbox[0], bbox[2])
            lon = random.uniform(bbox[1], bbox[3])
            
            if 'hotel' in amenity_types or 'motel' in amenity_types:
                name = random.choice(mock_hotels)
                amenity_type = random.choice(['hotel', 'motel'])
                cuisine = None
            else:
                name = random.choice(mock_restaurants)
                amenity_type = random.choice(['restaurant', 'cafe', 'fast_food'])
                cuisine = random.choice(['American', 'Mexican', 'Italian', 'Asian', 'Various'])
            
            amenity = {
                'name': f"{name} #{i+1}",
                'type': amenity_type,
                'lat': lat,
                'lon': lon,
                'rating': round(random.uniform(3.5, 4.8), 1),
                'cuisine': cuisine,
                'price_level': random.randint(1, 3)
            }
            amenities.append(amenity)
        
        return amenities

# Made with Bob
