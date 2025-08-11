# ClaimsAnomaly + Claims Service Integration Documentation

## Overview

This document describes the integration between **ClaimsAnomaly** (high-level ML application) and **Claims** (foundational service), creating a unified system that combines:

- **ClaimsAnomaly**: ML anomaly detection, real-time scoring, batch processing, and risk analytics
- **Claims Service**: FHIR-based CRUD operations, standard compliance, and data validation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ClaimsAnomaly                            │
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

## Key Components

### 1. Claims Service Client (`claims_service_client.py`)

**Purpose**: HTTP client for communicating with the Claims service

**Features**:
- Async HTTP client using `httpx`
- Comprehensive error handling and fallback mechanisms
- Support for all Claims service endpoints
- Health check functionality

**Key Methods**:
```python
# CRUD Operations
await client.create_claim(claim_data)
await client.get_claim(claim_id)
await client.get_claims(skip=0, limit=100, status=None, patient_id=None)
await client.update_claim(claim_id, claim_data)
await client.delete_claim(claim_id)

# Relationship Operations
await client.get_claim_responses_for_claim(claim_id)
await client.get_patient_claims(patient_id)

# Statistics
await client.get_claims_stats()
await client.health_check()
```

### 2. Data Transformer (`ClaimsDataTransformer`)

**Purpose**: Transform data between ClaimsAnomaly and FHIR formats

**Features**:
- Bidirectional transformation (ClaimsAnomaly ↔ FHIR)
- Maintains data integrity during conversion
- Handles complex nested structures
- Preserves all essential claim information

**Key Methods**:
```python
# ClaimsAnomaly to FHIR
fhir_claim = ClaimsDataTransformer.anomaly_claim_to_fhir(anomaly_claim_data)

# FHIR to ClaimsAnomaly
anomaly_claim = ClaimsDataTransformer.fhir_claim_to_anomaly(fhir_claim_data)

# Batch transformations
fhir_claims = ClaimsDataTransformer.batch_anomaly_to_fhir(batch_claims)
anomaly_claims = ClaimsDataTransformer.batch_fhir_to_anomaly(batch_fhir_claims)
```

### 3. Enhanced Inference Engine (`enhanced_inference.py`)

**Purpose**: Orchestrates ML operations between ClaimsAnomaly and Claims service

**Features**:
- Combines local ML processing with Claims service operations
- Automatic fallback to local processing when Claims service unavailable
- Comprehensive error handling and logging
- Maintains all original ClaimsAnomaly ML functionality

**Key Methods**:
```python
# ML Scoring with Integration
result = await engine.score_single_claim(claim_data, use_fhir=True)
batch_result = await engine.score_batch_claims(batch_claims, use_fhir=True)

# Service Integration
claims_data = await engine.get_claims_for_scoring(limit=100, use_fhir=True)
service_result = await engine.score_claims_from_service(limit=100, use_fhir=True)

# Statistics and Health
stats = await engine.get_anomaly_statistics(use_fhir=True)
health_status = await engine.health_check()
validation_result = await engine.validate_claim_data(claim_data)
```

### 4. Enhanced API Routes (`enhanced_fastapi_app.py`)

**Purpose**: API endpoints that provide integrated ML functionality

**Features**:
- Combines ClaimsAnomaly and Claims service capabilities
- Maintains backward compatibility
- Provides comprehensive error handling
- Includes all original ML functionality

**Key Endpoints**:
```
POST   /api/v1/score                    # Score single claim with FHIR integration
POST   /api/v1/score/batch              # Score batch claims with FHIR integration
POST   /api/v1/score/from-service       # Score claims from Claims service
GET    /api/v1/claims/from-service      # Get claims from Claims service
GET    /api/v1/stats/anomaly            # Get anomaly statistics
GET    /api/v1/health/integration       # Health check
POST   /api/v1/validate/claim           # Validate claim data
GET    /api/v1/model/info               # Model information
```

## Data Flow

### 1. Single Claim Scoring Process

```
1. User submits claim for scoring
   ↓
2. Enhanced Inference Engine receives claim
   ↓
3. Local ML model scores claim for anomalies
   ↓
4. Data Transformer converts to FHIR format
   ↓
5. Claims Service Client stores claim in Claims service
   ↓
6. Combined result returned to user
```

### 2. Batch Claim Scoring Process

```
1. User submits batch of claims
   ↓
2. Enhanced Inference Engine processes batch
   ↓
3. Local ML model scores all claims
   ↓
4. Data Transformer converts batch to FHIR format
   ↓
5. Claims Service Client stores claims in Claims service
   ↓
6. Combined results returned to user
```

### 3. Service Integration Process

```
1. User requests scoring from Claims service
   ↓
2. Enhanced Inference Engine retrieves claims from service
   ↓
3. Data Transformer converts FHIR claims to ClaimsAnomaly format
   ↓
4. Local ML model scores claims
   ↓
5. Results returned to user
```

### 4. Fallback Mechanism

```
1. Primary operation fails (Claims service unavailable)
   ↓
2. Enhanced Inference Engine detects error
   ↓
3. Automatic fallback to local ML processing
   ↓
4. Operation completed using local capabilities
   ↓
5. Result marked with fallback status
   ↓
6. User receives result with fallback indication
```

## Configuration

### Environment Variables

```bash
# Claims Service Configuration
CLAIMS_SERVICE_URL=http://localhost:8001
CLAIMS_SERVICE_TIMEOUT=30

# Integration Settings
USE_FHIR_BY_DEFAULT=true
ENABLE_FALLBACK=true
LOG_INTEGRATION_DETAILS=true
```

### Docker Compose Configuration

```yaml
services:
  claims-anomaly:
    # ... existing configuration ...
    environment:
      - CLAIMS_SERVICE_URL=http://claims-service:8001
    depends_on:
      - claims-service
    ports:
      - "8002:8002"

  claims-service:
    # ... Claims service configuration ...
    ports:
      - "8001:8000"
```

## API Examples

### 1. Score Single Claim with Integration

```bash
curl -X POST "http://localhost:8002/api/v1/score" \
  -H "Content-Type: application/json" \
  -d '{
    "claim_id": "TEST-001",
    "submission_date": "2024-01-15",
    "provider_id": "PROVIDER-123",
    "provider_specialty": "Cardiology",
    "patient_age": 45,
    "patient_gender": "M",
    "cpt_code": "99213",
    "icd_code": "I10",
    "units_of_service": 1,
    "billed_amount": 150.00,
    "paid_amount": 120.00,
    "place_of_service": "11",
    "prior_authorization": "N",
    "modifier": "",
    "is_anomaly": 0
  }' \
  -G -d "use_fhir=true"
```

**Response**:
```json
{
  "claim_id": "TEST-001",
  "risk_score": 0.85,
  "classification": "high_risk",
  "top_drivers": ["billed_amount", "provider_specialty"],
  "timestamp": "2024-01-01T12:00:00Z",
  "fhir_claim_id": "uuid-12345",
  "integration_status": "success",
  "stored_in_fhir": true
}
```

### 2. Score Batch Claims with Integration

```bash
curl -X POST "http://localhost:8002/api/v1/score/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "claims": [
      {
        "claim_id": "TEST-001",
        "submission_date": "2024-01-15",
        "provider_id": "PROVIDER-123",
        "provider_specialty": "Cardiology",
        "patient_age": 45,
        "patient_gender": "M",
        "cpt_code": "99213",
        "icd_code": "I10",
        "units_of_service": 1,
        "billed_amount": 150.00,
        "paid_amount": 120.00,
        "place_of_service": "11",
        "prior_authorization": "N",
        "modifier": "",
        "is_anomaly": 0
      }
    ],
    "use_fhir": true
  }'
```

**Response**:
```json
{
  "results": [
    {
      "claim_id": "TEST-001",
      "risk_score": 0.85,
      "classification": "high_risk",
      "top_drivers": ["billed_amount", "provider_specialty"],
      "timestamp": "2024-01-01T12:00:00Z",
      "fhir_claim_id": "uuid-12345",
      "integration_status": "success",
      "stored_in_fhir": true
    }
  ],
  "count": 1,
  "timestamp": "2024-01-01T12:00:00Z",
  "integration_status": "success",
  "stored_in_fhir": true,
  "successfully_stored": 1
}
```

### 3. Score Claims from Service

```bash
curl -X POST "http://localhost:8002/api/v1/score/from-service?limit=10&use_fhir=true"
```

**Response**:
```json
{
  "message": "Scored 5 claims from fhir",
  "results": [
    {
      "claim_id": "SERVICE-001",
      "risk_score": 0.72,
      "classification": "medium_risk",
      "top_drivers": ["patient_age", "cpt_code"],
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "count": 5,
  "source": "fhir",
  "integration_status": "local_only"
}
```

### 4. Health Check Integration

```bash
curl -X GET "http://localhost:8002/api/v1/health/integration"
```

**Response**:
```json
{
  "health_status": {
    "local": {
      "status": "healthy",
      "model_loaded": true,
      "timestamp": "2024-01-01T12:00:00Z"
    },
    "fhir": {
      "status": "healthy"
    },
    "overall_status": "healthy"
  },
  "integration": "enhanced_claims_anomaly"
}
```

## Testing

### Running Integration Tests

```bash
# Navigate to ClaimsAnomaly directory
cd AIFoundation/MLFoundation/Traditional/ClaimsAnamoly

# Run integration tests
python3 test_integration.py
```

### Test Coverage

The integration test suite covers:

1. **Service Health Checks**
   - Claims service health
   - ClaimsAnomaly health
   - Integration health

2. **ML Scoring Operations**
   - Single claim scoring
   - Batch claim scoring
   - Service integration scoring
   - Error handling and fallback

3. **Data Transformation**
   - ClaimsAnomaly to FHIR conversion
   - FHIR to ClaimsAnomaly conversion
   - Batch transformations

4. **Model and Statistics**
   - Model information
   - Anomaly statistics
   - Integration features

5. **Validation and Examples**
   - Claim data validation
   - Example endpoints
   - Error handling

## Benefits

### For ClaimsAnomaly

- ✅ **FHIR Compliance**: Standard healthcare data format
- ✅ **Reduced Complexity**: Leverages foundational service
- ✅ **Better Interoperability**: Standard data exchange
- ✅ **Maintained ML Capabilities**: All original features preserved

### For Claims Service

- ✅ **Enhanced ML Processing**: Higher-level anomaly detection
- ✅ **Advanced Analytics**: Risk assessment and insights
- ✅ **Real-time Scoring**: Intelligent processing capabilities
- ✅ **Batch Processing**: Sophisticated ML workflows

### For Overall System

- ✅ **Unified Data Model**: Consistent data representation
- ✅ **Scalable Architecture**: Service-oriented design
- ✅ **Better Maintainability**: Separation of concerns
- ✅ **Future-Proof**: Standards-based approach

## Troubleshooting

### Common Issues

1. **Claims Service Unavailable**
   - **Symptom**: Integration status shows "fallback"
   - **Solution**: Check Claims service is running on port 8001
   - **Command**: `curl http://localhost:8001/health`

2. **ML Model Not Loaded**
   - **Symptom**: API returns "ML model not loaded" error
   - **Solution**: Check model file exists at `models/claims_anomaly_model.pkl`
   - **Debug**: Check application logs for model loading errors

3. **Data Transformation Errors**
   - **Symptom**: Scoring fails with transformation error
   - **Solution**: Check claim data format compliance
   - **Debug**: Enable detailed logging

4. **Performance Issues**
   - **Symptom**: Slow scoring response times
   - **Solution**: Check network connectivity between services
   - **Optimization**: Implement caching if needed

### Debug Mode

Enable detailed logging by setting environment variables:

```bash
export LOG_LEVEL=DEBUG
export LOG_INTEGRATION_DETAILS=true
```

### Health Monitoring

Monitor integration health:

```bash
# Check overall health
curl http://localhost:8002/api/v1/health/integration

# Check individual services
curl http://localhost:8002/health
curl http://localhost:8001/health
```

## Migration Guide

### From ClaimsAnomaly Only

1. **Deploy Claims Service**
   ```bash
   cd HealthcareFoundation/CoreServices/Claims
   docker-compose up -d
   ```

2. **Update ClaimsAnomaly Configuration**
   ```bash
   # Add Claims service URL to environment
   export CLAIMS_SERVICE_URL=http://localhost:8001
   ```

3. **Test Integration**
   ```bash
   python3 test_integration.py
   ```

4. **Update API Calls**
   - Use enhanced endpoints for integrated functionality
   - Original endpoints remain available for backward compatibility

### Data Migration

1. **Export Existing Data**
   ```python
   # Export ClaimsAnomaly training data
   import pandas as pd
   df = pd.read_csv('training_data.csv')
   df.to_csv('claims_anomaly_backup.csv', index=False)
   ```

2. **Transform to FHIR Format**
   ```python
   # Use ClaimsDataTransformer to convert existing data
   transformer = ClaimsDataTransformer()
   fhir_data = transformer.anomaly_claim_to_fhir(anomaly_claim_data)
   ```

3. **Import to Claims Service**
   ```python
   # Use Claims service client to import data
   async with ClaimsServiceClient() as client:
       await client.create_claim(fhir_data)
   ```

## Future Enhancements

### Planned Features

1. **Real-time Synchronization**
   - Bidirectional data sync between services
   - Event-driven updates
   - Conflict resolution

2. **Advanced Caching**
   - Redis-based caching layer
   - Intelligent cache invalidation
   - Performance optimization

3. **Enhanced Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Alerting and notifications

4. **Batch Operations**
   - Bulk claim processing
   - Batch data migration
   - Performance optimization

### API Evolution

1. **GraphQL Support**
   - Flexible querying
   - Reduced over-fetching
   - Better frontend integration

2. **Webhook Integration**
   - Real-time notifications
   - Event-driven architecture
   - External system integration

3. **API Versioning**
   - Backward compatibility
   - Gradual migration
   - Feature flags

## Conclusion

The ClaimsAnomaly + Claims Service integration provides a robust, scalable, and standards-compliant solution for healthcare claims anomaly detection. By combining the strengths of both systems, it delivers enhanced functionality while maintaining reliability and performance.

The integration is designed to be:
- **Non-disruptive**: Existing functionality preserved
- **Scalable**: Service-oriented architecture
- **Reliable**: Comprehensive error handling and fallback
- **Standards-compliant**: FHIR-based data model
- **Future-ready**: Extensible and maintainable

For support and questions, refer to the troubleshooting section or contact the development team. 