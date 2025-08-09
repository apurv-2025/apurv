"""
TaskManager Integration Service for Scheduling2.0
Handles integration with PlatformServices TaskManager for notifications and reminders
"""

import httpx
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Appointment, Patient, Client, Organization
from app.models.notification_models import (
    AppointmentReminder, NotificationHistory, NotificationSettings,
    PatientNotificationPreferences, ClientNotificationPreferences
)

logger = logging.getLogger(__name__)

class TaskManagerIntegration:
    """Integration service for PlatformServices TaskManager"""
    
    def __init__(self, task_manager_url: str = "http://localhost:8001"):
        self.task_manager_url = task_manager_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def create_task(self, task_data: Dict[str, Any]) -> Optional[int]:
        """Create a task in TaskManager"""
        try:
            response = await self.client.post(
                f"{self.task_manager_url}/tasks/",
                json=task_data
            )
            response.raise_for_status()
            result = response.json()
            return result.get("id")
        except Exception as e:
            logger.error(f"Failed to create task in TaskManager: {e}")
            return None
    
    async def get_task_status(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get task status from TaskManager"""
        try:
            response = await self.client.get(f"{self.task_manager_url}/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get task status from TaskManager: {e}")
            return None
    
    async def update_task_status(self, task_id: int, status: str, result: Dict[str, Any] = None):
        """Update task status in TaskManager"""
        try:
            update_data = {"status": status}
            if result:
                update_data["result"] = result
            
            response = await self.client.put(
                f"{self.task_manager_url}/tasks/{task_id}",
                json=update_data
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to update task status in TaskManager: {e}")

class NotificationService:
    """Service for handling notifications and reminders"""
    
    def __init__(self, task_manager_url: str = "http://localhost:8001"):
        self.task_manager = TaskManagerIntegration(task_manager_url)
    
    async def schedule_appointment_reminders(
        self,
        appointment: Appointment,
        db: Session,
        custom_reminders: Optional[List[int]] = None
    ) -> List[AppointmentReminder]:
        """Schedule reminders for an appointment"""
        reminders = []
        
        # Get notification preferences
        notification_prefs = await self._get_notification_preferences(appointment, db)
        if not notification_prefs:
            logger.warning(f"No notification preferences found for appointment {appointment.id}")
            return reminders
        
        # Determine reminder times
        email_reminders = custom_reminders or notification_prefs.get("email_reminders", [24, 2])
        sms_reminders = custom_reminders or notification_prefs.get("sms_reminders", [24, 2])
        
        # Create email reminders
        if notification_prefs.get("email_enabled", True):
            for hours_before in email_reminders:
                reminder = await self._create_reminder(
                    appointment, db, "EMAIL", hours_before, notification_prefs
                )
                if reminder:
                    reminders.append(reminder)
        
        # Create SMS reminders
        if notification_prefs.get("sms_enabled", True):
            for hours_before in sms_reminders:
                reminder = await self._create_reminder(
                    appointment, db, "SMS", hours_before, notification_prefs
                )
                if reminder:
                    reminders.append(reminder)
        
        return reminders
    
    async def _get_notification_preferences(
        self,
        appointment: Appointment,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """Get notification preferences for appointment recipient"""
        # Get organization settings
        org_settings = db.query(NotificationSettings).filter(
            NotificationSettings.organization_id == appointment.practitioner.organization_id
        ).first()
        
        if not org_settings:
            return None
        
        # Get patient/client preferences
        if appointment.patient_id:
            prefs = db.query(PatientNotificationPreferences).filter(
                PatientNotificationPreferences.patient_id == appointment.patient_id
            ).first()
            
            if prefs:
                return {
                    "email_enabled": prefs.email_enabled and org_settings.email_enabled,
                    "sms_enabled": prefs.sms_enabled and org_settings.sms_enabled,
                    "email_reminders": prefs.email_reminders or org_settings.default_email_reminders,
                    "sms_reminders": prefs.sms_reminders or org_settings.default_sms_reminders,
                    "email_address": prefs.email_address or appointment.patient.email,
                    "phone_number": prefs.phone_number or appointment.patient.phone,
                    "templates": org_settings.email_templates,
                    "sms_templates": org_settings.sms_templates
                }
        
        elif appointment.client_id:
            prefs = db.query(ClientNotificationPreferences).filter(
                ClientNotificationPreferences.client_id == appointment.client_id
            ).first()
            
            if prefs:
                return {
                    "email_enabled": prefs.email_enabled and org_settings.email_enabled,
                    "sms_enabled": prefs.sms_enabled and org_settings.sms_enabled,
                    "email_reminders": prefs.email_reminders or org_settings.default_email_reminders,
                    "sms_reminders": prefs.sms_reminders or org_settings.default_sms_reminders,
                    "email_address": prefs.email_address or appointment.client.email,
                    "phone_number": prefs.phone_number or appointment.client.phone,
                    "templates": org_settings.email_templates,
                    "sms_templates": org_settings.sms_templates
                }
        
        # Fallback to organization defaults
        return {
            "email_enabled": org_settings.email_enabled,
            "sms_enabled": org_settings.sms_enabled,
            "email_reminders": org_settings.default_email_reminders,
            "sms_reminders": org_settings.default_sms_reminders,
            "email_address": appointment.patient.email if appointment.patient_id else appointment.client.email,
            "phone_number": appointment.patient.phone if appointment.patient_id else appointment.client.phone,
            "templates": org_settings.email_templates,
            "sms_templates": org_settings.sms_templates
        }
    
    async def _create_reminder(
        self,
        appointment: Appointment,
        db: Session,
        reminder_type: str,
        hours_before: int,
        notification_prefs: Dict[str, Any]
    ) -> Optional[AppointmentReminder]:
        """Create a reminder record and schedule it in TaskManager"""
        try:
            # Calculate reminder time
            appointment_datetime = datetime.combine(
                appointment.appointment_date,
                appointment.start_time
            )
            reminder_time = appointment_datetime - timedelta(hours=hours_before)
            
            # Skip if reminder time is in the past
            if reminder_time <= datetime.now():
                logger.warning(f"Reminder time {reminder_time} is in the past for appointment {appointment.id}")
                return None
            
            # Create message content
            subject, message = self._create_reminder_content(
                appointment, reminder_type, hours_before, notification_prefs
            )
            
            # Create reminder record
            reminder = AppointmentReminder(
                appointment_id=appointment.id,
                reminder_type=reminder_type,
                reminder_time=reminder_time,
                hours_before_appointment=hours_before,
                subject=subject,
                message=message,
                status="PENDING"
            )
            
            db.add(reminder)
            db.flush()  # Get the ID
            
            # Create task in TaskManager
            task_data = {
                "name": f"Appointment Reminder - {appointment.id}",
                "description": f"Send {reminder_type.lower()} reminder for appointment {appointment.id}",
                "task_type": reminder_type.lower(),
                "payload": {
                    "reminder_id": reminder.id,
                    "appointment_id": appointment.id,
                    "recipient_email": notification_prefs.get("email_address"),
                    "recipient_phone": notification_prefs.get("phone_number"),
                    "subject": subject,
                    "message": message,
                    "appointment_date": appointment.appointment_date.isoformat(),
                    "appointment_time": appointment.start_time.isoformat(),
                    "practitioner_name": f"{appointment.practitioner.family_name}, {appointment.practitioner.given_names[0] if appointment.practitioner.given_names else ''}"
                },
                "scheduled_time": reminder_time.isoformat(),
                "callback_url": f"http://localhost:8000/api/notifications/reminder-callback/{reminder.id}",
                "max_retries": 3
            }
            
            async with self.task_manager as tm:
                task_id = await tm.create_task(task_data)
                if task_id:
                    reminder.task_manager_task_id = task_id
                    db.commit()
                    logger.info(f"Created reminder {reminder.id} with TaskManager task {task_id}")
                    return reminder
                else:
                    db.rollback()
                    logger.error(f"Failed to create TaskManager task for reminder {reminder.id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            db.rollback()
            return None
    
    def _create_reminder_content(
        self,
        appointment: Appointment,
        reminder_type: str,
        hours_before: int,
        notification_prefs: Dict[str, Any]
    ) -> tuple[str, str]:
        """Create subject and message content for reminder"""
        appointment_datetime = datetime.combine(appointment.appointment_date, appointment.start_time)
        date_str = appointment.appointment_date.strftime("%B %d, %Y")
        time_str = appointment.start_time.strftime("%I:%M %p")
        
        practitioner_name = f"{appointment.practitioner.family_name}, {appointment.practitioner.given_names[0] if appointment.practitioner.given_names else ''}"
        
        if reminder_type == "EMAIL":
            templates = notification_prefs.get("templates", {})
            template = templates.get("appointment_reminder", "Reminder: You have an appointment on {date} at {time}.")
            
            subject = f"Appointment Reminder - {date_str}"
            message = template.format(
                date=date_str,
                time=time_str,
                practitioner=practitioner_name,
                hours_before=hours_before
            )
        else:  # SMS
            templates = notification_prefs.get("sms_templates", {})
            template = templates.get("appointment_reminder", "Reminder: Appt {date} at {time}")
            
            subject = ""
            message = template.format(
                date=appointment.appointment_date.strftime("%m/%d"),
                time=time_str,
                practitioner=practitioner_name,
                hours_before=hours_before
            )
        
        return subject, message
    
    async def send_immediate_notification(
        self,
        appointment: Appointment,
        db: Session,
        notification_type: str,  # 'confirmation', 'cancellation', 'reschedule'
        notification_prefs: Optional[Dict[str, Any]] = None
    ) -> Optional[NotificationHistory]:
        """Send immediate notification for appointment changes"""
        try:
            if not notification_prefs:
                notification_prefs = await self._get_notification_preferences(appointment, db)
            
            if not notification_prefs:
                return None
            
            # Create notification content
            subject, message = self._create_notification_content(
                appointment, notification_type, notification_prefs
            )
            
            # Determine notification method
            notification_method = "EMAIL"
            if notification_prefs.get("sms_enabled", True):
                notification_method = "BOTH"
            
            # Create notification history record
            notification = NotificationHistory(
                notification_type=notification_method,
                notification_category=notification_type.upper(),
                recipient_type="PATIENT" if appointment.patient_id else "CLIENT",
                recipient_id=appointment.patient_id or appointment.client_id,
                recipient_email=notification_prefs.get("email_address"),
                recipient_phone=notification_prefs.get("phone_number"),
                subject=subject,
                message=message,
                appointment_id=appointment.id,
                status="SENT"
            )
            
            db.add(notification)
            db.flush()
            
            # Create task in TaskManager for immediate execution
            task_data = {
                "name": f"Immediate Notification - {appointment.id}",
                "description": f"Send {notification_type} notification for appointment {appointment.id}",
                "task_type": notification_method.lower(),
                "payload": {
                    "notification_id": notification.id,
                    "appointment_id": appointment.id,
                    "recipient_email": notification_prefs.get("email_address"),
                    "recipient_phone": notification_prefs.get("phone_number"),
                    "subject": subject,
                    "message": message,
                    "notification_type": notification_type
                },
                "scheduled_time": datetime.now().isoformat(),
                "callback_url": f"http://localhost:8000/api/notifications/callback/{notification.id}",
                "max_retries": 3
            }
            
            async with self.task_manager as tm:
                task_id = await tm.create_task(task_data)
                if task_id:
                    notification.task_manager_task_id = task_id
                    db.commit()
                    logger.info(f"Created immediate notification {notification.id} with TaskManager task {task_id}")
                    return notification
                else:
                    db.rollback()
                    logger.error(f"Failed to create TaskManager task for notification {notification.id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error sending immediate notification: {e}")
            db.rollback()
            return None
    
    def _create_notification_content(
        self,
        appointment: Appointment,
        notification_type: str,
        notification_prefs: Dict[str, Any]
    ) -> tuple[str, str]:
        """Create subject and message content for notification"""
        date_str = appointment.appointment_date.strftime("%B %d, %Y")
        time_str = appointment.start_time.strftime("%I:%M %p")
        practitioner_name = f"{appointment.practitioner.family_name}, {appointment.practitioner.given_names[0] if appointment.practitioner.given_names else ''}"
        
        templates = notification_prefs.get("templates", {})
        sms_templates = notification_prefs.get("sms_templates", {})
        
        if notification_type == "confirmation":
            email_template = templates.get("appointment_confirmation", "Your appointment has been confirmed for {date} at {time}.")
            sms_template = sms_templates.get("appointment_confirmation", "Appt confirmed: {date} at {time}")
        elif notification_type == "cancellation":
            email_template = templates.get("appointment_cancellation", "Your appointment on {date} has been cancelled.")
            sms_template = sms_templates.get("appointment_cancellation", "Appt cancelled: {date}")
        elif notification_type == "reschedule":
            email_template = templates.get("appointment_reschedule", "Your appointment has been rescheduled to {date} at {time}.")
            sms_template = sms_templates.get("appointment_reschedule", "Appt rescheduled: {date} at {time}")
        else:
            email_template = "Your appointment has been updated."
            sms_template = "Appt updated"
        
        subject = f"Appointment {notification_type.title()} - {date_str}"
        message = email_template.format(
            date=date_str,
            time=time_str,
            practitioner=practitioner_name
        )
        
        return subject, message
    
    async def cancel_appointment_reminders(
        self,
        appointment_id: int,
        db: Session
    ) -> bool:
        """Cancel all reminders for an appointment"""
        try:
            # Get all pending reminders
            reminders = db.query(AppointmentReminder).filter(
                AppointmentReminder.appointment_id == appointment_id,
                AppointmentReminder.status == "PENDING"
            ).all()
            
            async with self.task_manager as tm:
                for reminder in reminders:
                    # Update reminder status
                    reminder.status = "CANCELLED"
                    
                    # Cancel task in TaskManager if it exists
                    if reminder.task_manager_task_id:
                        await tm.update_task_status(
                            reminder.task_manager_task_id,
                            "cancelled",
                            {"reason": "Appointment cancelled"}
                        )
            
            db.commit()
            logger.info(f"Cancelled {len(reminders)} reminders for appointment {appointment_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling reminders: {e}")
            db.rollback()
            return False
    
    async def reschedule_appointment_reminders(
        self,
        appointment: Appointment,
        db: Session
    ) -> bool:
        """Reschedule reminders for an updated appointment"""
        try:
            # Cancel existing reminders
            await self.cancel_appointment_reminders(appointment.id, db)
            
            # Create new reminders
            await self.schedule_appointment_reminders(appointment, db)
            
            logger.info(f"Rescheduled reminders for appointment {appointment.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error rescheduling reminders: {e}")
            return False 