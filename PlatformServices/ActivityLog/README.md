# Setup Instructions (README.md)

## Activity Log System Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. **Clone and setup the project structure:**
```bash
mkdir activity-log-system
cd activity-log-system

# Create directory structure
mkdir -p backend frontend

# Copy the backend code to backend/
# Copy the frontend code to frontend/src/
```

2. **Start the services:**
```bash
docker-compose up -d
```

3. **Run database migrations:**
```bash
docker-compose exec backend alembic upgrade head
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### Database Schema

The system includes the following main tables:
- **users**: User accounts and authentication
- **clients**: Client information 
- **activity_events**: All activity logs with metadata
- **documents**: Document references for tracking

### API Endpoints

- `GET /api/activity-events` - Get activity events with filtering
- `POST /api/activity-events` - Create a new activity event
- `POST /api/events/sign-in` - Log sign-in events
- `POST /api/events/hipaa-audit` - Log HIPAA audit events
- `POST /api/events/history` - Log history events
- `GET /api/clients` - Get clients list

### Security Features

- JWT-based authentication (placeholder in demo)
- IP address logging
- User agent tracking
- Session management
- HIPAA-compliant audit logging

### Customization

The system is designed to be modular:
- Add new event types in the models
- Extend filtering capabilities
- Customize the frontend components
- Add new audit log categories

### Production Considerations

1. **Security:**
   - Implement proper JWT authentication
   - Add rate limiting
   - Use HTTPS only
   - Secure database credentials

2. **Performance:**
   - Add database indexing
   - Implement caching
   - Optimize queries
   - Add pagination

3. **Monitoring:**
   - Add logging
   - Set up health checks
   - Monitor database performance
   - Add alerting
