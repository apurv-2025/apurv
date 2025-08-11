#!/bin/bash

# =============================================================================
# Integrated ClaimsAnamoly + Claims Service Startup Script
# =============================================================================

set -e

echo "🚀 Starting Integrated ClaimsAnamoly + Claims Service System"
echo "=========================================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping integrated system..."
    docker-compose -f docker-compose.integrated.yml down
    echo "✅ Cleanup completed"
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Check if integrated docker-compose file exists
if [ ! -f "docker-compose.integrated.yml" ]; then
    echo "❌ docker-compose.integrated.yml not found!"
    exit 1
fi

echo "📋 System Components:"
echo "  • Claims Service (FHIR-compliant): http://localhost:8001"
echo "  • Claims Service Frontend: http://localhost:3000"
echo "  • ClaimsAnamoly API (ML): http://localhost:8000"
echo "  • ClaimsAnamoly Frontend: http://localhost:3001"
echo "  • PostgreSQL Database: localhost:5432"
echo ""

echo "🔧 Starting services..."
docker-compose -f docker-compose.integrated.yml up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

# Check Claims Service
echo "  • Checking Claims Service..."
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "    ✅ Claims Service is healthy"
else
    echo "    ⚠️  Claims Service health check failed"
fi

# Check ClaimsAnamoly API
echo "  • Checking ClaimsAnamoly API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "    ✅ ClaimsAnamoly API is healthy"
else
    echo "    ⚠️  ClaimsAnamoly API health check failed"
fi

# Check integration health
echo "  • Checking integration health..."
if curl -f http://localhost:8000/api/v1/health/integration > /dev/null 2>&1; then
    echo "    ✅ Integration is healthy"
else
    echo "    ⚠️  Integration health check failed"
fi

echo ""
echo "🎉 Integrated system is running!"
echo ""
echo "📊 Access Points:"
echo "  • Claims Service API: http://localhost:8001"
echo "  • Claims Service Docs: http://localhost:8001/docs"
echo "  • Claims Service Frontend: http://localhost:3000"
echo "  • ClaimsAnamoly API: http://localhost:8000"
echo "  • ClaimsAnamoly Docs: http://localhost:8000/docs"
echo "  • ClaimsAnamoly Frontend: http://localhost:3001"
echo ""
echo "🔍 Test Integration:"
echo "  • Test ClaimsAnamoly scoring: curl -X POST http://localhost:8000/api/v1/score"
echo "  • Get claims from service: curl http://localhost:8000/api/v1/claims/from-service"
echo "  • Score claims from service: curl -X POST http://localhost:8000/api/v1/score/from-service"
echo ""
echo "📝 Logs:"
echo "  • View all logs: docker-compose -f docker-compose.integrated.yml logs -f"
echo "  • Claims Service logs: docker-compose -f docker-compose.integrated.yml logs -f claims-service"
echo "  • ClaimsAnamoly logs: docker-compose -f docker-compose.integrated.yml logs -f claims-anomaly-api"
echo ""
echo "Press Ctrl+C to stop the system"

# Keep the script running
wait 