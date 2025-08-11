#!/bin/bash

# Integrated Prior Authorization + Patient Microservice Startup Script

set -e

echo "🚀 Starting Integrated Prior Authorization + Patient Microservice System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose and try again."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose.integrated.yml down --remove-orphans
else
    docker compose -f docker-compose.integrated.yml down --remove-orphans
fi

# Build and start services
echo "🔨 Building and starting integrated services..."
if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose.integrated.yml up --build -d
else
    docker compose -f docker-compose.integrated.yml up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."

# Check Patient microservice database
if docker exec patient_postgres pg_isready -U fhir_user -d fhir_db > /dev/null 2>&1; then
    echo "✅ Patient Database is ready"
else
    echo "❌ Patient Database is not ready"
fi

# Check Patient microservice backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Patient Microservice Backend is ready"
else
    echo "❌ Patient Microservice Backend is not ready"
fi

# Check Patient microservice frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Patient Microservice Frontend is ready"
else
    echo "❌ Patient Microservice Frontend is not ready"
fi

# Check Prior Authorization database
if docker exec preauth_postgres pg_isready -U insuranceuser -d health_insurance_preauth_db > /dev/null 2>&1; then
    echo "✅ Prior Authorization Database is ready"
else
    echo "❌ Prior Authorization Database is not ready"
fi

# Check Prior Authorization backend API
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Prior Authorization Backend API is ready"
else
    echo "❌ Prior Authorization Backend API is not ready"
fi

# Check Prior Authorization frontend
if curl -f http://localhost:3002 > /dev/null 2>&1; then
    echo "✅ Prior Authorization Frontend is ready"
else
    echo "❌ Prior Authorization Frontend is not ready"
fi

echo ""
echo "🎉 Integrated System is starting up!"
echo ""
echo "📋 Service URLs:"
echo ""
echo "🏥 Patient Microservice:"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   Frontend:        http://localhost:3000"
echo "   Database:        localhost:5432"
echo ""
echo "🔐 Prior Authorization System:"
echo "   Backend API:     http://localhost:8002"
echo "   API Docs:        http://localhost:8002/docs"
echo "   Frontend:        http://localhost:3002"
echo "   Database:        localhost:5435"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:       docker-compose -f docker-compose.integrated.yml logs -f"
echo "   Stop services:   docker-compose -f docker-compose.integrated.yml down"
echo "   Restart:         docker-compose -f docker-compose.integrated.yml restart"
echo ""
echo "🧪 Test the APIs:"
echo "   Patient Service: curl http://localhost:8000/health"
echo "   PreAuth Service: curl http://localhost:8002/health"
echo ""
echo "📝 Integration Notes:"
echo "   - Prior Authorization now uses Patient microservice for patient data"
echo "   - No redundant patient information in Prior Authorization"
echo "   - Patient microservice handles all FHIR Patient operations"
echo "   - Prior Authorization focuses on authorization requests and EDI processing"
echo "" 