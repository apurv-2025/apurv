# AI Agent Integration for PatientPortal

## Overview

The PatientPortal has been enhanced with comprehensive AI Agent capabilities, providing intelligent assistance for patients to manage their health information, appointments, medications, and more. This integration follows the same architecture pattern as AgenticClaimsProcessing and Scheduling2.0, ensuring consistency across the healthcare platform.

## Features

### 🤖 AI Health Assistant
- **Intelligent Chat Interface**: Natural language conversations with AI about health topics
- **Context-Aware Responses**: AI understands patient portal context and provides relevant assistance
- **Multi-Modal Support**: Text-based chat with enhanced features and tool suggestions

### 📅 Appointment Management
- **Smart Scheduling**: AI-powered appointment booking with availability checking
- **Recommendation Engine**: Suggests optimal appointment times and doctor preferences
- **Follow-up Coordination**: Automated follow-up appointment scheduling

### 💊 Medication Management
- **Medication Tracking**: Real-time medication status and refill monitoring
- **Smart Reminders**: AI-configured medication reminders and alerts
- **Interaction Checking**: Drug interaction analysis and safety recommendations

### 🧪 Lab Results Analysis
- **AI Interpretation**: Intelligent analysis and explanation of lab results
- **Trend Analysis**: Historical comparison and health trend identification
- **Personalized Insights**: Customized recommendations based on results

### 👨‍⚕️ Doctor Finder
- **Specialist Search**: Find doctors by specialty, location, and availability
- **Rating Integration**: Doctor ratings and patient reviews
- **Insurance Compatibility**: Filter by insurance acceptance

### 📊 Health Summary Generation
- **Comprehensive Reports**: AI-generated health summaries with insights
- **Trend Analysis**: Health metrics tracking over time
- **Recommendation Engine**: Personalized health recommendations

## Architecture

### Backend Components

#### 1. Agentic Integration (`agentic_integration.py`)
```python
class AgenticPatientPortal:
    """Main class that integrates Agentic Core with Patient Portal"""
    
    async def chat_with_patient_data(self, message, user_id, context)
    async def schedule_appointment_ai(self, patient_id, appointment_type, preferred_date)
    async def check_medications_ai(self, patient_id)
    async def analyze_lab_results_ai(self, patient_id, lab_result_id)
    async def generate_health_summary_ai(self, patient_id, report_type)
    async def setup_medication_reminder_ai(self, patient_id, medication_id, reminder_time)
    async def find_doctors_ai(self, specialty, location)
```

#### 2. AI Tools
- **AppointmentSchedulingTool**: Smart appointment booking
- **MedicationCheckTool**: Medication status and refill management
- **LabResultsTool**: Lab result analysis and interpretation
- **HealthSummaryTool**: Comprehensive health report generation
- **MedicationReminderTool**: Reminder configuration
- **DoctorFinderTool**: Doctor search and booking

#### 3. API Routes (`routers/agent.py`)
```python
@router.post("/chat")                    # Chat with AI
@router.post("/schedule-appointment")     # Schedule appointments
@router.post("/check-medications")        # Check medications
@router.post("/analyze-lab-results")      # Analyze lab results
@router.post("/generate-health-summary")  # Generate health summary
@router.post("/setup-medication-reminder") # Set up reminders
@router.post("/find-doctors")             # Find doctors
@router.get("/tools")                     # List available tools
@router.get("/health")                    # Health status
@router.get("/metrics")                   # Performance metrics
```

### Frontend Components

#### 1. Main Agent Page (`components/Agent.jsx`)
- Unified interface for all AI agent functionality
- Tabbed navigation between chat and dashboard
- Quick action buttons and health insights

#### 2. Chat Components
- **AgentChat**: Basic chat interface with message history
- **EnhancedAgentChat**: Advanced chat with tool suggestions and context awareness

#### 3. Dashboard (`components/agent/AgentDashboard.jsx`)
- Health metrics and AI performance data
- Real-time insights and recommendations
- Activity tracking and tool usage statistics

#### 4. Service Layer (`services/agentService.js`)
```javascript
class AgentService {
  async chat(message, userId, context)
  async scheduleAppointment(patientId, appointmentType, preferredDate)
  async checkMedications(patientId)
  async analyzeLabResults(patientId, labResultId)
  async generateHealthSummary(patientId, reportType)
  async findDoctors(specialty, location)
  // ... additional methods
}
```

## Data Models

### Agent Schemas (`schemas/agent.py`)
```python
class TaskType(str, Enum):
    CHAT = "chat"
    SCHEDULE_APPOINTMENT = "schedule_appointment"
    CHECK_MEDICATIONS = "check_medications"
    VIEW_LAB_RESULTS = "view_lab_results"
    GENERATE_HEALTH_SUMMARY = "generate_health_summary"
    SETUP_MEDICATION_REMINDER = "setup_medication_reminder"
    FIND_DOCTOR = "find_doctor"

class AgentRequest(BaseModel):
    task_type: TaskType
    user_id: str
    task_description: str
    context: Optional[Dict[str, Any]]

class AgentResponse(BaseModel):
    task_id: str
    task_type: TaskType
    status: AgentStatus
    response: str
    result: Optional[Dict[str, Any]]
```

## Installation & Setup

### Backend Setup

1. **Install Dependencies**
```bash
cd PatientPlatform/PatientPortal/backend
pip install -r requirements.txt
```

2. **Initialize Agentic Core**
```python
from app.agentic_integration import initialize_agentic_patient_portal

# Initialize with your preferred model provider
initialize_agentic_patient_portal(
    model_provider="openai",  # or "anthropic", "mock"
    api_key="your-api-key",
    database_url="your-database-url"
)
```

3. **Start the Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd PatientPlatform/PatientPortal/frontend
npm install
```

2. **Configure Environment**
```bash
# .env
REACT_APP_API_URL=http://localhost:8000
```

3. **Start Development Server**
```bash
npm start
```

## Usage Examples

### Chat with AI Assistant
```javascript
import agentService from '../services/agentService';

// Basic chat
const response = await agentService.chat(
  "I need to schedule an appointment",
  "user123",
  { patient_portal: true }
);

// Enhanced chat with context
const response = await agentService.chat(
  "Check my medication refills",
  "user123",
  { 
    patient_portal: true,
    include_refills: true,
    include_interactions: true
  }
);
```

### Schedule Appointment
```javascript
const appointment = await agentService.scheduleAppointment(
  "patient123",
  "annual_physical",
  "2024-02-15T10:00:00Z"
);
```

### Check Medications
```javascript
const medications = await agentService.checkMedications("patient123");
console.log(medications.result.medications);
```

### Analyze Lab Results
```javascript
const analysis = await agentService.analyzeLabResults("patient123", "lab_001");
console.log(analysis.result.lab_results[0].ai_interpretation);
```

### Generate Health Summary
```javascript
const summary = await agentService.generateHealthSummary(
  "patient123",
  "comprehensive"
);
console.log(summary.result.health_summary.ai_insights);
```

## API Endpoints

### Chat & Tasks
- `POST /agent/chat` - Chat with AI assistant
- `POST /agent/tasks` - Create agent tasks
- `GET /agent/tasks/{task_id}/status` - Get task status
- `GET /agent/tasks/active` - Get active tasks

### Health Management
- `POST /agent/schedule-appointment` - Schedule appointments
- `POST /agent/check-medications` - Check medications
- `POST /agent/analyze-lab-results` - Analyze lab results
- `POST /agent/generate-health-summary` - Generate health summary
- `POST /agent/setup-medication-reminder` - Set up reminders
- `POST /agent/find-doctors` - Find doctors

### System Management
- `GET /agent/tools` - List available tools
- `GET /agent/health` - Health status
- `GET /agent/metrics` - Performance metrics
- `GET /agent/conversation-history/{user_id}` - Get conversation history
- `DELETE /agent/conversations/{user_id}` - Clear conversation history

## Configuration

### Environment Variables
```bash
# AI Model Configuration
AI_MODEL_PROVIDER=openai  # openai, anthropic, mock
AI_API_KEY=your-api-key
AI_MODEL_NAME=gpt-4

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/patientportal

# Application Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
DEBUG=True
```

### Model Providers
The system supports multiple AI model providers:

1. **OpenAI** (Default)
   - Models: GPT-4, GPT-3.5-turbo
   - Features: Full conversation support, tool calling

2. **Anthropic**
   - Models: Claude-3, Claude-2
   - Features: Advanced reasoning, safety features

3. **Mock** (Development)
   - Models: Simulated responses
   - Features: Fast development, no API costs

## Security & Privacy

### Data Protection
- All patient data is encrypted in transit and at rest
- AI interactions are logged for audit purposes
- Personal health information is anonymized in logs
- HIPAA-compliant data handling

### Access Control
- User authentication required for all AI interactions
- Role-based access control for different features
- Session management and timeout handling
- API rate limiting to prevent abuse

## Monitoring & Analytics

### Health Monitoring
- Real-time system health checks
- AI model performance monitoring
- Database connection status
- Tool availability tracking

### Performance Metrics
- Response time tracking
- Success rate monitoring
- User engagement analytics
- Tool usage statistics

### Error Handling
- Comprehensive error logging
- Graceful degradation for AI failures
- User-friendly error messages
- Automatic retry mechanisms

## Development

### Adding New Tools
1. Create tool class in `agentic_integration.py`
2. Add tool to `_register_tools()` method
3. Create API endpoint in `routers/agent.py`
4. Add frontend service method
5. Update UI components

### Testing
```bash
# Backend tests
cd backend
pytest tests/test_agent.py

# Frontend tests
cd frontend
npm test
```

### Mock Mode
For development without API costs:
```python
# Backend
initialize_agentic_patient_portal(model_provider="mock")

# Frontend
const response = await agentService.mockChat(message, userId);
```

## Troubleshooting

### Common Issues

1. **AI Model Not Responding**
   - Check API key configuration
   - Verify model provider settings
   - Check network connectivity

2. **Database Connection Issues**
   - Verify database URL
   - Check database server status
   - Review connection pool settings

3. **Frontend Not Loading**
   - Check API URL configuration
   - Verify CORS settings
   - Review browser console for errors

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features
- Voice interaction support
- Image analysis for medical documents
- Predictive health analytics
- Integration with wearable devices
- Multi-language support
- Advanced natural language processing

### Scalability Improvements
- Microservices architecture
- Load balancing for AI requests
- Caching layer for common queries
- Database sharding for large datasets
- CDN integration for static assets

## Support

For technical support or questions about the AI Agent integration:

1. Check the troubleshooting section
2. Review the API documentation
3. Contact the development team
4. Submit issues through the project repository

## License

This AI Agent integration is part of the PatientPortal project and follows the same licensing terms as the main application. 