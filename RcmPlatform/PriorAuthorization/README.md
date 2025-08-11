# Prior Authorization System

A comprehensive healthcare prior authorization system that handles EDI 278/275 transactions for insurance verification and authorization requests.

## 🏗️ Architecture

This system provides a complete solution for healthcare prior authorization processing:

- **EDI 278 Processing**: Prior authorization requests and responses
- **EDI 275 Processing**: Patient information management
- **Real-time Verification**: Insurance eligibility and benefits
- **Automated Workflows**: Streamlined authorization processes
- **Compliance**: HIPAA and healthcare standards compliance

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- PostgreSQL 12+

### 1. Start the System

```bash
# Clone the repository (if not already done)
cd RcmPlatform/PriorAuthorization

# Start all services
docker-compose up --build
```

### 2. Access the Services

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | FastAPI backend |
| API Documentation | http://localhost:8000/docs | Interactive API docs |
| Frontend | http://localhost:3000 | React frontend |
| Database | localhost:5432 | PostgreSQL database |

### 3. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Check database connection
docker exec health_insurance_preauth_db pg_isready -U insuranceuser -d health_insurance_preauth_db
```

## 📊 System Components

### Backend (FastAPI)

- **EDI 278 Processing**: Prior authorization requests and responses
- **EDI 275 Processing**: Patient information management
- **Code Management**: CPT, HCPCS, ICD-10, and service type codes
- **Audit Trail**: Complete authorization audit logging
- **File Upload**: Supporting documentation management

### Frontend (React)

- **Prior Authorization Dashboard**: Request management and tracking
- **Patient Information**: Patient demographics and insurance details
- **Code Lookup**: CPT, HCPCS, and diagnosis code search
- **Document Management**: File upload and retrieval
- **Reporting**: Authorization statistics and analytics

### Database (PostgreSQL)

- **Patient Information**: Demographics, insurance, medical history
- **Authorization Requests**: EDI 278 request tracking
- **Authorization Responses**: EDI 278 response management
- **Code Tables**: Healthcare procedure and diagnosis codes
- **Audit Logs**: Complete activity tracking

## 🔧 API Endpoints

### Prior Authorization

- `POST /api/v1/prior-auth/` - Submit authorization request
- `GET /api/v1/prior-auth/{request_id}` - Get request details
- `PUT /api/v1/prior-auth/{request_id}` - Update request
- `GET /api/v1/prior-auth/` - List all requests
- `POST /api/v1/prior-auth/{request_id}/decision` - Submit decision

### Patient Information

- `POST /api/v1/patients/` - Create patient record
- `GET /api/v1/patients/{patient_id}` - Get patient details
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `GET /api/v1/patients/` - List patients
- `POST /api/v1/patients/{patient_id}/edi-275` - Generate EDI 275

### Code Management

- `GET /api/v1/codes/procedures` - Search procedure codes
- `GET /api/v1/codes/diagnoses` - Search diagnosis codes
- `GET /api/v1/codes/service-types` - Get service type codes

## 📋 Database Schema

### Core Tables

1. **patient_information** - Patient demographics and insurance
2. **prior_authorization_requests** - EDI 278 request tracking
3. **prior_authorization_responses** - EDI 278 response management
4. **service_type_codes** - Healthcare service type codes
5. **procedure_codes** - CPT/HCPCS procedure codes
6. **diagnosis_codes** - ICD-10 diagnosis codes
7. **authorization_audit** - Complete audit trail

### Key Features

- **EDI Compliance**: Full EDI 278/275 transaction support
- **Audit Trail**: Complete activity logging
- **Code Management**: Healthcare code lookup and validation
- **File Management**: Supporting documentation storage
- **Status Tracking**: Real-time authorization status

## 🛠️ Development

### Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd RcmPlatform/PriorAuthorization

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://insuranceuser:insurancepass123@localhost:5432/health_insurance_preauth_db"
export SECRET_KEY="your-secret-key"

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Database Management

```bash
# Connect to database
docker exec -it health_insurance_preauth_db psql -U insuranceuser -d health_insurance_preauth_db

# Run migrations
docker exec health_insurance_preauth_backend alembic upgrade head

# Reset database
docker-compose down -v
docker-compose up --build
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prior authorization endpoint
curl -X POST http://localhost:8000/api/v1/prior-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient_first_name": "John",
    "patient_last_name": "Doe",
    "patient_dob": "1990-01-01",
    "patient_gender": "M",
    "member_id": "MEM123456",
    "requesting_provider_npi": "1234567890",
    "procedure_codes": [{"code": "99213"}],
    "diagnosis_codes": [{"code": "E11.9", "is_primary": true}],
    "service_date_from": "2024-01-15",
    "medical_necessity": "Patient requires evaluation and management"
  }'
```

## 🔒 Security & Compliance

### HIPAA Compliance

- **Data Encryption**: All sensitive data encrypted at rest and in transit
- **Access Controls**: Role-based access control (RBAC)
- **Audit Logging**: Complete activity audit trail
- **Data Retention**: Configurable data retention policies

### Security Features

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based permissions
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Secure cross-origin requests

## 📈 Monitoring & Logging

### Health Checks

- **API Health**: `/health` endpoint for service status
- **Database Health**: Connection monitoring
- **Service Dependencies**: Dependency health tracking

### Logging

- **Application Logs**: Structured logging with correlation IDs
- **Audit Logs**: Complete activity tracking
- **Error Logs**: Detailed error reporting and monitoring

## 🚀 Deployment

### Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export SECRET_KEY="your-production-secret-key"
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://insuranceuser:insurancepass123@postgres:5432/health_insurance_preauth_db` |
| `SECRET_KEY` | JWT secret key | `BCPucohgb5sgE5-iK5wF30MyjGzwspJaryigw5dKwkw` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `DEBUG` | Debug mode | `True` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- **Documentation**: Check the API docs at http://localhost:8000/docs
- **Issues**: Create an issue in the repository
- **Email**: Contact the development team

## 🔄 Version History

- **v1.0.0** - Initial release with EDI 278/275 support
- **v1.1.0** - Added file upload and audit logging
- **v1.2.0** - Enhanced security and compliance features

---

**Note**: This system is designed for healthcare use and includes HIPAA compliance features. Ensure proper security measures are in place for production deployment.
