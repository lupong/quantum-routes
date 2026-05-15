# Quantum Scenic Route Optimizer 🗺️⚛️

A quantum-powered web application that finds optimal scenic routes between cities using IBM Quantum computing and real-world data.

[![Quantum](https://img.shields.io/badge/Quantum-IBM%20Qiskit-blueviolet)](https://quantum.ibm.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)](https://fastapi.tiangolo.com/)

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
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide
- [YOUR_TASKS.md](YOUR_TASKS.md) - User task checklist
- [HACKATHON_NOTES.md](HACKATHON_NOTES.md) - Development history

**Archived Docs** (older deployment guides):
- `docs/archive/` - Previous deployment documentation

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

Built with:
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

**Built with ⚛️ quantum computing and ❤️ for scenic road trips**