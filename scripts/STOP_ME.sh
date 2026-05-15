#!/bin/bash

echo "🛑 Stopping Quantum Scenic Route Optimizer..."

# Kill backend
pkill -f "uvicorn main:app"

# Kill frontend
pkill -f "vite"

echo "✅ All services stopped"
