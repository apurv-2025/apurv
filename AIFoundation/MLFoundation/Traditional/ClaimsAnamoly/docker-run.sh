#!/bin/bash

# Claims Anomaly Detection System - Docker Runner
# This script provides easy commands to run the system in Docker

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t claims-anomaly-detection .
    print_success "Docker image built successfully!"
}

# Function to run the demo
run_demo() {
    print_status "Running demo in Docker..."
    docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection python3 run_demo.py
}

# Function to run tests
run_tests() {
    print_status "Running tests in Docker..."
    docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection python3 run_tests.py
}

# Function to start the full stack
start_api() {
    print_status "Starting full stack with Docker Compose..."
    docker compose up -d
    print_success "Full stack started successfully!"
    print_status "Frontend: http://localhost:3000"
    print_status "API Server: http://localhost:8000"
    print_status "API Documentation: http://localhost:8000/docs"
    print_status "Health Check: http://localhost:8000/health"
}

# Function to stop the API server
stop_api() {
    print_status "Stopping API server..."
    docker compose down
    print_success "API server stopped!"
}

# Function to show logs
show_logs() {
    print_status "Showing API server logs..."
    docker compose logs -f claims-anomaly-api
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker compose down
    docker system prune -f
    print_success "Cleanup completed!"
}

# Function to show status
show_status() {
    print_status "Checking container status..."
    docker compose ps
}

# Function to test the full stack
test_api() {
    print_status "Testing full stack..."
    
    # Wait for servers to start
    sleep 10
    
    # Test API health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "API health check passed!"
        
        # Test API example endpoint
        if curl -f http://localhost:8000/api/v1/example > /dev/null 2>&1; then
            print_success "API example endpoint working!"
        else
            print_error "API example endpoint failed!"
            return 1
        fi
        
        # Test frontend
        if curl -f http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is accessible!"
        else
            print_error "Frontend is not accessible!"
            return 1
        fi
        
        print_success "Full stack testing completed!"
    else
        print_error "API health check failed!"
        return 1
    fi
}

# Function to show help
show_help() {
    echo "Claims Anomaly Detection System - Docker Runner"
    echo "=============================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     - Build the Docker image"
    echo "  demo      - Run the demo in Docker"
    echo "  test      - Run tests in Docker"
    echo "  start     - Start the API server with Docker Compose"
    echo "  stop      - Stop the API server"
    echo "  restart   - Restart the API server"
    echo "  logs      - Show API server logs"
    echo "  status    - Show container status"
    echo "  test-api  - Test API endpoints"
    echo "  cleanup   - Clean up Docker resources"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build      # Build the Docker image"
    echo "  $0 start      # Start the API server"
    echo "  $0 test-api   # Test the API endpoints"
    echo ""
}

# Main script logic
case "${1:-help}" in
    build)
        check_docker
        build_image
        ;;
    demo)
        check_docker
        run_demo
        ;;
    test)
        check_docker
        run_tests
        ;;
    start)
        check_docker
        start_api
        ;;
    stop)
        check_docker
        stop_api
        ;;
    restart)
        check_docker
        stop_api
        sleep 2
        start_api
        ;;
    logs)
        check_docker
        show_logs
        ;;
    status)
        check_docker
        show_status
        ;;
    test-api)
        check_docker
        test_api
        ;;
    cleanup)
        check_docker
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac 