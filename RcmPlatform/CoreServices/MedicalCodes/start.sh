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
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

echo "📦 Starting services with Docker Compose..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Testing application..."
python test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Application started successfully!"
    echo ""
    echo "Access the application at:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To stop the application, run: docker-compose down"
else
    echo ""
    echo "❌ Application failed to start properly."
    echo "Check the logs with: docker-compose logs"
    exit 1
fi 