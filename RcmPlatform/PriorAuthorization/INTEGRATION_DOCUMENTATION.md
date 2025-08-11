# Prior Authorization + Patient Microservice Integration

## Overview

This document describes the integration between the Prior Authorization system and the Patient microservice from HealthcareFoundation/CoreServices/Patient. The integration eliminates redundant patient information and creates a proper microservice architecture.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Integrated System                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   Patient       │    │     Prior Authorization            │ │
│  │  Microservice   │    │                                     │ │
│  │                 │    │  ┌─────────────────────────────┐    │ │
│  │  ┌─────────────┐│    │  │     Patient Client          │    │ │
│  │  │   FastAPI   ││◄───┤  │  (HTTP Client to Patient    │    │ │
│  │  │   Backend   ││    │  │   Microservice)             │    │ │
│  │  └─────────────┘│    │  └─────────────────────────────┘    │ │
│  │                 │    │                                     │ │
│  │  ┌─────────────┐│    │  ┌─────────────────────────────┐    │ │
│  │  │   React     ││    │  │   Prior Authorization       │    │ │
│  │  │  Frontend   ││    │  │   Service                   │    │ │
│  │  └─────────────┘│    │  └─────────────────────────────┘    │ │
│  │                 │    │                                     │ │
│  │  ┌─────────────┐│    │  ┌─────────────────────────────┐    │ │
│  │  │ PostgreSQL  ││    │  │   EDI Processing            │    │ │
│  │  │  Database   ││    │  │   (275/278)                 │    │ │
│  │  └─────────────┘│    │  └─────────────────────────────┘    │ │
│  └─────────────────┘    │                                     │ │
│                         │  ┌─────────────────────────────┐    │ │
│                         │  │   Healthcare Codes          │    │ │
│                         │  │   Management                │    │ │
│                         │  └─────────────────────────────┘    │ │
│                         │                                     │ │
│                         │  ┌─────────────────────────────┐    │ │
│                         │  │   React Frontend            │    │ │
│                         │  └─────────────────────────────┘    │ │
│                         └─────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Benefits

### 1. **Elimination of Data Redundancy**
- Prior Authorization no longer stores patient information locally
- Single source of truth for patient data in Patient microservice
- Reduced data synchronization issues

### 2. **Proper Microservice Architecture**
- Clear separation of concerns
- Patient microservice handles all FHIR Patient operations
- Prior Authorization focuses on authorization requests and EDI processing

### 3. **FHIR Compliance**
- Patient microservice provides full FHIR Patient resource support
- Standardized patient data format across the system
- Better interoperability with other healthcare systems

### 4. **Scalability**
- Independent scaling of Patient and Prior Authorization services
- Reduced database load on Prior Authorization system
- Better resource utilization

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Patient Backend | 8000 | Patient microservice API |
| Patient Frontend | 3000 | Patient management UI |
| Patient Database | 5432 | Patient data storage |
| Prior Auth Backend | 8002 | Prior authorization API |
| Prior Auth Frontend | 3002 | Prior authorization UI |
| Prior Auth Database | 5435 | Authorization data storage |

## Integration Components

### 1. Patient Client (`app/services/patient_client.py`)

The Patient Client is responsible for communicating with the Patient microservice:

```python
class PatientClientSync:
    def get_patient(self, patient_id: str) -> Optional[PatientResponse]
    def create_patient(self, patient_data: PatientCreate) -> PatientResponse
    def update_patient(self, patient_id: str, patient_update: PatientUpdate) -> Optional[PatientResponse]
    def search_patients(self, **filters) -> List[PatientResponse]
    def get_patient_by_identifier(self, identifier_value: str) -> Optional[PatientResponse]
```

### 2. Data Transformation

The integration includes bidirectional data transformation between Prior Authorization and Patient microservice formats:

#### Prior Authorization → Patient Microservice
```python
def _convert_to_patient_create(self, patient_data: PatientInformationCreate) -> PatientCreate:
    # Converts Prior Authorization patient format to FHIR Patient format
```

#### Patient Microservice → Prior Authorization
```python
def _convert_from_patient_response(self, patient: PatientResponse) -> PatientInformation:
    # Converts FHIR Patient format to Prior Authorization format
```

### 3. Updated Patient Service (`app/services/patient_service.py`)

The Patient Service now uses the Patient Client instead of local database operations:

```python
class PatientService:
    def __init__(self):
        self.edi_service = EDI275Service()
        # No longer uses local DAO
    
    def create_patient(self, db: Session, patient_data: PatientInformationCreate) -> PatientInformation:
        # Creates patient via Patient microservice
        patient_create = self._convert_to_patient_create(patient_data)
        patient_response = patient_client.create_patient(patient_create)
        return self._convert_from_patient_response(patient_response)
```

## API Endpoints

### Prior Authorization Patient Endpoints

All Prior Authorization patient endpoints now proxy to the Patient microservice:

- `POST /api/v1/patients/` - Create patient (via Patient microservice)
- `GET /api/v1/patients/{patient_id}` - Get patient (via Patient microservice)
- `PUT /api/v1/patients/{patient_id}` - Update patient (via Patient microservice)
- `GET /api/v1/patients/member/{member_id}` - Get patient by member ID
- `GET /api/v1/patients/` - Search patients (via Patient microservice)
- `GET /api/v1/patients/{patient_id}/edi275` - Generate EDI 275

### Patient Microservice Endpoints

The Patient microservice provides full FHIR Patient resource support:

- `POST /patients` - Create FHIR Patient
- `GET /patients` - List patients
- `GET /patients/{patient_id}` - Get patient by ID
- `GET /patients/fhir/{fhir_id}` - Get patient by FHIR ID
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient
- `GET /patients/search/name` - Search by name

## Setup and Deployment

### 1. Quick Start

```bash
# Start the integrated system
cd RcmPlatform/PriorAuthorization
./start_integrated.sh
```

### 2. Manual Setup

```bash
# Start Patient microservice
cd HealthcareFoundation/CoreServices/Patient
docker-compose up -d

# Start Prior Authorization (with Patient service URL)
cd RcmPlatform/PriorAuthorization
export PATIENT_SERVICE_URL=http://localhost:8000
docker-compose up -d
```

### 3. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PATIENT_SERVICE_URL` | `http://localhost:8000` | Patient microservice URL |
| `DATABASE_URL` | `postgresql://...` | Prior Authorization database URL |

## Testing

### 1. Integration Test

```bash
# Run comprehensive integration test
python3 test_integration.py
```

### 2. Manual Testing

```bash
# Test Patient microservice
curl http://localhost:8000/health

# Test Prior Authorization
curl http://localhost:8002/health

# Create patient via Patient microservice
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{"fhir_id": "TEST001", "family_name": "Doe", "given_names": ["John"]}'

# Get patient via Prior Authorization
curl http://localhost:8002/api/v1/patients/{patient_id}
```

## Data Flow

### 1. Patient Creation Flow

```
1. Prior Authorization receives patient creation request
2. Converts to FHIR Patient format
3. Sends to Patient microservice
4. Patient microservice creates FHIR Patient
5. Returns patient data
6. Prior Authorization converts back to its format
7. Returns response to client
```

### 2. Patient Retrieval Flow

```
1. Prior Authorization receives patient retrieval request
2. Sends request to Patient microservice
3. Patient microservice returns FHIR Patient data
4. Prior Authorization converts to its format
5. Returns response to client
```

### 3. EDI Generation Flow

```
1. Prior Authorization receives EDI generation request
2. Retrieves patient from Patient microservice
3. Converts patient data to Prior Authorization format
4. Generates EDI 275/278 content
5. Returns EDI response
```

## Error Handling

### 1. Patient Service Unavailable

If the Patient microservice is unavailable:

```python
try:
    patient = patient_client.get_patient(patient_id)
except PatientClientError as e:
    # Handle service unavailable
    raise HTTPException(status_code=503, detail="Patient service unavailable")
```

### 2. Data Transformation Errors

```python
try:
    patient_create = self._convert_to_patient_create(patient_data)
except Exception as e:
    # Handle transformation errors
    raise HTTPException(status_code=400, detail=f"Invalid patient data: {str(e)}")
```

## Monitoring and Health Checks

### 1. Service Health

```bash
# Check Patient microservice health
curl http://localhost:8000/health

# Check Prior Authorization health
curl http://localhost:8002/health
```

### 2. Integration Health

The Prior Authorization service includes integration health checks:

```python
# Check if Patient microservice is available
patient_service_healthy = patient_client.health_check()
```

## Migration from Standalone

### 1. Data Migration

If migrating from a standalone Prior Authorization system with local patient data:

1. Export patient data from Prior Authorization database
2. Transform to FHIR Patient format
3. Import into Patient microservice
4. Update Prior Authorization to use Patient microservice

### 2. Configuration Changes

1. Set `PATIENT_SERVICE_URL` environment variable
2. Remove local patient database tables
3. Update API endpoints to use Patient Client
4. Test integration thoroughly

## Troubleshooting

### Common Issues

1. **Patient Service Connection Failed**
   - Check if Patient microservice is running
   - Verify `PATIENT_SERVICE_URL` is correct
   - Check network connectivity

2. **Data Transformation Errors**
   - Verify patient data format
   - Check FHIR Patient schema compliance
   - Review transformation logic

3. **Performance Issues**
   - Monitor Patient microservice response times
   - Consider caching frequently accessed patient data
   - Optimize database queries

### Debug Commands

```bash
# Check service logs
docker-compose -f docker-compose.integrated.yml logs -f

# Check specific service
docker logs patient_backend
docker logs preauth_backend

# Test network connectivity
docker exec preauth_backend curl http://patient_backend:8000/health
```

## Future Enhancements

### 1. Caching Layer
- Implement Redis caching for frequently accessed patient data
- Reduce Patient microservice load
- Improve response times

### 2. Event-Driven Architecture
- Use message queues for patient updates
- Real-time synchronization between services
- Better scalability and reliability

### 3. Advanced Integration
- Direct FHIR resource references
- Bulk patient operations
- Advanced search capabilities

## Conclusion

The integration between Prior Authorization and Patient microservice provides:

- ✅ **Eliminated data redundancy**
- ✅ **Proper microservice architecture**
- ✅ **FHIR compliance**
- ✅ **Better scalability**
- ✅ **Clear separation of concerns**
- ✅ **Improved maintainability**

This integration serves as a model for other microservice integrations in the healthcare platform. 