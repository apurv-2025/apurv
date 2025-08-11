# AI Assistant Integration for Prior Authorization System

## Overview

This document describes the integration of an AI assistant into the Prior Authorization system, based on the agentic-core framework and following the pattern established in the Insurance Verification system. The AI assistant provides intelligent automation and natural language interaction for prior authorization workflows.

## Architecture

### Integration Components

1. **Agentic Integration Service** (`app/services/agentic_integration.py`)
   - Real integration with agentic-core framework
   - Custom prior authorization tools
   - Fallback to mock implementation if agentic-core is unavailable

2. **AI API Endpoints** (`app/api/api_v1/endpoints/agent.py`)
   - RESTful API endpoints for AI assistant functionality
   - Chat, tool execution, and management capabilities

3. **React Frontend Component** (`frontend/src/components/AIAssistant.jsx`)
   - Floating chat widget
   - Real-time conversation interface
   - Example suggestions and tool integration

4. **Custom AI Tools**
   - Prior authorization creation
   - Status checking
   - EDI generation
   - Patient lookup
   - Code lookup

## AI Assistant Features

### 🤖 Natural Language Processing
- **Chat Interface**: Natural language conversations about prior authorization
- **Context Awareness**: Maintains conversation context and history
- **Multi-turn Dialogues**: Handles complex multi-step workflows

### 🛠️ Custom Tools Integration

#### 1. Prior Authorization Tool
- **Name**: `create_prior_authorization`
- **Purpose**: Create new prior authorization requests
- **Parameters**: patient_id, provider_npi, procedure_codes, diagnosis_codes, service_date, medical_necessity

#### 2. Authorization Status Tool
- **Name**: `check_authorization_status`
- **Purpose**: Check status of authorization requests
- **Parameters**: request_id

#### 3. EDI Generation Tool
- **Name**: `generate_edi`
- **Purpose**: Generate EDI 278/275 documents
- **Parameters**: edi_type, patient_id, request_id, provider_npi, service_date, birth_date, gender

#### 4. Patient Lookup Tool
- **Name**: `lookup_patient`
- **Purpose**: Lookup patient information
- **Parameters**: patient_id, member_id

#### 5. Code Lookup Tool
- **Name**: `lookup_codes`
- **Purpose**: Find healthcare codes
- **Parameters**: code_type, search_term, code

### 📊 Workflow Automation
- **Complex Workflows**: Multi-step prior authorization processes
- **Batch Operations**: Handle multiple requests efficiently
- **Error Recovery**: Graceful handling of failures

## API Endpoints

### Chat Endpoints

- `POST /api/v1/agent/chat` - Chat with AI assistant
- `GET /api/v1/agent/conversations/{user_id}` - Get conversation history
- `DELETE /api/v1/agent/conversations/{conversation_id}` - Delete conversation

### Tool Endpoints

- `POST /api/v1/agent/create-prior-auth` - Create prior authorization request
- `POST /api/v1/agent/check-status` - Check authorization status
- `POST /api/v1/agent/generate-edi` - Generate EDI documents
- `POST /api/v1/agent/lookup-patient` - Lookup patient information
- `POST /api/v1/agent/lookup-codes` - Lookup healthcare codes
- `POST /api/v1/agent/complex-workflow` - Process complex workflows

### Management Endpoints

- `GET /api/v1/agent/tools` - Get available tools
- `GET /api/v1/agent/health` - Check AI assistant health
- `GET /api/v1/agent/examples` - Get example interactions

## Frontend Integration

### React Component Features

1. **Floating Chat Widget**
   - Always-available chat interface
   - Minimizable and expandable
   - Responsive design

2. **Real-time Messaging**
   - Live message updates
   - Typing indicators
   - Message timestamps

3. **Example Suggestions**
   - Pre-built example queries
   - Quick-start interactions
   - Contextual suggestions

4. **Conversation Management**
   - Clear conversation history
   - Message count tracking
   - Persistent user sessions

### Usage Example

```jsx
import AIAssistant from './components/AIAssistant';

function App() {
  return (
    <div>
      {/* Your app content */}
      <AIAssistant />
    </div>
  );
}
```

## Configuration

### Environment Variables

```bash
# AI Model Configuration
AI_MODEL_PROVIDER=openai|anthropic|custom
AI_API_KEY=your_api_key_here

# Database Configuration (for conversation storage)
DATABASE_URL=postgresql://user:pass@localhost/preauth_db

# Application Configuration
DEBUG=true
```

### Agentic Core Integration

The system integrates with the agentic-core framework from `AIFoundation/AgenticFoundation/agentic-core`:

```python
from app.services.agentic_integration import create_agentic_prior_authorization

# Create AI assistant instance
agentic_service = create_agentic_prior_authorization(
    model_provider="openai",
    api_key=os.getenv("AI_API_KEY"),
    database_url=os.getenv("DATABASE_URL")
)
```

## Usage Examples

### 1. Chat with AI Assistant

```bash
curl -X POST http://localhost:8002/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to create a prior authorization for patient John Doe",
    "user_id": "user_123"
  }'
```

### 2. Create Prior Authorization via AI

```bash
curl -X POST http://localhost:8002/api/v1/agent/create-prior-auth \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT123456",
    "provider_npi": "1234567890",
    "procedure_codes": [
      {"code": "99213", "description": "Office visit"}
    ],
    "diagnosis_codes": [
      {"code": "E11.9", "description": "Diabetes", "is_primary": true}
    ],
    "service_date": "2024-01-15",
    "medical_necessity": "Patient requires evaluation"
  }'
```

### 3. Generate EDI Document

```bash
curl -X POST http://localhost:8002/api/v1/agent/generate-edi \
  -H "Content-Type: application/json" \
  -d '{
    "edi_type": "278",
    "patient_id": "PAT123456",
    "request_id": "AUTH123456",
    "provider_npi": "1234567890"
  }'
```

### 4. Lookup Healthcare Codes

```bash
curl -X POST http://localhost:8002/api/v1/agent/lookup-codes \
  -H "Content-Type: application/json" \
  -d '{
    "code_type": "procedure",
    "search_term": "office visit"
  }'
```

## Testing

### Run AI Integration Tests

```bash
# Test AI assistant functionality
python3 test_ai_integration.py
```

### Manual Testing

```bash
# Test AI health
curl http://localhost:8002/api/v1/agent/health

# Test available tools
curl http://localhost:8002/api/v1/agent/tools

# Test examples
curl http://localhost:8002/api/v1/agent/examples
```

## Error Handling

### Graceful Degradation

The AI assistant includes fallback mechanisms:

1. **Agentic Core Unavailable**: Falls back to mock implementation
2. **API Errors**: Returns meaningful error messages
3. **Network Issues**: Handles connection failures gracefully
4. **Invalid Input**: Validates and provides helpful feedback

### Error Response Format

```json
{
  "success": false,
  "error": "Error description",
  "response": "User-friendly error message"
}
```

## Performance Considerations

### Optimization Strategies

1. **Async Processing**: All AI operations are asynchronous
2. **Connection Pooling**: Efficient HTTP client usage
3. **Caching**: Conversation history and tool results
4. **Rate Limiting**: Respect API rate limits

### Monitoring

- Health check endpoints for AI assistant status
- Performance metrics for response times
- Error tracking and logging
- Usage analytics

## Security

### Data Protection

1. **Input Validation**: All user inputs are validated
2. **API Key Management**: Secure handling of AI API keys
3. **User Isolation**: Conversation history per user
4. **Data Encryption**: Sensitive data encryption in transit

### Access Control

- User authentication for conversation history
- API rate limiting
- Input sanitization
- Output filtering

## Integration with Existing Systems

### Prior Authorization Integration

The AI assistant integrates seamlessly with existing Prior Authorization functionality:

1. **Patient Microservice**: Uses patient data from integrated microservice
2. **EDI Services**: Leverages existing EDI 275/278 generation
3. **Code Management**: Uses existing healthcare code systems
4. **Database**: Integrates with existing authorization data

### Agentic Core Integration

Based on the Insurance Verification pattern, the integration includes:

1. **Real Agentic Integration**: Direct integration with agentic-core
2. **Fallback Support**: Mock implementation when agentic-core unavailable
3. **Custom Tools**: Prior authorization specific tools
4. **Error Handling**: Comprehensive error management

## Future Enhancements

### Planned Features

1. **Advanced NLP**: Better understanding of medical terminology
2. **Multi-language Support**: Support for multiple languages
3. **Voice Interface**: Voice-to-text and text-to-speech
4. **Advanced Analytics**: Usage patterns and optimization insights
5. **Integration APIs**: Connect with external AI services

### Scalability Improvements

1. **Microservice Architecture**: Separate AI service deployment
2. **Load Balancing**: Distribute AI requests across instances
3. **Caching Layer**: Redis caching for frequent queries
4. **Queue System**: Async processing for complex workflows

## Troubleshooting

### Common Issues

1. **Agentic Core Not Available**
   - Check if agentic-core is properly installed
   - Verify path configuration
   - Check import errors

2. **API Key Issues**
   - Verify AI_API_KEY environment variable
   - Check API key validity
   - Ensure proper permissions

3. **Database Connection**
   - Verify DATABASE_URL configuration
   - Check database connectivity
   - Ensure proper schema

4. **Frontend Issues**
   - Check API endpoint availability
   - Verify CORS configuration
   - Check browser console for errors

### Debug Commands

```bash
# Check AI assistant health
curl http://localhost:8002/api/v1/agent/health

# Test basic chat functionality
curl -X POST http://localhost:8002/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'

# Check available tools
curl http://localhost:8002/api/v1/agent/tools

# View service logs
docker logs preauth_backend
```

## Conclusion

The AI assistant integration provides:

- ✅ **Intelligent Automation**: AI-powered prior authorization workflows
- ✅ **Natural Language Interface**: Conversational interaction with the system
- ✅ **Custom Tools**: Prior authorization specific AI capabilities
- ✅ **Seamless Integration**: Works with existing Prior Authorization system
- ✅ **Graceful Degradation**: Fallback support when AI services unavailable
- ✅ **Comprehensive Testing**: Full test coverage for AI functionality
- ✅ **Modern UI**: React-based chat interface
- ✅ **Scalable Architecture**: Ready for production deployment

This integration transforms the Prior Authorization system into an intelligent, user-friendly platform that leverages AI to streamline healthcare workflows. 