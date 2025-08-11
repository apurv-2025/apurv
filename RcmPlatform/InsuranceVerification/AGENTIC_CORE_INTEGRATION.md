# Agentic Core Integration with InsuranceVerification

## Overview

This document describes the integration between InsuranceVerification and the Agentic Core framework from ClaimsProcessing. The integration provides AI-powered capabilities for insurance verification, eligibility checks, document analysis, and EDI processing.

## Architecture

### Integration Components

1. **Real Agentic Integration** (`real_agentic_integration.py`)
   - Direct integration with the actual AgenticCore from ClaimsProcessing
   - Custom insurance-specific tools
   - Fallback to mock implementation if agentic-core is unavailable

2. **Mock Agentic Integration** (`agentic_integration.py`)
   - Standalone mock implementation for development/testing
   - Used as fallback when real agentic-core is not available

3. **API Endpoints** (`agent.py`)
   - RESTful API endpoints for AI agent functionality
   - Chat, verification, extraction, and analysis capabilities

4. **Frontend Components**
   - AgentPage: Main AI agent interface
   - AgentChat: Chat interface with AI assistant
   - AgentTools: Tool-based interface for specific tasks
   - AgentDashboard: Analytics and metrics dashboard

## Features

### AI Agent Capabilities

1. **Insurance Verification**
   - Verify coverage and eligibility
   - Check multiple service types
   - Real-time coverage details

2. **Document Analysis**
   - Extract insurance information from cards/documents
   - OCR and image processing
   - Confidence scoring

3. **Eligibility Checks**
   - Patient eligibility verification
   - Service-specific checks
   - Authorization requirements

4. **EDI Analysis**
   - 270/271 transaction analysis
   - EDI validation and parsing
   - Transaction monitoring

5. **AI Chat Assistant**
   - Natural language processing
   - Context-aware responses
   - Conversation history

### Tools Integration

The integration includes four custom tools for the AgenticCore:

1. **InsuranceVerificationTool**
   - Name: `verify_insurance`
   - Purpose: Verify insurance coverage and eligibility
   - Parameters: member_id, provider_npi, service_type

2. **InsuranceExtractionTool**
   - Name: `extract_insurance_info`
   - Purpose: Extract information from documents
   - Parameters: file_path, file_type

3. **EligibilityCheckTool**
   - Name: `check_eligibility`
   - Purpose: Check patient eligibility
   - Parameters: member_id, service_type, provider_npi

4. **EDIAnalysisTool**
   - Name: `analyze_edi`
   - Purpose: Analyze EDI transactions
   - Parameters: edi_content, transaction_type

## API Endpoints

### Chat Endpoints

- `POST /api/v1/agent/chat` - Chat with AI assistant
- `GET /api/v1/agent/conversations/{user_id}` - Get conversation history
- `DELETE /api/v1/agent/conversations/{conversation_id}` - Delete conversation

### Tool Endpoints

- `POST /api/v1/agent/verify-insurance` - Verify insurance coverage
- `POST /api/v1/agent/extract-insurance-info` - Extract document information
- `POST /api/v1/agent/check-eligibility` - Check patient eligibility
- `POST /api/v1/agent/analyze-edi` - Analyze EDI transactions
- `POST /api/v1/agent/complex-verification` - Multi-service verification

### Management Endpoints

- `GET /api/v1/agent/tools` - List available tools
- `GET /api/v1/agent/health` - Check agent health
- `GET /api/v1/agent/metrics` - Get performance metrics
- `POST /api/v1/agent/batch-verification` - Batch verification

## Installation and Setup

### Prerequisites

1. **Agentic Core Access**
   - Ensure AIFoundation/AgenticFoundation/agentic-core is available
   - Set up proper Python path to include agentic-core

2. **Dependencies**
   ```bash
   pip install httpx==0.25.2 openai==1.3.7 anthropic==0.7.7
   ```

3. **Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   export DATABASE_URL="your-database-url"
   ```

### Configuration

The integration automatically detects if AgenticCore is available:

- **Available**: Uses real AgenticCore with custom tools
- **Unavailable**: Falls back to mock implementation

### Force Mock Mode

To force mock implementation (for development/testing):

```python
from app.services.real_agentic_integration import create_agentic_insurance_verification

agentic = create_agentic_insurance_verification(force_mock=True)
```

## Usage Examples

### Basic Chat

```python
from app.services.real_agentic_integration import agentic_insurance_verification

# Chat with AI assistant
response = await agentic_insurance_verification.chat_with_insurance_data(
    message="Can you verify insurance for member 123456789?",
    user_id="user-123"
)
print(response["response"])
```

### Insurance Verification

```python
# Verify insurance coverage
result = await agentic_insurance_verification.verify_insurance_coverage(
    member_id="123456789",
    provider_npi="1234567890",
    service_type="30"
)

if result["success"]:
    coverage = result["result"]
    print(f"Eligible: {coverage['is_eligible']}")
    print(f"Deductible: {coverage['coverage_details']['deductible']}")
```

### Document Extraction

```python
# Extract insurance information
result = await agentic_insurance_verification.extract_insurance_information(
    file_path="/uploads/insurance_card.jpg",
    file_type="image"
)

if result["success"]:
    info = result["result"]["extracted_info"]
    print(f"Member ID: {info['member_id']}")
    print(f"Plan: {info['plan_name']}")
```

### EDI Analysis

```python
# Analyze EDI transaction
edi_content = "ISA*00*...~GS*HS*..."
result = await agentic_insurance_verification.analyze_edi_transaction(
    edi_content=edi_content,
    transaction_type="270"
)

if result["success"]:
    analysis = result["result"]["analysis"]
    print(f"Segments found: {analysis['segments_found']}")
```

## Frontend Integration

### Agent Page

The main AI agent interface is available at `/agent` and includes:

- **AI Assistant Tab**: Chat interface with natural language processing
- **AI Tools Tab**: Direct access to specific tools and forms
- **Analytics Tab**: Performance metrics and usage statistics

### Quick Actions

The interface provides quick action buttons for common tasks:

- Verify Coverage
- Extract Info
- Check Eligibility
- Analyze EDI

### Real-time Features

- Live chat with AI assistant
- Real-time tool execution
- Performance monitoring
- Error handling and recovery

## Testing

### Integration Tests

Run the comprehensive test suite:

```bash
cd RcmPlatform/InsuranceVerification
python3 test_agent_integration.py
```

### Test Coverage

The test suite covers:

1. **Service Health**
   - InsuranceVerification service status
   - AI agent health check

2. **Core Functionality**
   - Chat with AI assistant
   - Insurance verification
   - Eligibility checks
   - Document extraction
   - EDI analysis

3. **Advanced Features**
   - Complex verification (multiple services)
   - Batch processing
   - Tool availability
   - Performance metrics

4. **Error Handling**
   - Invalid data handling
   - Service failures
   - Network issues

5. **Performance**
   - Concurrent requests
   - Response times
   - Load testing

## Monitoring and Analytics

### Metrics Available

- Total requests processed
- Success/failure rates
- Average response times
- Tool usage statistics
- User activity patterns

### Health Monitoring

- Agent status monitoring
- Tool availability checks
- Performance alerts
- Error rate tracking

## Troubleshooting

### Common Issues

1. **Agentic Core Not Available**
   - Check if AIFoundation/AgenticFoundation/agentic-core exists
   - Verify Python path configuration
   - Check import statements

2. **API Key Issues**
   - Verify environment variables
   - Check API key validity
   - Ensure proper permissions

3. **Tool Registration Failures**
   - Check tool class definitions
   - Verify BaseTool inheritance
   - Review tool registration process

4. **Performance Issues**
   - Monitor response times
   - Check concurrent request limits
   - Review database connections

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Fallback Mode

If AgenticCore is unavailable, the system automatically falls back to mock implementation with full functionality.

## Security Considerations

1. **API Key Management**
   - Secure storage of API keys
   - Environment variable usage
   - Key rotation policies

2. **Data Privacy**
   - PII handling in insurance data
   - Secure transmission of sensitive information
   - Data retention policies

3. **Access Control**
   - User authentication
   - Role-based permissions
   - API rate limiting

## Future Enhancements

### Planned Features

1. **Advanced AI Models**
   - Multi-modal AI capabilities
   - Enhanced natural language processing
   - Real-time learning

2. **Integration Expansions**
   - Additional insurance providers
   - Real-time eligibility APIs
   - Advanced EDI processing

3. **Performance Optimizations**
   - Caching strategies
   - Async processing improvements
   - Database optimizations

### Roadmap

- **Phase 1**: Basic integration (Current)
- **Phase 2**: Advanced AI capabilities
- **Phase 3**: Real-time provider integration
- **Phase 4**: Predictive analytics

## Support and Maintenance

### Documentation

- API documentation available at `/docs`
- Interactive testing at `/redoc`
- Code examples in test files

### Updates

- Regular dependency updates
- Security patches
- Feature enhancements

### Community

- Issue reporting and tracking
- Feature requests
- Community contributions

## Conclusion

The Agentic Core integration with InsuranceVerification provides a powerful AI-powered platform for insurance verification tasks. The integration is designed to be robust, scalable, and maintainable, with proper fallback mechanisms and comprehensive testing.

The system successfully bridges the gap between traditional insurance verification processes and modern AI capabilities, providing users with intelligent, efficient, and user-friendly tools for managing insurance-related tasks. 