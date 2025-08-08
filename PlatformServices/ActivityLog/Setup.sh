#!/bin/bash
# setup.sh - Complete setup script for Activity Log System

set -e

echo "🚀 Setting up Activity Log System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create project structure
print_status "Creating project structure..."
mkdir -p activity-log-system/{backend,frontend/src,frontend/public}
cd activity-log-system

# Create backend files
print_status "Setting up backend..."
cat > backend/.env << EOF
DATABASE_URL=postgresql://activity_user:activity_password@localhost:5432/activity_log_db
SECRET_KEY=your-super-secret-key-change-in-production-$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

cat > backend/requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.21
psycopg2-binary==2.9.7
alembic==1.12.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
bcrypt==4.1.2
EOF

# Create frontend configuration
print_status "Setting up frontend..."
cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000/api
EOF

cat > frontend/package.json << EOF
{
  "name": "activity-log-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.4",
    "@testing-library/react": "^13.3.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4",
    "lucide-react": "^0.263.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24"
  }
}
EOF

cat > frontend/tailwind.config.js << EOF
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

cat > frontend/postcss.config.js << EOF
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

cat > frontend/src/index.css << EOF
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

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
EOF

cat > frontend/src/index.js << EOF
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import ActivityLog from './ActivityLog';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ActivityLog />
  </React.StrictMode>
);
EOF

cat > frontend/public/index.html << EOF
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Activity Log System" />
    <title>Activity Log System</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: activity_log_db
    environment:
      POSTGRES_DB: activity_log_db
      POSTGRES_USER: activity_user
      POSTGRES_PASSWORD: activity_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U activity_user -d activity_log_db"]
      interval: 30s
      timeout: 10s
      retries: 5

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: activity_log_backend
    environment:
      DATABASE_URL: postgresql://activity_user:activity_password@postgres:5432/activity_log_db
      SECRET_KEY: your-super-secret-key-change-in-production
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

volumes:
  postgres_data:
EOF

# Create init.sql for sample data
cat > init.sql << EOF
-- Create sample data
INSERT INTO users (id, email, hashed_password, full_name, is_active, created_at) 
VALUES 
    ('mock-user-id', 'user@example.com', 'hashed_password123', 'John Doe', true, NOW())
ON CONFLICT (id) DO NOTHING;

INSERT INTO clients (id, first_name, last_name, email, created_by, created_at)
VALUES 
    ('client-1', 'Jamie', 'D. Appleseed', 'jamie@example.com', 'mock-user-id', NOW())
ON CONFLICT (id) DO NOTHING;
EOF

# Create backend Dockerfile
cat > backend/Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOF

# Create alembic configuration
mkdir -p backend/alembic/versions

cat > backend/alembic.ini << EOF
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = postgresql://activity_user:activity_password@postgres:5432/activity_log_db

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF

cat > backend/alembic/env.py << 'EOF'
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the parent directory to sys.path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models import Base
from config import settings

# this is the Alembic Config object
config = context.config

# Set the database URL
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF

cat > backend/alembic/script.py.mako << 'EOF'
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
EOF

# Create development scripts
cat > start-dev.sh << EOF
#!/bin/bash
echo "🚀 Starting Activity Log System in development mode..."

# Start PostgreSQL
print_status "Starting PostgreSQL..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Start backend
print_status "Starting backend..."
cd backend
python -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=\$!

# Start frontend
print_status "Starting frontend..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=\$!

echo "✅ System started!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'kill \$BACKEND_PID \$FRONTEND_PID; docker-compose down; exit' INT
wait
EOF

chmod +x start-dev.sh

cat > start-docker.sh << EOF
#!/bin/bash
echo "🐳 Starting Activity Log System with Docker..."

# Start all services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

echo "✅ System started!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
EOF

chmod +x start-docker.sh

# Create README
cat > README.md << EOF
# Activity Log System

A modular activity logging system built with React/Tailwind frontend and FastAPI/PostgreSQL backend.

## Features

- **Three Activity Views**: History, Sign In Events, and HIPAA Audit Log
- **Modular Architecture**: Separate frontend and backend with clean APIs
- **HIPAA Compliant**: Audit logging for healthcare applications
- **Real-time Filtering**: Search and filter activities by date, type, and content
- **Responsive Design**: Modern UI built with Tailwind CSS
- **Docker Support**: Easy deployment with Docker Compose

## Quick Start

### Option 1: Docker (Recommended)
\`\`\`bash
./start-docker.sh
\`\`\`

### Option 2: Development Mode
\`\`\`bash
./start-dev.sh
\`\`\`

## Manual Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### Backend Setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
\`\`\`

### Frontend Setup
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

## Project Structure

\`\`\`
activity-log-system/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # Database operations
│   ├── services.py       # Business logic
│   ├── config.py         # Configuration
│   └── alembic/          # Database migrations
├── frontend/
│   └── src/
│       └── ActivityLog.js # React components
└── docker-compose.yml
\`\`\`

## API Endpoints

- \`GET /api/activity-events\` - List activity events
- \`POST /api/activity-events\` - Create activity event
- \`POST /api/events/sign-in\` - Log sign-in event
- \`POST /api/events/hipaa-audit\` - Log HIPAA event
- \`POST /api/events/history\` - Log history event

## Environment Variables

### Backend (.env)
\`\`\`
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

### Frontend (.env)
\`\`\`
REACT_APP_API_URL=http://localhost:8000/api
\`\`\`

## Development

### Database Migrations
\`\`\`bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
\`\`\`

### Adding New Event Types
1. Update \`models.py\` event_type enum
2. Add new service methods in \`services.py\`
3. Create new API endpoints in \`main.py\`
4. Update frontend components

## Production Deployment

1. Set strong SECRET_KEY
2. Use production database
3. Enable HTTPS
4. Add authentication
5. Configure logging
6. Set up monitoring

## License

MIT License
EOF

print_status "✅ Project structure created successfully!"
print_status "📁 Project location: $(pwd)"
print_status ""
print_status "Next steps:"
print_status "1. Copy your backend code to: backend/"
print_status "2. Copy your frontend code to: frontend/src/ActivityLog.js"
print_status "3. Run: ./start-docker.sh (for Docker)"
print_status "   Or: ./start-dev.sh (for development)"
print_status ""
print_status "🌐 The application will be available at:"
print_status "   Frontend: http://localhost:3000"
print_status "   Backend:  http://localhost:8000"
print_status "   API Docs: http://localhost:8000/docs"
