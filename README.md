# Quantum Scenic Route Optimizer 🗺️⚛️
## Built with IBM Bob: From Idea to Impact in One Day

**A full-stack quantum web application built entirely with IBM Bob in ~6 hours**

This project demonstrates how Bob accelerates development velocity—taking a developer with zero quantum computing experience from empty repository to working quantum-powered application in a single afternoon.

[![Quantum](https://img.shields.io/badge/Quantum-IBM%20Qiskit-blueviolet)](https://quantum.ibm.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)](https://fastapi.tiangolo.com/)

---

## 🚀 Built with Bob

**Total Development Time**: ~6 hours (May 15, 2026)  
**Total Bobcoins Consumed**: 7.58 Bobcoins  
**Lines of Code**: ~2,500+ across backend, frontend, and infrastructure  
**Developer Quantum Experience**: Zero → Production-ready

### What Bob Built End-to-End

Bob handled the complete development lifecycle without manual intervention:

1. **Quantum Algorithm Implementation** (1.50 Bobcoins)
   - QAOA (Quantum Approximate Optimization Algorithm) circuit design
   - QUBO problem formulation for multi-objective route optimization
   - IBM Quantum Runtime integration with cloud authentication
   - Classical fallback mechanism when quantum hardware unavailable

2. **Backend API Development** (1.50 Bobcoins)
   - FastAPI server with Pydantic validation models
   - OSRM integration for real driving routes
   - OpenStreetMap Overpass API for POI data
   - Multi-objective scoring system (scenic, dining, lodging, POI)
   - CORS configuration and error handling

3. **Frontend Application** (0.44 Bobcoins)
   - React 18 + Vite build system
   - Interactive Leaflet.js map visualization
   - Form components with preference sliders
   - Route comparison interface
   - Responsive CSS styling

4. **Infrastructure & DevOps** (1.00 Bobcoins)
   - Docker configuration
   - Shell scripts for one-command startup/shutdown
   - Environment variable management
   - Multiple deployment configurations (Heroku, Fly.io, Railway, IBM Cloud)

5. **Documentation** (2.14 Bobcoins)
   - Comprehensive technical documentation
   - API reference
   - Deployment guides
   - Development session notes

6. **Failed Deployment Attempts** (2.00 Bobcoins - wasted)
   - IBM Cloud Code Engine exploration (account limitations discovered)
   - Multiple platform evaluations

### Bob's Repo-Wide Context in Action

Three concrete moments where Bob's understanding of the entire codebase mattered:

1. **QAOA Bitstring → Route Scoring Integration**  
   Bob wired the quantum measurement results from `quantum_optimizer.py` (bitstrings representing route selections) directly into the multi-objective scoring layer in `route_scorer.py`, ensuring the QUBO cost function weights matched the user's preference sliders from the React form. The quantum circuit's cost Hamiltonian encodes the exact same `scenic_score`, `dining_score`, `lodging_score`, and `poi_score` that the frontend displays.

2. **Classical Fallback Path**  
   When quantum hardware is unavailable, Bob implemented a seamless fallback in `quantum_optimizer.py` that uses the same scoring logic as the quantum path, ensuring consistent results. The `main.py` endpoint handles both paths transparently, and the frontend shows a "✨ Quantum Optimized" badge only when real quantum hardware was used—all without the user needing to understand the difference.

3. **Pydantic Models ↔ React Form Consistency**  
   Bob kept the `RouteRequest` Pydantic model in `backend/main.py` (with fields like `start_lat`, `start_lon`, `preferences`, `num_routes`, `use_quantum`) perfectly synchronized with the React form state in `frontend/src/components/RouteForm.jsx`. The preference weights sum to 1.0 on both sides, and the API validates this server-side while the frontend enforces it with range sliders.

---

## 🎯 Why This Matters for "Turn Idea into Impact Faster"

This project is a case study in AI-accelerated development:

- **Non-Expert → Production**: A developer with no quantum computing background shipped a working quantum application in one day
- **Full-Stack Velocity**: Bob handled backend (Python/FastAPI), frontend (React/Vite), quantum algorithms (Qiskit), infrastructure (Docker), and documentation—no context switching
- **Real Integration**: Not a toy demo—uses actual IBM Quantum hardware, real OSRM routing data, and real OpenStreetMap POI data
- **Production-Ready Code**: Clean architecture, type hints, error handling, CORS, environment variables, one-command deployment

**The quantum algorithm is the proof point**—it demonstrates Bob can handle complex, specialized domains (quantum computing) while maintaining consistency across the entire stack. The same AI that wrote QAOA circuits also wrote React components and deployment scripts.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/quantum-scenic-routes.git
cd quantum-scenic-routes

# 2. (Optional) Add IBM Quantum token
cp backend/.env.example backend/.env
# Edit backend/.env and add your token from https://quantum.ibm.com/

# 3. Start everything
./scripts/RUN_ME.sh

# 4. Open http://localhost:5173 in your browser
```

**That's it!** The app works without a quantum token (uses classical fallback).

---

## ✨ Features

- **🔬 Real Quantum Computing**: Uses QAOA algorithm on IBM Quantum hardware
- **🗺️ Real Routing Data**: OSRM for actual driving routes
- **📍 Real POI Data**: OpenStreetMap via Overpass API
- **🎯 Multi-Objective Optimization**: Balance scenic, dining, lodging, and POI
- **🗺️ Interactive Maps**: Leaflet.js visualization with route comparison
- **⚡ Fast & Modern**: FastAPI backend, React frontend, Vite build
- **🔄 Classical Fallback**: Works without quantum access

---

## 📸 Demo

Try these example scenarios:

1. **Scenic Road Trip**: Houston → Denver (Scenic 60%)
2. **Foodie Tour**: San Francisco → Seattle (Dining 50%)
3. **Balanced Trip**: Chicago → New York (All 25%)

---

## 🏗️ Architecture

```
Frontend (React + Leaflet)
    ↓ HTTP/REST
Backend (FastAPI + Qiskit)
    ↓
├─→ OSRM (Routing)
├─→ Overpass API (POI Data)
└─→ IBM Quantum (QAOA Optimization)
```

**Tech Stack**:
- Backend: Python, FastAPI, Qiskit, IBM Quantum Runtime
- Frontend: React, Vite, Leaflet, Axios
- Quantum: QAOA algorithm, IBM Quantum hardware

---

## 🎯 How It Works

1. **User Input**: Select cities and set preferences (scenic, POI, dining, lodging)
2. **Route Generation**: OSRM creates candidate routes with real road data
3. **POI Scoring**: OpenStreetMap data scores each route for attractions, dining, lodging
4. **Quantum Optimization**: QAOA algorithm finds optimal route combinations
5. **Visualization**: Interactive map displays routes with detailed scores

### Quantum Algorithm (QAOA)

The route optimization uses **Quantum Approximate Optimization Algorithm**:
- Formulates route selection as QUBO problem
- Encodes user preferences as cost function weights
- Executes on IBM Quantum hardware
- Extracts top routes from quantum measurements
- Falls back to classical optimization if quantum unavailable

---

## 📚 Documentation

**Complete documentation is now consolidated in one place:**

👉 **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete guide covering:
- Quick Start & Installation
- Architecture & Design
- Usage Guide & API Reference
- Quantum Algorithm Details
- Deployment Options
- Troubleshooting
- Development Notes

**Quick Reference**:
- [HACKATHON_NOTES.md](HACKATHON_NOTES.md) - Bob development case study
- [YOUR_TASKS.md](YOUR_TASKS.md) - User task checklist

---

## 🛠️ Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- IBM Quantum account (optional, free tier available)

### Manual Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Scripts

- `./scripts/RUN_ME.sh` - Start both backend and frontend
- `./scripts/STOP_ME.sh` - Stop all services
- `./scripts/CHECK_STATUS.sh` - Check if services are running

---

## 🚀 Deployment

### Local Development (Recommended)
```bash
./scripts/RUN_ME.sh
```

### Public Access with ngrok
```bash
ngrok http 8000
```

### Production Deployment

**Recommended Platforms**:
1. **Heroku** - Free tier, CLI support
2. **Fly.io** - Modern platform, fast deployment
3. **Railway** - Simple pricing, GitHub integration
4. **IBM Cloud** - Native integration (requires paid account)

See [DOCUMENTATION.md](DOCUMENTATION.md#deployment-options) for detailed deployment guides.

---

## 📊 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/routes/optimize` - Main optimization endpoint
- `GET /api/routes/example` - Example route (Houston → Denver)

Full API reference in [DOCUMENTATION.md](DOCUMENTATION.md#api-reference).

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend won't start?**
```bash
cd frontend
npm install
npm run dev
```

**Ports in use?**
```bash
./scripts/STOP_ME.sh
./scripts/RUN_ME.sh
```

More troubleshooting in [DOCUMENTATION.md](DOCUMENTATION.md#troubleshooting).

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

---

## 📝 License

MIT License - Built for hackathon demonstration

---

## 🙏 Acknowledgments

**Built with**:
- [IBM Bob](https://www.ibm.com/products/watsonx-code-assistant) - AI pair programmer that built this entire project
- [IBM Quantum Platform](https://quantum.ibm.com/)
- [Qiskit](https://qiskit.org/) - Quantum computing SDK
- [OpenStreetMap](https://www.openstreetmap.org/) - POI data
- [OSRM](http://project-osrm.org/) - Routing engine
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework
- [Leaflet](https://leafletjs.com/) - Map visualization

---

## 📞 Support

- **Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- **IBM Quantum**: https://quantum.ibm.com/docs
- **Qiskit Tutorials**: https://qiskit.org/learn

---

**Built with ⚛️ quantum computing, 🤖 IBM Bob, and ❤️ for scenic road trips**