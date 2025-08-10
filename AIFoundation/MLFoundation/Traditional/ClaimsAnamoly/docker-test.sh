#!/bin/bash

# Docker Test Script for Claims Anomaly Detection System
# This script tests the complete Docker setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    print_status "Running: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        print_success "$test_name"
        ((TESTS_PASSED++))
    else
        print_error "$test_name"
        ((TESTS_FAILED++))
    fi
}

# Function to check if Docker is available
check_docker() {
    print_status "Checking Docker availability..."
    if command -v docker > /dev/null 2>&1; then
        print_success "Docker is installed"
        if docker info > /dev/null 2>&1; then
            print_success "Docker is running"
            return 0
        else
            print_error "Docker is not running"
            return 1
        fi
    else
        print_error "Docker is not installed"
        return 1
    fi
}

# Function to check if Docker Compose is available
check_docker_compose() {
    print_status "Checking Docker Compose availability..."
    if command -v docker-compose > /dev/null 2>&1; then
        print_success "Docker Compose is installed"
        return 0
    else
        print_error "Docker Compose is not installed"
        return 1
    fi
}

# Function to build and test Docker image
test_docker_build() {
    print_status "Testing Docker build..."
    
    # Build the image
    if docker build -t claims-anomaly-detection . > /dev/null 2>&1; then
        print_success "Docker image built successfully"
        
        # Test if the image exists
        if docker images | grep -q claims-anomaly-detection; then
            print_success "Docker image exists"
            return 0
        else
            print_error "Docker image not found after build"
            return 1
        fi
    else
        print_error "Docker build failed"
        return 1
    fi
}

# Function to test demo in Docker
test_docker_demo() {
    print_status "Testing demo in Docker..."
    
    # Run demo in Docker (timeout after 60 seconds)
    if timeout 60 docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection python3 run_demo.py > /dev/null 2>&1; then
        print_success "Demo ran successfully in Docker"
        return 0
    else
        print_error "Demo failed in Docker"
        return 1
    fi
}

# Function to test API in Docker
test_docker_api() {
    print_status "Testing API in Docker..."
    
    # Start the API server
    docker-compose up -d > /dev/null 2>&1
    
    # Wait for server to start
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "API health check passed"
        
        # Test example endpoint
        if curl -f http://localhost:8000/api/v1/example > /dev/null 2>&1; then
            print_success "API example endpoint working"
            
            # Stop the server
            docker-compose down > /dev/null 2>&1
            return 0
        else
            print_error "API example endpoint failed"
            docker-compose down > /dev/null 2>&1
            return 1
        fi
    else
        print_error "API health check failed"
        docker-compose down > /dev/null 2>&1
        return 1
    fi
}

# Function to test volume mounting
test_volume_mounting() {
    print_status "Testing volume mounting..."
    
    # Create a test file
    echo "test" > models/test_file.txt
    
    # Run container and check if file is accessible
    if docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection ls /app/models/test_file.txt > /dev/null 2>&1; then
        print_success "Volume mounting works correctly"
        rm -f models/test_file.txt
        return 0
    else
        print_error "Volume mounting failed"
        rm -f models/test_file.txt
        return 1
    fi
}

# Main test execution
main() {
    echo "🐳 Docker Test Suite for Claims Anomaly Detection System"
    echo "========================================================"
    echo ""
    
    # Check prerequisites
    if ! check_docker; then
        print_error "Docker tests cannot proceed"
        exit 1
    fi
    
    if ! check_docker_compose; then
        print_error "Docker Compose tests cannot proceed"
        exit 1
    fi
    
    echo ""
    print_status "Starting Docker tests..."
    echo ""
    
    # Run tests
    run_test "Docker Build" "test_docker_build"
    run_test "Volume Mounting" "test_volume_mounting"
    run_test "Docker Demo" "test_docker_demo"
    run_test "Docker API" "test_docker_api"
    
    echo ""
    echo "========================================================"
    print_status "Test Results Summary:"
    echo "  Tests Passed: $TESTS_PASSED"
    echo "  Tests Failed: $TESTS_FAILED"
    echo "  Total Tests:  $((TESTS_PASSED + TESTS_FAILED))"
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_success "All Docker tests passed! 🎉"
        echo ""
        print_status "You can now use the following commands:"
        echo "  ./docker-run.sh build     # Build the Docker image"
        echo "  ./docker-run.sh start     # Start the API server"
        echo "  ./docker-run.sh demo      # Run the demo"
        echo "  ./docker-run.sh test-api  # Test the API"
        exit 0
    else
        print_error "Some Docker tests failed! ❌"
        exit 1
    fi
}

# Run main function
main "$@" 