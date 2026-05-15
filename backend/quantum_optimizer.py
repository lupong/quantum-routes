"""
Quantum Route Optimizer using QAOA
Optimizes scenic route selection using quantum computing
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import Sampler
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as RuntimeSampler
from typing import List, Dict, Tuple
import os


class QuantumRouteOptimizer:
    """Uses QAOA to optimize route selection based on multiple objectives"""
    
    def __init__(self, use_quantum_hardware: bool = False):
        self.use_quantum_hardware = use_quantum_hardware
        self.service = None
        
        if use_quantum_hardware:
            token = os.getenv("IBM_QUANTUM_TOKEN")
            crn = os.getenv("IBM_CLOUD_CRN")
            if token and crn:
                try:
                    # Use IBM Cloud channel with CRN
                    self.service = QiskitRuntimeService(
                        channel="ibm_cloud",
                        token=token,
                        instance=crn
                    )
                    print(f"✅ Connected to IBM Quantum Cloud (CRN: {crn[:50]}...)")
                except Exception as e:
                    print(f"Warning: Could not connect to IBM Quantum: {e}")
                    self.use_quantum_hardware = False
            else:
                print(f"Warning: Missing IBM_QUANTUM_TOKEN or IBM_CLOUD_CRN")
                self.use_quantum_hardware = False
    
    def formulate_qubo(self, routes: List[Dict], preferences: Dict[str, float]) -> np.ndarray:
        """
        Convert route optimization to QUBO (Quadratic Unconstrained Binary Optimization)
        
        Args:
            routes: List of route dictionaries with scores
            preferences: User preferences for different factors
        
        Returns:
            QUBO matrix
        """
        n = len(routes)
        Q = np.zeros((n, n))
        
        # Diagonal terms: individual route scores (negative because we minimize)
        for i, route in enumerate(routes):
            score = (
                preferences.get('scenic', 0.25) * route.get('scenic_score', 0) +
                preferences.get('dining', 0.25) * route.get('dining_score', 0) +
                preferences.get('lodging', 0.25) * route.get('lodging_score', 0) +
                preferences.get('poi', 0.25) * route.get('poi_score', 0)
            )
            Q[i, i] = -score  # Negative because QAOA minimizes
        
        # Off-diagonal terms: penalize similar routes (encourage diversity)
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self._calculate_route_similarity(routes[i], routes[j])
                Q[i, j] = similarity * 0.5  # Penalty for selecting similar routes
                Q[j, i] = Q[i, j]
        
        return Q
    
    def _calculate_route_similarity(self, route1: Dict, route2: Dict) -> float:
        """Calculate similarity between two routes (0-1)"""
        # Simple similarity based on shared waypoints
        waypoints1 = set(route1.get('waypoints', []))
        waypoints2 = set(route2.get('waypoints', []))
        
        if not waypoints1 or not waypoints2:
            return 0.0
        
        intersection = len(waypoints1 & waypoints2)
        union = len(waypoints1 | waypoints2)
        
        return intersection / union if union > 0 else 0.0
    
    def build_qaoa_circuit(self, Q: np.ndarray, p: int = 1) -> QuantumCircuit:
        """
        Build QAOA circuit for the QUBO problem
        
        Args:
            Q: QUBO matrix
            p: Number of QAOA layers
        
        Returns:
            Parameterized quantum circuit
        """
        n = Q.shape[0]
        qc = QuantumCircuit(n)
        
        # Initialize in superposition
        qc.h(range(n))
        
        # QAOA layers
        beta = [Parameter(f'β_{i}') for i in range(p)]
        gamma = [Parameter(f'γ_{i}') for i in range(p)]
        
        for layer in range(p):
            # Cost Hamiltonian (problem encoding)
            for i in range(n):
                qc.rz(2 * gamma[layer] * Q[i, i], i)
            
            for i in range(n):
                for j in range(i + 1, n):
                    if Q[i, j] != 0:
                        qc.cx(i, j)
                        qc.rz(2 * gamma[layer] * Q[i, j], j)
                        qc.cx(i, j)
            
            # Mixer Hamiltonian
            for i in range(n):
                qc.rx(2 * beta[layer], i)
        
        # Measurement
        qc.measure_all()
        
        return qc
    
    def optimize_routes(
        self, 
        routes: List[Dict], 
        preferences: Dict[str, float],
        num_routes_to_select: int = 3
    ) -> List[Tuple[int, float]]:
        """
        Optimize route selection using QAOA
        
        Args:
            routes: List of candidate routes
            preferences: User preferences
            num_routes_to_select: Number of routes to return
        
        Returns:
            List of (route_index, score) tuples
        """
        if len(routes) <= num_routes_to_select:
            # If we have fewer routes than requested, return all
            return [(i, self._calculate_total_score(routes[i], preferences)) 
                    for i in range(len(routes))]
        
        # Formulate QUBO
        Q = self.formulate_qubo(routes, preferences)
        
        # Build QAOA circuit
        qc = self.build_qaoa_circuit(Q, p=1)
        
        # Optimize parameters (simplified for hackathon - using fixed params)
        # In production, would use classical optimizer to find best beta/gamma
        params = [0.5, 0.5]  # [beta, gamma]
        
        # Execute circuit
        if self.use_quantum_hardware and self.service:
            try:
                backend = self.service.least_busy(operational=True, simulator=False)
                sampler = RuntimeSampler(backend)
                job = sampler.run([qc], parameter_values=[params], shots=1024)
                result = job.result()
                counts = result[0].data.meas.get_counts()
            except Exception as e:
                print(f"Quantum execution failed: {e}, falling back to simulator")
                counts = self._run_classical_simulation(qc, params)
        else:
            counts = self._run_classical_simulation(qc, params)
        
        # Extract best routes from measurement results
        selected_routes = self._extract_top_routes(counts, routes, preferences, num_routes_to_select)
        
        return selected_routes
    
    def _run_classical_simulation(self, qc: QuantumCircuit, params: List[float]) -> Dict:
        """Run circuit on classical simulator"""
        sampler = Sampler()
        bound_circuit = qc.assign_parameters(params)
        job = sampler.run(bound_circuit, shots=1024)
        result = job.result()
        
        # Convert result to counts dictionary
        quasi_dists = result.quasi_dists[0]
        counts = {format(k, f'0{qc.num_qubits}b'): int(v * 1024) 
                 for k, v in quasi_dists.items()}
        
        return counts
    
    def _calculate_total_score(self, route: Dict, preferences: Dict[str, float]) -> float:
        """Calculate total weighted score for a route"""
        return (
            preferences.get('scenic', 0.25) * route.get('scenic_score', 0) +
            preferences.get('dining', 0.25) * route.get('dining_score', 0) +
            preferences.get('lodging', 0.25) * route.get('lodging_score', 0) +
            preferences.get('poi', 0.25) * route.get('poi_score', 0)
        )
    
    def _extract_top_routes(
        self, 
        counts: Dict, 
        routes: List[Dict],
        preferences: Dict[str, float],
        num_routes: int
    ) -> List[Tuple[int, float]]:
        """Extract top routes from measurement results"""
        route_scores = []
        
        # Analyze measurement results
        for bitstring, count in counts.items():
            # Each bit represents whether to include that route
            selected_indices = [i for i, bit in enumerate(bitstring) if bit == '1']
            
            if len(selected_indices) == 0:
                continue
            
            # Calculate combined score for this selection
            total_score = sum(
                self._calculate_total_score(routes[i], preferences) 
                for i in selected_indices
            ) / len(selected_indices)
            
            # Weight by measurement frequency
            weighted_score = total_score * count
            
            for idx in selected_indices:
                route_scores.append((idx, weighted_score))
        
        # If quantum didn't give good results, fall back to classical ranking
        if not route_scores:
            route_scores = [
                (i, self._calculate_total_score(routes[i], preferences))
                for i in range(len(routes))
            ]
        
        # Aggregate scores for each route
        route_score_dict = {}
        for idx, score in route_scores:
            if idx not in route_score_dict:
                route_score_dict[idx] = 0
            route_score_dict[idx] += score
        
        # Sort and return top routes
        sorted_routes = sorted(route_score_dict.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_routes[:num_routes]

# Made with Bob
