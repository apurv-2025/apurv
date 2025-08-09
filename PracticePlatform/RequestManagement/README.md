# Practice Management - Request Management System

A full-stack application for managing appointment requests between clients and practitioners.

## Features

- **Client Portal**: Submit appointment requests
- **Practitioner Dashboard**: Review and approve/deny requests
- **Real-time Updates**: Live status updates
- **Modern UI**: Built with React and Tailwind CSS
- **RESTful API**: FastAPI backend with PostgreSQL

## Technology Stack

- **Frontend**: React 18, Tailwind CSS, Lucide React Icons
- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose

## Project Structure

```
RequestManagement/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Backend container config
│   └── .env                # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── api.js          # API integration
│   │   └── index.js        # React entry point
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container config
├── init.sql                # Database schema & sample data
├── docker-compose.yml      # Multi-container orchestration
└── README.md              # This file
```

## Quick Start with Docker

1. **Prerequisites**
   - Docker and Docker Compose installed
   - Ports 3000, 5432, and 8000 available

2. **Run the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup (Development)

### Database Setup
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Create database and run schema
psql postgres -c "CREATE DATABASE practice_management;"
psql practice_management -f init.sql
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `GET /practitioners` - List all practitioners
- `GET /clients` - List all clients
- `GET /appointment-requests` - List all appointment requests
- `POST /appointment-requests` - Create new request
- `PUT /appointment-requests/{id}` - Update request status
- `GET /appointment-requests/pending` - Get pending requests
- `GET /appointment-requests/client/{id}` - Get client's requests

## Environment Variables

### Backend (.env)
```
DB_HOST=localhost
DB_NAME=practice_management
DB_USER=postgres
DB_PASSWORD=password
DB_PORT=5432
```

## Database Schema

- **practitioners**: Healthcare providers
- **clients**: Patients/clients
- **appointment_requests**: Request submissions
- **appointments**: Approved appointments

## Development Notes

- Backend runs on port 8000
- Frontend runs on port 3000
- Database runs on port 5432
- CORS is configured for local development
- Sample data is automatically loaded