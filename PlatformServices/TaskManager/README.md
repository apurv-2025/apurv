# Task Manager System

A comprehensive task scheduling and execution system built with FastAPI, React, and PostgreSQL. Perfect for medical practices, AI agents, and any service that needs reliable task scheduling with monitoring capabilities.

## Features

- **Task Scheduling**: Schedule tasks for immediate or future execution
- **Multiple Task Types**: Support for email, SMS, webhooks, and custom reminders
- **Retry Logic**: Automatic retry with configurable limits
- **Real-time Monitoring**: Track task execution status and history
- **Callback Support**: Webhook notifications when tasks complete
- **API & UI Access**: Both programmatic API and user-friendly web interface
- **AI Agent Ready**: Perfect for AI systems that need to schedule and monitor tasks

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Using Docker (Recommended)

1. **Clone and setup**:
```bash
git clone <repository>
cd task-manager
```

2. **Create environment file**:
```bash
# .env
DATABASE_URL=postgresql://taskuser:taskpass@postgres:5432/taskmanager
REDIS_URL=redis://redis:6379
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

3. **Start services**:
```bash
docker-compose up -d
```

4. **Access the application**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: Deploy the React component or integrate into your app

### Manual Setup

1. **Database Setup**:
```bash
# Install PostgreSQL and create database
createdb taskmanager
```

2. **Backend Setup**:
```bash
cd backend
pip install -r requirements.txt

# Update database connection in database.py
export DATABASE_URL=postgresql://username:password@localhost/taskmanager

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

3. **Frontend Setup**:
```bash
cd frontend
npm install
npm start
```

## API Usage

### Authentication
Currently, the API is open. In production, implement proper authentication:

```python
# Add to main.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verify_token(token: str = Depends(security)):
    # Implement your token verification logic
    pass
```

### Core Endpoints

#### Create Task
```bash
POST /api/tasks/
Content-Type: application/json

{
  "name": "Send Appointment Reminder",
  "description": "Remind patient of upcoming appointment",
  "task_type": "email",
  "scheduled_time": "2024-12-25T14:00:00Z",
  "payload": {
    "to_email": "patient@example.com",
    "subject": "Appointment Reminder - Tomorrow at 2 PM",
    "body": "Dear John, this is a friendly reminder of your appointment tomorrow at 2:00 PM with Dr. Smith. Please arrive 15 minutes early."
  },
  "callback_url": "https://your-system.com/task-completed",
  "max_retries": 3
}
```

#### Get Tasks
```bash
# Get all tasks
GET /api/tasks/

# Filter by status
GET /api/tasks/?status=pending

# Pagination
GET /api/tasks/?skip=0&limit=10
```

#### Execute Task Immediately
```bash
POST /api/tasks/{task_id}/execute
```

#### Get Task Execution History
```bash
GET /api/tasks/{task_id}/executions
```

### Task Types and Payloads

#### Email Task
```json
{
  "task_type": "email",
  "payload": {
    "to_email": "patient@example.com",
    "subject": "Your Appointment Reminder",
    "body": "Your appointment is scheduled for tomorrow at 2:00 PM."
  }
}
```

#### SMS Task
```json
{
  "task_type": "sms", 
  "payload": {
    "phone_number": "+1234567890",
    "message": "Reminder: Your appointment is tomorrow at 2 PM."
  }
}
```

#### Webhook Task
```json
{
  "task_type": "webhook",
  "payload": {
    "url": "https://external-api.com/notify",
    "method": "POST",
    "data": {
      "patient_id": "12345",
      "appointment_date": "2024-12-25",
      "message": "Reminder sent"
    },
    "headers": {
      "Authorization": "Bearer your-token"
    }
  }
}
```

#### Reminder Task (Flexible)
```json
{
  "task_type": "reminder",
  "payload": {
    "type": "email",  // or "sms"
    "recipient": "patient@example.com",
    "message": "Your lab results are ready for pickup."
  }
}
```

## AI Agent Integration

### Python Agent Example
```python
import requests
from datetime import datetime, timedelta
import asyncio

class TaskManagerClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    async def schedule_reminder(self, patient_email, appointment_time, doctor_name):
        # Schedule reminder 24 hours before appointment
        reminder_time = appointment_time - timedelta(hours=24)
        
        task_data = {
            "name": f"24h Appointment Reminder - {doctor_name}",
            "description": f"Remind patient of appointment with {doctor_name}",
            "task_type": "email",
            "scheduled_time": reminder_time.isoformat() + "Z",
            "payload": {
                "to_email": patient_email,
                "subject": "Appointment Reminder - Tomorrow",
                "body": f"Dear Patient, this is a reminder of your appointment tomorrow with {doctor_name}."
            },
            "callback_url": "https://your-ai-system.com/reminder-sent"
        }
        
        response = requests.post(f"{self.base_url}/api/tasks/", json=task_data)
        return response.json()
    
    async def check_task_status(self, task_id):
        response = requests.get(f"{self.base_url}/api/tasks/{task_id}")
        return response.json()
    
    async def get_failed_tasks(self):
        response = requests.get(f"{self.base_url}/api/tasks/?status=failed")
        return response.json()

# Usage
client = TaskManagerClient()

# Schedule a reminder
appointment_time = datetime.now() + timedelta(days=1, hours=14)  # Tomorrow at 2 PM
task = await client.schedule_reminder(
    patient_email="john.doe@example.com",
    appointment_time=appointment_time,
    doctor_name="Dr. Smith"
)

print(f"Task scheduled: {task['id']}")

# Check status later
status = await client.check_task_status(task['id'])
print(f"Task status: {status['status']}")
```

### Node.js Agent Example
```javascript
const axios = require('axios');

class TaskManagerClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async scheduleFollowUp(patientPhone, visitDate) {
        // Schedule follow-up SMS 3 days after visit
        const followUpDate = new Date(visitDate);
        followUpDate.setDate(followUpDate.getDate() + 3);
        
        const taskData = {
            name: 'Post-Visit Follow-up',
            description: 'Check on patient after recent visit',
            task_type: 'sms',
            scheduled_time: followUpDate.toISOString(),
            payload: {
                phone_number: patientPhone,
                message: 'How are you feeling after your recent visit? Please reply if you have any concerns.'
            },
            callback_url: 'https://your-system.com/followup-sent'
        };
        
        const response = await axios.post(`${this.baseUrl}/api/tasks/`, taskData);
        return response.data;
    }
    
    async getBulkTaskStatus(taskIds) {
        const tasks = await Promise.all(
            taskIds.map(id => axios.get(`${this.baseUrl}/api/tasks/${id}`))
        );
        return tasks.map(response => response.data);
    }
}

// Usage
const client = new TaskManagerClient();
const task = await client.scheduleFollowUp('+1234567890', new Date());
```

## Production Considerations

### Security
1. **Authentication**: Implement proper API authentication
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **Input Validation**: Validate all inputs thoroughly
4. **HTTPS**: Use HTTPS in production

### Scaling
1. **Job Queue**: Replace background tasks with Celery + Redis
2. **Database**: Use connection pooling and read replicas
3. **Monitoring**: Add logging and metrics collection
4. **Load Balancing**: Use nginx or similar for load balancing

### Enhanced Email/SMS Setup
```python
# email_service.py
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_pass = os.getenv('SMTP_PASS')
    
    async def send_email(self, to_email, subject, body):
        msg = MimeMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MimeText(body, 'plain'))
        
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_pass)
        server.send_message(msg)
        server.quit()

# sms_service.py (using Twilio)
from twilio.rest import Client
import os

class SMSService:
    def __init__(self):
        self.client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    async def send_sms(self, to_number, message):
        message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=to_number
        )
        return message.sid
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Monitoring and Logging
```python
# logging_config.py
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('task_manager.log'),
        logging.StreamHandler()
    ]
)

# Add to task_executor.py
import logging
logger = logging.getLogger(__name__)

async def execute_task(self, task_id: int):
    logger.info(f"Starting execution of task {task_id}")
    # ... existing code ...
    logger.info(f"Completed execution of task {task_id} with status {status}")
```

## Medical Practice Use Case

This system is perfect for medical practices to automate patient communications:

### Appointment Reminders
```python
# Schedule reminder when appointment is booked
def book_appointment(patient_id, doctor_id, appointment_time):
    # ... booking logic ...
    
    # Schedule 24-hour reminder
    reminder_time = appointment_time - timedelta(hours=24)
    schedule_task({
        "name": f"24h Reminder - Patient {patient_id}",
        "task_type": "email",
        "scheduled_time": reminder_time,
        "payload": {
            "to_email": patient.email,
            "subject": "Appointment Reminder - Tomorrow",
            "body": generate_reminder_email(patient, appointment_time, doctor)
        }
    })
    
    # Schedule 2-hour reminder
    final_reminder = appointment_time - timedelta(hours=2)
    schedule_task({
        "name": f"2h Reminder - Patient {patient_id}",
        "task_type": "sms",
        "scheduled_time": final_reminder,
        "payload": {
            "phone_number": patient.phone,
            "message": f"Reminder: Your appointment with {doctor.name} is in 2 hours."
        }
    })
```

### Post-Visit Follow-ups
```python
def complete_visit(patient_id, visit_date):
    # ... visit completion logic ...
    
    # Schedule follow-up in 3 days
    followup_date = visit_date + timedelta(days=3)
    schedule_task({
        "name": f"Post-visit Follow-up - Patient {patient_id}",
        "task_type": "sms",
        "scheduled_time": followup_date,
        "payload": {
            "phone_number": patient.phone,
            "message": "How are you feeling after your recent visit? Please call us if you have any concerns."
        },
        "callback_url": f"https://practice-system.com/followup-sent/{patient_id}"
    })
```

This TaskManager system provides a robust, scalable solution for any application that needs reliable task scheduling and execution with comprehensive monitoring capabilities.
