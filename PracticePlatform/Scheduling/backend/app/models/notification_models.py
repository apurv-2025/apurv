"""
Notification and Reminder Models for Scheduling2.0
Supports multiple reminders and notification settings
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Text, JSON, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.database import Base

# ============================================================================
# Notification Settings Model
# ============================================================================
class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Organization-level settings
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Email settings
    email_enabled = Column(Boolean, default=True)
    email_smtp_host = Column(String(255))
    email_smtp_port = Column(Integer, default=587)
    email_username = Column(String(255))
    email_password = Column(String(255))  # Should be encrypted in production
    email_from_address = Column(String(255))
    email_from_name = Column(String(255))
    
    # SMS settings
    sms_enabled = Column(Boolean, default=True)
    sms_provider = Column(String(50))  # twilio, aws_sns, etc.
    sms_api_key = Column(String(255))
    sms_api_secret = Column(String(255))
    sms_from_number = Column(String(20))
    
    # Default reminder settings
    default_email_reminders = Column(JSON, default=lambda: [24, 2])  # Hours before appointment
    default_sms_reminders = Column(JSON, default=lambda: [24, 2])    # Hours before appointment
    
    # Notification templates
    email_templates = Column(JSON, default=lambda: {
        "appointment_confirmation": "Your appointment has been confirmed for {date} at {time}.",
        "appointment_reminder": "Reminder: You have an appointment tomorrow at {time}.",
        "appointment_cancellation": "Your appointment on {date} has been cancelled.",
        "appointment_reschedule": "Your appointment has been rescheduled to {date} at {time}."
    })
    
    sms_templates = Column(JSON, default=lambda: {
        "appointment_confirmation": "Appt confirmed: {date} at {time}",
        "appointment_reminder": "Reminder: Appt tomorrow at {time}",
        "appointment_cancellation": "Appt cancelled: {date}",
        "appointment_reschedule": "Appt rescheduled: {date} at {time}"
    })
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    organization = relationship("Organization", back_populates="notification_settings")

# ============================================================================
# Patient Notification Preferences Model
# ============================================================================
class PatientNotificationPreferences(Base):
    __tablename__ = "patient_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    # Notification preferences
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=True)
    
    # Reminder preferences (hours before appointment)
    email_reminders = Column(JSON, default=lambda: [24, 2])  # 24 hours and 2 hours before
    sms_reminders = Column(JSON, default=lambda: [24, 2])    # 24 hours and 2 hours before
    
    # Notification types
    appointment_confirmation = Column(Boolean, default=True)
    appointment_reminder = Column(Boolean, default=True)
    appointment_cancellation = Column(Boolean, default=True)
    appointment_reschedule = Column(Boolean, default=True)
    waitlist_notification = Column(Boolean, default=True)
    
    # Contact information (can override patient's default)
    email_address = Column(String(255))
    phone_number = Column(String(20))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    patient = relationship("Patient", back_populates="notification_preferences")

# ============================================================================
# Client Notification Preferences Model
# ============================================================================
class ClientNotificationPreferences(Base):
    __tablename__ = "client_notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Notification preferences
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=True)
    
    # Reminder preferences (hours before appointment)
    email_reminders = Column(JSON, default=lambda: [24, 2])  # 24 hours and 2 hours before
    sms_reminders = Column(JSON, default=lambda: [24, 2])    # 24 hours and 2 hours before
    
    # Notification types
    appointment_confirmation = Column(Boolean, default=True)
    appointment_reminder = Column(Boolean, default=True)
    appointment_cancellation = Column(Boolean, default=True)
    appointment_reschedule = Column(Boolean, default=True)
    waitlist_notification = Column(Boolean, default=True)
    
    # Contact information (can override client's default)
    email_address = Column(String(255))
    phone_number = Column(String(20))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    client = relationship("Client", back_populates="notification_preferences")

# ============================================================================
# Appointment Reminders Model
# ============================================================================
class AppointmentReminder(Base):
    __tablename__ = "appointment_reminders"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False)
    
    # Reminder details
    reminder_type = Column(Enum('EMAIL', 'SMS', 'BOTH', name="reminder_type_enum"), nullable=False)
    reminder_time = Column(DateTime(timezone=True), nullable=False)  # When to send the reminder
    hours_before_appointment = Column(Integer, nullable=False)  # Hours before appointment
    
    # Notification content
    subject = Column(String(255))  # For email
    message = Column(Text, nullable=False)
    
    # Status tracking
    status = Column(Enum('PENDING', 'SENT', 'FAILED', 'CANCELLED', name="reminder_status_enum"), default='PENDING')
    sent_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Task Manager integration
    task_manager_task_id = Column(Integer)  # Reference to TaskManager task
    task_manager_execution_id = Column(Integer)  # Reference to TaskManager execution
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    appointment = relationship("Appointment", back_populates="reminders")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_appointment_reminder_time', 'reminder_time'),
        Index('idx_appointment_reminder_status', 'status'),
        Index('idx_appointment_reminder_appointment', 'appointment_id'),
    )

# ============================================================================
# Notification History Model
# ============================================================================
class NotificationHistory(Base):
    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True, index=True)
    
    # Notification details
    notification_type = Column(Enum('EMAIL', 'SMS', 'BOTH', name="notification_type_enum"), nullable=False)
    notification_category = Column(Enum('CONFIRMATION', 'REMINDER', 'CANCELLATION', 'RESCHEDULE', 'WAITLIST', name="notification_category_enum"), nullable=False)
    
    # Recipient information
    recipient_type = Column(Enum('PATIENT', 'CLIENT', 'PRACTITIONER', name="recipient_type_enum"), nullable=False)
    recipient_id = Column(Integer, nullable=False)
    recipient_email = Column(String(255))
    recipient_phone = Column(String(20))
    
    # Content
    subject = Column(String(255))
    message = Column(Text, nullable=False)
    
    # Status and tracking
    status = Column(Enum('SENT', 'FAILED', 'BOUNCED', 'DELIVERED', name="notification_status_enum"), default='SENT')
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    delivered_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Related entities
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    waitlist_entry_id = Column(Integer, ForeignKey("waitlist_entries.id"))
    
    # Task Manager integration
    task_manager_task_id = Column(Integer)
    task_manager_execution_id = Column(Integer)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    appointment = relationship("Appointment", back_populates="notification_history")
    waitlist_entry = relationship("WaitlistEntry", back_populates="notification_history")
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_notification_history_recipient', 'recipient_type', 'recipient_id'),
        Index('idx_notification_history_sent_at', 'sent_at'),
        Index('idx_notification_history_status', 'status'),
        Index('idx_notification_history_appointment', 'appointment_id'),
    ) 