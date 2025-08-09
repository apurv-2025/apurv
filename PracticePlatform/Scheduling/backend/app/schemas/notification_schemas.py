"""
Notification Schemas for Scheduling2.0
Pydantic models for notification requests and responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# ============================================================================
# Enums
# ============================================================================

class ReminderType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    BOTH = "BOTH"

class ReminderStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class NotificationType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    BOTH = "BOTH"

class NotificationCategory(str, Enum):
    CONFIRMATION = "CONFIRMATION"
    REMINDER = "REMINDER"
    CANCELLATION = "CANCELLATION"
    RESCHEDULE = "RESCHEDULE"
    WAITLIST = "WAITLIST"

class NotificationStatus(str, Enum):
    SENT = "SENT"
    FAILED = "FAILED"
    BOUNCED = "BOUNCED"
    DELIVERED = "DELIVERED"

class RecipientType(str, Enum):
    PATIENT = "PATIENT"
    CLIENT = "CLIENT"
    PRACTITIONER = "PRACTITIONER"

# ============================================================================
# Notification Settings Schemas
# ============================================================================

class NotificationSettingsBase(BaseModel):
    organization_id: str = Field(..., description="Organization ID")
    email_enabled: bool = Field(default=True, description="Enable email notifications")
    sms_enabled: bool = Field(default=True, description="Enable SMS notifications")
    default_email_reminders: List[int] = Field(default=[24, 2], description="Default email reminder hours")
    default_sms_reminders: List[int] = Field(default=[24, 2], description="Default SMS reminder hours")

class NotificationSettingsCreate(NotificationSettingsBase):
    email_smtp_host: Optional[str] = Field(None, description="SMTP host for email")
    email_smtp_port: int = Field(default=587, description="SMTP port for email")
    email_username: Optional[str] = Field(None, description="Email username")
    email_password: Optional[str] = Field(None, description="Email password")
    email_from_address: Optional[str] = Field(None, description="From email address")
    email_from_name: Optional[str] = Field(None, description="From name")
    sms_provider: Optional[str] = Field(None, description="SMS provider (twilio, aws_sns, etc.)")
    sms_api_key: Optional[str] = Field(None, description="SMS API key")
    sms_api_secret: Optional[str] = Field(None, description="SMS API secret")
    sms_from_number: Optional[str] = Field(None, description="From phone number")
    email_templates: Dict[str, str] = Field(default_factory=dict, description="Email templates")
    sms_templates: Dict[str, str] = Field(default_factory=dict, description="SMS templates")

class NotificationSettingsUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    default_email_reminders: Optional[List[int]] = None
    default_sms_reminders: Optional[List[int]] = None
    email_smtp_host: Optional[str] = None
    email_smtp_port: Optional[int] = None
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    email_from_address: Optional[str] = None
    email_from_name: Optional[str] = None
    sms_provider: Optional[str] = None
    sms_api_key: Optional[str] = None
    sms_api_secret: Optional[str] = None
    sms_from_number: Optional[str] = None
    email_templates: Optional[Dict[str, str]] = None
    sms_templates: Optional[Dict[str, str]] = None

class NotificationSettings(NotificationSettingsBase):
    id: int
    email_smtp_host: Optional[str] = None
    email_smtp_port: int = 587
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    email_from_address: Optional[str] = None
    email_from_name: Optional[str] = None
    sms_provider: Optional[str] = None
    sms_api_key: Optional[str] = None
    sms_api_secret: Optional[str] = None
    sms_from_number: Optional[str] = None
    email_templates: Dict[str, str] = Field(default_factory=dict)
    sms_templates: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ============================================================================
# Patient Notification Preferences Schemas
# ============================================================================

class PatientNotificationPreferencesBase(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    email_enabled: bool = Field(default=True, description="Enable email notifications")
    sms_enabled: bool = Field(default=True, description="Enable SMS notifications")
    email_reminders: List[int] = Field(default=[24, 2], description="Email reminder hours")
    sms_reminders: List[int] = Field(default=[24, 2], description="SMS reminder hours")
    appointment_confirmation: bool = Field(default=True, description="Send appointment confirmation")
    appointment_reminder: bool = Field(default=True, description="Send appointment reminders")
    appointment_cancellation: bool = Field(default=True, description="Send appointment cancellation")
    appointment_reschedule: bool = Field(default=True, description="Send appointment reschedule")
    waitlist_notification: bool = Field(default=True, description="Send waitlist notifications")

class PatientNotificationPreferencesCreate(PatientNotificationPreferencesBase):
    email_address: Optional[str] = Field(None, description="Override email address")
    phone_number: Optional[str] = Field(None, description="Override phone number")

class PatientNotificationPreferencesUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    email_reminders: Optional[List[int]] = None
    sms_reminders: Optional[List[int]] = None
    appointment_confirmation: Optional[bool] = None
    appointment_reminder: Optional[bool] = None
    appointment_cancellation: Optional[bool] = None
    appointment_reschedule: Optional[bool] = None
    waitlist_notification: Optional[bool] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None

class PatientNotificationPreferences(PatientNotificationPreferencesBase):
    id: int
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ============================================================================
# Client Notification Preferences Schemas
# ============================================================================

class ClientNotificationPreferencesBase(BaseModel):
    client_id: int = Field(..., description="Client ID")
    email_enabled: bool = Field(default=True, description="Enable email notifications")
    sms_enabled: bool = Field(default=True, description="Enable SMS notifications")
    email_reminders: List[int] = Field(default=[24, 2], description="Email reminder hours")
    sms_reminders: List[int] = Field(default=[24, 2], description="SMS reminder hours")
    appointment_confirmation: bool = Field(default=True, description="Send appointment confirmation")
    appointment_reminder: bool = Field(default=True, description="Send appointment reminders")
    appointment_cancellation: bool = Field(default=True, description="Send appointment cancellation")
    appointment_reschedule: bool = Field(default=True, description="Send appointment reschedule")
    waitlist_notification: bool = Field(default=True, description="Send waitlist notifications")

class ClientNotificationPreferencesCreate(ClientNotificationPreferencesBase):
    email_address: Optional[str] = Field(None, description="Override email address")
    phone_number: Optional[str] = Field(None, description="Override phone number")

class ClientNotificationPreferencesUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    email_reminders: Optional[List[int]] = None
    sms_reminders: Optional[List[int]] = None
    appointment_confirmation: Optional[bool] = None
    appointment_reminder: Optional[bool] = None
    appointment_cancellation: Optional[bool] = None
    appointment_reschedule: Optional[bool] = None
    waitlist_notification: Optional[bool] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None

class ClientNotificationPreferences(ClientNotificationPreferencesBase):
    id: int
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ============================================================================
# Appointment Reminder Schemas
# ============================================================================

class AppointmentReminderBase(BaseModel):
    appointment_id: int = Field(..., description="Appointment ID")
    reminder_type: ReminderType = Field(..., description="Type of reminder")
    reminder_time: datetime = Field(..., description="When to send the reminder")
    hours_before_appointment: int = Field(..., description="Hours before appointment")
    subject: Optional[str] = Field(None, description="Email subject")
    message: str = Field(..., description="Reminder message")

class AppointmentReminderCreate(AppointmentReminderBase):
    pass

class AppointmentReminderResponse(AppointmentReminderBase):
    id: int
    status: ReminderStatus
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    task_manager_task_id: Optional[int] = None
    task_manager_execution_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ============================================================================
# Notification History Schemas
# ============================================================================

class NotificationHistoryBase(BaseModel):
    notification_type: NotificationType = Field(..., description="Type of notification")
    notification_category: NotificationCategory = Field(..., description="Category of notification")
    recipient_type: RecipientType = Field(..., description="Type of recipient")
    recipient_id: int = Field(..., description="Recipient ID")
    recipient_email: Optional[str] = Field(None, description="Recipient email")
    recipient_phone: Optional[str] = Field(None, description="Recipient phone")
    subject: Optional[str] = Field(None, description="Email subject")
    message: str = Field(..., description="Notification message")

class NotificationHistoryResponse(NotificationHistoryBase):
    id: int
    status: NotificationStatus
    sent_at: datetime
    delivered_at: Optional[datetime] = None
    error_message: Optional[str] = None
    appointment_id: Optional[int] = None
    waitlist_entry_id: Optional[int] = None
    task_manager_task_id: Optional[int] = None
    task_manager_execution_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

# ============================================================================
# Request/Response Schemas
# ============================================================================

class ScheduleRemindersRequest(BaseModel):
    custom_reminders: Optional[List[int]] = Field(None, description="Custom reminder hours")
    
    @validator('custom_reminders')
    def validate_reminders(cls, v):
        if v is not None:
            for hours in v:
                if hours < 0 or hours > 168:  # Max 1 week
                    raise ValueError("Reminder hours must be between 0 and 168")
        return v

class SendNotificationRequest(BaseModel):
    notification_type: str = Field(..., description="Type of notification")
    custom_message: Optional[str] = Field(None, description="Custom message override")

class NotificationTemplateUpdate(BaseModel):
    email_templates: Optional[Dict[str, str]] = Field(None, description="Email templates")
    sms_templates: Optional[Dict[str, str]] = Field(None, description="SMS templates")

# ============================================================================
# Bulk Operations Schemas
# ============================================================================

class BulkNotificationRequest(BaseModel):
    recipient_ids: List[int] = Field(..., description="List of recipient IDs")
    recipient_type: RecipientType = Field(..., description="Type of recipients")
    notification_type: NotificationType = Field(..., description="Type of notification")
    message: str = Field(..., description="Notification message")
    subject: Optional[str] = Field(None, description="Email subject")

class BulkReminderRequest(BaseModel):
    appointment_ids: List[int] = Field(..., description="List of appointment IDs")
    reminder_type: ReminderType = Field(..., description="Type of reminder")
    hours_before: List[int] = Field(..., description="Hours before appointment")

# ============================================================================
# Statistics Schemas
# ============================================================================

class NotificationStatistics(BaseModel):
    total_notifications: int
    successful_notifications: int
    failed_notifications: int
    email_notifications: int
    sms_notifications: int
    average_delivery_time: Optional[float] = None
    success_rate: float

class ReminderStatistics(BaseModel):
    total_reminders: int
    pending_reminders: int
    sent_reminders: int
    failed_reminders: int
    cancelled_reminders: int
    email_reminders: int
    sms_reminders: int
    success_rate: float 