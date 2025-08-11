# Survey Feature Implementation

## Overview

The Patient Portal now includes a comprehensive survey system that allows healthcare providers to collect feedback from patients after visits or AI agent interactions. This feature helps improve patient satisfaction and service quality through systematic feedback collection and analysis.

## Features

### 1. Survey Types
- **Visit Surveys**: Triggered after completed medical appointments
- **AI Chat Surveys**: Triggered after AI agent conversations
- **General Surveys**: General patient satisfaction surveys

### 2. Question Types
- **Rating Questions**: 1-5 star ratings
- **Multiple Choice**: Predefined options
- **Text Questions**: Open-ended responses
- **Yes/No Questions**: Binary responses

### 3. Survey Management
- Create and manage surveys
- View survey responses and analytics
- Export survey data
- Track response rates and satisfaction scores

## Backend Implementation

### Database Schema

#### Surveys Table
```sql
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    survey_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Survey Questions Table
```sql
CREATE TABLE survey_questions (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    options JSONB,
    required BOOLEAN DEFAULT TRUE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### Survey Responses Table
```sql
CREATE TABLE survey_responses (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL REFERENCES surveys(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id) ON DELETE SET NULL,
    conversation_id VARCHAR(255),
    response_data JSONB NOT NULL,
    overall_rating FLOAT CHECK (overall_rating >= 1 AND overall_rating <= 5),
    feedback_text TEXT,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

#### Survey Management
- `POST /surveys/` - Create a new survey
- `GET /surveys/` - Get all surveys
- `GET /surveys/active` - Get active surveys
- `GET /surveys/{survey_id}` - Get survey with questions
- `PUT /surveys/{survey_id}` - Update survey
- `DELETE /surveys/{survey_id}` - Delete survey

#### Survey Questions
- `POST /surveys/{survey_id}/questions` - Add question to survey
- `GET /surveys/{survey_id}/questions` - Get survey questions
- `PUT /surveys/questions/{question_id}` - Update question
- `DELETE /surveys/questions/{question_id}` - Delete question

#### Survey Responses
- `POST /surveys/responses` - Submit survey response
- `GET /surveys/responses` - Get survey responses
- `GET /surveys/responses/{response_id}` - Get specific response
- `PUT /surveys/responses/{response_id}` - Update response

#### Survey Analytics
- `GET /surveys/{survey_id}/analytics` - Get survey analytics
- `GET /surveys/eligibility/{survey_type}` - Check survey eligibility
- `POST /surveys/trigger` - Trigger survey for user

#### Survey Templates
- `POST /surveys/templates/visit` - Create visit survey template
- `POST /surveys/templates/ai-chat` - Create AI chat survey template

## Frontend Implementation

### Components

#### Survey.jsx
Main survey component that handles:
- Loading survey questions
- Rendering different question types
- Form validation
- Response submission

#### SurveyModal.jsx
Modal wrapper for surveys that provides:
- Modal overlay
- Completion confirmation
- Auto-close functionality

#### SurveyManagement.jsx
Administrative interface for:
- Viewing all surveys
- Analyzing responses
- Managing survey settings
- Exporting data

### Integration Points

#### AI Agent Chat (EnhancedAgentChat.jsx)
- Automatically triggers surveys after 5+ messages
- Manual survey trigger via "Feedback" button
- Tracks conversation ID for survey responses
- Shows thank you message after survey completion

#### Appointments (EnhancedAppointments.jsx)
- Shows survey button for completed appointments
- Tracks appointment ID for survey responses
- Marks surveys as completed
- Prevents duplicate surveys for same appointment

### Survey Service (surveyService.js)
Centralized service for all survey-related API calls:
- Survey CRUD operations
- Response submission
- Analytics retrieval
- Eligibility checking

## Usage Examples

### Creating a Visit Survey Template
```javascript
// Backend API call
POST /surveys/templates/visit

// Creates a survey with questions:
// 1. Overall experience rating
// 2. Doctor care satisfaction
// 3. Wait time satisfaction
// 4. Staff satisfaction
// 5. Recommendation likelihood
// 6. Additional comments
```

### Triggering a Survey
```javascript
// Check eligibility
const eligibility = await surveyService.checkSurveyEligibility(
  'visit', 
  appointmentId, 
  null
);

if (eligibility.eligible) {
  // Show survey modal
  setShowSurveyModal(true);
}
```

### Submitting a Response
```javascript
const responseData = {
  survey_id: survey.id,
  response_data: {
    "1": 5,  // Question ID: Rating
    "2": 4,  // Question ID: Rating
    "3": true,  // Question ID: Yes/No
    "4": "Great experience!"  // Question ID: Text
  },
  overall_rating: 4.5,
  feedback_text: "Very satisfied with the service",
  appointment_id: appointmentId,
  conversation_id: conversationId
};

await surveyService.submitSurveyResponse(responseData);
```

## Configuration

### Survey Triggers
- **Visit Surveys**: Automatically available after appointment completion
- **AI Chat Surveys**: Triggered after 5+ messages or manually
- **General Surveys**: Available on-demand

### Survey Settings
- **Active/Inactive**: Control survey availability
- **Required Questions**: Mark questions as mandatory
- **Question Order**: Control question sequence
- **Response Validation**: Ensure data quality

## Analytics and Reporting

### Key Metrics
- **Response Rate**: Percentage of eligible patients who completed surveys
- **Average Rating**: Overall satisfaction score
- **Question Analytics**: Individual question performance
- **Trend Analysis**: Satisfaction trends over time

### Export Options
- **CSV Export**: Raw response data
- **Analytics Report**: Summary statistics
- **Trend Report**: Time-based analysis

## Security and Privacy

### Data Protection
- Survey responses are linked to user accounts
- Personal information is not collected in surveys
- Responses are anonymized for analytics
- Access controls for survey management

### Compliance
- HIPAA-compliant data handling
- Patient consent for survey participation
- Secure data transmission and storage
- Audit trails for survey access

## Future Enhancements

### Planned Features
1. **Survey Templates**: Pre-built survey designs
2. **Conditional Logic**: Dynamic question flow
3. **Multi-language Support**: Internationalization
4. **Advanced Analytics**: Machine learning insights
5. **Integration APIs**: Third-party survey tools
6. **Mobile Optimization**: Enhanced mobile experience

### Technical Improvements
1. **Real-time Analytics**: Live dashboard updates
2. **Automated Reports**: Scheduled report generation
3. **API Rate Limiting**: Performance optimization
4. **Caching**: Improved response times
5. **Webhook Support**: External system integration

## Troubleshooting

### Common Issues

#### Survey Not Loading
- Check survey eligibility
- Verify survey is active
- Ensure user authentication

#### Response Submission Fails
- Validate required fields
- Check network connectivity
- Verify API endpoint availability

#### Analytics Not Updating
- Refresh data manually
- Check database connectivity
- Verify calculation logic

### Debug Mode
Enable debug logging for detailed error information:
```javascript
// Frontend
localStorage.setItem('surveyDebug', 'true');

// Backend
logging.getLogger('survey').setLevel('DEBUG')
```

## Support

For technical support or feature requests, please contact the development team or create an issue in the project repository. 