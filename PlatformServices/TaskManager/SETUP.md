# TaskManager Quick Setup

## Prerequisites
- Docker and Docker Compose installed
- Git

## Quick Start

1. **Clone and navigate to the project**:
```bash
git clone <repository-url>
cd TaskManager
```

2. **Start the application**:
```bash
docker-compose up -d
```

3. **Access the application**:
- Frontend: http://localhost
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Services

The application consists of:
- **Frontend**: React application with modern UI
- **Backend**: FastAPI application with task scheduling
- **Database**: PostgreSQL for data persistence
- **Redis**: For caching and future job queue

## Configuration

Edit the `.env` file to configure:
- Database connection
- Email settings (SMTP)
- SMS settings (Twilio)
- Application settings

## API Usage

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Email",
    "description": "Send test email",
    "task_type": "email",
    "payload": {
      "to_email": "test@example.com",
      "subject": "Test Subject",
      "body": "Test body"
    },
    "scheduled_time": "2024-01-01T12:00:00Z"
  }'
```

### Get All Tasks
```bash
curl "http://localhost:8000/api/tasks/"
```

### Execute Task Immediately
```bash
curl -X POST "http://localhost:8000/api/tasks/1/execute"
```

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## Troubleshooting

1. **Database connection issues**: Check if PostgreSQL container is running
2. **Frontend not loading**: Check if the API is accessible at http://localhost:8000
3. **Task execution failing**: Check the logs with `docker-compose logs api`

## Stopping the Application
```bash
docker-compose down
```

To remove all data:
```bash
docker-compose down -v
``` 