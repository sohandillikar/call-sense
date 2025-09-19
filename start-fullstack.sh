#!/bin/bash

# Start Full-Stack AI Business Assistant
# This script starts both the backend and frontend

echo "🚀 Starting AI Business Assistant Full-Stack Application"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start backend services
echo "📦 Starting backend services..."
docker compose up -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 10

# Check if backend is healthy
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is ready!"
else
    echo "❌ Backend failed to start. Check logs with: docker compose logs app"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
npm run dev &

# Get the frontend PID
FRONTEND_PID=$!

echo ""
echo "🎉 Full-stack application is running!"
echo "=================================================="
echo "📊 Backend API: http://localhost:8000"
echo "🎨 Frontend UI: http://localhost:5173"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $FRONTEND_PID 2>/dev/null
    cd ..
    docker compose down
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait
