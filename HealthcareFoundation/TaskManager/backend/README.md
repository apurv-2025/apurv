# README.md
# Task Management System - FastAPI Backend

A modern, high-performance task management system built with **FastAPI**, **PostgreSQL**, and **React**. This FastAPI backend provides automatic API documentation, async support, and excellent performance.

## 🚀 Features

### **Backend (FastAPI)**
- ⚡ **High Performance** - Built with FastAPI for maximum speed
- 📚 **Automatic API Documentation** - Interactive docs with Swagger UI
- 🔒 **Type Safety** - Full type hints with Pydantic models
- 🗄️ **Database** - PostgreSQL with SQLAlchemy ORM
- 📝 **Migrations** - Alembic for database versioning
- 🧪 **Testing** - Comprehensive test suite with pytest
- 📁 **File Uploads** - Secure file handling with validation
- 🔍 **Advanced Filtering** - Search, filter, and pagination
- 📊 **Statistics** - Task analytics and reporting

### **API Features**
- ✅ **Task Management** - CRUD operations with priorities and due dates
- 👥 **Client Management** - Organize tasks by clients
- 📎 **File Attachments** - Upload and manage task attachments
- 🔍 **Search & Filter** - Advanced query capabilities
- 📈 **Analytics** - Task statistics and insights

## 📋 Prerequisites

- **Python 3.11+**
- **PostgreSQL 13+**
- **Docker & Docker Compose** (recommended)

## 🛠️ Quick Start

### **Option 1: Docker Compose (Recommended)**

```bash
# Clone the repository
git clone <repository-url>
cd task-management-fastapi

# Start all services
docker-compose up -d

# Initialize database with sample data
docker-compose exec backend python scripts/init_db.py
```

### **Option 2: Local Development**

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# 4. Set up database
createdb taskmanager
alembic upgrade head
python scripts/init_db.py

# 5. Start the server
uvicorn main:app --reload
```

## 🌐 Access Points

- **API Server**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **API Schema**: http://localhost:8000/api/v1/openapi.json

## 📁 Project Structure

```
task-management-fastapi/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py                 # API router
│   │       └── endpoints/
│   │           ├── tasks.py           # Task endpoints
│   │           ├── clients.py         # Client endpoints
│   │           └── attachments.py     # File upload endpoints
│   ├── core/
│   │   ├── config.py                  # App configuration
│   │   ├── database.py                # Database setup
│   │   └── security.py                # Authentication (future)
│   ├── crud/
│   │   ├── base.py                    # Base CRUD operations
│   │   ├── crud_task.py               # Task CRUD
│   │   ├── crud_client.py             # Client CRUD
│   │   └── crud_attachment.py         # Attachment CRUD
│   ├── models/
│   │   └── models.py                  # SQLAlchemy models
│   ├── schemas/
│   │   ├── task.py                    # Task Pydantic models
│   │   ├── client.py                  # Client Pydantic models
│   │   ├── attachment.py              # Attachment Pydantic models
│   │   └── response.py                # Response models
│   └── utils/
│       ├── file_utils.py              # File handling utilities
│       ├── validators.py              # Data validation
│       └── exceptions.py              # Custom exceptions
├── alembic/                           # Database migrations
├── tests/                             # Test suite
├── scripts/                           # Utility scripts
├── uploads/                           # File uploads directory
├── main.py                            # FastAPI application
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                # Production setup
├── docker-compose.dev.yml            # Development setup
└── Dockerfile                        # Container definition
```

## 🔧 API Endpoints

### **Tasks**
```http
GET    /api/v1/tasks/                    # List tasks (with filtering)
POST   /api/v1/tasks/                    # Create task
GET    /api/v1/tasks/{id}                # Get task
PUT    /api/v1/tasks/{id}                # Update task
DELETE /api/v1/tasks/{id}                # Delete task
GET    /api/v1/tasks/stats/overview      # Task statistics
GET    /api/v1/tasks/overdue/            # Overdue tasks
GET    /api/v1/tasks/due-today/          # Tasks due today
```

### **Clients**
```http
GET    /api/v1/clients/                  # List clients
POST   /api/v1/clients/                  # Create client
GET    /api/v1/clients/{id}              # Get client
PUT    /api/v1/clients/{id}              # Update client
DELETE /api/v1/clients/{id}              # Delete client
GET    /api/v1/clients/{id}/tasks        # Get client tasks
```

### **Attachments**
```http
POST   /api/v1/attachments/upload        # Upload file
GET    /api/v1/attachments/{id}          # Get attachment info
GET    /api/v1/attachments/{id}/download # Download file
DELETE /api/v1/attachments/{id}          # Delete attachment
GET    /api/v1/attachments/task/{id}/    # Get task attachments
```

## 📊 Advanced Features

### **Filtering & Search**
```http
# Filter tasks by status, priority, client, etc.
GET /api/v1/tasks/?status=todo&priority=high&client_id=1

# Search tasks by name or description
GET /api/v1/tasks/?search=project

# Get overdue tasks
GET /api/v1/tasks/?overdue=true

# Pagination
GET /api/v1/tasks/?skip=0&limit=10
```

### **Task Statistics**
```http
GET /api/v1/tasks/stats/overview
```
Returns:
```json
{
  "total_tasks": 150,
  "completed_tasks": 45,
  "pending_tasks": 105,
  "overdue_tasks": 12,
  "due_today": 5,
  "completion_rate": 30.0
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_tasks.py

# Run tests with verbose output
pytest -v
```

## 📦 Database Operations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Initialize with sample data
python scripts/init_db.py
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/taskmanager

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File uploads
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=["txt","pdf","png","jpg","jpeg","gif","doc","docx"]

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### **Development vs Production**
```bash
# Development
ENVIRONMENT=development
DEBUG=True

# Production
ENVIRONMENT=production
DEBUG=False
```

## 🐳 Docker Commands

```bash
# Development with hot reload
docker-compose -f docker-compose.dev.yml up

# Production deployment
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run commands in container
docker-compose exec backend python scripts/init_db.py

# Database backup
docker-compose exec postgres pg_dump -U taskuser taskmanager > backup.sql
```

## 🚀 Production Deployment

### **Using Docker Compose**
```bash
# Build and deploy
docker-compose up -d --build

# SSL setup (add certificates to nginx/ssl/)
docker-compose -f docker-compose.prod.yml up -d
```

### **Using a Process Manager**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Environment Setup**
```bash
# Production environment variables
export ENVIRONMENT=production
export DEBUG=False
export DATABASE_URL=postgresql://user:pass@prod-db:5432/taskmanager
export SECRET_KEY=your-very-secure-secret-key
```

## 🔍 Monitoring & Logging

### **Health Check**
```http
GET /health
```

### **API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **Logging**
```python
# Logs are automatically configured
# Check logs with:
docker-compose logs -f backend
```

## 🧰 Development Tools

### **Code Quality**
```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### **Database Tools**
```bash
# Connect to database
docker-compose exec postgres psql -U taskuser -d taskmanager

# Reset database
docker-compose down -v
docker-compose up -d
python scripts/init_db.py
```

## 🔧 Customization

### **Adding New Endpoints**
1. Create Pydantic schema in `app/schemas/`
2. Add CRUD operations in `app/crud/`
3. Create API endpoints in `app/api/v1/endpoints/`
4. Add to main router in `app/api/v1/api.py`

### **Database Models**
1. Add model to `app/models/models.py`
2. Create migration: `alembic revision --autogenerate -m "Add model"`
3. Apply: `alembic upgrade head`

## 🛠️ Troubleshooting

### **Common Issues**

**Database Connection:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# View database logs
docker-compose logs postgres
```

**File Upload Issues:**
```bash
# Check uploads directory permissions
chmod 755 uploads/

# Check file size limits in nginx config
client_max_body_size 50M;
```

**Migration Issues:**
```bash
# Reset migrations (development only)
alembic downgrade base
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - The Python SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **Alembic** - Database migration tool for SQLAlchemy
- **PostgreSQL** - Advanced open source database

---

## 📞 Support

For support, please create an issue in the repository or contact the development team.
