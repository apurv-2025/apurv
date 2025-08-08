# scripts/deploy_production.sh
#!/bin/bash

# Production deployment script for FastAPI Task Management System

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Configuration
PROJECT_NAME="task-manager-fastapi"
BACKUP_DIR="/opt/backups"
LOG_FILE="/var/log/deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a $LOG_FILE
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a $LOG_FILE
    exit 1
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root for security reasons"
fi

# Verify required commands exist
command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
command -v docker-compose >/dev/null 2>&1 || error "Docker Compose is required but not installed"

log "Starting deployment of $PROJECT_NAME..."

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup current deployment if it exists
if [ -d "/opt/$PROJECT_NAME" ]; then
    log "Creating backup of current deployment..."
    tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz" -C /opt $PROJECT_NAME
    log "Backup created successfully"
fi

# Pull latest code
log "Pulling latest code..."
cd /opt/$PROJECT_NAME || error "Project directory not found"
git pull origin main || error "Failed to pull latest code"

# Check if .env file exists
if [ ! -f ".env" ]; then
    warn ".env file not found. Please create it from .env.example"
    cp .env.example .env
    warn "Please edit .env file with production values before continuing"
    read -p "Press enter when .env is configured..."
fi

# Backup database
log "Backing up database..."
docker-compose exec -T postgres pg_dump -U taskuser taskmanager > "$BACKUP_DIR/db-backup-$(date +%Y%m%d-%H%M%S).sql" || warn "Database backup failed"

# Build new images
log "Building Docker images..."
docker-compose build --no-cache || error "Failed to build Docker images"

# Run database migrations
log "Running database migrations..."
docker-compose run --rm backend alembic upgrade head || error "Database migration failed"

# Start services
log "Starting services..."
docker-compose up -d || error "Failed to start services"

# Wait for services to be ready
log "Waiting for services to start..."
sleep 30

# Health check
log "Performing health check..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        log "Health check passed!"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Health check failed after 30 attempts"
    fi
    sleep 2
done

# Clean up old Docker images
log "Cleaning up old Docker images..."
docker image prune -f

log "✅ Deployment completed successfully!"
log "🌐 Application is available at: http://localhost:8000"
log "📚 API Documentation: http://localhost:8000/docs"
