#!/bin/bash

# Scheduling2.0 - Startup Script
# This script helps you start the Scheduling2.0 application

set -e

echo "🚀 Starting Scheduling2.0..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping containers..."
    docker-compose down
    echo "✅ Cleanup complete"
}

# Set up trap to cleanup on script exit
trap cleanup EXIT

# Build and start the application
echo "🔨 Building and starting containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."

# Check database
if docker-compose exec -T postgres pg_isready -U scheduling_user -d scheduling2_db > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready"
    exit 1
fi

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is ready"
else
    echo "❌ Backend is not ready"
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is ready"
else
    echo "❌ Frontend is not ready"
    exit 1
fi

echo ""
echo "🎉 Scheduling2.0 is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the application"

# Keep the script running
wait 