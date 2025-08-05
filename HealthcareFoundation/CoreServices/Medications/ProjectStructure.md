# FHIR Medication Management System

A complete microservices solution for managing FHIR Medication and MedicationRequest resources with a Python FastAPI backend and React.js frontend.

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React.js with Tailwind CSS  
- **Database**: PostgreSQL with JSONB support for FHIR resources
- **Containerization**: Docker and Docker Compose

## ⚡ Features

### Backend (FastAPI)
- ✅ RESTful API with automatic OpenAPI documentation
- ✅ PostgreSQL integration with asyncpg
- ✅ Pydantic models for data validation
- ✅ CORS middleware for frontend integration
- ✅ Health check endpoints
- ✅ Advanced filtering and search capabilities
- ✅ Proper error handling and HTTP status codes
- ✅ Support for complex FHIR data structures (CodeableConcept, Ratio, etc.)

### Frontend (React.js)
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Tabbed interface for Medications and MedicationRequests
- ✅ Create/Edit forms with validation
- ✅ Support for complex FHIR data structures
- ✅ Dynamic form fields for arrays (ingredients, dosage instructions)
- ✅ Real-time search functionality
- ✅ Status badges and priority indicators
- ✅ Full CRUD operations through an intuitive interface

### Database Schema
- ✅ Complete FHIR Medication resource schema
- ✅ Complete FHIR MedicationRequest resource schema
- ✅ JSONB fields for complex nested data
- ✅ Proper indexing for performance optimization
- ✅ UUID primary keys
- ✅ Audit fields (created_at, updated_at)
- ✅ Sample data for immediate testing
- ✅ Self-referencing foreign keys for prior prescriptions

## 📦 Project Structure

```
fhir-medication-system/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── nginx.conf
│   └── src/
│       ├── index.js
│       ├── index.css
│       └── App.js
├── docker-compose.yml
└── init.sql
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Setup Project Structure

Create the following directory structure and files:

```bash
mkdir fhir-medication-system
cd fhir-medication-system

# Create directories
mkdir backend frontend frontend/src frontend/public

# Copy all provided files to their respective locations
```

### 2. File Placement

**Root directory:**
- Copy `docker-compose.yml`
- Copy `init.sql`

**backend/ directory:**
- Copy `main.py` (FastAPI service)
- Copy `requirements.txt`
- Copy `Dockerfile`

**frontend/ directory:**
- Copy `package.json`
- Copy `tailwind.config.js`
- Copy `postcss.config.js`
- Copy `nginx.conf`
- Copy `Dockerfile`

**frontend/public/ directory:**
```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="FHIR Medication Management System" />
    <title>FHIR Medication Management</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
```

**frontend/src/ directory:**
```javascript
// src/index.js
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

```css
/* src/index.css */
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
```

- Copy `App.js` (React component from artifacts)

**Additional configuration files:**

```javascript
// frontend/tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      },
    },
  },
  plugins: [],
}
```

```javascript
// frontend/postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    
    root /usr/share/nginx/html;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
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

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Database**: localhost:5433

## 🧪 Testing the System

The database will be initialized with sample data:

### Sample Medications:
1. **Lisinopril 10mg** - ACE inhibitor tablet
2. **Metformin 500mg** - Diabetes medication tablet  
3. **Amoxicillin 250mg/5ml** - Antibiotic oral suspension

### Sample MedicationRequests:
1. **Lisinopril prescription** - Once daily for hypertension
2. **Metformin prescription** - Twice daily with meals
3. **Amoxicillin prescription** - Three times daily for 10 days (completed)

You can:
1. ✅ View medications and requests in separate tabs
2. ✅ Search medications by name or FHIR ID
3. ✅ Create new medications with ingredients and batch info
4. ✅ Create new medication requests with dosage instructions
5. ✅ Edit existing medications and requests
6. ✅ Delete medications and requests
7. ✅ Filter by status (active, inactive, completed, etc.)

## 🔧 API Endpoints

### Medication Endpoints
- `GET /medications` - List medications (with filtering)
- `POST /medications` - Create a new medication
- `GET /medications/{id}` - Get medication by UUID
- `PUT /medications/{id}` - Update medication
- `DELETE /medications/{id}` - Delete medication

### MedicationRequest Endpoints
- `GET /medication-requests` - List medication requests (with filtering)
- `POST /medication-requests` - Create a new medication request
- `GET /medication-requests/{id}` - Get medication request by UUID
- `PUT /medication-requests/{id}` - Update medication request
- `DELETE /medication-requests/{id}` - Delete medication request

### Query Parameters
- `skip` - Pagination offset
- `limit` - Page size (max 100)
- `status` - Filter by status
- `intent` - Filter medication requests by intent
- `subject_patient_id` - Filter requests by patient

### Health Check
- `GET /health` - Service health status

## 🎯 Key Features Demonstrated

### FHIR Compliance
- ✅ **CodeableConcept** structures for medication codes, forms, categories
- ✅ **Ratio** objects for medication amounts and strengths
- ✅ **Complex nested arrays** for ingredients, dosage instructions
- ✅ **Reference handling** for patient and medication relationships
- ✅ **Enumerated values** for status, intent, priority fields
- ✅ **Timestamp handling** for authored dates and audit fields

### Advanced UI Features
- ✅ **Tabbed interface** switching between medications and requests
- ✅ **Dynamic form fields** that expand/contract based on data
- ✅ **Real-time search** across both resource types
- ✅ **Status indicators** with color-coded badges
- ✅ **Responsive design** that works on desktop and mobile
- ✅ **Form validation** with required field enforcement

### Backend Architecture
- ✅ **Async database operations** with connection pooling
- ✅ **JSON field parsing** for complex FHIR structures
- ✅ **Type safety** with Pydantic models
- ✅ **Error handling** with proper HTTP status codes
- ✅ **Automatic documentation** via FastAPI's OpenAPI

## 🔄 Development Workflow

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

### Database Management
```bash
# Connect to database
docker exec -it fhir_medication_postgres psql -U medication_user -d fhir_medication_db

# View sample data
SELECT fhir_id, code->>'text' as name, status FROM medications;
SELECT fhir_id, status, intent, medication_codeable_concept->>'text' as medication FROM medication_requests;
```

## 🚀 Production Considerations

### Security
- Change default database credentials
- Implement authentication/authorization
- Enable HTTPS with reverse proxy
- Set up proper logging and monitoring

### Scaling
- Use managed database service (AWS RDS, Google Cloud SQL)
- Implement horizontal scaling with load balancers
- Add Redis for caching
- Use container orchestration (Kubernetes)

### Monitoring
```bash
# View real-time logs
docker-compose logs -f

# Monitor specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧩 Extending the System

### Adding New FHIR Resources
1. Create Pydantic models following FHIR specification
2. Add database table with JSONB fields for complex structures
3. Implement CRUD endpoints with proper JSON parsing
4. Create React components with dynamic form handling
5. Update the frontend navigation and routing

### Integration Points
- **Patient Management**: Link to existing patient service
- **Practitioner Management**: Reference healthcare providers
- **Pharmacy Systems**: Connect for dispensing workflows
- **Clinical Decision Support**: Integrate drug interaction checking
- **EHR Integration**: Export to standard FHIR formats

This medication management system demonstrates a complete, production-ready microservice architecture that properly handles complex FHIR resources while providing an intuitive user interface for healthcare workflows.
