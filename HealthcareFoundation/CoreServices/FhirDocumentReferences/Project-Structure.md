# FHIR Document Management System

A complete microservice solution for managing FHIR DocumentReference, Questionnaire, and QuestionnaireResponse resources with a modern React frontend.

## Features

- **FastAPI Backend** with full CRUD operations
- **React Frontend** with Tailwind CSS styling
- **PostgreSQL Database** with FHIR-compliant schema
- **Docker Containerization** for easy deployment
- **RESTful API** with automatic documentation

## Project Structure

```
fhir-system/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── init.sql
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone and setup the project structure:**

```bash
# Create project directory
mkdir fhir-system && cd fhir-system

# Create backend directory
mkdir backend
```

2. **Create backend files:**
   - Copy the FastAPI code to `backend/main.py`
   - Copy requirements to `backend/requirements.txt`
   - Copy backend Dockerfile to `backend/Dockerfile`

3. **Create frontend directory and files:**

```bash
# Create frontend directory structure
mkdir -p frontend/src frontend/public

# Create React app structure
cd frontend
npm init -y
```

   - Copy the React component to `frontend/src/App.js`
   - Copy index.js to `frontend/src/index.js`
   - Copy index.css to `frontend/src/index.css`
   - Copy package.json content
   - Copy tailwind.config.js
   - Copy nginx.conf
   - Copy frontend Dockerfile

4. **Add the remaining files:**
   - Copy docker-compose.yml to root
   - Copy init.sql to root

5. **Start the application:**

```bash
# From the root directory
docker-compose up --build
```

### Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Database:** localhost:5432 (user: user, password: password, db: fhir_db)

## API Endpoints

### Document References
- `POST /document-references/` - Create document reference
- `GET /document-references/` - List document references
- `GET /document-references/{id}` - Get specific document reference
- `PUT /document-references/{id}` - Update document reference
- `DELETE /document-references/{id}` - Delete document reference

### Questionnaires
- `POST /questionnaires/` - Create questionnaire
- `GET /questionnaires/` - List questionnaires
- `GET /questionnaires/{id}` - Get specific questionnaire
- `DELETE /questionnaires/{id}` - Delete questionnaire

### Questionnaire Responses
- `POST /questionnaire-responses/` - Create response
- `GET /questionnaire-responses/` - List responses
- `GET /questionnaire-responses/{id}` - Get specific response
- `DELETE /questionnaire-responses/{id}` - Delete response

## Frontend Features

- **Modern UI** with Tailwind CSS
- **Responsive Design** for desktop and mobile
- **Real-time Search** across all resources
- **Modal Forms** for creating new resources
- **Status Indicators** with color-coded badges
- **Detailed Views** with JSON formatting
- **Delete Confirmation** dialogs

## Database Schema

The system implements FHIR R4 compliant tables:

- `document_references` - For storing document metadata
- `questionnaires` - For form definitions
- `questionnaire_responses` - For form submissions
- Supporting tables: `patients`, `practitioners`, `organizations`, `encounters`

## Development

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

### Database Management

```bash
# Connect to database
docker exec -it fhir-system_db_1 psql -U user -d fhir_db

# View tables
\dt

# Query data
SELECT * FROM document_references;
```

## Configuration

### Environment Variables

Backend environment variables:
- `DATABASE_URL` - PostgreSQL connection string

### Docker Compose Override

Create `docker-compose.override.yml` for local customizations:

```yaml
version: '3.8'
services:
  backend:
    environment:
      - DEBUG=true
    volumes:
      - ./backend:/app
  frontend:
    volumes:
      - ./frontend:/app
```

## Security Considerations

- Add authentication middleware
- Implement input validation
- Use environment variables for secrets
- Enable HTTPS in production
- Add rate limiting
- Implement proper CORS policies

## Production Deployment

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml fhir-stack
```

### Using Kubernetes

```bash
# Create namespace
kubectl create namespace fhir-system

# Apply configurations
kubectl apply -f k8s/
```

### Environment-specific Configurations

Create separate compose files for different environments:

- `docker-compose.dev.yml` - Development
- `docker-compose.staging.yml` - Staging  
- `docker-compose.prod.yml` - Production

### Health Checks

The system includes health checks for:
- Database connectivity
- API responsiveness
- Frontend availability

### Monitoring

Consider adding:
- Application metrics (Prometheus)
- Log aggregation (ELK stack)
- Error tracking (Sentry)
- Performance monitoring (New Relic)

## Testing

### Backend Testing

```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

### Integration Testing

```bash
# Start services
docker-compose up -d

# Run integration tests
pytest tests/integration/
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Verify database is running
   docker-compose ps
   ```

2. **Frontend Build Issues**
   ```bash
   # Clear node modules and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **API CORS Issues**
   - Verify CORS settings in FastAPI
   - Check frontend API base URL
   - Ensure proper headers are set

4. **Docker Issues**
   ```bash
   # Clean up containers and volumes
   docker-compose down -v
   docker system prune -a
   
   # Rebuild from scratch
   docker-compose up --build
   ```

### Performance Optimization

1. **Database Optimization**
   - Add appropriate indexes
   - Use connection pooling
   - Implement query optimization

2. **API Optimization**
   - Add caching layers (Redis)
   - Implement pagination
   - Use async operations

3. **Frontend Optimization**
   - Implement lazy loading
   - Add service worker for caching
   - Optimize bundle size

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **JavaScript**: Use ESLint and Prettier
- **SQL**: Use consistent naming conventions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation at `/docs`
- Review the API documentation at `http://localhost:8000/docs`

## Changelog

### v1.0.0
- Initial release
- Basic CRUD operations for all FHIR resources
- React frontend with Tailwind CSS
- Docker containerization
- PostgreSQL database with FHIR schema

### Future Enhancements

- [ ] Authentication and authorization
- [ ] FHIR Bundle support
- [ ] Advanced search capabilities
- [ ] Audit logging
- [ ] Data validation
- [ ] Export functionality
- [ ] Mobile app support
- [ ] Real-time notifications
