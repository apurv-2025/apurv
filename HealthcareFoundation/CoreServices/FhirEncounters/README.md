# FHIR Management System

A complete microservice application for managing FHIR (Fast Healthcare Interoperability Resources) data with a Python FastAPI backend and React frontend.

## Features

- **CRUD Operations** for FHIR resources:
  - Encounters
  - Observations
  - Conditions
- **RESTful API** with FastAPI
- **Modern React Frontend** with Tailwind CSS
- **PostgreSQL Database** with JSONB support
- **Docker Containerization**
- **Real-time Data Management**

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   FastAPI       │    │   PostgreSQL    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Project Structure

```
fhir-microservice/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       └── index.css
├── docker-compose.yml
├── init.sql
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fhir-microservice
   ```

2. **Create the project structure:**
   ```bash
   mkdir -p backend frontend/src frontend/public
   ```

3. **Copy the files to their respective directories:**
   - Copy `main.py` and `requirements.txt` to `backend/`
   - Copy React files to `frontend/src/` and `frontend/public/`
   - Copy `package.json` and `tailwind.config.js` to `frontend/`
   - Copy Dockerfiles to their respective directories

4. **Start the application:**
   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

### Encounters
- `GET /encounters/` - List all encounters
- `POST /encounters/` - Create new encounter
- `GET /encounters/{id}` - Get specific encounter
- `PUT /encounters/{id}` - Update encounter
- `DELETE /encounters/{id}` - Delete encounter

### Observations
- `GET /observations/` - List all observations
- `POST /observations/` - Create new observation
- `GET /observations/{id}` - Get specific observation
- `PUT /observations/{id}` - Update observation
- `DELETE /observations/{id}` - Delete observation

### Conditions
- `GET /conditions/` - List all conditions
- `POST /conditions/` - Create new condition
- `GET /conditions/{id}` - Get specific condition
- `PUT /conditions/{id}` - Update condition
- `DELETE /conditions/{id}` - Delete condition

## Database Schema

The application uses the provided FHIR-compliant PostgreSQL schema with:

- **encounters** table for patient encounters
- **observations** table for clinical observations
- **conditions** table for patient conditions
- **patients** and **organizations** tables for references

## Development

### Backend Development

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Development

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the React development server:**
   ```bash
   npm start
   ```

### Database Setup

The database is automatically initialized with the provided schema and sample data when using Docker Compose.

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REACT_APP_API_URL` - Backend API URL for frontend

## Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## Features in Detail

### Backend (FastAPI)
- **SQLAlchemy ORM** with PostgreSQL
- **Pydantic models** for request/response validation
- **CORS middleware** for frontend integration
- **Health check endpoint**
- **Comprehensive error handling**

### Frontend (React)
- **Modern React hooks**
- **Tailwind CSS** for styling
- **Lucide React** icons
- **Responsive design**
- **Modal forms** for CRUD operations
- **Search functionality**
- **Status badges** with color coding

### Database
- **JSONB columns** for FHIR complex data types
- **UUID primary keys**
- **Proper indexes** for performance
- **Foreign key constraints**
- **Check constraints** for data validation

## Sample Data

The application includes sample patients and organizations for testing:

- **Patients:** John Doe, Jane Smith, Bob Johnson
- **Organizations:** General Hospital, City Clinic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the development team.
