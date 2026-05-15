#!/bin/bash

echo "🚀 Starting Quantum Scenic Route Optimizer..."
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "Please wait for backend setup to complete..."
    exit 1
fi

# Start backend in background
echo "📡 Starting backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "📝 Backend logs: tail -f backend.log"
echo ""

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend might still be starting..."
fi

echo ""
echo "🌐 Starting frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "✅ Starting frontend dev server..."
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
