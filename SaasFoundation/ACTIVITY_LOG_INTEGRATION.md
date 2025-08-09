# ActivityLog Integration with SaaSFoundation

## Overview

This document describes the complete integration between SaaSFoundation and the ActivityLog service. The integration provides comprehensive activity logging capabilities, automatically tracking all user actions and system events through API calls to the independent ActivityLog service.

## Features

### 🔄 **Automatic Activity Logging**
- Middleware-based automatic logging of all API endpoints
- Configurable activity mappings for different endpoints
- Request/response tracking with metadata
- Error logging and performance monitoring

### 📊 **Comprehensive Activity Tracking**
- User authentication events (login, logout, registration)
- User management activities (profile updates, settings changes)
- Organization management (creation, updates, deletion)
- Subscription and payment activities
- Notification and system events
- Custom activity logging capabilities

### 🔍 **Activity Management**
- Activity viewing and filtering
- Activity summaries and statistics
- Export capabilities (JSON, CSV)
- Health monitoring and error handling

## Architecture

### Service Integration
```
SaaSFoundation (Port 8000) ←→ ActivityLog Service (Port 8001)
     │                              │
     ├── HTTP API Calls            ├── Activity Storage
     ├── Middleware Logging        ├── Event Processing
     ├── Activity Management       └── Data Retrieval
     └── Health Monitoring
```

### Components

#### 1. ActivityLogService (`app/services/activity_log.py`)
- **Purpose**: Core service for communicating with ActivityLog service
- **Features**:
  - HTTP client for ActivityLog API calls
  - Specific logging methods for different activity types
  - Error handling and retry logic
  - Health checking capabilities

#### 2. ActivityLoggingMiddleware (`app/middleware/activity_logging.py`)
- **Purpose**: Automatic logging of all API requests
- **Features**:
  - Request/response interception
  - Activity mapping for different endpoints
  - Performance tracking
  - Error logging
  - Configurable exclusions

#### 3. Activity Log API (`app/api/v1/endpoints/activity_log.py`)
- **Purpose**: API endpoints for activity management
- **Features**:
  - Activity viewing and filtering
  - Statistics and summaries
  - Export functionality
  - Health monitoring

## API Endpoints

### Activity Management

#### Get Activity Events
```http
GET /api/v1/activity-log/activities
```

**Query Parameters:**
- `event_type` (optional): Filter by event type
- `event_category` (optional): Filter by event category
- `date_range` (optional): Date range filter (default: "all")
- `search` (optional): Search in event descriptions
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Number of records to return (default: 100, max: 1000)

**Response:**
```json
[
  {
    "id": "event-123",
    "date": "2024-01-15",
    "time": "14:30:00",
    "event": "User login",
    "eventType": "user_login_success",
    "ipAddress": "192.168.1.100",
    "location": "New York, NY",
    "userId": "user-123",
    "details": {
      "email": "user@example.com",
      "success": true
    }
  }
]
```

#### Get Activity Summary
```http
GET /api/v1/activity-log/activities/summary
```

**Response:**
```json
{
  "total_events": 150,
  "event_types": {
    "user_login_success": 45,
    "profile_update": 23,
    "organization_creation": 12
  },
  "event_categories": {
    "authentication": 67,
    "user_management": 34,
    "organization_management": 15
  },
  "latest_activity": {
    "id": "event-123",
    "event": "User login",
    "date": "2024-01-15"
  },
  "user_id": "user-123"
}
```

#### Get Activity Statistics
```http
GET /api/v1/activity-log/activities/stats?period=7d
```

**Response:**
```json
{
  "period": "7d",
  "total_events": 150,
  "avg_daily_events": 21.43,
  "unique_days": 7,
  "event_types": {
    "user_login_success": 45,
    "profile_update": 23
  },
  "event_categories": {
    "authentication": 67,
    "user_management": 34
  },
  "daily_activity": {
    "2024-01-15": 25,
    "2024-01-14": 22
  },
  "user_id": "user-123",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

#### Export Activities
```http
GET /api/v1/activity-log/activities/export?format=json
GET /api/v1/activity-log/activities/export?format=csv
```

#### Log Custom Activity
```http
POST /api/v1/activity-log/activities/log
```

**Request Body:**
```json
{
  "event_type": "custom_event",
  "event_category": "custom",
  "event_description": "Custom activity description",
  "event_metadata": {
    "custom_field": "custom_value",
    "timestamp": "2024-01-15T14:30:00Z"
  }
}
```

#### Check Health
```http
GET /api/v1/activity-log/activities/health
```

**Response:**
```json
{
  "service": "ActivityLog",
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:00Z",
  "endpoint": "http://localhost:8001"
}
```

## Activity Types

### Authentication Events
- `user_registration_success` / `user_registration_failed`
- `user_login_success` / `user_login_failed`
- `user_logout`
- `token_refresh`

### User Management Events
- `profile_view`
- `profile_update_success` / `profile_update_failed`
- `profile_deletion`

### Organization Management Events
- `organization_creation_success` / `organization_creation_failed`
- `organization_list`
- `organization_view`
- `organization_update_success` / `organization_update_failed`
- `organization_deletion`

### Subscription Management Events
- `subscription_creation_success` / `subscription_creation_failed`
- `subscription_list`
- `subscription_view`
- `subscription_update_success` / `subscription_update_failed`
- `subscription_cancellation_success` / `subscription_cancellation_failed`

### Payment Processing Events
- `payment_processing_success` / `payment_processing_failed`
- `payment_list`
- `payment_view`

### Invoice Management Events
- `invoice_generation_success` / `invoice_generation_failed`
- `invoice_list`
- `invoice_view`

### Notification Events
- `notification_sent_success` / `notification_sent_failed`
- `notification_list`

### Pricing Events
- `pricing_view`
- `pricing_plans_view`

## Configuration

### Environment Variables

```bash
# ActivityLog Service Configuration
ACTIVITY_LOG_URL=http://localhost:8001

# Optional: Custom configuration
ACTIVITY_LOG_TIMEOUT=30
ACTIVITY_LOG_RETRY_ATTEMPTS=3
ACTIVITY_LOG_ENABLED=true
```

### Middleware Configuration

The ActivityLoggingMiddleware can be configured with:

```python
# Excluded paths (not logged)
excluded_paths = {
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
    "/static",
    "/api/v1/health"
}

# Activity mappings for different endpoints
activity_mappings = {
    "POST /api/v1/auth/login": {
        "event_type": "user_login",
        "event_category": "authentication",
        "description_template": "User login attempt"
    }
    # ... more mappings
}
```

## Usage Examples

### Basic Activity Logging

```python
from app.services.activity_log import activity_logger

# Log user login
await activity_logger.log_user_login(
    user_id="user-123",
    email="user@example.com",
    request=request,
    success=True
)

# Log organization creation
await activity_logger.log_organization_creation(
    user_id="user-123",
    organization_name="Acme Corp",
    organization_id="org-456",
    request=request,
    success=True
)

# Log custom activity
await activity_logger.log_activity(
    event_type="custom_event",
    event_category="custom",
    event_description="Custom activity description",
    user_id="user-123",
    request=request,
    event_metadata={"custom_field": "value"}
)
```

### Retrieving Activities

```python
# Get all activities
activities = await activity_logger.get_activity_events(
    user_id="user-123",
    limit=100
)

# Get filtered activities
filtered_activities = await activity_logger.get_activity_events(
    user_id="user-123",
    event_type="user_login_success",
    date_range="7d"
)
```

### Health Checking

```python
# Check if ActivityLog service is healthy
is_healthy = await activity_logger.health_check()
if not is_healthy:
    logger.warning("ActivityLog service is not responding")
```

## Docker Compose Setup

```yaml
version: '3.8'
services:
  saas-foundation:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ACTIVITY_LOG_URL=http://activity-log:8001
    depends_on:
      - activity-log
      - postgres

  activity-log:
    build: ../../PlatformServices/ActivityLog/backend
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/activitylog
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=saas_foundation
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Testing

### Running Integration Tests

```bash
# Start services
cd SaasFoundation
docker-compose up -d

# Run integration tests
python test_activity_log_integration.py
```

### Test Coverage

The integration tests cover:

1. **Service Health**: Verify both services are running
2. **Activity Logging**: Test custom activity logging
3. **API Endpoint Logging**: Test automatic logging of API calls
4. **Activity Summary**: Test summary and statistics
5. **Activity Export**: Test JSON and CSV export
6. **Activity Filtering**: Test filtering and search
7. **Error Handling**: Test error scenarios
8. **Performance**: Test concurrent requests

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/activity-log/activities/health

# Test activity logging
curl -X POST http://localhost:8000/api/v1/activity-log/activities/log \
  -H "Content-Type: application/json" \
  -H "X-User-ID: test-user" \
  -d '{
    "event_type": "test_event",
    "event_category": "testing",
    "event_description": "Test activity"
  }'

# Test activity retrieval
curl http://localhost:8000/api/v1/activity-log/activities \
  -H "X-User-ID: test-user"
```

## Monitoring and Analytics

### Key Metrics

- **Activity Volume**: Number of activities logged per day
- **Activity Types**: Distribution of different activity types
- **User Engagement**: Activities per user
- **Error Rates**: Failed activity logging attempts
- **Response Times**: ActivityLog service response times

### Health Monitoring

```bash
# Check ActivityLog service health
curl http://localhost:8000/api/v1/activity-log/activities/health

# Check SaaSFoundation health
curl http://localhost:8000/api/v1/health
```

### Log Analysis

Activities can be analyzed for:

- **User Behavior**: Understanding how users interact with the system
- **Security Monitoring**: Detecting suspicious activities
- **Performance Analysis**: Identifying slow operations
- **Compliance**: Meeting audit and compliance requirements

## Security Considerations

### Data Protection
- All sensitive data is filtered before logging
- IP addresses and user agents are logged for security
- Activity metadata is sanitized

### Access Control
- Activities are filtered by user ID
- Admin users can access all activities
- Regular users can only see their own activities

### Privacy Compliance
- Personal data is minimized in logs
- Log retention policies can be configured
- Data export capabilities for user requests

## Troubleshooting

### Common Issues

1. **ActivityLog Service Unavailable**
   - Check if ActivityLog service is running
   - Verify network connectivity
   - Check ACTIVITY_LOG_URL configuration

2. **Activities Not Being Logged**
   - Check middleware configuration
   - Verify excluded paths
   - Check ActivityLog service health

3. **Performance Issues**
   - Monitor ActivityLog service response times
   - Check database performance
   - Consider rate limiting

### Debug Endpoints

```bash
# Check ActivityLog service status
curl http://localhost:8000/api/v1/activity-log/activities/health

# Check recent activities
curl http://localhost:8000/api/v1/activity-log/activities \
  -H "X-User-ID: test-user"
```

## Future Enhancements

### Planned Features
- Real-time activity streaming
- Advanced analytics dashboard
- Machine learning for anomaly detection
- Integration with external monitoring tools
- Activity-based notifications

### Integration Opportunities
- SIEM (Security Information and Event Management) integration
- Business intelligence tools
- Compliance reporting systems
- User behavior analytics

## Support

For technical support or questions about the ActivityLog integration:

1. Check the API documentation at `/docs`
2. Review the activity logs
3. Run the integration tests
4. Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Compatibility**: SaaSFoundation, ActivityLog Service 