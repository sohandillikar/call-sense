#!/bin/bash

# Start development servers for Customer Calls Manager

echo "🚀 Starting Customer Calls Manager Development Environment"
echo "=================================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check if ports are available
echo "Checking port availability..."
check_port 8000 || echo "Backend port 8000 is in use - make sure to stop existing backend"
check_port 3000 || echo "Frontend port 3000 is in use - make sure to stop existing frontend"

echo ""
echo "Starting Backend Server (FastAPI)..."
cd backend
python server.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo ""
echo "Starting Frontend Server (Vite)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Development servers started!"
echo "=================================================="
echo "Backend API:  http://localhost:8000"
echo "Frontend UI:  http://localhost:3000"
echo "API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping development servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
