#!/bin/bash

# Prior Authorization System Startup Script

set -e

echo "🚀 Starting Prior Authorization System..."

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
    docker-compose down --remove-orphans
else
    docker compose down --remove-orphans
fi

# Build and start services
echo "🔨 Building and starting services..."
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."

# Check database
if docker exec health_insurance_preauth_db pg_isready -U insuranceuser -d health_insurance_preauth_db > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready"
fi

# Check backend API
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ Backend API is ready"
else
    echo "❌ Backend API is not ready"
fi

# Check frontend
if curl -f http://localhost:3002 > /dev/null 2>&1; then
    echo "✅ Frontend is ready"
else
    echo "❌ Frontend is not ready"
fi

echo ""
echo "🎉 Prior Authorization System is starting up!"
echo ""
echo "📋 Service URLs:"
echo "   Backend API:     http://localhost:8002"
echo "   API Docs:        http://localhost:8002/docs"
echo "   Frontend:        http://localhost:3002"
echo "   Database:        localhost:5435"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:       docker-compose logs -f"
echo "   Stop services:   docker-compose down"
echo "   Restart:         docker-compose restart"
echo ""
echo "🧪 Test the API:"
echo "   curl http://localhost:8002/health"
echo "   curl http://localhost:8002/api/v1/patients/"
echo "" 