#!/bin/bash

# AI Business Assistant - Development Helper Script
# This script provides common development commands

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "AI Business Assistant - Development Helper"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  build       Build and start services"
    echo "  logs        Show logs for all services"
    echo "  logs-app    Show logs for FastAPI app only"
    echo "  shell       Access FastAPI app shell"
    echo "  db-shell    Access PostgreSQL shell"
    echo "  redis-shell Access Redis shell"
    echo "  migrate     Run database migrations"
    echo "  migrate-new Create new migration"
    echo "  test        Run tests (if available)"
    echo "  clean       Clean up containers and volumes"
    echo "  status      Show service status"
    echo "  tools       Start management tools (pgAdmin, Redis Commander)"
    echo "  help        Show this help message"
    echo ""
}

# Function to check if services are running
check_services() {
    # Use docker compose (v2) if available, otherwise fall back to docker-compose (v1)
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    if ! $DOCKER_COMPOSE ps | grep -q "Up"; then
        print_warning "Services are not running. Starting them..."
        $DOCKER_COMPOSE up -d
        sleep 10
    fi
}

# Main script logic
case "${1:-help}" in
    start)
        print_status "Starting all services..."
        $DOCKER_COMPOSE up -d
        print_success "Services started!"
        ;;
    
    stop)
        print_status "Stopping all services..."
        $DOCKER_COMPOSE down
        print_success "Services stopped!"
        ;;
    
    restart)
        print_status "Restarting all services..."
        $DOCKER_COMPOSE restart
        print_success "Services restarted!"
        ;;
    
    build)
        print_status "Building and starting services..."
        $DOCKER_COMPOSE up --build -d
        print_success "Services built and started!"
        ;;
    
    logs)
        print_status "Showing logs for all services..."
        $DOCKER_COMPOSE logs -f
        ;;
    
    logs-app)
        print_status "Showing logs for FastAPI app..."
        $DOCKER_COMPOSE logs -f app
        ;;
    
    shell)
        check_services
        print_status "Accessing FastAPI app shell..."
        $DOCKER_COMPOSE exec app bash
        ;;
    
    db-shell)
        check_services
        print_status "Accessing PostgreSQL shell..."
        $DOCKER_COMPOSE exec postgres psql -U postgres -d ai_business_assistant
        ;;
    
    redis-shell)
        check_services
        print_status "Accessing Redis shell..."
        $DOCKER_COMPOSE exec redis redis-cli
        ;;
    
    migrate)
        check_services
        print_status "Running database migrations..."
        $DOCKER_COMPOSE exec app alembic upgrade head
        print_success "Migrations completed!"
        ;;
    
    migrate-new)
        if [ -z "$2" ]; then
            print_error "Please provide a migration message: $0 migrate-new 'Your migration message'"
            exit 1
        fi
        check_services
        print_status "Creating new migration: $2"
        $DOCKER_COMPOSE exec app alembic revision --autogenerate -m "$2"
        print_success "Migration created!"
        ;;
    
    test)
        check_services
        print_status "Running tests..."
        $DOCKER_COMPOSE exec app python -m pytest tests/ -v
        ;;
    
    clean)
        print_warning "This will remove all containers, networks, and volumes. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            print_status "Cleaning up..."
            $DOCKER_COMPOSE down -v --remove-orphans
            docker system prune -f
            print_success "Cleanup completed!"
        else
            print_status "Cleanup cancelled."
        fi
        ;;
    
    status)
        print_status "Service status:"
        $DOCKER_COMPOSE ps
        echo ""
        print_status "Health checks:"
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            print_success "FastAPI app is healthy"
        else
            print_error "FastAPI app is not responding"
        fi
        ;;
    
    tools)
        print_status "Starting management tools..."
        $DOCKER_COMPOSE --profile tools up -d
        print_success "Management tools started!"
        echo "pgAdmin: http://localhost:5050 (admin@ai-business-assistant.com / admin)"
        echo "Redis Commander: http://localhost:8081"
        ;;
    
    help|*)
        show_help
        ;;
esac
