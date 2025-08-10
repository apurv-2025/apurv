# File: README.md
# Health Insurance Verification System - Backend

A modern FastAPI backend for health insurance eligibility verification with EDI 270/271 support.

## Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy ORM**: Powerful database abstraction layer
- **Modular Architecture**: Clean separation of concerns with services, CRUD, and schemas
- **EDI 270/271 Support**: Full implementation of healthcare eligibility transactions
- **OCR Processing**: Advanced text extraction from insurance cards
- **PostgreSQL Database**: Robust relational database with full ACID compliance
- **Comprehensive Logging**: Structured logging with rotation and levels
- **Docker Support**: Containerized deployment with health checks
- **Testing Suite**: Unit and integration tests with pytest
- **Database Migrations**: Alembic for schema version control

## Technology Stack

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM and database toolkit
- **PostgreSQL**: Primary database
- **Alembic**: Database migration tool
- **Tesseract**: OCR engine
- **OpenCV**: Image processing
- **Pydantic**: Data validation and serialization
- **pytest**: Testing framework

## Project Structure

```
app/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── security.py        # Security utilities
│   ├── logging.py         # Logging configuration
│   └── exceptions.py      # Custom exceptions
├── models/                 # SQLAlchemy models
│   └── models.py          # Database models
├── schemas/                # Pydantic schemas
│   ├── insurance_card.py  # Insurance card schemas
│   ├── eligibility.py     # Eligibility schemas
│   ├── provider.py        # Provider schemas
│   └── common.py          # Common schemas
├── crud/                   # CRUD operations
│   ├── base.py            # Base CRUD class
│   ├── crud_insurance_card.py
│   ├── crud_eligibility.py
│   └── crud_provider.py
├── services/               # Business logic
│   ├── ocr_service.py     # OCR processing
│   └── edi_service.py     # EDI transaction handling
└── api/                    # API routes
    └── api_v1/
        ├── api.py         # API router
        └── endpoints/     # Route handlers
            ├── upload.py
            ├── eligibility.py
            ├── providers.py
            └── health.py
```

## Installation and Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Tesseract OCR
- Docker (optional)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd health-insurance-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API settings
   ```

5. **Set up database:**
   ```bash
   # Create database
   createdb health_insurance_db
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build individual container:**
   ```bash
   docker build -t health-insurance-backend .
   docker run -p 8000:8000 health-insurance-backend
   ```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## Key Components

### Models and Database

The application uses SQLAlchemy models with proper relationships:

- **InsuranceCard**: Store OCR-extracted insurance information
- **EligibilityRequest**: EDI 270 transaction records
- **EligibilityResponse**: EDI 271 response records
- **Provider**: Healthcare provider information
- **TransactionLog**: Complete audit trail
- **AuditLog**: Change tracking

### Services

#### OCR Service
- Image preprocessing for better accuracy
- Text extraction from images and PDFs
- Intelligent parsing of insurance card data
- Confidence scoring

#### EDI Service
- EDI 270 generation (eligibility inquiry)
- EDI 271 generation (eligibility response)
- Standards-compliant formatting
- Transaction validation

### CRUD Operations

Generic CRUD base class with:
- Standard database operations (Create, Read, Update, Delete)
- Pagination support
- Error handling and logging
- Transaction management

### API Endpoints

#### Upload Endpoints
- `POST /api/v1/upload/insurance-card`: Upload and process insurance cards
- `GET /api/v1/upload/insurance-cards`: List processed cards

#### Eligibility Endpoints
- `POST /api/v1/eligibility/inquiry`: Submit EDI 270 eligibility inquiry
- `GET /api/v1/eligibility/response/{request_id}`: Get EDI 271 response
- `GET /api/v1/eligibility/requests`: List eligibility requests

#### Provider Endpoints
- `GET /api/v1/providers/`: List healthcare providers
- `POST /api/v1/providers/`: Create new provider
- `GET /api/v1/providers/{id}`: Get provider by ID
- `GET /api/v1/providers/npi/{npi}`: Get provider by NPI

#### Health Endpoints
- `GET /api/v1/health/`: Health check with dependency status

## Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/db_name

# Security
SECRET_KEY=your-secret-key

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIRECTORY=./uploads

# OCR
TESSERACT_CMD=/usr/bin/tesseract

# EDI
EDI_SUBMITTER_ID=YOUR_SUBMITTER_ID
EDI_RECEIVER_ID=YOUR_RECEIVER_ID
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_upload.py -v
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Performance and Scalability

### Database Optimization
- Proper indexing on frequently queried columns
- Connection pooling with configurable limits
- Query optimization with SQLAlchemy

### Async Processing
- Background task support for heavy operations
- Non-blocking file processing
- Async database operations where applicable

### Caching
- Redis integration for frequently accessed data
- Response caching for static lookups
- Session caching for user data

## Security Features

- Input validation with Pydantic
- SQL injection prevention through ORM
- File type and size validation
- Error handling without information leakage
- Comprehensive audit logging

## Monitoring and Logging

### Structured Logging
- JSON formatted logs for production
- Configurable log levels
- Log rotation and archival
- Request/response logging

### Health Monitoring
- Database connectivity checks
- Dependency status monitoring
- Performance metrics collection
- Error rate tracking

## Production Considerations

### Environment Setup
- Use environment-specific configuration
- Enable HTTPS with proper certificates
- Configure firewall and network security
- Set up monitoring and alerting

### Database
- Configure connection pooling
- Set up read replicas for scaling
- Implement backup and recovery procedures
- Monitor query performance

### Scaling
- Horizontal scaling with load balancers
- Container orchestration with Kubernetes
- Auto-scaling based on metrics
- CDN for static assets

## Contributing

1. Follow PEP 8 style guidelines
2. Write comprehensive tests for new features
3. Update documentation for API changes
4. Use type hints throughout the codebase
5. Follow the established project structure

## License

This project is licensed under the MIT License.
