# Scheduling2.0 - Patient & Practitioner Integration Guide

## Overview

This document describes the integration of Patient and Practitioner microservices from `HealthcareFoundation/CoreServices` into the `Scheduling2.0` application. The integration provides seamless access to patient and practitioner data through a unified API interface.

## Architecture

### Service Integration
- **Patient Service**: Integrated from `HealthcareFoundation/CoreServices/Patient`
- **Practitioner Service**: Integrated from `HealthcareFoundation/CoreServices/Practitioner`
- **Scheduling2.0**: Main application that orchestrates both services

### Network Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Scheduling2.0  │    │  Patient Service │
│   (Port 3000)   │◄──►│   (Port 8000)    │◄──►│  (Port 8001)     │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Practitioner     │
                       │ Service          │
                       │ (Port 8002)      │
                       └──────────────────┘
```

## Services

### 1. Patient Service Integration

**Service URL**: `http://patient-service:8000` (internal) / `http://localhost:8001` (external)

**Available Endpoints**:
- `GET /patients/` - List all patients
- `GET /patients/{patient_id}` - Get patient by UUID
- `GET /patients/fhir/{fhir_id}` - Get patient by FHIR ID
- `POST /patients/` - Create new patient
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient
- `GET /patients/search/name` - Search patients by name
- `POST /patients/search` - Search patients (POST method)
- `GET /patients/health/check` - Health check

**Database**: PostgreSQL on port 5433

### 2. Practitioner Service Integration

**Service URL**: `http://practitioner-service:8000` (internal) / `http://localhost:8002` (external)

**Available Endpoints**:
- `GET /practitioners/` - List all practitioners
- `GET /practitioners/{practitioner_id}` - Get practitioner by UUID
- `GET /practitioners/fhir/{fhir_id}` - Get practitioner by FHIR ID
- `POST /practitioners/` - Create new practitioner
- `PUT /practitioners/{practitioner_id}` - Update practitioner
- `DELETE /practitioners/{practitioner_id}` - Delete practitioner
- `GET /practitioners/search/name` - Search practitioners by name
- `GET /practitioners/search/identifier` - Search practitioners by identifier
- `POST /practitioners/search` - Search practitioners (POST method)
- `GET /practitioners/health/check` - Health check

**Database**: PostgreSQL on port 5434

## Implementation Details

### Service Classes

#### PatientService (`app/services/patient_service.py`)
```python
class PatientService:
    def __init__(self):
        self.base_url = os.getenv("PATIENT_SERVICE_URL", "http://patient-service:8000")
        self.timeout = 30.0
    
    async def get_patients(self, skip: int = 0, limit: int = 10, active: Optional[bool] = None)
    async def get_patient_by_id(self, patient_id: str)
    async def get_patient_by_fhir_id(self, fhir_id: str)
    async def create_patient(self, patient_data: Dict[str, Any])
    async def update_patient(self, patient_id: str, patient_data: Dict[str, Any])
    async def delete_patient(self, patient_id: str)
    async def search_patients_by_name(self, family_name: Optional[str] = None, given_name: Optional[str] = None, limit: int = 10)
    async def health_check(self)
```

#### PractitionerService (`app/services/practitioner_service.py`)
```python
class PractitionerService:
    def __init__(self):
        self.base_url = os.getenv("PRACTITIONER_SERVICE_URL", "http://practitioner-service:8000")
        self.timeout = 30.0
    
    async def get_practitioners(self, skip: int = 0, limit: int = 10, active: Optional[bool] = None)
    async def get_practitioner_by_id(self, practitioner_id: str)
    async def get_practitioner_by_fhir_id(self, fhir_id: str)
    async def create_practitioner(self, practitioner_data: Dict[str, Any])
    async def update_practitioner(self, practitioner_id: str, practitioner_data: Dict[str, Any])
    async def delete_practitioner(self, practitioner_id: str)
    async def search_practitioners_by_name(self, family_name: Optional[str] = None, given_name: Optional[str] = None, limit: int = 10)
    async def search_practitioners_by_identifier(self, identifier_value: str, identifier_system: Optional[str] = None, limit: int = 10)
    async def health_check(self)
```

### API Routers

#### Patients Router (`app/api/patients.py`)
- Provides RESTful endpoints for patient management
- Handles request/response transformation
- Includes error handling and validation

#### Practitioners Router (`app/api/practitioners.py`)
- Provides RESTful endpoints for practitioner management
- Handles request/response transformation
- Includes error handling and validation

## Docker Configuration

### Services in docker-compose.yml

1. **patient_postgres**: Patient service database (Port 5433)
2. **patient_service**: Patient microservice (Port 8001)
3. **practitioner_postgres**: Practitioner service database (Port 5434)
4. **practitioner_service**: Practitioner microservice (Port 8002)
5. **postgres**: Scheduling2.0 database (Port 5432)
6. **backend**: Scheduling2.0 API (Port 8000)
7. **frontend**: React frontend (Port 3000)

### Environment Variables

**Scheduling2.0 Backend**:
```yaml
PATIENT_SERVICE_URL: http://patient_service:8000
PRACTITIONER_SERVICE_URL: http://practitioner_service:8000
```

**Patient Service**:
```yaml
DATABASE_URL: postgresql://fhir_user:fhir_password@patient_postgres:5432/fhir_db
```

**Practitioner Service**:
```yaml
DATABASE_URL: postgresql://practitioner_user:practitioner_password@practitioner_postgres:5432/fhir_practitioner_db
```

## Usage Examples

### Creating a Patient
```bash
curl -X POST "http://localhost:8000/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "fhir_id": "patient-001",
    "family_name": "Doe",
    "given_names": ["John"],
    "gender": "male",
    "birth_date": "1990-01-01",
    "active": true
  }'
```

### Creating a Practitioner
```bash
curl -X POST "http://localhost:8000/practitioners/" \
  -H "Content-Type: application/json" \
  -d '{
    "fhir_id": "practitioner-001",
    "family_name": "Smith",
    "given_names": ["Dr. Jane"],
    "gender": "female",
    "birth_date": "1980-05-15",
    "active": true
  }'
```

### Searching Patients
```bash
curl "http://localhost:8000/patients/search/name?family_name=Doe&limit=10"
```

### Searching Practitioners
```bash
curl "http://localhost:8000/practitioners/search/name?family_name=Smith&limit=10"
```

### Health Checks
```bash
# Patient service health
curl "http://localhost:8000/patients/health/check"

# Practitioner service health
curl "http://localhost:8000/practitioners/health/check"
```

## Error Handling

The integration includes comprehensive error handling:

1. **Service Unavailable**: Returns 503 with service unavailable message
2. **Not Found**: Returns 404 with appropriate error message
3. **Bad Request**: Returns 400 with validation error details
4. **Internal Server Error**: Returns 500 with error details

## Health Monitoring

Each service includes health check endpoints:
- Patient Service: `/patients/health/check`
- Practitioner Service: `/practitioners/health/check`
- Scheduling2.0: `/health`

## Development

### Starting the Services
```bash
cd PracticeFoundation/Scheduling2.0
docker-compose up -d
```

### Service URLs (Development)
- **Scheduling2.0 API**: http://localhost:8000
- **Patient Service**: http://localhost:8001
- **Practitioner Service**: http://localhost:8002
- **Frontend**: http://localhost:3000

### Database Ports
- **Scheduling2.0 DB**: localhost:5432
- **Patient DB**: localhost:5433
- **Practitioner DB**: localhost:5434

## Integration Benefits

1. **Unified API**: Single endpoint for accessing patient and practitioner data
2. **FHIR Compliance**: Maintains FHIR standards for healthcare data
3. **Scalability**: Microservices can be scaled independently
4. **Fault Tolerance**: Graceful degradation when services are unavailable
5. **Data Consistency**: Each service manages its own data with proper validation

## Future Enhancements

1. **Caching Layer**: Implement Redis caching for frequently accessed data
2. **Event Streaming**: Add event-driven communication between services
3. **API Gateway**: Implement a proper API gateway for better routing and security
4. **Monitoring**: Add comprehensive monitoring and alerting
5. **Authentication**: Implement service-to-service authentication 