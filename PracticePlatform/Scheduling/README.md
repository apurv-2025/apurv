# Scheduling2.0

A unified scheduling system for medical and mental health practices, combining the best features from both MBH-Scheduling and Scheduling projects with integrated Patient and Practitioner microservices from HealthcareFoundation/CoreServices.

## 🚀 Features

### Core Functionality
- **Unified Patient/Client Management**: Support for both medical patients and mental health clients
- **Practitioner Management**: Complete practitioner profiles with specialties and availability
- **Appointment Scheduling**: Advanced calendar with conflict detection and availability management
- **Organization Support**: Multi-organization setup with FHIR compliance
- **Waitlist Management**: Priority-based waitlist system for mental health practices
- **Service Code Management**: Billing and service tracking
- **Location Management**: Support for multiple locations and telehealth
- **Patient Service Integration**: Full integration with HealthcareFoundation/CoreServices/Patient microservice
- **Practitioner Service Integration**: Full integration with HealthcareFoundation/CoreServices/Practitioner microservice

### Technical Features
- **Modern Tech Stack**: FastAPI backend, React frontend, PostgreSQL database
- **Docker Support**: Complete containerization for easy deployment
- **Authentication**: JWT-based authentication with role-based access control
- **Real-time Updates**: WebSocket support for live updates
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **API Documentation**: Auto-generated OpenAPI documentation

## 🏗️ Architecture

```
Scheduling2.0/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities and enums
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom React hooks
│   │   ├── contexts/       # React contexts
│   │   └── utils/          # Utility functions
│   ├── Dockerfile
│   └── package.json
├── database/               # Database initialization
│   └── init.sql
├── scripts/                # Utility scripts
├── docker-compose.yml      # Docker orchestration
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Authentication and authorization
- **Alembic**: Database migrations

### Frontend
- **React 18**: Modern React with hooks and concurrent features
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **React Hook Form**: Form handling and validation
- **React Big Calendar**: Calendar component
- **Axios**: HTTP client
- **React Toastify**: Toast notifications

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Database container

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Scheduling2.0
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Patient Service: http://localhost:8001
   - Practitioner Service: http://localhost:8002

4. **Test the integration**
   ```bash
   python test_integration.py
   python test_waitlist_integration.py
   ```

## 🔗 Service Integration

This application integrates with Patient and Practitioner microservices from HealthcareFoundation/CoreServices:

- **Patient Service**: FHIR-compliant patient management (Port 8001)
- **Practitioner Service**: FHIR-compliant practitioner management (Port 8002)

For detailed integration information, see [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md).
   - API Documentation: http://localhost:8000/docs

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL container
   docker run -d --name scheduling2-postgres \
     -e POSTGRES_DB=scheduling2_db \
     -e POSTGRES_USER=scheduling_user \
     -e POSTGRES_PASSWORD=scheduling_pass123 \
     -p 5432:5432 \
     postgres:17
   ```

## 📊 Database Schema

The unified database schema supports both medical and mental health practices:

### Core Entities

- **Users**: System users with role-based access
- **Practitioners**: Healthcare providers with specialties
- **Patients**: Medical patients
- **Clients**: Mental health clients
- **Appointments**: Unified appointment system
- **Locations**: Physical and virtual locations
- **Service Codes**: Billing and service tracking
- **Waitlist**: Priority-based waitlist management

### Key Features
- **Unified Appointments**: Single table supporting both patient and client appointments
- **FHIR Compliance**: FHIR resource support for practitioners
- **Flexible Billing**: Support for multiple billing types and service codes
- **Availability Management**: Practitioner availability tracking
- **Audit Trail**: Comprehensive audit fields on all entities

## 🔐 Authentication & Authorization

The system uses JWT-based authentication with role-based access control:

### User Roles
- **Admin**: Full system access
- **Practitioner**: Appointment and patient management
- **Nurse**: Patient care and scheduling
- **Receptionist**: Appointment scheduling and patient registration
- **Therapist**: Mental health specific features
- **Psychiatrist**: Mental health and medication management

### Security Features
- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- CORS configuration
- Input validation and sanitization

## 📱 Frontend Features

### Dashboard
- Overview of appointments, patients, and key metrics
- Quick actions for common tasks
- Real-time updates

### Calendar View
- Interactive calendar with appointment display
- Drag-and-drop appointment management
- Multiple view options (day, week, month)

### Patient/Client Management
- Comprehensive patient and client profiles
- Medical history and notes
- Insurance information
- Emergency contacts

### Appointment Scheduling
- Conflict detection
- Availability checking
- Service code integration
- Billing information

### Waitlist Management
- Priority-based waitlist with full CRUD operations
- Integration with Patient and Practitioner services
- Advanced filtering and search capabilities
- Waitlist statistics and analytics
- Scheduling from waitlist functionality
- Preferred dates and times management

## 🔧 Configuration

### Environment Variables

#### Backend
```env
DATABASE_URL=postgresql+asyncpg://scheduling_user:scheduling_pass123@localhost:5432/scheduling2_db
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

#### Frontend
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Production Deployment
1. Update environment variables for production
2. Build and push Docker images
3. Deploy using Docker Compose or Kubernetes
4. Set up SSL certificates
5. Configure database backups

### Environment-Specific Configurations
- Development: Local development with hot reload
- Staging: Production-like environment for testing
- Production: Optimized for performance and security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the setup guide in the documentation

## 🔄 Migration from Previous Versions

### From MBH-Scheduling
- All mental health features are preserved
- Enhanced with medical practice capabilities
- Improved database schema with better relationships

### From Scheduling
- All medical features are preserved
- Enhanced with mental health capabilities
- Unified appointment system

## 🗺️ Roadmap

### Upcoming Features
- [ ] Advanced reporting and analytics
- [ ] Mobile app support
- [ ] Integration with EHR systems
- [ ] Telehealth video integration
- [ ] Advanced billing and insurance integration
- [ ] Patient portal
- [ ] Automated appointment reminders
- [ ] Multi-language support

### Performance Improvements
- [ ] Database query optimization
- [ ] Caching layer implementation
- [ ] Frontend performance optimization
- [ ] API response optimization

---

**Scheduling2.0** - Unifying medical and mental health scheduling for better patient care. 