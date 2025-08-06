# Medical Codes Lookup Application

A comprehensive full-stack application for medical billing code lookup supporting CPT, ICD-10, HCPCS, and Modifier codes.

## Features

- **Comprehensive Code Coverage**: CPT (Categories I, II, III), ICD-10, HCPCS Level I & II, and Modifiers
- **Advanced Search**: Search by code number or description with filters
- **Real-time Results**: Fast, indexed database queries
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Copy Functionality**: One-click copying of codes for billing systems
- **Database Statistics**: Overview of available codes and categories

## Technology Stack

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **PostgreSQL**: Robust relational database with full-text search
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: Modern JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful, customizable icons

## Project Structure

```
MedicalCodes/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic response schemas
│   │   ├── database.py          # Database configuration
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── search.py        # Search endpoints
│   │       ├── codes.py         # Individual code lookup endpoints
│   │       └── utils.py         # Categories and stats endpoints
│   ├── requirements.txt         # Python dependencies
│   ├── seed_data.py            # Database seeding script
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── index.js            # React entry point
│   │   ├── index.css           # Tailwind CSS imports
│   │   ├── App.js              # Main React component
│   │   └── components/
│   │       └── MedicalCodesApp.jsx  # Main application component
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── package.json            # Node.js dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── postcss.config.js       # PostCSS configuration
│   └── Dockerfile
├── database/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 001_initial_schema.py  # Database schema migration
│   └── init_db.py              # Database initialization script
├── docker-compose.yml          # Docker orchestration
└── README.md
```

## Quick Start with Docker

The easiest way to run the application is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd MedicalCodes

# Start all services
docker-compose up -d

# The application will be available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## Manual Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb medical_codes

# Or using psql
psql -U postgres
CREATE DATABASE medical_codes;
\q
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://medicalcodes:secure_password_123@localhost:5432/medical_codes"
# On Windows:
# set DATABASE_URL=postgresql://medicalcodes:secure_password_123@localhost:5432/medical_codes

# Initialize database (run from project root)
cd ..
python database/init_db.py

# Start the FastAPI server
cd backend
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Search Endpoints
- `GET /api/search` - Search across all code types
- `GET /api/cpt/{code}` - Get specific CPT code
- `GET /api/icd10/{code}` - Get specific ICD-10 code
- `GET /api/hcpcs/{code}` - Get specific HCPCS code
- `GET /api/modifier/{modifier}` - Get specific modifier code

### Utility Endpoints
- `GET /api/categories` - Get all available categories
- `GET /api/stats` - Get database statistics

### Search Parameters
- `query` (required): Search term
- `code_type` (optional): Filter by cpt, icd10, hcpcs, or modifier
- `category` (optional): Filter by category
- `limit` (optional): Max results per code type (default: 50)

## Database Schema

### CPT Codes Table
- Primary fields: code, description, category, section
- Supports Category I, II, and III codes
- Indexed for fast search

### ICD-10 Codes Table
- Primary fields: code, description, code_type, chapter
- Supports both diagnosis and procedure codes
- Billable flag for insurance purposes

### HCPCS Codes Table
- Primary fields: code, description, level, category
- Supports Level I (CPT) and Level II codes
- Coverage status information

### Modifier Codes Table
- Primary fields: modifier, description, category
- Applies-to field for usage guidance

## Development

### Backend Development

The backend uses a modular structure:

- **Models** (`app/models.py`): SQLAlchemy database models
- **Schemas** (`app/schemas.py`): Pydantic response models
- **Routers** (`app/routers/`): API endpoint handlers
- **Database** (`app/database.py`): Database configuration

### Frontend Development

The frontend is a React application with:

- **Components** (`src/components/`): Reusable React components
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icon library

### Database Migrations

To add new database migrations:

1. Create a new file in `database/migrations/`
2. Follow the naming convention: `XXX_description.py`
3. Update the `init_db.py` script to include the new migration

## Data Sources and Compliance

This application structure supports importing official medical codes from:
- **CPT Codes**: American Medical Association (AMA)
- **ICD-10 Codes**: Centers for Medicare & Medicaid Services (CMS)
- **HCPCS Codes**: CMS Healthcare Common Procedure Coding System
- **Modifiers**: CMS and AMA modifier guidelines

## Adding Real Data

The seed script includes sample data for development. For production use:

1. **CPT Codes**: Purchase from AMA or use authorized distributor
2. **ICD-10 Codes**: Download from CMS website (free)
3. **HCPCS Codes**: Download from CMS website (free)
4. **Regular Updates**: Implement quarterly/annual update processes

## Performance Optimization

- Database indexes on commonly searched fields
- Connection pooling for database efficiency
- Pagination for large result sets
- Caching for frequently accessed categories

## Security Considerations

- Input validation and sanitization
- SQL injection protection via ORM
- CORS configuration for cross-origin requests
- Rate limiting for API endpoints (recommended for production)

## Deployment

### Backend Deployment
- Use production WSGI server (Gunicorn)
- Configure environment variables
- Set up database migrations
- Enable HTTPS

### Frontend Deployment
- Build optimized production bundle: `npm run build`
- Deploy to CDN or static hosting service
- Configure API endpoint URLs

## Contributing

1. Follow existing code style and conventions
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure database migrations are backward compatible

## License

This application structure is provided for educational and development purposes. Medical code data requires proper licensing from respective organizations (AMA, CMS) for production use.

## Support

For technical issues or questions about implementation, please refer to:
- FastAPI documentation: https://fastapi.tiangolo.com/
- React documentation: https://reactjs.org/
- Tailwind CSS documentation: https://tailwindcss.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/
