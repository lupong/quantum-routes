"""
Quantum Scenic Route Optimizer - FastAPI Backend
Main API endpoints for route optimization using quantum computing
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from quantum_optimizer import QuantumRouteOptimizer
from route_scorer import RouteScorer

app = FastAPI(
    title="Quantum Scenic Route Optimizer",
    description="Find optimal scenic routes using quantum computing",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
use_quantum = os.getenv("IBM_QUANTUM_TOKEN") is not None
quantum_optimizer = QuantumRouteOptimizer(use_quantum_hardware=use_quantum)
route_scorer = RouteScorer()


# Request/Response Models
class RouteRequest(BaseModel):
    start_lat: float = Field(..., description="Starting latitude")
    start_lon: float = Field(..., description="Starting longitude")
    end_lat: float = Field(..., description="Ending latitude")
    end_lon: float = Field(..., description="Ending longitude")
    preferences: Dict[str, float] = Field(
        default={'scenic': 0.25, 'dining': 0.25, 'lodging': 0.25, 'poi': 0.25},
        description="Optimization preferences (weights should sum to 1.0)"
    )
    num_routes: int = Field(default=3, ge=1, le=5, description="Number of routes to return")
    use_quantum: bool = Field(default=True, description="Use quantum optimization")


class POIModel(BaseModel):
    name: str
    type: str
    lat: float
    lon: float
    rating: Optional[float] = None
    description: Optional[str] = None


class WaypointModel(BaseModel):
    lat: float
    lon: float
    name: str


class RouteResponse(BaseModel):
    id: str
    start: WaypointModel
    end: WaypointModel
    waypoints: List[WaypointModel]
    distance_km: float
    duration_hours: float
    variant_type: str
    scenic_score: float
    poi_score: float
    dining_score: float
    lodging_score: float
    overall_score: float
    poi_count: int
    dining_count: int
    lodging_count: int
    poi_list: List[Dict]
    dining_list: List[Dict]
    lodging_list: List[Dict]
    geometry: Optional[List[List[float]]] = None
    quantum_optimized: bool = False


class OptimizationResponse(BaseModel):
    routes: List[RouteResponse]
    quantum_used: bool
    message: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Quantum Scenic Route Optimizer",
        "quantum_available": use_quantum
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "quantum_optimizer": "initialized",
        "route_scorer": "initialized",
        "quantum_hardware_available": use_quantum,
        "osrm_available": True  # Could add actual check
    }


@app.post("/api/routes/optimize", response_model=OptimizationResponse)
async def optimize_routes(request: RouteRequest):
    """
    Optimize scenic routes between two points using quantum computing
    
    This endpoint:
    1. Generates candidate routes using OSRM
    2. Scores routes based on POI data from OpenStreetMap
    3. Uses QAOA quantum algorithm to find optimal route selection
    4. Returns top-k routes with detailed information
    """
    try:
        # Validate coordinates
        if not (-90 <= request.start_lat <= 90) or not (-90 <= request.end_lat <= 90):
            raise HTTPException(status_code=400, detail="Invalid latitude values")
        if not (-180 <= request.start_lon <= 180) or not (-180 <= request.end_lon <= 180):
            raise HTTPException(status_code=400, detail="Invalid longitude values")
        
        # Normalize preferences
        pref_sum = sum(request.preferences.values())
        if pref_sum > 0:
            preferences = {k: v/pref_sum for k, v in request.preferences.items()}
        else:
            preferences = {'scenic': 0.25, 'dining': 0.25, 'lodging': 0.25, 'poi': 0.25}
        
        # Generate candidate routes using OSRM
        print(f"Generating routes from ({request.start_lat}, {request.start_lon}) to ({request.end_lat}, {request.end_lon})")
        candidate_routes = route_scorer.generate_candidate_routes(
            start=(request.start_lat, request.start_lon),
            end=(request.end_lat, request.end_lon),
            num_routes=min(request.num_routes * 2, 8)  # Generate more candidates
        )
        
        if not candidate_routes:
            raise HTTPException(status_code=500, detail="Failed to generate routes")
        
        # Use quantum optimization if requested and available
        quantum_used = False
        if request.use_quantum and use_quantum:
            try:
                print("Running quantum optimization...")
                selected_indices = quantum_optimizer.optimize_routes(
                    candidate_routes,
                    preferences,
                    num_routes_to_select=request.num_routes
                )
                
                # Get selected routes
                optimized_routes = [candidate_routes[idx] for idx, _ in selected_indices]
                for route in optimized_routes:
                    route['quantum_optimized'] = True
                quantum_used = True
                
            except Exception as e:
                print(f"Quantum optimization failed: {e}, using classical ranking")
                optimized_routes = sorted(
                    candidate_routes,
                    key=lambda r: (
                        preferences.get('scenic', 0.25) * r.get('scenic_score', 0) +
                        preferences.get('dining', 0.25) * r.get('dining_score', 0) +
                        preferences.get('lodging', 0.25) * r.get('lodging_score', 0) +
                        preferences.get('poi', 0.25) * r.get('poi_score', 0)
                    ),
                    reverse=True
                )[:request.num_routes]
        else:
            # Classical ranking
            print("Using classical optimization...")
            optimized_routes = sorted(
                candidate_routes,
                key=lambda r: (
                    preferences.get('scenic', 0.25) * r.get('scenic_score', 0) +
                    preferences.get('dining', 0.25) * r.get('dining_score', 0) +
                    preferences.get('lodging', 0.25) * r.get('lodging_score', 0) +
                    preferences.get('poi', 0.25) * r.get('poi_score', 0)
                ),
                reverse=True
            )[:request.num_routes]
        
        # Convert to response format
        route_responses = []
        for route in optimized_routes:
            route_responses.append(RouteResponse(
                id=route['id'],
                start=WaypointModel(**route['start']),
                end=WaypointModel(**route['end']),
                waypoints=[WaypointModel(**wp) for wp in route['waypoints']],
                distance_km=route['distance_km'],
                duration_hours=route['duration_hours'],
                variant_type=route['variant_type'],
                scenic_score=route['scenic_score'],
                poi_score=route['poi_score'],
                dining_score=route['dining_score'],
                lodging_score=route['lodging_score'],
                overall_score=route['overall_score'],
                poi_count=route['poi_count'],
                dining_count=route['dining_count'],
                lodging_count=route['lodging_count'],
                poi_list=route['poi_list'],
                dining_list=route['dining_list'],
                lodging_list=route['lodging_list'],
                geometry=route.get('geometry'),
                quantum_optimized=route.get('quantum_optimized', False)
            ))
        
        message = "Routes optimized using quantum computing" if quantum_used else "Routes ranked using classical optimization"
        
        return OptimizationResponse(
            routes=route_responses,
            quantum_used=quantum_used,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in route optimization: {e}")
        raise HTTPException(status_code=500, detail=f"Route optimization failed: {str(e)}")


@app.get("/api/routes/example")
async def get_example_routes():
    """Get example routes for demo purposes (Houston to Denver)"""
    # Houston coordinates
    houston = (29.7604, -95.3698)
    # Denver coordinates
    denver = (39.7392, -104.9903)
    
    request = RouteRequest(
        start_lat=houston[0],
        start_lon=houston[1],
        end_lat=denver[0],
        end_lon=denver[1],
        preferences={'scenic': 0.4, 'dining': 0.2, 'lodging': 0.2, 'poi': 0.2},
        num_routes=3,
        use_quantum=False  # Use classical for quick demo
    )
    
    return await optimize_routes(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
