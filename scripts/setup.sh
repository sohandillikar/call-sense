#!/bin/bash

# AI Business Assistant - Docker Setup Script
# This script helps set up the development environment

set -e

echo "🚀 Setting up AI Business Assistant..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed (try both v1 and v2)
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Use docker compose (v2) if available, otherwise fall back to docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ .env file created from template."
    else
        echo "❌ env.example template not found. Please create .env manually."
        exit 1
    fi
    
    echo "   Required API keys:"
    echo "   - GLADIA_API_KEY (for call transcription)"
    echo "   - BRIGHT_DATA_API_KEY (for web scraping)"
    echo "   - TIGERDATA_API_KEY (for time-series analytics)"
    echo "   - OPENAI_API_KEY (optional, for AI analysis)"
    echo ""
    echo "   You can also set these as environment variables instead."
else
    echo "✅ .env file already exists."
fi

# Build and start the services
echo "🔨 Building Docker images..."
$DOCKER_COMPOSE build

echo "🚀 Starting services..."
$DOCKER_COMPOSE up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are healthy
echo "🔍 Checking service health..."

# Check PostgreSQL
if $DOCKER_COMPOSE exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check Redis
if $DOCKER_COMPOSE exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
fi

# Check FastAPI app
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI application is ready"
else
    echo "❌ FastAPI application is not ready"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Service URLs:"
echo "   - FastAPI App: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "🛠️  Optional Management Tools:"
echo "   - pgAdmin: http://localhost:5050 (admin@ai-business-assistant.com / admin)"
echo "   - Redis Commander: http://localhost:8081"
echo "   To start these tools, run: $DOCKER_COMPOSE --profile tools up -d"
echo ""
echo "📚 Useful Commands:"
echo "   - View logs: $DOCKER_COMPOSE logs -f"
echo "   - Stop services: $DOCKER_COMPOSE down"
echo "   - Restart services: $DOCKER_COMPOSE restart"
echo "   - Rebuild and restart: $DOCKER_COMPOSE up --build -d"
echo ""
echo "🔧 Development Commands:"
echo "   - Run migrations: $DOCKER_COMPOSE exec app alembic upgrade head"
echo "   - Create migration: $DOCKER_COMPOSE exec app alembic revision --autogenerate -m 'Description'"
echo "   - Access app shell: $DOCKER_COMPOSE exec app bash"
echo "   - Access database: $DOCKER_COMPOSE exec postgres psql -U postgres -d ai_business_assistant"
