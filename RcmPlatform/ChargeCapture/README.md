# README.md
# Charge Capture System

A comprehensive charge capture system for healthcare practices built with FastAPI and React.

## Features

- **Specialty-Agnostic Design**: Configurable for different medical specialties
- **Real-time Validation**: CPT/ICD code validation with business rules
- **Template System**: Customizable charge templates per specialty/provider
- **Integration Ready**: Designed to integrate with existing EHR and billing systems
- **Mobile-Friendly**: Responsive design for point-of-care entry
- **Comprehensive Reporting**: Charge capture metrics and analytics

## Architecture

### Backend (FastAPI)
- **Models**: SQLAlchemy models for charges, templates, validation rules
- **Services**: Business logic layer with validation and reporting
- **API**: RESTful endpoints with comprehensive error handling
- **Database**: PostgreSQL with proper indexing for performance

### Frontend (React)
- **Components**: Modular React components with Tailwind CSS
- **State Management**: React hooks for local state
- **Code Search**: Real-time CPT/ICD code lookup
- **Validation**: Client-side and server-side validation
- **Templates**: Dynamic template selection and application

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Using Docker (Recommended)

1. Clone the repository
```bash
git clone <repository-url>
cd charge-capture-system
```

2. Start services with Docker Compose
```bash
docker-compose up -d
```

3. Initialize the database
```bash
docker-compose exec backend python database.py
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Initialize database
```bash
python database.py
```

5. Run the backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Navigate to frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm start
```

## API Documentation

### Key Endpoints

#### Charges
- `POST /charges` - Create a new charge
- `GET /charges/{charge_id}` - Get charge by ID
- `PUT /charges/{charge_id}` - Update charge
- `GET /charges` - Search charges with filters
- `POST /charges/validate` - Validate charge data
- `POST /charges/batch` - Create multiple charges

#### Templates
- `POST /templates` - Create charge template
- `GET /templates` - Get templates for provider/specialty
- `PUT /templates/{template_id}` - Update template

#### Reporting
- `GET /reports/charge-metrics` - Get charge capture metrics
- `GET /reports/provider-metrics` - Get provider-specific metrics
- `GET /encounters/without-charges` - Find missed charges

#### Code Lookup
- `GET /codes/cpt/search` - Search CPT codes
- `GET /codes/icd/search` - Search ICD codes
- `GET /codes/favorites/{provider_id}` - Get frequently used codes

## Database Schema

### Core Tables
- **providers** - Healthcare providers
- **patients** - Patient information
- **encounters** - Patient visits/encounters
- **charges** - Captured charges
- **charge_templates** - Specialty-specific templates
- **charge_validation_rules** - Business validation rules

### Key Relationships
- Charges belong to encounters, patients, and providers
- Templates can be provider-specific or system-wide
- Validation rules can be specialty or payer-specific

## Integration Points

### Medical Code Service Integration
The system is designed to integrate with your existing Medical Code Service:

```python
# In services.py
class ChargeService:
    def __init__(self, db: Session, medical_code_service=None):
        self.medical_code_service = medical_code_service
        
    def validate_charge(self, charge_data):
        # Validates against your code service
        if self.medical_code_service:
            valid_cpt = self.medical_code_service.validate_cpt_code(charge_data.cpt_code)
            valid_icd = self.medical_code_service.validate_icd_code(charge_data.icd_code)
```

### EHR Integration
- Pull encounter data from EHR
- Sync diagnoses and procedures
- Push charges back to EHR

### Billing System Integration
- Submit validated charges to billing
- Track claim status
- Handle rejections and resubmissions

## Configuration

### Specialty Templates
Templates can be configured per specialty with common code combinations:

```json
{
  "name": "Common Office Visits",
  "specialty": "Internal Medicine",
  "codes": [
    {
      "name": "Level 3 Established Visit",
      "cpt": "99213",
      "icd_options": ["Z00.00", "I10", "E11.9"],
      "default_units": 1
    }
  ]
}
```

### Validation Rules
Business rules can be configured to ensure compliance:

```json
{
  "rule_name": "Prevent High Level Visits for Routine Exams",
  "rule_type": "code_combination",
  "rule_config": {
    "cpt_codes": ["99215", "99205"],
    "prohibited_icd_codes": ["Z00.00", "Z00.01"],
    "severity": "warning"
  }
}
```

## Performance Considerations

- Database indexes on frequently queried fields
- API response caching for code lookups
- Pagination for large result sets
- Async processing for batch operations
- Database connection pooling

## Security

- HIPAA-compliant data handling
- Role-based access control
- Audit logging for all changes
- Secure API endpoints
- Data encryption in transit and at rest

## Testing

### Backend Tests
```bash
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Production Checklist
- [ ] Set production environment variables
- [ ] Configure SSL certificates
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Run security scans
- [ ] Performance testing
- [ ] Disaster recovery plan

### Environment Variables
```bash
# Production settings
API_DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-db:5432/charge_capture_db
SECRET_KEY=your-production-secret-key
LOG_LEVEL=WARNING
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact [your-support-email] or create an issue in the repository.
