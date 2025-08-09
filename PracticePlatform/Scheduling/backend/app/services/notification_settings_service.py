"""
Notification Settings Management Service for Scheduling2.0
Handles organization and user notification preferences
"""

import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.notification_models import (
    NotificationSettings, PatientNotificationPreferences, ClientNotificationPreferences
)
from app.models.models import Organization, Patient, Client

logger = logging.getLogger(__name__)

class NotificationSettingsService:
    """Service for managing notification settings and preferences"""
    
    @staticmethod
    def create_organization_settings(
        db: Session,
        organization_id: str,
        settings_data: Dict[str, Any]
    ) -> NotificationSettings:
        """Create notification settings for an organization"""
        try:
            # Check if settings already exist
            existing_settings = db.query(NotificationSettings).filter(
                NotificationSettings.organization_id == organization_id
            ).first()
            
            if existing_settings:
                raise ValueError(f"Notification settings already exist for organization {organization_id}")
            
            # Create new settings
            settings = NotificationSettings(
                organization_id=organization_id,
                **settings_data
            )
            
            db.add(settings)
            db.commit()
            db.refresh(settings)
            
            logger.info(f"Created notification settings for organization {organization_id}")
            return settings
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating notification settings: {e}")
            raise
    
    @staticmethod
    def update_organization_settings(
        db: Session,
        organization_id: str,
        settings_data: Dict[str, Any]
    ) -> NotificationSettings:
        """Update notification settings for an organization"""
        try:
            settings = db.query(NotificationSettings).filter(
                NotificationSettings.organization_id == organization_id
            ).first()
            
            if not settings:
                raise ValueError(f"Notification settings not found for organization {organization_id}")
            
            # Update fields
            for field, value in settings_data.items():
                if hasattr(settings, field):
                    setattr(settings, field, value)
            
            settings.updated_at = datetime.now()
            db.commit()
            db.refresh(settings)
            
            logger.info(f"Updated notification settings for organization {organization_id}")
            return settings
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating notification settings: {e}")
            raise
    
    @staticmethod
    def get_organization_settings(
        db: Session,
        organization_id: str
    ) -> Optional[NotificationSettings]:
        """Get notification settings for an organization"""
        return db.query(NotificationSettings).filter(
            NotificationSettings.organization_id == organization_id
        ).first()
    
    @staticmethod
    def create_patient_preferences(
        db: Session,
        patient_id: int,
        preferences_data: Dict[str, Any]
    ) -> PatientNotificationPreferences:
        """Create notification preferences for a patient"""
        try:
            # Check if patient exists
            patient = db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                raise ValueError(f"Patient {patient_id} not found")
            
            # Check if preferences already exist
            existing_prefs = db.query(PatientNotificationPreferences).filter(
                PatientNotificationPreferences.patient_id == patient_id
            ).first()
            
            if existing_prefs:
                raise ValueError(f"Notification preferences already exist for patient {patient_id}")
            
            # Create new preferences
            preferences = PatientNotificationPreferences(
                patient_id=patient_id,
                **preferences_data
            )
            
            db.add(preferences)
            db.commit()
            db.refresh(preferences)
            
            logger.info(f"Created notification preferences for patient {patient_id}")
            return preferences
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating patient preferences: {e}")
            raise
    
    @staticmethod
    def update_patient_preferences(
        db: Session,
        patient_id: int,
        preferences_data: Dict[str, Any]
    ) -> PatientNotificationPreferences:
        """Update notification preferences for a patient"""
        try:
            preferences = db.query(PatientNotificationPreferences).filter(
                PatientNotificationPreferences.patient_id == patient_id
            ).first()
            
            if not preferences:
                raise ValueError(f"Notification preferences not found for patient {patient_id}")
            
            # Update fields
            for field, value in preferences_data.items():
                if hasattr(preferences, field):
                    setattr(preferences, field, value)
            
            preferences.updated_at = datetime.now()
            db.commit()
            db.refresh(preferences)
            
            logger.info(f"Updated notification preferences for patient {patient_id}")
            return preferences
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating patient preferences: {e}")
            raise
    
    @staticmethod
    def get_patient_preferences(
        db: Session,
        patient_id: int
    ) -> Optional[PatientNotificationPreferences]:
        """Get notification preferences for a patient"""
        return db.query(PatientNotificationPreferences).filter(
            PatientNotificationPreferences.patient_id == patient_id
        ).first()
    
    @staticmethod
    def create_client_preferences(
        db: Session,
        client_id: int,
        preferences_data: Dict[str, Any]
    ) -> ClientNotificationPreferences:
        """Create notification preferences for a client"""
        try:
            # Check if client exists
            client = db.query(Client).filter(Client.id == client_id).first()
            if not client:
                raise ValueError(f"Client {client_id} not found")
            
            # Check if preferences already exist
            existing_prefs = db.query(ClientNotificationPreferences).filter(
                ClientNotificationPreferences.client_id == client_id
            ).first()
            
            if existing_prefs:
                raise ValueError(f"Notification preferences already exist for client {client_id}")
            
            # Create new preferences
            preferences = ClientNotificationPreferences(
                client_id=client_id,
                **preferences_data
            )
            
            db.add(preferences)
            db.commit()
            db.refresh(preferences)
            
            logger.info(f"Created notification preferences for client {client_id}")
            return preferences
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating client preferences: {e}")
            raise
    
    @staticmethod
    def update_client_preferences(
        db: Session,
        client_id: int,
        preferences_data: Dict[str, Any]
    ) -> ClientNotificationPreferences:
        """Update notification preferences for a client"""
        try:
            preferences = db.query(ClientNotificationPreferences).filter(
                ClientNotificationPreferences.client_id == client_id
            ).first()
            
            if not preferences:
                raise ValueError(f"Notification preferences not found for client {client_id}")
            
            # Update fields
            for field, value in preferences_data.items():
                if hasattr(preferences, field):
                    setattr(preferences, field, value)
            
            preferences.updated_at = datetime.now()
            db.commit()
            db.refresh(preferences)
            
            logger.info(f"Updated notification preferences for client {client_id}")
            return preferences
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating client preferences: {e}")
            raise
    
    @staticmethod
    def get_client_preferences(
        db: Session,
        client_id: int
    ) -> Optional[ClientNotificationPreferences]:
        """Get notification preferences for a client"""
        return db.query(ClientNotificationPreferences).filter(
            ClientNotificationPreferences.client_id == client_id
        ).first()
    
    @staticmethod
    def get_effective_preferences(
        db: Session,
        organization_id: str,
        patient_id: Optional[int] = None,
        client_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get effective notification preferences combining organization and user settings"""
        try:
            # Get organization settings
            org_settings = db.query(NotificationSettings).filter(
                NotificationSettings.organization_id == organization_id
            ).first()
            
            if not org_settings:
                logger.warning(f"No notification settings found for organization {organization_id}")
                return {}
            
            # Base preferences from organization
            effective_prefs = {
                "email_enabled": org_settings.email_enabled,
                "sms_enabled": org_settings.sms_enabled,
                "default_email_reminders": org_settings.default_email_reminders,
                "default_sms_reminders": org_settings.default_sms_reminders,
                "email_templates": org_settings.email_templates,
                "sms_templates": org_settings.sms_templates
            }
            
            # Override with user preferences if available
            if patient_id:
                patient_prefs = db.query(PatientNotificationPreferences).filter(
                    PatientNotificationPreferences.patient_id == patient_id
                ).first()
                
                if patient_prefs:
                    effective_prefs.update({
                        "email_enabled": patient_prefs.email_enabled and org_settings.email_enabled,
                        "sms_enabled": patient_prefs.sms_enabled and org_settings.sms_enabled,
                        "email_reminders": patient_prefs.email_reminders or org_settings.default_email_reminders,
                        "sms_reminders": patient_prefs.sms_reminders or org_settings.default_sms_reminders,
                        "email_address": patient_prefs.email_address,
                        "phone_number": patient_prefs.phone_number,
                        "appointment_confirmation": patient_prefs.appointment_confirmation,
                        "appointment_reminder": patient_prefs.appointment_reminder,
                        "appointment_cancellation": patient_prefs.appointment_cancellation,
                        "appointment_reschedule": patient_prefs.appointment_reschedule,
                        "waitlist_notification": patient_prefs.waitlist_notification
                    })
            
            elif client_id:
                client_prefs = db.query(ClientNotificationPreferences).filter(
                    ClientNotificationPreferences.client_id == client_id
                ).first()
                
                if client_prefs:
                    effective_prefs.update({
                        "email_enabled": client_prefs.email_enabled and org_settings.email_enabled,
                        "sms_enabled": client_prefs.sms_enabled and org_settings.sms_enabled,
                        "email_reminders": client_prefs.email_reminders or org_settings.default_email_reminders,
                        "sms_reminders": client_prefs.sms_reminders or org_settings.default_sms_reminders,
                        "email_address": client_prefs.email_address,
                        "phone_number": client_prefs.phone_number,
                        "appointment_confirmation": client_prefs.appointment_confirmation,
                        "appointment_reminder": client_prefs.appointment_reminder,
                        "appointment_cancellation": client_prefs.appointment_cancellation,
                        "appointment_reschedule": client_prefs.appointment_reschedule,
                        "waitlist_notification": client_prefs.waitlist_notification
                    })
            
            return effective_prefs
            
        except Exception as e:
            logger.error(f"Error getting effective preferences: {e}")
            return {}
    
    @staticmethod
    def validate_reminder_settings(
        email_reminders: List[int],
        sms_reminders: List[int]
    ) -> bool:
        """Validate reminder settings"""
        try:
            # Check email reminders
            for hours in email_reminders:
                if not isinstance(hours, int) or hours < 0 or hours > 168:
                    return False
            
            # Check SMS reminders
            for hours in sms_reminders:
                if not isinstance(hours, int) or hours < 0 or hours > 168:
                    return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def get_default_templates() -> Dict[str, Dict[str, str]]:
        """Get default notification templates"""
        return {
            "email_templates": {
                "appointment_confirmation": "Your appointment has been confirmed for {date} at {time} with {practitioner}.",
                "appointment_reminder": "Reminder: You have an appointment on {date} at {time} with {practitioner}.",
                "appointment_cancellation": "Your appointment on {date} at {time} has been cancelled.",
                "appointment_reschedule": "Your appointment has been rescheduled to {date} at {time} with {practitioner}.",
                "waitlist_notification": "A slot has become available for your waitlist request on {date} at {time}."
            },
            "sms_templates": {
                "appointment_confirmation": "Appt confirmed: {date} at {time}",
                "appointment_reminder": "Reminder: Appt {date} at {time}",
                "appointment_cancellation": "Appt cancelled: {date}",
                "appointment_reschedule": "Appt rescheduled: {date} at {time}",
                "waitlist_notification": "Slot available: {date} at {time}"
            }
        } 