# Notification & TaskManager Integration for Scheduling2.0

## Overview

This document describes the comprehensive notification system integrated with PlatformServices TaskManager for the Scheduling2.0 application. The system supports multiple reminders, email/SMS notifications, and flexible notification preferences.

## Features

### 🔔 **Multiple Reminders**
- Support for multiple reminder times (e.g., 24 hours, 2 hours, 1 hour before appointment)
- Configurable reminder intervals per organization and user
- Google Calendar-style reminder flexibility

### 📧 **Email & SMS Notifications**
- Dual notification channels (Email + SMS)
- Configurable SMTP settings for email
- Support for multiple SMS providers (Twilio, AWS SNS, etc.)
- Template-based messaging system

### ⚙️ **Flexible Settings**
- Organization-level notification settings
- Individual patient/client notification preferences
- Override capabilities for contact information
- Granular control over notification types

### 🔄 **TaskManager Integration**
- Seamless integration with PlatformServices TaskManager
- Automatic task scheduling and execution
- Callback handling for status updates
- Retry mechanisms and error handling

## Architecture

### Database Models

#### NotificationSettings
```sql
-- Organization-level notification configuration
CREATE TABLE notification_settings (
    id SERIAL PRIMARY KEY,
    organization_id UUID NOT NULL,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT TRUE,
    email_smtp_host VARCHAR(255),
    email_smtp_port INTEGER DEFAULT 587,
    email_username VARCHAR(255),
    email_password VARCHAR(255),
    email_from_address VARCHAR(255),
    email_from_name VARCHAR(255),
    sms_provider VARCHAR(50),
    sms_api_key VARCHAR(255),
    sms_api_secret VARCHAR(255),
    sms_from_number VARCHAR(20),
    default_email_reminders JSON DEFAULT '[24, 2]',
    default_sms_reminders JSON DEFAULT '[24, 2]',
    email_templates JSON,
    sms_templates JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### PatientNotificationPreferences
```sql
-- Patient-specific notification preferences
CREATE TABLE patient_notification_preferences (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT TRUE,
    email_reminders JSON DEFAULT '[24, 2]',
    sms_reminders JSON DEFAULT '[24, 2]',
    appointment_confirmation BOOLEAN DEFAULT TRUE,
    appointment_reminder BOOLEAN DEFAULT TRUE,
    appointment_cancellation BOOLEAN DEFAULT TRUE,
    appointment_reschedule BOOLEAN DEFAULT TRUE,
    waitlist_notification BOOLEAN DEFAULT TRUE,
    email_address VARCHAR(255),
    phone_number VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### AppointmentReminder
```sql
-- Individual appointment reminders
CREATE TABLE appointment_reminders (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    reminder_type VARCHAR(10) NOT NULL CHECK (reminder_type IN ('EMAIL', 'SMS', 'BOTH')),
    reminder_time TIMESTAMP WITH TIME ZONE NOT NULL,
    hours_before_appointment INTEGER NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'SENT', 'FAILED', 'CANCELLED')),
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    task_manager_task_id INTEGER,
    task_manager_execution_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### NotificationHistory
```sql
-- Notification delivery tracking
CREATE TABLE notification_history (
    id SERIAL PRIMARY KEY,
    notification_type VARCHAR(10) NOT NULL CHECK (notification_type IN ('EMAIL', 'SMS', 'BOTH')),
    notification_category VARCHAR(20) NOT NULL CHECK (notification_category IN ('CONFIRMATION', 'REMINDER', 'CANCELLATION', 'RESCHEDULE', 'WAITLIST')),
    recipient_type VARCHAR(20) NOT NULL CHECK (recipient_type IN ('PATIENT', 'CLIENT', 'PRACTITIONER')),
    recipient_id INTEGER NOT NULL,
    recipient_email VARCHAR(255),
    recipient_phone VARCHAR(20),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'SENT' CHECK (status IN ('SENT', 'FAILED', 'BOUNCED', 'DELIVERED')),
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    delivered_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    appointment_id INTEGER REFERENCES appointments(id),
    waitlist_entry_id INTEGER REFERENCES waitlist_entries(id),
    task_manager_task_id INTEGER,
    task_manager_execution_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Services

#### TaskManagerIntegration
- Handles communication with PlatformServices TaskManager
- Creates, updates, and monitors tasks
- Manages callback handling

#### NotificationService
- Core notification orchestration
- Manages reminder scheduling and sending
- Handles immediate notifications
- Integrates with TaskManager

#### NotificationSettingsService
- Manages organization and user preferences
- Validates settings and preferences
- Provides effective preference calculation

## API Endpoints

### Notification Settings

#### Organization Settings
```http
POST /api/notifications/settings/
GET /api/notifications/settings/{organization_id}
PUT /api/notifications/settings/{organization_id}
```

#### User Preferences
```http
POST /api/notifications/preferences/patient/
GET /api/notifications/preferences/patient/{patient_id}
PUT /api/notifications/preferences/patient/{patient_id}

POST /api/notifications/preferences/client/
GET /api/notifications/preferences/client/{client_id}
PUT /api/notifications/preferences/client/{client_id}
```

### Appointment Reminders

```http
POST /api/notifications/reminders/appointment/{appointment_id}
GET /api/notifications/reminders/appointment/{appointment_id}
DELETE /api/notifications/reminders/appointment/{appointment_id}
POST /api/notifications/reminders/appointment/{appointment_id}/reschedule
```

### Immediate Notifications

```http
POST /api/notifications/send/appointment/{appointment_id}
```

### Notification History

```http
GET /api/notifications/history/
GET /api/notifications/history/{notification_id}
```

### TaskManager Callbacks

```http
POST /api/notifications/callback/{notification_id}
POST /api/notifications/reminder-callback/{reminder_id}
```

### Templates

```http
GET /api/notifications/templates/{organization_id}
PUT /api/notifications/templates/{organization_id}
```

## Usage Examples

### Setting Up Organization Notifications

```python
# Create organization notification settings
settings_data = {
    "email_enabled": True,
    "sms_enabled": True,
    "email_smtp_host": "smtp.gmail.com",
    "email_smtp_port": 587,
    "email_username": "notifications@clinic.com",
    "email_password": "secure_password",
    "email_from_address": "notifications@clinic.com",
    "email_from_name": "Medical Clinic",
    "sms_provider": "twilio",
    "sms_api_key": "your_twilio_key",
    "sms_api_secret": "your_twilio_secret",
    "sms_from_number": "+1234567890",
    "default_email_reminders": [24, 2, 1],  # 24h, 2h, 1h before
    "default_sms_reminders": [24, 2],       # 24h, 2h before
    "email_templates": {
        "appointment_confirmation": "Your appointment has been confirmed for {date} at {time}.",
        "appointment_reminder": "Reminder: You have an appointment tomorrow at {time}."
    },
    "sms_templates": {
        "appointment_confirmation": "Appt confirmed: {date} at {time}",
        "appointment_reminder": "Reminder: Appt tomorrow at {time}"
    }
}

response = await client.post("/api/notifications/settings/", json=settings_data)
```

### Setting Patient Preferences

```python
# Set patient notification preferences
preferences_data = {
    "email_enabled": True,
    "sms_enabled": True,
    "email_reminders": [24, 2, 1],  # Override organization defaults
    "sms_reminders": [24],          # Only 24h SMS reminder
    "appointment_confirmation": True,
    "appointment_reminder": True,
    "appointment_cancellation": True,
    "appointment_reschedule": True,
    "waitlist_notification": False,  # Disable waitlist notifications
    "email_address": "patient@email.com",  # Override patient's default email
    "phone_number": "+1234567890"   # Override patient's default phone
}

response = await client.post("/api/notifications/preferences/patient/", json=preferences_data)
```

### Scheduling Appointment Reminders

```python
# Schedule reminders for an appointment
reminders_response = await client.post(
    f"/api/notifications/reminders/appointment/{appointment_id}",
    json={"custom_reminders": [24, 2, 1]}  # Optional custom reminder times
)

# Get scheduled reminders
reminders = await client.get(f"/api/notifications/reminders/appointment/{appointment_id}")

# Cancel all reminders for an appointment
await client.delete(f"/api/notifications/reminders/appointment/{appointment_id}")

# Reschedule reminders (e.g., after appointment update)
await client.post(f"/api/notifications/reminders/appointment/{appointment_id}/reschedule")
```

### Sending Immediate Notifications

```python
# Send appointment confirmation
await client.post(
    f"/api/notifications/send/appointment/{appointment_id}",
    json={"notification_type": "confirmation"}
)

# Send appointment cancellation
await client.post(
    f"/api/notifications/send/appointment/{appointment_id}",
    json={"notification_type": "cancellation"}
)

# Send appointment reschedule
await client.post(
    f"/api/notifications/send/appointment/{appointment_id}",
    json={"notification_type": "reschedule"}
)
```

### Viewing Notification History

```python
# Get notification history with filters
history = await client.get("/api/notifications/history/", params={
    "recipient_type": "PATIENT",
    "recipient_id": 123,
    "notification_type": "EMAIL",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-12-31T23:59:59Z",
    "limit": 50,
    "offset": 0
})
```

## TaskManager Integration

### Task Creation
When a reminder is scheduled, the system creates a task in TaskManager:

```json
{
    "name": "Appointment Reminder - 123",
    "description": "Send EMAIL reminder for appointment 123",
    "task_type": "email",
    "payload": {
        "reminder_id": 456,
        "appointment_id": 123,
        "recipient_email": "patient@email.com",
        "recipient_phone": "+1234567890",
        "subject": "Appointment Reminder - January 15, 2024",
        "message": "Reminder: You have an appointment on January 15, 2024 at 2:00 PM.",
        "appointment_date": "2024-01-15",
        "appointment_time": "14:00:00",
        "practitioner_name": "Dr. Smith"
    },
    "scheduled_time": "2024-01-14T14:00:00Z",
    "callback_url": "http://localhost:8000/api/notifications/reminder-callback/456",
    "max_retries": 3
}
```

### Callback Handling
TaskManager calls back to update reminder status:

```json
{
    "status": "success",
    "result": {
        "message_id": "msg_123456",
        "delivered_at": "2024-01-14T14:00:01Z"
    }
}
```

## Configuration

### Environment Variables

```bash
# TaskManager Configuration
TASK_MANAGER_URL=http://localhost:8001

# Email Configuration (if not using organization settings)
DEFAULT_SMTP_HOST=smtp.gmail.com
DEFAULT_SMTP_PORT=587
DEFAULT_EMAIL_USERNAME=notifications@clinic.com
DEFAULT_EMAIL_PASSWORD=secure_password

# SMS Configuration (if not using organization settings)
DEFAULT_SMS_PROVIDER=twilio
DEFAULT_SMS_API_KEY=your_twilio_key
DEFAULT_SMS_API_SECRET=your_twilio_secret
DEFAULT_SMS_FROM_NUMBER=+1234567890
```

### Docker Compose Integration

```yaml
version: '3.8'
services:
  scheduling:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - TASK_MANAGER_URL=http://taskmanager:8001
    depends_on:
      - taskmanager
      - postgres

  taskmanager:
    build: ../../PlatformServices/TaskManager/backend
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/taskmanager
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=scheduling
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Security Considerations

### Data Protection
- Email passwords and API secrets should be encrypted in production
- Use environment variables for sensitive configuration
- Implement proper access controls for notification settings

### Rate Limiting
- Implement rate limiting for notification endpoints
- Monitor TaskManager task creation to prevent abuse
- Set appropriate retry limits and backoff strategies

### Privacy Compliance
- Ensure notification preferences respect user privacy settings
- Implement opt-out mechanisms for all notification types
- Log notification activities for audit purposes

## Monitoring and Analytics

### Key Metrics
- Notification delivery success rates
- TaskManager task execution times
- User engagement with different notification types
- Reminder effectiveness (reduced no-shows)

### Health Checks
```http
GET /api/notifications/health
```

### Statistics Endpoints
```http
GET /api/notifications/statistics
GET /api/notifications/reminder-statistics
```

## Troubleshooting

### Common Issues

1. **TaskManager Connection Failed**
   - Check TaskManager service is running
   - Verify network connectivity
   - Check TASK_MANAGER_URL configuration

2. **Email Not Sending**
   - Verify SMTP settings in organization configuration
   - Check email credentials
   - Review email provider rate limits

3. **SMS Not Sending**
   - Verify SMS provider configuration
   - Check API credentials
   - Review SMS provider quotas

4. **Reminders Not Scheduled**
   - Check appointment data integrity
   - Verify notification preferences
   - Review reminder time calculations

### Debug Endpoints
```http
GET /api/notifications/debug/preferences/{patient_id}
GET /api/notifications/debug/effective-settings/{organization_id}
```

## Future Enhancements

### Planned Features
- Push notifications for mobile apps
- WhatsApp integration
- Voice call reminders
- Advanced template engine with dynamic content
- A/B testing for notification effectiveness
- Machine learning for optimal reminder timing

### Integration Opportunities
- Calendar system integration (Google Calendar, Outlook)
- Patient portal notification preferences
- Analytics dashboard for notification metrics
- Bulk notification campaigns
- Multi-language support

## Support

For technical support or questions about the notification system:

1. Check the API documentation at `/docs`
2. Review the notification logs
3. Test with the provided examples
4. Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Compatibility**: Scheduling2.0, PlatformServices TaskManager 