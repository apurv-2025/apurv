# Healthcare Patient Portal

A comprehensive healthcare patient portal built with React, FastAPI, and PostgreSQL. This application provides patients with secure access to their health information, appointments, medications, lab results, and communication with healthcare providers.

## 🚀 Features

- **Patient Dashboard**: Overview of appointments, medications, and health data
- **Appointment Management**: Schedule, view, and manage appointments
- **Medication Tracking**: View current medications and request refills
- **Lab Results**: Access and download lab test results
- **Secure Messaging**: Communicate with healthcare providers
- **Profile Management**: Update personal and insurance information
- **Responsive Design**: Modern UI that works on desktop and mobile

## 🏗️ Project Structure

```
PatientPortal/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic data validation schemas
│   │   ├── crud/          # Database CRUD operations
│   │   ├── routers/       # API route handlers
│   │   ├── auth.py        # Authentication utilities
│   │   ├── config.py      # Configuration settings
│   │   ├── database.py    # Database connection
│   │   ├── dependencies.py # FastAPI dependencies
│   │   └── main.py        # FastAPI application entry point
│   ├── alembic/           # Database migrations
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/              # React Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service functions
│   │   └── utils/         # Utility functions
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container configuration
├── database/              # Database initialization
│   └── init.sql          # Database schema and sample data
└── docker-compose.yml     # Multi-container orchestration
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust, open-source database
- **Alembic**: Database migration tool
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations
- **bcrypt**: Password hashing

### Frontend
- **React 18**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful & consistent icon toolkit
- **React Router**: Declarative routing for React
- **Axios**: Promise-based HTTP client

### DevOps
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker applications

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository:**
```bash
git clone <repository-url>
cd PatientPortal
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
createdb healthcare_portal
psql healthcare_portal < ../database/init.sql

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### User Management
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile

### Appointments
- `GET /appointments` - Get user appointments
- `POST /appointments` - Create new appointment
- `PUT /appointments/{id}` - Update appointment

### Medications
- `GET /medications` - Get user medications
- `POST /medications/{id}/refill` - Request medication refill

### Lab Results
- `GET /lab-results` - Get user lab results

### Messages
- `GET /messages` - Get user messages
- `PUT /messages/{id}/read` - Mark message as read

## 🗄️ Database Schema

The application uses PostgreSQL with the following main tables:

- **users** - Patient information and authentication
- **doctors** - Healthcare provider information
- **appointments** - Appointment scheduling and management
- **medications** - Prescription and medication tracking
- **lab_results** - Laboratory test results
- **messages** - Patient-provider communication

## 🔒 Security Features

- JWT-based authentication with secure token handling
- Password hashing with bcrypt
- CORS protection for cross-origin requests
- SQL injection prevention with SQLAlchemy ORM
- Input validation with Pydantic schemas
- Secure HTTP headers and middleware

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚀 Production Deployment

1. **Environment Configuration:**
   - Update environment variables in `.env`
   - Set strong SECRET_KEY
   - Configure proper database credentials
   - Set up SSL/TLS certificates

2. **Infrastructure:**
   - Use production-grade WSGI server (Gunicorn)
   - Set up reverse proxy (Nginx)
   - Configure monitoring and logging
   - Implement proper backup strategies

3. **Security:**
   - Enable HTTPS
   - Set up proper firewall rules
   - Implement rate limiting
   - Regular security audits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@healthcareportal.com or create an issue in the repository.

## 🔄 Changelog

### Version 2.0.0
- Refactored backend with proper modular structure
- Separated frontend components for better maintainability
- Improved database schema with proper relationships
- Enhanced security features
- Added comprehensive API documentation
- Improved error handling and validation
