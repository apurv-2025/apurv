"""
Notification API endpoints for Scheduling2.0
Handles notification settings, reminders, and TaskManager callbacks
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.notification_models import (
    NotificationSettings, PatientNotificationPreferences, ClientNotificationPreferences,
    AppointmentReminder, NotificationHistory
)
from app.services.task_manager_integration import NotificationService
from app.schemas.notification_schemas import (
    NotificationSettingsCreate, NotificationSettingsUpdate,
    PatientNotificationPreferencesCreate, PatientNotificationPreferencesUpdate,
    ClientNotificationPreferencesCreate, ClientNotificationPreferencesUpdate,
    AppointmentReminderCreate, AppointmentReminderResponse,
    NotificationHistoryResponse
)

router = APIRouter()

# Initialize notification service
notification_service = NotificationService()

# ============================================================================
# Notification Settings Endpoints
# ============================================================================

@router.post("/settings/", response_model=NotificationSettings)
async def create_notification_settings(
    settings: NotificationSettingsCreate,
    db: Session = Depends(get_db)
):
    """Create notification settings for an organization"""
    try:
        db_settings = NotificationSettings(**settings.dict())
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
        return db_settings
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/settings/{organization_id}", response_model=NotificationSettings)
async def get_notification_settings(
    organization_id: str,
    db: Session = Depends(get_db)
):
    """Get notification settings for an organization"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.organization_id == organization_id
    ).first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    
    return settings

@router.put("/settings/{organization_id}", response_model=NotificationSettings)
async def update_notification_settings(
    organization_id: str,
    settings: NotificationSettingsUpdate,
    db: Session = Depends(get_db)
):
    """Update notification settings for an organization"""
    db_settings = db.query(NotificationSettings).filter(
        NotificationSettings.organization_id == organization_id
    ).first()
    
    if not db_settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    
    for field, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, field, value)
    
    db_settings.updated_at = datetime.now()
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ============================================================================
# Patient Notification Preferences Endpoints
# ============================================================================

@router.post("/preferences/patient/", response_model=PatientNotificationPreferences)
async def create_patient_notification_preferences(
    preferences: PatientNotificationPreferencesCreate,
    db: Session = Depends(get_db)
):
    """Create notification preferences for a patient"""
    try:
        db_preferences = PatientNotificationPreferences(**preferences.dict())
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)
        return db_preferences
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/preferences/patient/{patient_id}", response_model=PatientNotificationPreferences)
async def get_patient_notification_preferences(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """Get notification preferences for a patient"""
    preferences = db.query(PatientNotificationPreferences).filter(
        PatientNotificationPreferences.patient_id == patient_id
    ).first()
    
    if not preferences:
        raise HTTPException(status_code=404, detail="Patient notification preferences not found")
    
    return preferences

@router.put("/preferences/patient/{patient_id}", response_model=PatientNotificationPreferences)
async def update_patient_notification_preferences(
    patient_id: int,
    preferences: PatientNotificationPreferencesUpdate,
    db: Session = Depends(get_db)
):
    """Update notification preferences for a patient"""
    db_preferences = db.query(PatientNotificationPreferences).filter(
        PatientNotificationPreferences.patient_id == patient_id
    ).first()
    
    if not db_preferences:
        raise HTTPException(status_code=404, detail="Patient notification preferences not found")
    
    for field, value in preferences.dict(exclude_unset=True).items():
        setattr(db_preferences, field, value)
    
    db_preferences.updated_at = datetime.now()
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

# ============================================================================
# Client Notification Preferences Endpoints
# ============================================================================

@router.post("/preferences/client/", response_model=ClientNotificationPreferences)
async def create_client_notification_preferences(
    preferences: ClientNotificationPreferencesCreate,
    db: Session = Depends(get_db)
):
    """Create notification preferences for a client"""
    try:
        db_preferences = ClientNotificationPreferences(**preferences.dict())
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)
        return db_preferences
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/preferences/client/{client_id}", response_model=ClientNotificationPreferences)
async def get_client_notification_preferences(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Get notification preferences for a client"""
    preferences = db.query(ClientNotificationPreferences).filter(
        ClientNotificationPreferences.client_id == client_id
    ).first()
    
    if not preferences:
        raise HTTPException(status_code=404, detail="Client notification preferences not found")
    
    return preferences

@router.put("/preferences/client/{client_id}", response_model=ClientNotificationPreferences)
async def update_client_notification_preferences(
    client_id: int,
    preferences: ClientNotificationPreferencesUpdate,
    db: Session = Depends(get_db)
):
    """Update notification preferences for a client"""
    db_preferences = db.query(ClientNotificationPreferences).filter(
        ClientNotificationPreferences.client_id == client_id
    ).first()
    
    if not db_preferences:
        raise HTTPException(status_code=404, detail="Client notification preferences not found")
    
    for field, value in preferences.dict(exclude_unset=True).items():
        setattr(db_preferences, field, value)
    
    db_preferences.updated_at = datetime.now()
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

# ============================================================================
# Appointment Reminders Endpoints
# ============================================================================

@router.post("/reminders/appointment/{appointment_id}", response_model=List[AppointmentReminderResponse])
async def schedule_appointment_reminders(
    appointment_id: int,
    custom_reminders: Optional[List[int]] = None,
    db: Session = Depends(get_db)
):
    """Schedule reminders for an appointment"""
    from app.models.models import Appointment
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    reminders = await notification_service.schedule_appointment_reminders(
        appointment, db, custom_reminders
    )
    
    return [AppointmentReminderResponse.from_orm(reminder) for reminder in reminders]

@router.get("/reminders/appointment/{appointment_id}", response_model=List[AppointmentReminderResponse])
async def get_appointment_reminders(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Get all reminders for an appointment"""
    reminders = db.query(AppointmentReminder).filter(
        AppointmentReminder.appointment_id == appointment_id
    ).all()
    
    return [AppointmentReminderResponse.from_orm(reminder) for reminder in reminders]

@router.delete("/reminders/appointment/{appointment_id}")
async def cancel_appointment_reminders(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Cancel all reminders for an appointment"""
    success = await notification_service.cancel_appointment_reminders(appointment_id, db)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to cancel reminders")
    
    return {"message": "Reminders cancelled successfully"}

@router.post("/reminders/appointment/{appointment_id}/reschedule")
async def reschedule_appointment_reminders(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Reschedule reminders for an appointment"""
    from app.models.models import Appointment
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    success = await notification_service.reschedule_appointment_reminders(appointment, db)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reschedule reminders")
    
    return {"message": "Reminders rescheduled successfully"}

# ============================================================================
# Notification History Endpoints
# ============================================================================

@router.get("/history/", response_model=List[NotificationHistoryResponse])
async def get_notification_history(
    recipient_type: Optional[str] = None,
    recipient_id: Optional[int] = None,
    notification_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get notification history with filters"""
    query = db.query(NotificationHistory)
    
    if recipient_type:
        query = query.filter(NotificationHistory.recipient_type == recipient_type)
    
    if recipient_id:
        query = query.filter(NotificationHistory.recipient_id == recipient_id)
    
    if notification_type:
        query = query.filter(NotificationHistory.notification_type == notification_type)
    
    if start_date:
        query = query.filter(NotificationHistory.sent_at >= start_date)
    
    if end_date:
        query = query.filter(NotificationHistory.sent_at <= end_date)
    
    notifications = query.order_by(NotificationHistory.sent_at.desc()).offset(offset).limit(limit).all()
    
    return [NotificationHistoryResponse.from_orm(notification) for notification in notifications]

@router.get("/history/{notification_id}", response_model=NotificationHistoryResponse)
async def get_notification_by_id(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific notification by ID"""
    notification = db.query(NotificationHistory).filter(
        NotificationHistory.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return NotificationHistoryResponse.from_orm(notification)

# ============================================================================
# TaskManager Callback Endpoints
# ============================================================================

@router.post("/callback/{notification_id}")
async def notification_callback(
    notification_id: int,
    callback_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Callback endpoint for TaskManager to update notification status"""
    notification = db.query(NotificationHistory).filter(
        NotificationHistory.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Update notification status based on callback data
    status = callback_data.get("status")
    if status == "success":
        notification.status = "DELIVERED"
        notification.delivered_at = datetime.now()
    elif status == "failed":
        notification.status = "FAILED"
        notification.error_message = callback_data.get("error", "Unknown error")
    
    db.commit()
    
    return {"message": "Notification status updated"}

@router.post("/reminder-callback/{reminder_id}")
async def reminder_callback(
    reminder_id: int,
    callback_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Callback endpoint for TaskManager to update reminder status"""
    reminder = db.query(AppointmentReminder).filter(
        AppointmentReminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    # Update reminder status based on callback data
    status = callback_data.get("status")
    if status == "success":
        reminder.status = "SENT"
        reminder.sent_at = datetime.now()
    elif status == "failed":
        reminder.status = "FAILED"
        reminder.error_message = callback_data.get("error", "Unknown error")
    
    db.commit()
    
    return {"message": "Reminder status updated"}

# ============================================================================
# Immediate Notification Endpoints
# ============================================================================

@router.post("/send/appointment/{appointment_id}")
async def send_appointment_notification(
    appointment_id: int,
    notification_type: str,  # 'confirmation', 'cancellation', 'reschedule'
    db: Session = Depends(get_db)
):
    """Send immediate notification for appointment changes"""
    from app.models.models import Appointment
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    notification = await notification_service.send_immediate_notification(
        appointment, db, notification_type
    )
    
    if not notification:
        raise HTTPException(status_code=500, detail="Failed to send notification")
    
    return {"message": "Notification sent successfully", "notification_id": notification.id}

# ============================================================================
# Notification Templates Endpoints
# ============================================================================

@router.get("/templates/{organization_id}")
async def get_notification_templates(
    organization_id: str,
    db: Session = Depends(get_db)
):
    """Get notification templates for an organization"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.organization_id == organization_id
    ).first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    
    return {
        "email_templates": settings.email_templates,
        "sms_templates": settings.sms_templates
    }

@router.put("/templates/{organization_id}")
async def update_notification_templates(
    organization_id: str,
    templates: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update notification templates for an organization"""
    settings = db.query(NotificationSettings).filter(
        NotificationSettings.organization_id == organization_id
    ).first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    
    if "email_templates" in templates:
        settings.email_templates = templates["email_templates"]
    
    if "sms_templates" in templates:
        settings.sms_templates = templates["sms_templates"]
    
    settings.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Templates updated successfully"} 