# README.md

# Task Management System

A comprehensive task management application built with React, Flask, and PostgreSQL. Features include task creation, client management, file attachments, and real-time notifications.

## 🚀 Features

- **Task Management**: Create, edit, delete, and organize tasks with priorities and due dates
- **Client Management**: Manage client information and associate tasks with clients
- **File Attachments**: Upload and manage file attachments for tasks
- **Search & Filter**: Advanced search and filtering capabilities
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Real-time Notifications**: Toast notifications for user feedback
- **RESTful API**: Well-documented API endpoints

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 13+
- Docker and Docker Compose (for containerized deployment)

## 🛠️ Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd task-management-system
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Database: localhost:5432

## 🔧 Manual Development Setup

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Initialize database**
```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database
createdb taskmanager

# Run migrations
flask db upgrade

# Seed with sample data (optional)
flask seed-db
```

5. **Start the development server**
```bash
python run.py
```

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm start
```

The application will be available at http://localhost:3000

## 📁 Project Structure

```
task-management-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── task.py
│   │   │   ├── client.py
│   │   │   └── attachment.py
│   │   ├── routes/
│   │   │   ├── task_routes.py
│   │   │   ├── client_routes.py
│   │   │   └── attachment_routes.py
│   │   ├── services/
│   │   │   ├── task_service.py
│   │   │   ├── client_service.py
│   │   │   └── attachment_service.py
│   │   └── utils/
│   │       ├── validators.py
│   │       ├── decorators.py
│   │       └── file_utils.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   ├── Tasks/
│   │   │   ├── Clients/
│   │   │   └── UI/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   ├── models/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## 🔐 Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://username:password@localhost/taskmanager
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/taskmanager

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# File uploads
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800  # 50MB

# Environment
FLASK_ENV=development
DEBUG=True
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

## 🚀 API Documentation

### Tasks Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `GET /api/tasks/stats` - Get task statistics

### Clients Endpoints

- `GET /api/clients` - Get all clients
- `POST /api/clients` - Create a new client
- `GET /api/clients/{id}` - Get a specific client
- `PUT /api/clients/{id}` - Update a client
- `DELETE /api/clients/{id}` - Delete a client

### Attachments Endpoints

- `POST /api/attachments/upload` - Upload a file
- `GET /api/attachments/{id}` - Get attachment metadata
- `GET /api/attachments/{id}/download` - Download a file
- `DELETE /api/attachments/{id}` - Delete an attachment

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Production Deployment

### Using Docker Compose

1. **Update environment variables for production**
```bash
# Create production .env files
cp backend/.env.example backend/.env.production
cp frontend/.env.example frontend/.env.production
# Update with production values
```

2. **Deploy with SSL**
```bash
# Add SSL certificates to nginx/ssl/
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

1. **Backend deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
```

2. **Frontend deployment**
```bash
# Build for production
npm run build

# Serve with Nginx or Apache
```

## 📊 Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    due_time TIME,
    priority VARCHAR(20) DEFAULT 'none',
    status VARCHAR(20) DEFAULT 'todo',
    client_id INTEGER REFERENCES clients(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Clients Table
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    company VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Task Attachments Table
```sql
CREATE TABLE task_attachments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Database Configuration
```python
# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
```

### Frontend Configuration
```javascript
// src/config/api.js
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  TIMEOUT: 10000,
  MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
};
```

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**
```bash
# Check PostgreSQL status
sudo service postgresql status

# Restart PostgreSQL
sudo service postgresql restart
```

2. **File upload issues**
```bash
# Check uploads directory permissions
chmod 755 backend/uploads
```

3. **Frontend build errors**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Performance Optimization

1. **Database Optimization**
```sql
-- Add indexes for better query performance
CREATE INDEX idx_tasks_status_date ON tasks(status, due_date);
CREATE INDEX idx_tasks_client ON tasks(client_id);
```

2. **Frontend Optimization**
```javascript
// Use React.memo for expensive components
export default React.memo(TaskCard);

// Implement lazy loading
const TasksView = lazy(() => import('./components/Tasks/TasksView'));
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask team for the lightweight Python framework
- Tailwind CSS for the utility-first CSS framework
- Lucide React for the beautiful icons

---

## 📞 Support

For support, email support@taskmanager.com or create an issue in the repository.

# scripts/setup.sh
#!/bin/bash

# Task Management System Setup Script

echo "🚀 Setting up Task Management System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/uploads
mkdir -p nginx/ssl
mkdir -p database/backups

# Copy environment files
echo "🔧 Setting up environment files..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env (please update with your values)"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Created frontend/.env"
fi

# Set proper permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh
chmod 755 backend/uploads

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec backend flask db upgrade

# Seed database with sample data
echo "🌱 Seeding database with sample data..."
docker-compose exec backend flask seed-db

echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   Database: localhost:5432"
echo ""
echo "📚 Check the README.md for more information."

# scripts/backup.sh
#!/bin/bash

# Database backup script

BACKUP_DIR="database/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="taskmanager_backup_$DATE.sql"

echo "📦 Creating database backup..."

# Create backup
docker-compose exec postgres pg_dump -U taskuser taskmanager > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Backup created successfully: $BACKUP_FILE"
    
    # Keep only last 7 backups
    ls -t $BACKUP_DIR/taskmanager_backup_*.sql | tail -n +8 | xargs -r rm
    echo "🧹 Cleaned up old backups"
else
    echo "❌ Backup failed!"
    exit 1
fi

# scripts/deploy.sh
#!/bin/bash

# Production deployment script

echo "🚀 Deploying to production..."

# Pull latest changes
git pull origin main

# Build and deploy with Docker Compose
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend flask db upgrade

echo "✅ Production deployment complete!"

# Health check
echo "🏥 Running health check..."
sleep 5
curl -f http://localhost/health || echo "⚠️ Health check failed"
