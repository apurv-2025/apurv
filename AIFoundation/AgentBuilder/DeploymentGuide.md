# AI Agent Builder - Complete Deployment Guide

## 🚀 Quick Start Guide

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 13+**
- **Docker & Docker Compose** (recommended)
- **Git**

### Environment Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/ai-agent-builder.git
cd ai-agent-builder
```

2. **Set up environment variables:**

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ai_agents_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=another-secret-for-jwt-tokens

# LLM Configuration
LLM_PROVIDER=openai  # Options: openai, ollama, huggingface
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Alternative LLM Providers
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
HUGGINGFACE_TOKEN=your-hf-token

# Vector Database
VECTOR_PROVIDER=pinecone  # Options: pinecone, faiss
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp

# Security & Compliance
ENABLE_AUDIT_LOGGING=true
ENABLE_PII_DETECTION=true
DATA_RETENTION_DAYS=2190  # 6 years for HIPAA compliance

# Application Settings
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
ENVIRONMENT=development  # development, staging, production

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

### Development Setup

#### Option 1: Docker Compose (Recommended)

1. **Start all services:**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Backend API server
- Frontend React application
- Redis (for caching)
- Monitoring tools (optional)

#### Option 2: Manual Setup

1. **Set up the database:**
```bash
# Start PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=your_password -p 5432:5432 -d postgres:15

# Or use your local PostgreSQL installation
```

2. **Set up the backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Set up the frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### Testing the Installation

1. **Backend API:**
   - Visit http://localhost:8000/docs for API documentation
   - Test health endpoint: http://localhost:8000/health

2. **Frontend Application:**
   - Visit http://localhost:3000
   - Register a new account
   - Create your first AI agent

## 🏭 Production Deployment

### Docker Production Setup

1. **Create production environment file:**

```env
# .env.production
DATABASE_URL=postgresql://username:password@db-host:5432/ai_agents_db
SECRET_KEY=production-secret-key-very-long-and-random
ENVIRONMENT=production
FRONTEND_URL=https://your-domain.com
BACKEND_URL=https://api.your-domain.com
```

2. **Build and deploy:**

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### AWS Deployment

#### Using AWS ECS with Fargate

1. **Create ECR repositories:**
```bash
aws ecr create-repository --repository-name ai-agent-builder-backend
aws ecr create-repository --repository-name ai-agent-builder-frontend
```

2. **Build and push images:**
```bash
# Backend
docker build -t ai-agent-builder-backend ./backend
docker tag ai-agent-builder-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-agent-builder-backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-agent-builder-backend:latest

# Frontend
docker build -t ai-agent-builder-frontend ./frontend
docker tag ai-agent-builder-frontend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-agent-builder-frontend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-agent-builder-frontend:latest
```

3. **Create ECS task definition:**

```json
{
  "family": "ai-agent-builder",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-agent-builder-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://username:password@rds-endpoint:5432/ai_agents_db"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-agent-builder",
          "awslogs-region": "$AWS_REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Using AWS Lambda (Serverless)

For the backend API, you can deploy using AWS Lambda with the Serverless Framework:

```yaml
# serverless.yml
service: ai-agent-builder-api

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    DATABASE_URL: ${env:DATABASE_URL}
    SECRET_KEY: ${env:SECRET_KEY}

functions:
  api:
    handler: main.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true

plugins:
  - serverless-python-requirements
  - serverless-wsgi

custom:
  wsgi:
    app: main.app
  pythonRequirements:
    dockerizePip: true
```

### Google Cloud Platform (GCP) Deployment

#### Using Cloud Run

1. **Build and push to Container Registry:**
```bash
# Backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/ai-agent-builder-backend ./backend

# Frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/ai-agent-builder-frontend ./frontend
```

2. **Deploy to Cloud Run:**
```bash
# Backend
gcloud run deploy ai-agent-builder-backend \
  --image gcr.io/$PROJECT_ID/ai-agent-builder-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Frontend
gcloud run deploy ai-agent-builder-frontend \
  --image gcr.io/$PROJECT_ID/ai-agent-builder-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Kubernetes Deployment

1. **Create namespace:**
```bash
kubectl create namespace ai-agent-builder
```

2. **Deploy PostgreSQL:**
```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: ai-agent-builder
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: ai_agents_db
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

3. **Deploy backend:**
```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-builder-backend
  namespace: ai-agent-builder
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/ai-agent-builder-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: secret-key
```

## 🔒 Security Configuration

### SSL/TLS Setup

1. **Using Let's Encrypt with Nginx:**

```nginx
# nginx.conf
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Database Security

1. **Enable SSL for PostgreSQL:**
```sql
-- In postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'
```

2. **Create read-only database user:**
```sql
CREATE USER readonly_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE ai_agents_db TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
```

### Environment-Specific Configuration

#### Development
```env
DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_CORS=true
RATE_LIMITING=false
```

#### Staging
```env
DEBUG=false
LOG_LEVEL=INFO
ENABLE_CORS=true
RATE_LIMITING=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

#### Production
```env
DEBUG=false
LOG_LEVEL=WARNING
ENABLE_CORS=false
RATE_LIMITING=true
RATE_LIMIT_REQUESTS=50
RATE_LIMIT_WINDOW=60
SECURE_COOKIES=true
SESSION_TIMEOUT=3600
```

## 📊 Monitoring & Observability

### Application Monitoring

1. **Install monitoring stack:**
```bash
# Using Docker Compose
docker-compose -f docker-compose.monitoring.yml up -d
```

2. **Configure Prometheus scraping:**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-agent-builder-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'ai-agent-builder-frontend'
    static_configs:
      - targets: ['frontend:3000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
```

3. **Set up Grafana dashboards:**
   - Import pre-built dashboards for FastAPI and PostgreSQL
   - Create custom dashboards for agent performance metrics
   - Set up alerting rules for critical metrics

### Log Management

1. **Centralized logging with ELK Stack:**
```yaml
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "ai-agent-builder" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{WORD:logger} - %{WORD:level} - %{GREEDYDATA:message}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "ai-agent-builder-%{+YYYY.MM.dd}"
  }
}
```

### Health Checks

1. **Kubernetes health checks:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/detailed
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

2. **Docker health checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## 🔄 Backup & Recovery

### Database Backups

1. **Automated PostgreSQL backups:**
```bash
#!/bin/bash
# backup.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="ai_agents_backup_$TIMESTAMP.sql"

pg_dump -h $DB_HOST -U $DB_USER -d ai_agents_db > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://your-backup-bucket/database/

# Keep only last 30 days of backups
find . -name "ai_agents_backup_*.sql" -mtime +30 -delete
```

2. **Set up backup cron job:**
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### Disaster Recovery

1. **Database restoration:**
```bash
# Restore from backup
psql -h $DB_HOST -U $DB_USER -d ai_agents_db < backup_file.sql

# Or restore from S3
aws s3 cp s3://your-backup-bucket/database/latest.sql - | psql -h $DB_HOST -U $DB_USER -d ai_agents_db
```

2. **Application state recovery:**
```bash
# Restore uploaded documents
aws s3 sync s3://your-backup-bucket/documents/ ./uploads/

# Restore vector database
# This depends on your vector provider (Pinecone vs FAISS)
```

## 📋 Maintenance Tasks

### Regular Maintenance

1. **Database maintenance:**
```sql
-- Run weekly
VACUUM ANALYZE;

-- Clean old audit logs (older than 6 years for HIPAA)
DELETE FROM audit_logs WHERE timestamp < NOW() - INTERVAL '6 years';

-- Update statistics
ANALYZE;
```

2. **Log rotation:**
```bash
# Add to logrotate.d
/var/log/ai-agent-builder/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 app app
    postrotate
        systemctl reload ai-agent-builder
    endscript
}
```

### Security Updates

1. **Update dependencies:**
```bash
# Backend
pip list --outdated
pip install -U package_name

# Frontend
npm audit
npm update
```

2. **Security scanning:**
```bash
# Python security scan
bandit -r backend/

# Node.js security scan
npm audit

# Container security scan
trivy image your-image:latest
```

## 🚨 Troubleshooting

### Common Issues

1. **Database connection errors:**
```bash
# Check PostgreSQL status
systemctl status postgresql

# Check connection
psql -h localhost -U postgres -d ai_agents_db

# View logs
tail -f /var/log/postgresql/postgresql.log
```

2. **LLM API errors:**
```bash
# Test OpenAI connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5}' \
     https://api.openai.com/v1/chat/completions
```

3. **Frontend build issues:**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Check build
npm run build
```

### Performance Issues

1. **Database performance:**
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename = 'agents';
```

2. **Memory usage:**
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head

# Check PostgreSQL memory
SELECT pg_size_pretty(pg_total_relation_size('agents')) as size;
```

This comprehensive deployment guide covers everything from development setup to production deployment, security configuration, monitoring, and maintenance. The application is designed to be HIPAA-compliant and production-ready for medical practices of all sizes.
