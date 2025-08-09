# Mental Health EHR - Progress Notes System

A comprehensive, HIPAA-compliant electronic health record system specifically designed for mental and behavioral health professionals to create, manage, and store progress notes.

## 🏥 Features

### Core Functionality
- **Multiple Note Formats**: Support for SOAP, DAP, BIRP, and PAIP note templates
- **Digital Signatures**: Secure note signing with timestamp and audit trail
- **Role-Based Access Control**: Clinician, Supervisor, Admin, and Billing Staff roles
- **Auto-Save**: Automatic draft saving every 60 seconds
- **Version Control**: Track note versions and changes
- **Audit Logging**: Complete audit trail for compliance

### Security & Compliance
- **HIPAA Compliant**: Encrypted data at rest and in transit
- **JWT Authentication**: Secure token-based authentication
- **Session Management**: Automatic timeout after inactivity
- **Access Controls**: Role-based permissions for note access
- **Audit Trail**: Complete logging of all user actions

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Rich Text Editor**: Professional note editing with spell-check
- **Search & Filter**: Advanced search capabilities across notes
- **Dashboard**: Overview of note statistics and recent activity
- **File Attachments**: Support for PDFs, images, and documents

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **FastAPI**: Modern, fast Python web framework
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Alembic**: Database migration tool

**Frontend:**
- **React 18**: Modern JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and development server
- **Lucide React**: Beautiful & consistent icon pack

**Infrastructure:**
- **Docker**: Containerization for easy deployment
- **Docker Compose**: Multi-container application orchestration
- **PostgreSQL**: Production-ready database

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/mental-health-ehr.git
   cd mental-health-ehr
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database:**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - pgAdmin (optional): http://localhost:5050

6. **Default login credentials:**
   - Email: `admin@clinic.com`
   - Password: `admin123`

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```bash
   # Install PostgreSQL and create database
   createdb mental_health_ehr
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database settings
   ```

6. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

7. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
mental-health-ehr/
├── backend/
│   ├── routes/                 # API endpoints
│   │   ├── auth.py            # Authentication routes
│   │   ├── users.py           # User management
│   │   ├── patients.py        # Patient management
│   │   ├── notes.py           # Progress notes
│   │   └── templates.py       # Note templates
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── services.py            # Business logic
│   ├── database.py            # Database configuration
│   ├── auth.py                # Authentication utilities
│   ├── config.py              # Application settings
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── alembic.ini           # Database migration config
│   └── migrations/           # Database migrations
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── utils/            # Utility functions
│   │   ├── App.jsx           # Main application component
│   │   └── main.jsx          # Application entry point
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   └── tailwind.config.js    # Tailwind CSS configuration
├── docker-compose.yml        # Docker services configuration
├── .env.example             # Environment variables template
└── README.md               # Project documentation
```

## 🔧 Configuration

### Environment Variables

#### Backend Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/mental_health_ehr` |
| `SECRET_KEY` | JWT secret key (change in production) | `your-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `UPLOAD_DIRECTORY` | File upload directory | `./uploads` |
| `MAX_FILE_SIZE` | Maximum file upload size (bytes) | `10485760` (10MB) |
| `SESSION_TIMEOUT_MINUTES` | User session timeout | `15` |

#### Frontend Configuration

The frontend configuration is managed through Vite and can be customized in `vite.config.js`.

### Database Schema

The application uses PostgreSQL with the following main tables:

- **users**: System users (clinicians, supervisors, admins)
- **patients**: Patient information
- **progress_notes**: Progress notes with content and metadata
- **note_templates**: Customizable note templates
- **note_attachments**: File attachments for notes
- **audit_logs**: Complete audit trail
- **patient_clinicians**: Patient-clinician relationships

## 🔐 Security Features

### Authentication & Authorization
- JWT-based authentication with configurable expiration
- Role-based access control (RBAC)
- Session timeout for inactive users
- Password hashing using bcrypt

### Data Protection
- All sensitive data encrypted at rest
- HTTPS/TLS encryption in transit
- SQL injection prevention through ORM
- Input validation and sanitization

### Audit & Compliance
- Complete audit logging of all user actions
- Immutable audit trail
- HIPAA-compliant data handling
- Version control for all note changes

## 📊 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User authentication |
| GET | `/auth/me` | Get current user info |

### Progress Notes Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes/` | List progress notes with filters |
| POST | `/notes/` | Create new progress note |
| GET | `/notes/{id}` | Get specific progress note |
| PUT | `/notes/{id}` | Update progress note |
| POST | `/notes/{id}/draft` | Save note as draft |
| POST | `/notes/{id}/sign` | Sign progress note |
| POST | `/notes/{id}/unlock` | Unlock signed note (supervisor only) |
| GET | `/notes/dashboard` | Get dashboard statistics |

### Patient Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/` | List patients |
| POST | `/patients/` | Create new patient |
| GET | `/patients/{id}` | Get specific patient |
| PUT | `/patients/{id}` | Update patient information |

### User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List users (admin only) |
| POST | `/users/` | Create new user (admin only) |
| GET | `/users/{id}` | Get specific user |
| PUT | `/users/{id}` | Update user information |

For complete API documentation, visit http://localhost:8000/docs when running the application.

## 🧪 Testing

### Backend Testing

```bash
cd backend
pip install -r requirements.txt
pytest
```

### Frontend Testing

```bash
cd frontend
npm install
npm test
```

## 🚀 Deployment

### Production Deployment with Docker

1. **Update environment variables for production:**
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production settings
   ```

2. **Use production Docker Compose:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Set up reverse proxy (nginx):**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Database Backups

```bash
# Backup database
docker-compose exec db pg_dump -U postgres mental_health_ehr > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres mental_health_ehr < backup.sql
```

## 🔧 Development

### Adding New Note Templates

1. **Create template in database:**
   ```python
   # Add to note_templates table or via API
   template = {
       "name": "Custom Template",
       "template_type": "Custom",
       "structure": {
           "custom_field_1": "",
           "custom_field_2": "",
           "notes": ""
       }
   }
   ```

2. **Create React component:**
   ```javascript
   const CustomNoteTemplate = ({ content, onChange, isReadOnly }) => {
       // Implementation
   };
   ```

3. **Register in note editor:**
   ```javascript
   // Add to renderNoteTemplate() in NoteEditor component
   case 'Custom':
       return <CustomNoteTemplate {...templateProps} />;
   ```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Issues:**
```bash
# Check if PostgreSQL is running
docker-compose ps db

# Check database logs
docker-compose logs db
```

**Frontend Build Issues:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Backend Issues:**
```bash
# Check backend logs
docker-compose logs backend

# Restart backend service
docker-compose restart backend
```

### Performance Optimization

1. **Database Indexing:** Ensure proper indexes on frequently queried columns
2. **API Pagination:** Use pagination for large result sets
3. **Caching:** Implement Redis caching for frequently accessed data
4. **CDN:** Use CDN for static assets in production

## 📋 Compliance & Standards

### HIPAA Compliance
- ✅ Administrative Safeguards: Access controls, assigned security responsibility
- ✅ Physical Safeguards: Workstation controls, device and media controls
- ✅ Technical Safeguards: Access control, audit controls, integrity, transmission security

### Clinical Standards
- ✅ Support for industry-standard note formats (SOAP, DAP, BIRP, PAIP)
- ✅ Digital signature capabilities
- ✅ Version control and audit trails
- ✅ Role-based access controls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript code
- Write tests for new features
- Update documentation for API changes
- Ensure HIPAA compliance for all changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Email: support@mentalhealthehr.com
- Documentation: https://docs.mentalhealthehr.com
- Issues: https://github.com/your-username/mental-health-ehr/issues

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [React](https://reactjs.org/) for the powerful frontend library
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [PostgreSQL](https://www.postgresql.org/) for the robust database system

---

**⚠️ Important Security Notice:** This application handles sensitive medical information. Ensure proper security measures, regular updates, and compliance with local healthcare regulations before deploying in a production environment.
