# Agentic Core - Deployment Guide

## 🚀 **Quick Start Deployment**

### **Option 1: Docker Compose (Recommended)**

```bash
# Clone the repository
git clone https://github.com/agentic/core.git
cd agentic-core

# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env

# Start the services
docker-compose up -d

# Check status
docker-compose ps
```

### **Option 2: Standalone Installation**

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend && npm install

# Set up database
psql -U postgres -d agentic_core -f database/schema.sql

# Start backend
cd backend && uvicorn main:app --reload --port 8000

# Start frontend (in another terminal)
cd frontend && npm start
```

## 📋 **Environment Configuration**

### **Required Environment Variables**

```bash
# AI Model Configuration
AI_MODEL_PROVIDER=openai|anthropic|custom
AI_MODEL_NAME=gpt-4|claude-3-sonnet|custom
AI_API_KEY=your_api_key_here

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/agentic_core
REDIS_URL=redis://localhost:6379

# Application Configuration
APP_NAME=Agentic Core
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### **Optional Environment Variables**

```bash
# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_PASSWORD=admin

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_PATH=/app/uploads

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External Services
SENTRY_DSN=your-sentry-dsn
```

## 🐳 **Docker Deployment**

### **Production Docker Compose**

```bash
# Start production services
docker-compose --profile prod up -d

# Start with monitoring
docker-compose --profile prod --profile monitoring up -d

# Scale services
docker-compose --profile prod up -d --scale agentic-backend=3
```

### **Custom Docker Build**

```bash
# Build custom image
docker build -t my-agentic:latest .

# Run with custom configuration
docker run -d \
  --name agentic-app \
  -p 8000:8000 \
  -e AI_API_KEY=your-key \
  -e DATABASE_URL=postgresql://... \
  my-agentic:latest
```

### **Kubernetes Deployment**

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-core
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-core
  template:
    metadata:
      labels:
        app: agentic-core
    spec:
      containers:
      - name: agentic
        image: agentic/core:latest
        ports:
        - containerPort: 8000
        env:
        - name: AI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agentic-secrets
              key: ai-api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: agentic-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## ☁️ **Cloud Deployment**

### **AWS Deployment**

#### **ECS Fargate**

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name agentic-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster agentic-cluster \
  --service-name agentic-service \
  --task-definition agentic-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

#### **AWS Lambda (Serverless)**

```python
# lambda_function.py
import json
from agentic_core import AgenticCore

def lambda_handler(event, context):
    agentic = AgenticCore(
        model_provider="openai",
        api_key=os.environ["AI_API_KEY"]
    )
    
    try:
        response = await agentic.chat(
            message=event["message"],
            user_id=event["user_id"]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.dict())
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### **Google Cloud Platform**

#### **Cloud Run**

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/agentic-core

# Deploy to Cloud Run
gcloud run deploy agentic-core \
  --image gcr.io/PROJECT_ID/agentic-core \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars AI_API_KEY=your-key
```

### **Azure**

#### **Azure Container Instances**

```bash
# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name agentic-container \
  --image agentic/core:latest \
  --dns-name-label agentic-app \
  --ports 8000 \
  --environment-variables AI_API_KEY=your-key
```

## 🔧 **Configuration Management**

### **Configuration Files**

#### **Backend Configuration**

```yaml
# config/config.yaml
app:
  name: "Agentic Core"
  version: "1.0.0"
  debug: false

database:
  url: "postgresql://user:pass@localhost/agentic_core"
  pool_size: 10
  max_overflow: 20

ai:
  provider: "openai"
  model: "gpt-4"
  max_tokens: 4000
  temperature: 0.7

security:
  secret_key: "your-secret-key"
  jwt_secret: "your-jwt-secret"
  cors_origins: ["http://localhost:3000"]

monitoring:
  prometheus_enabled: true
  log_level: "INFO"
```

#### **Frontend Configuration**

```javascript
// config/config.js
export const config = {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  model: process.env.REACT_APP_MODEL || 'gpt-4',
  theme: process.env.REACT_APP_THEME || 'light',
  enableHistory: process.env.REACT_APP_ENABLE_HISTORY === 'true',
  enableMetrics: process.env.REACT_APP_ENABLE_METRICS === 'true',
};
```

### **Environment-Specific Configurations**

#### **Development**

```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://localhost/agentic_dev
REDIS_URL=redis://localhost:6379
```

#### **Staging**

```bash
# .env.staging
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://staging-db/agentic_staging
REDIS_URL=redis://staging-redis:6379
```

#### **Production**

```bash
# .env.production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod-db/agentic_prod
REDIS_URL=redis://prod-redis:6379
```

## 📊 **Monitoring & Observability**

### **Health Checks**

```bash
# Check application health
curl http://localhost:8000/health

# Check database connectivity
curl http://localhost:8000/health/database

# Check AI model connectivity
curl http://localhost:8000/health/ai-model
```

### **Metrics Collection**

#### **Prometheus Configuration**

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agentic-core'
    static_configs:
      - targets: ['agentic-backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

#### **Grafana Dashboards**

```json
// monitoring/grafana/dashboards/agentic-dashboard.json
{
  "dashboard": {
    "title": "Agentic Core Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agentic_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(agentic_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### **Logging Configuration**

```python
# logging_config.py
import logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## 🔒 **Security Configuration**

### **Authentication & Authorization**

```python
# auth_config.py
from agentic_core.auth import JWTAuth

auth_config = {
    "secret_key": os.getenv("JWT_SECRET"),
    "algorithm": "HS256",
    "access_token_expire_minutes": 30,
    "refresh_token_expire_days": 7,
}

auth = JWTAuth(**auth_config)
```

### **Rate Limiting**

```python
# rate_limiting.py
from agentic_core.security import RateLimiter

rate_limiter = RateLimiter(
    max_requests=int(os.getenv("RATE_LIMIT_REQUESTS", 100)),
    window_seconds=int(os.getenv("RATE_LIMIT_WINDOW", 3600))
)
```

### **CORS Configuration**

```python
# cors_config.py
from fastapi.middleware.cors import CORSMiddleware

cors_config = {
    "allow_origins": os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["*"],
}

app.add_middleware(CORSMiddleware, **cors_config)
```

## 🚀 **Scaling Strategies**

### **Horizontal Scaling**

```bash
# Scale backend services
docker-compose up -d --scale agentic-backend=5

# Load balancer configuration
docker-compose up -d nginx
```

### **Database Scaling**

```bash
# Read replicas
docker-compose up -d postgres-replica

# Connection pooling
docker-compose up -d pgbouncer
```

### **Caching Strategy**

```bash
# Redis cluster
docker-compose up -d redis-cluster

# CDN configuration
# Configure CloudFront, CloudFlare, or similar
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions**

```yaml
# .github/workflows/deploy.yml
name: Deploy Agentic Core

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r backend/requirements.txt
          pytest backend/tests/
          npm install --prefix frontend
          npm test --prefix frontend

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
        run: |
          docker build -t agentic/core:${{ github.sha }} .
          docker push agentic/core:${{ github.sha }}
      - name: Deploy to production
        run: |
          # Deploy to your cloud provider
```

### **GitLab CI**

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pip install -r backend/requirements.txt
    - pytest backend/tests/
    - npm install --prefix frontend
    - npm test --prefix frontend

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/agentic-core agentic=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## 📝 **Troubleshooting**

### **Common Issues**

#### **Database Connection Issues**

```bash
# Check database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# Check connection pool
curl http://localhost:8000/health/database
```

#### **AI Model Issues**

```bash
# Test AI model connectivity
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "test"}'
```

#### **Memory Issues**

```bash
# Check memory usage
docker stats

# Increase memory limits
docker-compose up -d --scale agentic-backend=2
```

### **Log Analysis**

```bash
# View application logs
docker-compose logs -f agentic-backend

# View specific service logs
docker-compose logs -f postgres

# Search logs for errors
docker-compose logs agentic-backend | grep ERROR
```

## 📚 **Additional Resources**

- [API Documentation](./docs/api.md)
- [Component Library](./docs/components.md)
- [Tool Development](./docs/tools.md)
- [Performance Tuning](./docs/performance.md)
- [Security Best Practices](./docs/security.md) 