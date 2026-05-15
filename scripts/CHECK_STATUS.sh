#!/bin/bash

echo "🔍 Checking Quantum Scenic Route Optimizer Status..."
echo ""

# Check backend
echo "📡 Backend Status:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ Backend is running at http://localhost:8000"
    curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "  Response: $(curl -s http://localhost:8000/health)"
else
    echo "  ❌ Backend is NOT running"
fi
echo ""

# Check frontend
echo "🌐 Frontend Status:"
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "  ✅ Frontend is running at http://localhost:5173"
else
    echo "  ❌ Frontend is NOT running"
fi
echo ""

# Check processes
echo "🔧 Running Processes:"
ps aux | grep -E "(uvicorn|vite)" | grep -v grep || echo "  No processes found"
echo ""

# Check backend logs
echo "📝 Recent Backend Logs (last 10 lines):"
if [ -f backend.log ]; then
    tail -10 backend.log
else
    echo "  No backend.log file found"
fi
echo ""

# Test API endpoint
echo "🧪 Testing API Endpoint:"
echo "  Sending test request to /api/routes/example..."
curl -s http://localhost:8000/api/routes/example 2>&1 | head -20
echo ""
echo "Done!"
