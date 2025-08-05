# Patient Management System

A complete microservices solution for managing FHIR Patient resources with a Python FastAPI backend and React.js frontend.

## Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React.js with Tailwind CSS
- **Database**: PostgreSQL with JSONB support for FHIR resources
- **Containerization**: Docker and Docker Compose

## Features

### Backend (FastAPI)
- ✅ Full CRUD operations for FHIR Patient resources
- ✅ RESTful API with automatic OpenAPI documentation
- ✅ PostgreSQL integration with asyncpg
- ✅ Pydantic models for data validation
- ✅ CORS middleware for frontend integration
- ✅ Health check endpoints
- ✅ Advanced search capabilities
- ✅ Proper error handling and HTTP status codes

### Frontend (React.js)
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Patient list view with search functionality
- ✅ Create/Edit patient forms with validation
- ✅ Support for complex FHIR data structures
- ✅ Dynamic form fields for arrays (names, contacts, addresses)
- ✅ Patient status management
- ✅ Real-time API integration

### Database Schema
- ✅ Complete FHIR Patient resource schema
- ✅ JSONB fields for complex nested data
- ✅ Proper indexing for performance
- ✅ UUID primary keys
- ✅ Audit fields (created_at, updated_at)
- ✅ Sample data for testing

## Project Structure

```
fhir-patient-system/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── nginx.conf
│   └── src/
│       └── App.js
├── docker-compose.yml
└── init.sql
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Setup Project Structure

Create the following directory structure and files:

```bash
mkdir fhir-patient-system
cd fhir-patient-system

# Create directories
mkdir backend frontend

# Backend files
mkdir backend
# Copy the Python code to backend/main.py
# Copy requirements.txt to backend/
# Copy Dockerfile to backend/

# Frontend files  
mkdir frontend/src frontend/public
# Copy the React component to frontend/src/App.js
# Copy package.json to frontend/
# Copy Dockerfile to frontend/
# Copy nginx.conf to frontend/
# Copy tailwind.config.js to frontend/

# Root files
# Copy docker-compose.yml to root
# Copy init.sql to root
```

### 2. Frontend Setup Files

Create these additional files in the frontend directory:

**frontend/public/index.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="FHIR Patient Management System" />
    <title>FHIR Patient Management</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
```

**frontend/src/index.js**:
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**frontend/src/index.css**:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
```

**frontend/postcss.config.js**:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 3. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

### 5. Test the System

The database will be initialized with sample patient data. You can:

1. View the patient list in the frontend
2. Search for patients by family name
3. Create new patients
4. Edit existing patients
5. Delete patients
6. Test the API directly at http://localhost:8000/docs

## API Endpoints

### Core CRUD Operations
- `GET /patients` - List all patients (with filtering)
- `POST /patients` - Create a new patient
- `GET /patients/{id}` - Get patient by UUID
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient

### Additional Endpoints
- `GET /patients/fhir/{fhir_id}` - Get patient by FHIR ID
- `GET /patients/search/name` - Search patients by name
- `GET /health` - Health check

### Query Parameters
- `skip` - Pagination offset
- `limit` - Page size (max 100)
- `active` - Filter by active status
- `gender` - Filter by gender
- `family_name` - Search by family name
- `given_name` - Search by given name

## Database Schema Details

The patients table supports the full FHIR Patient resource specification:

### Core Fields
- `id` - UUID primary key
- `fhir_id` - FHIR resource identifier (unique)
- `active` - Boolean status flag

### Demographics
- `family_name` - Last name
- `given_names` - Array of first/middle names
- `prefix` / `suffix` - Name prefixes/suffixes
- `gender` - Enumerated gender values
- `birth_date` - Date of birth
- `deceased_boolean` / `deceased_date_time` - Death status

### Contact Information
- `telecom` - JSONB array of phone/email contacts
- `addresses` - JSONB array of addresses

### Medical Information
- `identifiers` - JSONB array of medical record numbers, SSN, etc.
- `marital_status_code` / `marital_status_display` - Marital status
- `communication` - JSONB array of language preferences
- `general_practitioner` - JSONB array of GP references
- `managing_organization` - UUID reference
- `photo` - JSONB array of patient photos
- `links` - JSONB array of linked patient records

### Metadata
- `fhir_resource` - Complete FHIR resource as JSONB
- `created_at` / `updated_at` - Audit timestamps

## Development

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run locally (ensure PostgreSQL is running)
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
docker exec -it fhir_postgres psql -U fhir_user -d fhir_db

# View patient data
SELECT id, fhir_id, family_name, given_names, gender FROM patients;

# Reset database
docker-compose down -v
docker-compose up --build
```

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- Default: `postgresql://fhir_user:fhir_password@postgres:5432/fhir_db`

### Frontend
- `REACT_APP_API_URL` - Backend API URL
- Default: `http://localhost:8000`

## Production Deployment

### Environment-Specific Configurations

**Production docker-compose.override.yml**:
```yaml
version: '3.8'
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - /var/lib/postgresql/data:/var/lib/postgresql/data
  
  backend:
    environment:
      DATABASE_URL: postgresql://fhir_user:${DB_PASSWORD}@postgres:5432/fhir_db
    restart: unless-stopped
  
  frontend:
    restart: unless-stopped
```

### Security Considerations
- Change default database credentials
- Use environment variables for secrets
- Enable HTTPS with reverse proxy (nginx/traefik)
- Implement authentication/authorization
- Set up proper logging and monitoring
- Configure backup strategies

### Scaling
- Use managed database service (AWS RDS, Google Cloud SQL)
- Implement horizontal scaling with load balancers
- Add Redis for caching
- Use container orchestration (Kubernetes)

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps
   
   # View logs
   docker-compose logs postgres
   ```

2. **CORS Errors**
   - Ensure backend CORS middleware is configured
   - Check frontend API URL configuration

3. **Build Failures**
   ```bash
   # Clean rebuild
   docker-compose down -v
   docker system prune -f
   docker-compose up --build
   ```

4. **Port Conflicts**
   - Change ports in docker-compose.yml if needed
   - Check for running services: `netstat -tulpn`

### Monitoring

View real-time logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Performance Optimization

1. **Database Indexing**
   - Indexes are already created for common queries
   - Monitor slow queries with pg_stat_statements

2. **API Optimization**
   - Implement response caching
   - Add pagination for large datasets
   - Use database connection pooling

3. **Frontend Optimization**
   - Implement virtual scrolling for large lists
   - Add client-side caching
   - Optimize bundle size

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
