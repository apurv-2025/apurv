# 🐳 Docker Support for Claims Anomaly Detection System

This document provides comprehensive instructions for running the Claims Anomaly Detection System using Docker.

## 📋 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **curl**: For API testing (usually pre-installed)

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
# Build the image
./docker-run.sh build

# Or manually
docker build -t claims-anomaly-detection .
```

### 2. Start the API Server

```bash
# Start the API server
./docker-run.sh start

# Or manually
docker-compose up -d
```

### 3. Test the API

```bash
# Test API endpoints
./docker-run.sh test-api

# Or manually
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/example
```

### 4. Access the API

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 Available Commands

### Docker Runner Script

The `docker-run.sh` script provides easy commands:

```bash
./docker-run.sh build      # Build Docker image
./docker-run.sh demo       # Run demo in Docker
./docker-run.sh test       # Run tests in Docker
./docker-run.sh start      # Start API server
./docker-run.sh stop       # Stop API server
./docker-run.sh restart    # Restart API server
./docker-run.sh logs       # Show server logs
./docker-run.sh status     # Show container status
./docker-run.sh test-api   # Test API endpoints
./docker-run.sh cleanup    # Clean up Docker resources
./docker-run.sh help       # Show help
```

### Manual Docker Commands

```bash
# Build image
docker build -t claims-anomaly-detection .

# Run demo
docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection python3 run_demo.py

# Run tests
docker run --rm -v "$(pwd)/models:/app/models" claims-anomaly-detection python3 run_tests.py

# Start API server
docker-compose up -d

# Stop API server
docker-compose down

# View logs
docker-compose logs -f claims-anomaly-api

# Check status
docker-compose ps
```

## 🔧 Configuration

### Environment Variables

You can customize the Docker setup by modifying `docker-compose.yml`:

```yaml
environment:
  - PYTHONPATH=/app
  - LOG_LEVEL=INFO
  - MODEL_PATH=/app/models/claims_anomaly_model.pkl
```

### Port Configuration

The API server runs on port 8000 by default. To change the port:

```yaml
ports:
  - "8080:8000"  # Map host port 8080 to container port 8000
```

### Volume Mounting

The following directories are mounted as volumes:

- `./models:/app/models` - Trained models
- `./data:/app/data` - Data files
- `./logs:/app/logs` - Log files

## 🧪 Testing

### Run Complete Docker Test Suite

```bash
./docker-test.sh
```

This will test:
- Docker build process
- Volume mounting
- Demo execution
- API functionality

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test example endpoint
curl http://localhost:8000/api/v1/example

# Test single claim scoring
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "claim_id": "TEST_001",
    "submission_date": "2025-08-01",
    "provider_id": "PROV_00001",
    "provider_specialty": "Internal Medicine",
    "patient_age": 45,
    "patient_gender": "M",
    "cpt_code": "99214",
    "icd_code": "I10",
    "units_of_service": 1,
    "billed_amount": 200.0,
    "paid_amount": 180.0,
    "place_of_service": "11",
    "prior_authorization": "N"
  }'
```

## 📊 Monitoring

### Health Checks

The container includes automatic health checks:

```bash
# Check container health
docker ps

# View health check logs
docker inspect claims-anomaly-detection
```

### Logs

```bash
# View real-time logs
./docker-run.sh logs

# Or manually
docker-compose logs -f claims-anomaly-api
```

### Resource Usage

```bash
# Check resource usage
docker stats claims-anomaly-detection
```

## 🔒 Security

### Non-Root User

The container runs as a non-root user (`app`) for security.

### Network Isolation

The container uses a dedicated Docker network for isolation.

### Volume Permissions

Ensure proper permissions for mounted volumes:

```bash
# Set proper permissions
chmod 755 models data logs
```

## 🚀 Production Deployment

### Using Docker Compose

```bash
# Start in production mode
docker-compose -f docker-compose.yml up -d

# With custom environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Using Docker Swarm

```bash
# Deploy to swarm
docker stack deploy -c docker-compose.yml claims-anomaly
```

### Using Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using the port
lsof -i :8000

# Use a different port
docker-compose up -d -p 8080:8000
```

#### Permission Denied

```bash
# Fix volume permissions
sudo chown -R $USER:$USER models data logs
```

#### Model Not Found

```bash
# Ensure model exists
ls -la models/

# Run demo to generate model
./docker-run.sh demo
```

#### Container Won't Start

```bash
# Check logs
docker-compose logs claims-anomaly-api

# Check container status
docker-compose ps
```

### Debug Mode

```bash
# Run in debug mode
docker-compose up

# Or with specific service
docker-compose up claims-anomaly-api
```

## 📈 Performance

### Resource Limits

You can set resource limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
    reservations:
      cpus: '1.0'
      memory: 1G
```

### Scaling

```bash
# Scale the service
docker-compose up -d --scale claims-anomaly-api=3
```

## 🔄 Updates

### Rebuilding the Image

```bash
# Rebuild with no cache
docker build --no-cache -t claims-anomaly-detection .

# Update and restart
./docker-run.sh build
./docker-run.sh restart
```

### Updating Dependencies

```bash
# Update requirements.txt
# Then rebuild
./docker-run.sh build
```

## 📝 Examples

### Complete Workflow

```bash
# 1. Build the image
./docker-run.sh build

# 2. Run the demo to generate model
./docker-run.sh demo

# 3. Start the API server
./docker-run.sh start

# 4. Test the API
./docker-run.sh test-api

# 5. Use the API
curl http://localhost:8000/docs
```

### Development Workflow

```bash
# 1. Start API server
./docker-run.sh start

# 2. View logs
./docker-run.sh logs

# 3. Test changes
./docker-run.sh test-api

# 4. Stop server
./docker-run.sh stop
```

## 🎯 Best Practices

1. **Always use volumes** for persistent data
2. **Set resource limits** in production
3. **Use health checks** for monitoring
4. **Run as non-root user** for security
5. **Keep images updated** regularly
6. **Monitor logs** for issues
7. **Use Docker Compose** for multi-service setups

## 📞 Support

If you encounter issues:

1. Check the logs: `./docker-run.sh logs`
2. Run the test suite: `./docker-test.sh`
3. Check container status: `./docker-run.sh status`
4. Review this documentation
5. Check the main README.md for general troubleshooting

---

**Happy Dockerizing! 🐳** 