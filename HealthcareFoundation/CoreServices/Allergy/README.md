# FHIR AllergyIntolerance Microservice

A complete microservice solution for managing FHIR AllergyIntolerance resources with a Python FastAPI backend and React frontend.

## Features

### Backend (Python FastAPI)
- **Full CRUD operations** for AllergyIntolerance resources
- **FHIR-compliant schema** with proper data validation
- **PostgreSQL database** with optimized indexes
- **RESTful API** with OpenAPI documentation
- **Filtering and pagination** support
- **Health check endpoints**
- **Docker containerization**

### Frontend (React + Tailwind)
- **Modern React interface** with hooks
- **Responsive design** with Tailwind CSS
- **Complete CRUD functionality**
- **Advanced filtering** and search capabilities
- **Real-time form validation**
- **Status and criticality indicators**
- **Mobile-friendly design**

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Running the Application

1. **Clone and setup the project structure:**
```bash
mkdir fhir-allergy-service
cd fhir-allergy-service

# Create backend directory
mkdir backend
# Place main.py and requirements.txt in backend/
# Place Dockerfile in backend/

# Create frontend directory  
mkdir frontend
# Create src/ directory in frontend/
# Place AllergyManagement.jsx in frontend/src/
# Place App.js in frontend/src/
# Place index.css in frontend/src/
# Place package.json, Dockerfile, nginx.conf, tailwind.config.js in frontend/

# Place docker-compose.yml and init.sql in root directory
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Access the application:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Project Structure

```
fhir-allergy-service/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── AllergyManagement.jsx  # Main React component
│   │   ├── App.js          # React app entry
│   │   └── index.css       # Tailwind styles
│   ├── package.json        # Node dependencies
│   ├── Dockerfile          # Frontend container
│   ├── nginx.conf          # Nginx configuration
│   └── tailwind.config.js  # Tailwind configuration
├── docker-compose.yml      # Multi-container setup
├── init.sql               # Database initialization
└── README.md              # This file
```

## API Endpoints

### AllergyIntolerance Operations
- `POST /allergies` - Create new allergy
- `GET /allergies` - List allergies (with filtering)
- `GET /allergies/{id}` - Get specific allergy
- `PUT /allergies/{id}` - Update allergy
- `DELETE /allergies/{id}` - Delete allergy

### Query Parameters
- `skip` - Pagination offset
- `limit` - Results per page (max 1000)
- `patient_id` - Filter by patient
- `clinical_status` - Filter by status

### Health Check
- `GET /health` - Service health status

## Database Schema

The service implements the complete FHIR AllergyIntolerance resource schema:

### Core Fields
- `fhir_id` - Unique FHIR identifier
- `clinical_status` - active | inactive | resolved
- `verification_status` - unconfirmed | confirmed | refuted | entered-in-error
- `type` - allergy | intolerance
- `categories` - food, medication, environment, biologic
- `criticality` - low | high | unable-to-assess

### Clinical Data
- `code` - Substance/allergen (JSONB CodeableConcept)
- `patient_id` - Reference to patient
- `onset_*` - Various onset representations
- `reactions` - Reaction details (JSONB)
- `notes` - Clinical notes (JSONB)

### Audit Fields
- `created_at` - Record creation timestamp
- `updated_at` - Last modification timestamp

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it fhir-allergy-service_db_1 psql -U postgres -d fhir_db

# View tables
\dt

# Query allergies
SELECT fhir_id, clinical_status, code->>'text' as substance FROM allergy_intolerances;
```

## Configuration

### Environment Variables

**Backend:**
- `DATABASE_URL` - PostgreSQL connection string

**Frontend:**
- `REACT_APP_API_URL` - Backend API URL

### Docker Compose Override
Create `docker-compose.override.yml` for custom configurations:

```yaml
version: '3.8'
services:
  backend:
    environment:
      - DEBUG=true
  frontend:
    environment:
      - REACT_APP_API_URL=http://localhost:8000
```

## Sample Data

The service includes sample data:
- 3 patients (John Doe, Jane Smith, Bob Johnson)
- 3 allergies/intolerances (Peanuts, Penicillin, Lactose)

## Production Considerations

### Security
- Enable authentication/authorization
- Use HTTPS with proper certificates
- Implement rate limiting
- Add input sanitization
- Use environment-specific secrets

### Performance
- Add Redis caching layer
- Implement database connection pooling
- Add API response caching
- Optimize database queries with proper indexes

### Monitoring
- Add logging and metrics collection
- Implement health checks
- Set up alerts for critical errors
- Add performance monitoring

### Scalability
- Use horizontal pod autoscaling
- Implement database read replicas
- Add load balancing
- Consider microservice patterns

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
