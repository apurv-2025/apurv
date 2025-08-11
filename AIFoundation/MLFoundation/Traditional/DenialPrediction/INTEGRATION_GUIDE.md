# DenialPrediction + Claims Service Integration Guide

## 🎯 Overview

This guide explains how to use the integrated system that combines **DenialPrediction** (ML denial prediction) with **Claims Service** (FHIR-compliant CRUD operations).

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DenialPrediction                         │
│  (High-level ML Application with Prediction Capabilities)   │
├─────────────────────────────────────────────────────────────┤
│  • ML Prediction Models                                     │
│  • Real-time Scoring Engine                                 │
│  • Batch Processing Capabilities                            │
│  • Risk Assessment & Analytics                              │
│  • Enhanced Inference Engine                                │
│  • AI-powered Insights                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │ API Calls (httpx)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      Claims Service                         │
│  (Foundational FHIR-based CRUD Service)                    │
├─────────────────────────────────────────────────────────────┤
│  • FHIR Claim Resources (Extended)                         │
│  • Basic CRUD Operations                                    │
│  • Database Schema (Enhanced)                              │
│  • Data Validation                                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Docker and Docker Compose** installed
2. **Git** for cloning repositories
3. **curl** for testing API endpoints

### 1. Start the Integrated System

```bash
# Navigate to DenialPrediction directory
cd AIFoundation/MLFoundation/Traditional/DenialPrediction

# Make the startup script executable
chmod +x run_integrated.sh

# Start the integrated system
./run_integrated.sh
```

### 2. Verify System Health

The startup script will automatically check the health of all services. You can also manually verify:

```bash
# Check Claims Service
curl http://localhost:8002/health

# Check DenialPrediction API
curl http://localhost:8003/health

# Check Integration Health
curl http://localhost:8003/health/integration
```

## 📊 System Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Claims Service API | http://localhost:8002 | FHIR-compliant claims management |
| Claims Service Docs | http://localhost:8002/docs | Interactive API documentation |
| Claims Service Frontend | http://localhost:3002 | React-based UI |
| DenialPrediction API | http://localhost:8003 | ML prediction endpoints |
| DenialPrediction Docs | http://localhost:8003/docs | Interactive API documentation |
| DenialPrediction Frontend | http://localhost:3003 | Streamlit dashboard |
| MLflow UI | http://localhost:5000 | Model tracking and management |
| PostgreSQL Database | localhost:5435 | Enhanced database with ML fields |

## 🔧 API Usage Examples

### 1. Basic DenialPrediction Operations

#### Single Claim Prediction
```bash
curl -X POST http://localhost:8003/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "claim_id": "CLM_001",
    "provider_id": "PROV_001",
    "payer_id": "PAYER_001",
    "patient_id": "PAT_001",
    "cpt_codes": ["99213", "80048"],
    "icd_codes": ["E11.9", "Z79.4"],
    "claim_amount": 250.00,
    "service_date": "2024-01-15",
    "patient_age": 45,
    "patient_gender": "M",
    "place_of_service": "11"
  }'
```

#### Batch Prediction
```bash
curl -X POST http://localhost:8003/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "claims": [
      {
        "claim_id": "CLM_001",
        "provider_id": "PROV_001",
        "payer_id": "PAYER_001",
        "patient_id": "PAT_001",
        "cpt_codes": ["99213"],
        "icd_codes": ["E11.9"],
        "claim_amount": 150.00,
        "service_date": "2024-01-15",
        "patient_age": 45,
        "patient_gender": "M",
        "place_of_service": "11"
      }
    ]
  }'
```

### 2. Claims Service Integration

#### Get Claims from Claims Service
```bash
curl "http://localhost:8003/api/v1/claims/from-service?limit=10&status=active"
```

#### Predict Denials for Claims from Service
```bash
curl -X POST "http://localhost:8003/api/v1/predict/from-claims-service?limit=50&status=active"
```

#### Get Integration Statistics
```bash
curl http://localhost:8003/api/v1/stats/integration
```

### 3. Claims Service Operations

#### Create a Claim
```bash
curl -X POST http://localhost:8002/api/v1/claims \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "Claim",
    "status": "active",
    "use": "claim",
    "patient_id": "PAT_001",
    "insurer_id": "PAYER_001",
    "provider_id": "PROV_001",
    "created": "2024-01-15T10:00:00Z",
    "total": {
      "currency": "USD",
      "value": 250.00
    },
    "item": [
      {
        "sequence": 1,
        "productOrService": {
          "coding": [
            {
              "system": "http://www.ama-assn.org/go/cpt",
              "code": "99213"
            }
          ]
        }
      }
    ],
    "diagnosis": [
      {
        "sequence": 1,
        "diagnosisCodeableConcept": {
          "coding": [
            {
              "system": "http://hl7.org/fhir/sid/icd-10",
              "code": "E11.9"
            }
          ]
        }
      }
    ],
    "insurance": [
      {
        "coverage": {
          "reference": "Coverage/PAYER_001"
        }
      }
    ]
  }'
```

#### Get Claims with Predictions
```bash
curl "http://localhost:8002/api/v1/stats/claims/predictions?limit=10&risk_level=HIGH"
```

#### Get Claims Statistics
```bash
curl http://localhost:8002/api/v1/stats/claims
```

## 🔄 Data Flow Examples

### 1. End-to-End Prediction Workflow

```python
import httpx
import asyncio

async def complete_prediction_workflow():
    """Complete workflow: Create claim → Predict denial → Update with results"""
    
    # 1. Create claim in Claims Service
    async with httpx.AsyncClient() as client:
        claim_data = {
            "resource_type": "Claim",
            "status": "active",
            "use": "claim",
            "patient_id": "PAT_001",
            "insurer_id": "PAYER_001",
            "provider_id": "PROV_001",
            "created": "2024-01-15T10:00:00Z",
            "total": {"currency": "USD", "value": 500.00},
            "item": [{
                "sequence": 1,
                "productOrService": {
                    "coding": [{"system": "http://www.ama-assn.org/go/cpt", "code": "99213"}]
                }
            }],
            "diagnosis": [{
                "sequence": 1,
                "diagnosisCodeableConcept": {
                    "coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": "E11.9"}]
                }
            }],
            "insurance": [{"coverage": {"reference": "Coverage/PAYER_001"}}]
        }
        
        response = await client.post("http://localhost:8002/api/v1/claims", json=claim_data)
        claim = response.json()
        claim_id = claim["id"]
        
        # 2. Get claim in DenialPrediction format
        response = await client.get(f"http://localhost:8003/api/v1/claims/from-service?claim_id={claim_id}")
        prediction_claim = response.json()["data"]["claims"][0]
        
        # 3. Make prediction
        prediction_data = {
            "claim_id": prediction_claim["claim_id"],
            "provider_id": prediction_claim["provider_id"],
            "payer_id": prediction_claim["payer_id"],
            "patient_id": prediction_claim["patient_id"],
            "cpt_codes": prediction_claim["cpt_codes"],
            "icd_codes": prediction_claim["icd_codes"],
            "claim_amount": prediction_claim["claim_amount"],
            "service_date": prediction_claim["service_date"],
            "patient_age": prediction_claim["patient_age"],
            "patient_gender": prediction_claim["patient_gender"],
            "place_of_service": prediction_claim["place_of_service"]
        }
        
        response = await client.post("http://localhost:8003/api/v1/predict", json=prediction_data)
        prediction_result = response.json()
        
        # 4. Update claim with prediction results
        update_data = {
            "denial_probability": prediction_result["denial_probability"],
            "risk_level": prediction_result["risk_level"],
            "model_version": prediction_result["model_version"],
            "top_risk_factors": prediction_result["top_risk_factors"],
            "recommended_actions": prediction_result["recommended_actions"]
        }
        
        await client.put(f"http://localhost:8002/api/v1/claims/{claim_id}", json=update_data)
        
        print(f"✅ Completed prediction workflow for claim {claim_id}")
        print(f"   Denial Probability: {prediction_result['denial_probability']:.2%}")
        print(f"   Risk Level: {prediction_result['risk_level']}")

# Run the workflow
asyncio.run(complete_prediction_workflow())
```

### 2. Batch Processing Workflow

```python
import httpx
import asyncio

async def batch_prediction_workflow():
    """Process multiple claims in batch"""
    
    async with httpx.AsyncClient() as client:
        # 1. Get claims from Claims Service
        response = await client.get("http://localhost:8003/api/v1/claims/from-service?limit=100&status=active")
        claims = response.json()["data"]["claims"]
        
        # 2. Process predictions in batch
        response = await client.post("http://localhost:8003/api/v1/predict/from-claims-service?limit=100&status=active")
        result = response.json()
        
        print(f"✅ Processed {result['data']['processed_count']} claims")
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message']}")

# Run the batch workflow
asyncio.run(batch_prediction_workflow())
```

## 📈 Monitoring and Analytics

### 1. Integration Health Monitoring

```bash
# Check overall integration health
curl http://localhost:8003/health/integration

# Response example:
{
  "denial_prediction_status": "healthy",
  "claims_service_status": "healthy", 
  "integration_status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

### 2. Performance Metrics

```bash
# Get DenialPrediction statistics
curl http://localhost:8003/api/v1/stats/integration

# Get Claims Service statistics
curl http://localhost:8002/api/v1/stats/claims
curl http://localhost:8002/api/v1/stats/predictions
curl http://localhost:8002/api/v1/stats/denials
```

### 3. Model Performance Tracking

Access MLflow UI at http://localhost:5000 to:
- Track model versions and performance
- Compare model metrics
- Monitor model drift
- Manage model lifecycle

## 🔧 Configuration

### Environment Variables

#### DenialPrediction API
```bash
CLAIMS_SERVICE_URL=http://localhost:8002  # Claims Service URL
LOG_LEVEL=INFO                           # Logging level
PYTHONPATH=/app                          # Python path
```

#### Claims Service
```bash
DATABASE_URL=postgresql://fhir_user:fhir_password_2024!@claims-db:5432/fhir_claims_db
CORS_ORIGINS=http://localhost:3002,http://localhost:3003
LOG_LEVEL=info
ENVIRONMENT=development
```

### Database Schema

The enhanced database includes:

1. **Extended Claims Table** with ML prediction fields
2. **Predictions Table** for storing prediction results
3. **Denial Records Table** for denial management
4. **Remediation Actions Table** for workflow automation
5. **Model Versions Table** for model tracking
6. **Feature Store Table** for caching computed features
7. **Audit Log Table** for compliance

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using the ports
lsof -i :8002 -i :8003 -i :3002 -i :3003

# Stop conflicting services
sudo lsof -ti:8002 | xargs kill -9
```

#### 2. Database Connection Issues
```bash
# Check database health
docker exec claims-integrated-db pg_isready -U fhir_user -d fhir_claims_db

# View database logs
docker logs claims-integrated-db
```

#### 3. Service Startup Issues
```bash
# Check service logs
docker-compose -f docker-compose.integrated.yml logs claims-service
docker-compose -f docker-compose.integrated.yml logs denial-prediction-api

# Restart specific service
docker-compose -f docker-compose.integrated.yml restart claims-service
```

#### 4. Integration Issues
```bash
# Test Claims Service connectivity
curl -v http://localhost:8002/health

# Test DenialPrediction connectivity
curl -v http://localhost:8003/health

# Check integration health
curl -v http://localhost:8003/health/integration
```

### Debug Mode

To run in debug mode with detailed logging:

```bash
# Set debug logging
export LOG_LEVEL=DEBUG

# Restart services
docker-compose -f docker-compose.integrated.yml down
docker-compose -f docker-compose.integrated.yml up --build
```

## 🔒 Security Considerations

### 1. Authentication
- Implement JWT tokens for API access
- Use API keys for service-to-service communication
- Enable HTTPS in production

### 2. Data Protection
- Encrypt sensitive data at rest
- Use secure database connections
- Implement audit logging for compliance

### 3. Network Security
- Use internal Docker networks
- Restrict external access to necessary ports
- Implement rate limiting

## 📚 Additional Resources

### Documentation
- [Claims Service API Docs](http://localhost:8002/docs)
- [DenialPrediction API Docs](http://localhost:8003/docs)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)

### Code Examples
- [Integration Examples](./examples/)
- [API Client Libraries](./api/clients/)
- [Testing Scripts](./tests/)

### Support
- Check logs: `docker-compose -f docker-compose.integrated.yml logs`
- Health checks: Use the health endpoints
- Database queries: Connect to PostgreSQL on port 5435

## 🎯 Next Steps

1. **Customize Models**: Train custom ML models for your specific use case
2. **Add Workflows**: Implement automated denial resolution workflows
3. **Scale Up**: Deploy to production with proper monitoring
4. **Extend Integration**: Add more healthcare services to the ecosystem

This integrated system provides a powerful foundation for healthcare claim management with AI-powered insights and predictions. 