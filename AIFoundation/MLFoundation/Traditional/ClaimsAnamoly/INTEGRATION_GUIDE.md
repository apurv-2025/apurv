# ClaimsAnamoly + Claims Service Integration Guide

## 🎯 Overview

This guide explains how to use the integrated system that combines **ClaimsAnamoly** (ML anomaly detection) with **Claims Service** (FHIR-compliant CRUD operations).

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ClaimsAnamoly                            │
│  (High-level ML Application with Anomaly Detection)         │
├─────────────────────────────────────────────────────────────┤
│  • ML Anomaly Detection Models                              │
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
│  • FHIR Claim Resources                                     │
│  • Basic CRUD Operations                                    │
│  • Database Schema                                          │
│  • Data Validation                                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 8000, 8001, 3000, 3001, 5432 available

### 1. Start the Integrated System

```bash
cd AIFoundation/MLFoundation/Traditional/ClaimsAnamoly
./run_integrated.sh
```

This will start:
- **Claims Service**: http://localhost:8001
- **Claims Service Frontend**: http://localhost:3000
- **ClaimsAnamoly API**: http://localhost:8000
- **ClaimsAnamoly Frontend**: http://localhost:3001
- **PostgreSQL Database**: localhost:5432

### 2. Verify System Health

```bash
# Check Claims Service
curl http://localhost:8001/health

# Check ClaimsAnamoly API
curl http://localhost:8000/health

# Check Integration Health
curl http://localhost:8000/api/v1/health/integration
```

## 📊 API Endpoints

### ClaimsAnamoly API (Port 8000)

#### Core ML Endpoints
- `POST /api/v1/score` - Score single claim with FHIR integration
- `POST /api/v1/score/batch` - Score batch claims with FHIR integration
- `GET /api/v1/model/info` - Get model information

#### Integration Endpoints
- `GET /api/v1/claims/from-service` - Get claims from Claims service
- `POST /api/v1/score/from-service` - Score claims from Claims service
- `GET /api/v1/stats/anomaly` - Get anomaly statistics with FHIR data
- `GET /api/v1/health/integration` - Check integration health

#### Utility Endpoints
- `POST /api/v1/validate/claim` - Validate claim data
- `GET /api/v1/example` - Get example claim data

### Claims Service API (Port 8001)

#### FHIR CRUD Endpoints
- `GET /api/v1/claims` - List claims with filtering
- `POST /api/v1/claims` - Create new claim
- `GET /api/v1/claims/{id}` - Get specific claim
- `PUT /api/v1/claims/{id}` - Update claim
- `DELETE /api/v1/claims/{id}` - Delete claim

#### Related Resources
- `GET /api/v1/claim-responses` - List claim responses
- `POST /api/v1/claim-responses` - Create claim response
- `GET /api/v1/coverages` - List coverage information
- `POST /api/v1/coverages` - Create coverage

#### Utility Endpoints
- `GET /api/v1/stats/claims` - Get claims statistics
- `GET /api/v1/patients/{id}/claims` - Get patient claims

## 🔧 Usage Examples

### 1. Score a Single Claim with FHIR Integration

```bash
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "claim_id": "CLM001",
    "submission_date": "2024-01-15",
    "provider_id": "PROV001",
    "provider_specialty": "Cardiology",
    "patient_age": 45,
    "patient_gender": "M",
    "cpt_code": "99213",
    "icd_code": "I10",
    "units_of_service": 1,
    "billed_amount": 150.00,
    "paid_amount": 120.00,
    "place_of_service": "11",
    "prior_authorization": "N"
  }'
```

**Response:**
```json
{
  "claim_id": "CLM001",
  "risk_score": 0.85,
  "classification": "high_risk",
  "top_drivers": ["billed_amount", "provider_specialty", "cpt_code"],
  "timestamp": "2024-01-15T10:30:00Z",
  "fhir_claim_id": "fhir-claim-123",
  "integration_status": "success",
  "stored_in_fhir": true
}
```

### 2. Score Claims from Claims Service

```bash
curl -X POST http://localhost:8000/api/v1/score/from-service?limit=10
```

This will:
1. Retrieve 10 claims from the Claims service
2. Score them using the ML model
3. Return anomaly detection results

### 3. Get Claims from Claims Service

```bash
curl http://localhost:8000/api/v1/claims/from-service?limit=5
```

### 4. Create a Claim in Claims Service

```bash
curl -X POST http://localhost:8001/api/v1/claims \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT001",
    "provider_id": "PROV001",
    "status": "active",
    "type": "institutional",
    "use": "claim",
    "created": "2024-01-15T10:00:00Z",
    "insurer_id": "INS001",
    "provider_id": "PROV001",
    "priority": "normal",
    "funds_reserve": "none",
    "related": [],
    "prescription": false,
    "original_prescription": false,
    "payee": null,
    "referral": null,
    "facility": null,
    "care_team": [],
    "insurance": [],
    "accident": null,
    "employment_impacted": null,
    "hospitalization": null,
    "item": [],
    "total": {
      "currency": "USD",
      "value": 150.00
    }
  }'
```

## 🔍 Integration Features

### 1. Automatic Data Transformation
- ClaimsAnamoly format ↔ FHIR format conversion
- Maintains data integrity during transformation
- Handles complex nested structures

### 2. Fallback Mechanism
- If Claims service is unavailable, falls back to local ML processing
- Graceful degradation with status indicators
- Automatic retry mechanisms

### 3. Enhanced Analytics
- Combines ML insights with FHIR data
- Cross-references claims across systems
- Provides comprehensive risk assessment

### 4. Real-time Processing
- Immediate scoring with FHIR storage
- Batch processing capabilities
- Asynchronous operations for large datasets

## 🛠️ Configuration

### Environment Variables

#### ClaimsAnamoly API
```bash
CLAIMS_SERVICE_URL=http://claims-service:8000  # Internal Docker network
CLAIMS_SERVICE_BASE_URL=http://localhost:8001  # External access
LOG_LEVEL=INFO
PYTHONPATH=/app
```

#### Claims Service
```bash
DATABASE_URL=postgresql://fhir_user:fhir_password_2024!@claims-db:5432/fhir_claims_db
SECRET_KEY=your-super-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Docker Configuration
- **Claims Service**: Port 8001 (external), 8000 (internal)
- **ClaimsAnamoly**: Port 8000 (external)
- **Frontends**: Ports 3000, 3001
- **Database**: Port 5432

## 📈 Monitoring and Logs

### View Logs
```bash
# All services
docker-compose -f docker-compose.integrated.yml logs -f

# Specific service
docker-compose -f docker-compose.integrated.yml logs -f claims-anomaly-api
docker-compose -f docker-compose.integrated.yml logs -f claims-service
```

### Health Checks
```bash
# Claims Service health
curl http://localhost:8001/health

# ClaimsAnamoly health
curl http://localhost:8000/health

# Integration health
curl http://localhost:8000/api/v1/health/integration
```

### Statistics
```bash
# Claims statistics
curl http://localhost:8001/api/v1/stats/claims

# Anomaly statistics with FHIR integration
curl http://localhost:8000/api/v1/stats/anomaly
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Conflicts
**Problem**: Services won't start due to port conflicts
**Solution**: 
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :8001
lsof -i :3000
lsof -i :3001

# Stop conflicting services or change ports in docker-compose.integrated.yml
```

#### 2. Database Connection Issues
**Problem**: Claims service can't connect to database
**Solution**:
```bash
# Check database container
docker-compose -f docker-compose.integrated.yml logs claims-db

# Restart database
docker-compose -f docker-compose.integrated.yml restart claims-db
```

#### 3. Integration Failures
**Problem**: ClaimsAnamoly can't connect to Claims service
**Solution**:
```bash
# Check Claims service health
curl http://localhost:8001/health

# Check network connectivity
docker-compose -f docker-compose.integrated.yml exec claims-anomaly-api ping claims-service

# Restart services
docker-compose -f docker-compose.integrated.yml restart claims-service claims-anomaly-api
```

#### 4. Model Loading Issues
**Problem**: ML model not found
**Solution**:
```bash
# Check if model file exists
ls -la models/claims_anomaly_model.pkl

# If missing, the system will work with fallback mode
# Check logs for details
docker-compose -f docker-compose.integrated.yml logs claims-anomaly-api
```

## 🚀 Production Deployment

### Security Considerations
1. Change default passwords in production
2. Use HTTPS for all external communications
3. Implement proper authentication and authorization
4. Secure database connections
5. Use environment-specific configuration

### Scaling Considerations
1. Use external database for production
2. Implement load balancing for APIs
3. Use Redis for caching
4. Monitor resource usage
5. Implement proper logging and monitoring

### Environment Variables for Production
```bash
# Claims Service
DATABASE_URL=postgresql://user:pass@prod-db:5432/fhir_claims_db
SECRET_KEY=your-production-secret-key
ENVIRONMENT=production
LOG_LEVEL=warning

# ClaimsAnamoly
CLAIMS_SERVICE_URL=http://prod-claims-service:8000
LOG_LEVEL=warning
```

## 📚 Additional Resources

- [ClaimsAnamoly Documentation](./README.md)
- [Claims Service Documentation](../../../../HealthcareFoundation/CoreServices/Claims/README.md)
- [Integration Documentation](./INTEGRATION_DOCUMENTATION.md)
- [API Documentation](http://localhost:8000/docs) (when running)
- [FHIR Claims Resource](https://www.hl7.org/fhir/claim.html)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs for error details
3. Verify all services are running and healthy
4. Test individual components separately
5. Check network connectivity between services 