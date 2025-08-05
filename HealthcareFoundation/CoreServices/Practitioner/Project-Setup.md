# FHIR Practitioner Management System

A complete microservices solution for managing FHIR Practitioner resources with a Python FastAPI backend and React.js frontend.

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React.js with Tailwind CSS  
- **Database**: PostgreSQL with JSONB support for FHIR resources
- **Containerization**: Docker and Docker Compose

## ⚡ Features

### Backend (FastAPI)
- ✅ Full CRUD operations for FHIR Practitioner resources
- ✅ RESTful API with automatic OpenAPI documentation
- ✅ PostgreSQL integration with asyncpg
- ✅ Pydantic models for data validation
- ✅ CORS middleware for frontend integration
- ✅ Health check endpoints
- ✅ Advanced search capabilities (by name and identifier)
- ✅ Proper error handling and HTTP status codes
- ✅ Support for complex FHIR data structures

### Frontend (React.js)
- ✅ Modern, responsive UI with Tailwind CSS
- ✅ Create/Edit forms with validation
- ✅ Support for complex FHIR data structures
- ✅ Dynamic form fields for arrays (names, contacts, addresses, qualifications)
- ✅ Real-time search functionality (name and identifier search)
- ✅ Status badges and professional information display
- ✅ Full CRUD operations through an intuitive interface

### Database Schema
- ✅ Complete FHIR Practitioner resource schema
- ✅ JSONB fields for complex nested data (identifiers, qualifications, etc.)
- ✅ Proper indexing for performance optimization
- ✅ UUID primary keys
- ✅ Audit fields (created_at, updated_at)
- ✅ Sample data for immediate testing
- ✅ Support for professional identifiers (NPI, DEA, License numbers)

## 📦 Project Structure

```
fhir-practitioner-system/
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
mkdir fhir-practitioner-system
cd fhir-practitioner-system

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
- Copy `Dockerfile` (from medication service, update ports)

**frontend/ directory:**
- Copy `package.json` (from medication service)
- Copy `tailwind.config.js`
- Copy `postcss.config.js`
- Copy `nginx.conf`
- Copy `Dockerfile` (from medication service)

**frontend/public/ directory:**
```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="FHIR Practitioner Management System" />
    <title>FHIR Practitioner Management</title>
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

### 3. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3002
- **Backend API**: http://localhost:8002
- **API Documentation**: http://localhost:8002/docs
- **Database**: localhost:5434

## 🧪 Testing the System

The database will be initialized with sample practitioners:

### Sample Practitioners:
1. **Dr. John Robert Smith, MD** - Cardiologist with NPI and DEA numbers
2. **Dr. Sarah Marie Johnson, RN, MSN** - Nurse with advanced nursing qualifications
3. **Dr. Robert James Williams, PhD, LCSW** - Clinical Social Worker/Psychologist
4. **Dr. Emily Claire Davis, PharmD** - Clinical Pharmacist

You can:
1. ✅ View practitioners in a card-based layout
2. ✅ Search practitioners by name or identifier (NPI, DEA, License)
3. ✅ Create new practitioners with multiple qualifications
4. ✅ Edit existing practitioners and their professional information
5. ✅ Manage multiple identifiers (NPI, DEA, Medical License, Tax ID)
6. ✅ Add professional qualifications with issuing institutions
7. ✅ Manage multiple contact methods and addresses
8. ✅ Set language preferences and communication details
9. ✅ Delete practitioners
10. ✅ Filter by active/inactive status

## 🔧 API Endpoints

### Practitioner Endpoints
- `GET /practitioners` - List practitioners (with filtering)
- `POST /practitioners` - Create a new practitioner
- `GET /practitioners/{id}` - Get practitioner by UUID
- `GET /practitioners/fhir/{fhir_id}` - Get practitioner by FHIR ID
- `PUT /practitioners/{id}` - Update practitioner
- `DELETE /practitioners/{id}` - Delete practitioner

### Search Endpoints
- `GET /practitioners/search/name` - Search by family name or given name
- `GET /practitioners/search/identifier` - Search by identifier value (NPI, DEA, etc.)

### Query Parameters
- `skip` - Pagination offset
- `limit` - Page size (max 100)
- `active` - Filter by active status
- `gender` - Filter by gender
- `family_name` - Search parameter for name search
- `given_name` - Search parameter for name search
- `identifier_value` - Search parameter for identifier search
- `identifier_system` - Optional system filter for identifier search

### Health Check
- `GET /health` - Service health status

## 🎯 Key FHIR Features Demonstrated

### Professional Identity Management
- ✅ **Multiple Identifiers** - NPI, DEA, Medical License, Tax ID support
- ✅ **Name Components** - Prefix (Dr.), given names, family name, suffix (MD, PhD)
- ✅ **Professional Status** - Active/inactive practitioner tracking

### Qualifications & Credentials
- ✅ **Educational Background** - Degrees, certifications with issuing institutions
- ✅ **Period Tracking** - Start and end dates for qualifications
- ✅ **Multiple Credentials** - Support for multiple degrees and certifications

### Contact & Location
- ✅ **Multiple Contact Methods** - Phone, email, fax with work/home designations
- ✅ **Multiple Addresses** - Work, home, temporary addresses
- ✅ **Communication Languages** - Multiple languages with preference indicators

### FHIR Compliance
- ✅ **CodeableConcept** structures for qualifications and identifiers
- ✅ **Complex nested arrays** for qualifications, communication, contacts
- ✅ **Reference handling** for organizational relationships
- ✅ **Enumerated values** for gender, contact types, address types
- ✅ **Date handling** for birth dates and qualification periods

## 🔍 Advanced Search Features

### Name Search
```
GET /practitioners/search/name?family_name=Smith
GET /practitioners/search/name?given_name=John&family_name=Smith
```

### Identifier Search
```
GET /practitioners/search/identifier?identifier_value=1234567890
GET /practitioners/search/identifier?identifier_value=BS1234567&identifier_system=DEA
```

### Filtering
```
GET /practitioners?active=true&gender=female&limit=20
```

## 🛠️ Development

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
docker exec -it fhir_practitioner_postgres psql -U practitioner_user -d fhir_practitioner_db

# View sample data
SELECT fhir_id, family_name, given_names, identifiers->0->>'value' as npi FROM practitioners;
```

## 🔐 Production Considerations

### Security
- Change default database credentials
- Implement authentication/authorization for practitioner access
- Enable HTTPS with reverse proxy
- Set up proper logging and monitoring
- Implement role-based access control

### Compliance
- **HIPAA Compliance** - Ensure PHI protection for practitioner data
- **Professional Licensing** - Validate NPI and license numbers
- **Credential Verification** - Implement verification workflows
- **Audit Trails** - Track all changes to practitioner records

### Scaling
- Use managed database service (AWS RDS, Google Cloud SQL)
- Implement horizontal scaling with load balancers
- Add Redis for caching frequently accessed practitioner data
- Use container orchestration (Kubernetes)

## 📊 Sample Data Features

The system includes realistic sample practitioners representing different healthcare roles:

- **Physicians** with medical school credentials and board certifications
- **Nurses** with BSN/MSN degrees and nursing licenses
- **Mental Health Professionals** with PhD and clinical licenses
- **Pharmacists** with PharmD and specialty certifications

Each practitioner includes:
- ✅ **Professional identifiers** (NPI, DEA, state licenses)
- ✅ **Educational credentials** with issuing institutions and dates
- ✅ **Contact information** for work settings
- ✅ **Language capabilities** for patient communication
- ✅ **Addresses** for practice locations

## 🧩 Integration Points

### Healthcare Systems
- **EHR Integration** - Connect with electronic health record systems
- **Credentialing Systems** - Integrate with hospital credentialing databases
- **Scheduling Systems** - Link to appointment and scheduling platforms
- **Billing Systems** - Connect with practice management and billing

### Regulatory
- **NPI Registry** - Validate against NPPES database
- **License Verification** - Check state medical board databases
- **DEA Verification** - Validate controlled substance prescribing authority
- **Continuing Education** - Track CME and license renewal requirements

This practitioner management system provides a comprehensive foundation for healthcare workforce management with full FHIR compliance and modern user experience design.
