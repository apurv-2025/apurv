#!/bin/bash

# Medical Codes Application Startup Script

echo "🚀 Starting Medical Codes Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    echo "📦 Using 'docker compose' (newer version)..."
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "📦 Using 'docker-compose'..."
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo "🛑 Stopping any existing containers..."
$DOCKER_COMPOSE_CMD down

echo "📦 Starting services with Docker Compose..."
$DOCKER_COMPOSE_CMD up -d

echo "⏳ Waiting for database to be ready..."
sleep 15

echo "🗄️ Initializing database..."
# Run database initialization
docker exec -it medicalcodes-backend-1 python -c "
import sys
import os
sys.path.append('/app')

# Create tables
from app.database import engine, Base
from app.models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
Base.metadata.create_all(bind=engine)
print('✅ Database tables created')

# Seed data
from seed_data import seed_database
seed_database()
print('✅ Database seeded successfully')
"

if [ $? -eq 0 ]; then
    echo "✅ Database initialization completed"
else
    echo "❌ Database initialization failed"
    echo "Check the logs with: $DOCKER_COMPOSE_CMD logs backend"
    exit 1
fi

echo "⏳ Waiting for services to fully start..."
sleep 10

echo "🔍 Testing application..."
python test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Application started successfully!"
    echo ""
    echo "Access the application at:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8001"
    echo "  API Documentation: http://localhost:8001/docs"
    echo ""
    echo "To stop the application, run: $DOCKER_COMPOSE_CMD down"
    echo "To view logs, run: $DOCKER_COMPOSE_CMD logs -f"
else
    echo ""
    echo "❌ Application failed to start properly."
    echo "Check the logs with: $DOCKER_COMPOSE_CMD logs"
    exit 1
fi 