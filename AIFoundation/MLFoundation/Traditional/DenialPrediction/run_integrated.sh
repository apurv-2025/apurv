#!/bin/bash

# DenialPrediction + Claims Service Integrated System Startup Script
# This script starts both services with proper integration

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

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    docker-compose -f docker-compose.integrated.yml down
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Check prerequisites
print_status "Checking prerequisites..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    else
        DOCKER_COMPOSE_CMD="docker compose"
    fi
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

print_success "Docker and Docker Compose are available"

# Check if ports are available
print_status "Checking port availability..."

check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $port is already in use"
        return 1
    else
        print_success "Port $port is available"
        return 0
    fi
}

check_port 5435 || print_warning "PostgreSQL port 5435 may have conflicts"
check_port 8002 || print_warning "Claims Service port 8002 may have conflicts"
check_port 8003 || print_warning "DenialPrediction port 8003 may have conflicts"
check_port 3002 || print_warning "Claims Frontend port 3002 may have conflicts"
check_port 3003 || print_warning "DenialPrediction Frontend port 3003 may have conflicts"

# Display system information
echo ""
print_status "DenialPrediction + Claims Service Integrated System"
echo "=========================================================="
echo ""
echo "📋 System Components:"
echo "  • Claims Service (FHIR-compliant): http://localhost:8002"
echo "  • Claims Service Frontend: http://localhost:3002"
echo "  • DenialPrediction API (ML): http://localhost:8003"
echo "  • DenialPrediction Frontend: http://localhost:3003"
echo "  • PostgreSQL Database: localhost:5435"
echo "  • MLflow (Model Tracking): http://localhost:5000"
echo "  • Redis (Caching): localhost:6379"
echo ""

# Stop any existing containers
print_status "Stopping any existing containers..."
$DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml down --remove-orphans

# Build and start services
print_status "Building and starting services..."
$DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml up --build -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 45

# Check service health
print_status "Checking service health..."

# Check Claims Service
print_status "  • Checking Claims Service..."
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    print_success "    ✅ Claims Service is healthy"
else
    print_warning "    ⚠️  Claims Service health check failed"
fi

# Check DenialPrediction API
print_status "  • Checking DenialPrediction API..."
if curl -f http://localhost:8003/health > /dev/null 2>&1; then
    print_success "    ✅ DenialPrediction API is healthy"
else
    print_warning "    ⚠️  DenialPrediction API health check failed"
fi

# Check integration health
print_status "  • Checking integration health..."
if curl -f http://localhost:8003/health/integration > /dev/null 2>&1; then
    print_success "    ✅ Integration is healthy"
else
    print_warning "    ⚠️  Integration health check failed"
fi

# Check database
print_status "  • Checking database..."
if docker exec claims-integrated-db pg_isready -U fhir_user -d fhir_claims_db > /dev/null 2>&1; then
    print_success "    ✅ Database is healthy"
else
    print_warning "    ⚠️  Database health check failed"
fi

echo ""
print_success "Integrated system is running!"
echo ""
echo "📊 Access Points:"
echo "  • Claims Service API: http://localhost:8002"
echo "  • Claims Service Docs: http://localhost:8002/docs"
echo "  • Claims Service Frontend: http://localhost:3002"
echo "  • DenialPrediction API: http://localhost:8003"
echo "  • DenialPrediction Docs: http://localhost:8003/docs"
echo "  • DenialPrediction Frontend: http://localhost:3003"
echo "  • MLflow UI: http://localhost:5000"
echo ""
echo "🔍 Test Integration:"
echo "  • Test DenialPrediction scoring: curl -X POST http://localhost:8003/api/v1/predict"
echo "  • Get claims from service: curl http://localhost:8003/api/v1/claims/from-service"
echo "  • Score claims from service: curl -X POST http://localhost:8003/api/v1/predict/from-claims-service"
echo "  • Get integration stats: curl http://localhost:8003/api/v1/stats/integration"
echo ""
echo "📝 Logs:"
echo "  • View all logs: $DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml logs -f"
echo "  • Claims Service logs: $DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml logs -f claims-service"
echo "  • DenialPrediction logs: $DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml logs -f denial-prediction-api"
echo ""
echo "🛠️  Management:"
echo "  • Stop system: $DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml down"
echo "  • Restart system: $DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml restart"
echo "  • View containers: docker ps | grep claims-integrated"
echo ""
echo "Press Ctrl+C to stop the system"

# Keep the script running and show logs
print_status "Showing real-time logs (press Ctrl+C to stop)..."
$DOCKER_COMPOSE_CMD -f docker-compose.integrated.yml logs -f 