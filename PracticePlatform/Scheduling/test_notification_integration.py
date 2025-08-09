#!/usr/bin/env python3
"""
Test script for Notification & TaskManager Integration
Demonstrates the key features of the notification system
"""

import asyncio
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any

# Configuration
SCHEDULING_API_URL = "http://localhost:8000"
TASK_MANAGER_URL = "http://localhost:8001"

class NotificationIntegrationTest:
    """Test class for notification integration"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_organization_id = "test-org-123"
        self.test_patient_id = 1
        self.test_appointment_id = 1
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_organization_settings(self):
        """Test organization notification settings"""
        print("🔧 Testing Organization Notification Settings...")
        
        # Create organization settings
        settings_data = {
            "organization_id": self.test_organization_id,
            "email_enabled": True,
            "sms_enabled": True,
            "email_smtp_host": "smtp.gmail.com",
            "email_smtp_port": 587,
            "email_username": "notifications@testclinic.com",
            "email_password": "test_password",
            "email_from_address": "notifications@testclinic.com",
            "email_from_name": "Test Medical Clinic",
            "sms_provider": "twilio",
            "sms_api_key": "test_twilio_key",
            "sms_api_secret": "test_twilio_secret",
            "sms_from_number": "+1234567890",
            "default_email_reminders": [24, 2, 1],  # 24h, 2h, 1h before
            "default_sms_reminders": [24, 2],       # 24h, 2h before
            "email_templates": {
                "appointment_confirmation": "Your appointment has been confirmed for {date} at {time} with {practitioner}.",
                "appointment_reminder": "Reminder: You have an appointment on {date} at {time} with {practitioner}.",
                "appointment_cancellation": "Your appointment on {date} at {time} has been cancelled.",
                "appointment_reschedule": "Your appointment has been rescheduled to {date} at {time} with {practitioner}."
            },
            "sms_templates": {
                "appointment_confirmation": "Appt confirmed: {date} at {time}",
                "appointment_reminder": "Reminder: Appt {date} at {time}",
                "appointment_cancellation": "Appt cancelled: {date}",
                "appointment_reschedule": "Appt rescheduled: {date} at {time}"
            }
        }
        
        try:
            response = await self.client.post(
                f"{SCHEDULING_API_URL}/api/notifications/settings/",
                json=settings_data
            )
            response.raise_for_status()
            print("✅ Organization settings created successfully")
            
            # Get settings
            response = await self.client.get(
                f"{SCHEDULING_API_URL}/api/notifications/settings/{self.test_organization_id}"
            )
            response.raise_for_status()
            settings = response.json()
            print(f"✅ Retrieved organization settings: {settings['id']}")
            
        except Exception as e:
            print(f"❌ Error with organization settings: {e}")
    
    async def test_patient_preferences(self):
        """Test patient notification preferences"""
        print("\n👤 Testing Patient Notification Preferences...")
        
        preferences_data = {
            "patient_id": self.test_patient_id,
            "email_enabled": True,
            "sms_enabled": True,
            "email_reminders": [24, 2, 1],  # Override organization defaults
            "sms_reminders": [24],          # Only 24h SMS reminder
            "appointment_confirmation": True,
            "appointment_reminder": True,
            "appointment_cancellation": True,
            "appointment_reschedule": True,
            "waitlist_notification": False,  # Disable waitlist notifications
            "email_address": "patient@test.com",  # Override patient's default email
            "phone_number": "+1234567890"   # Override patient's default phone
        }
        
        try:
            response = await self.client.post(
                f"{SCHEDULING_API_URL}/api/notifications/preferences/patient/",
                json=preferences_data
            )
            response.raise_for_status()
            print("✅ Patient preferences created successfully")
            
            # Get preferences
            response = await self.client.get(
                f"{SCHEDULING_API_URL}/api/notifications/preferences/patient/{self.test_patient_id}"
            )
            response.raise_for_status()
            prefs = response.json()
            print(f"✅ Retrieved patient preferences: {prefs['id']}")
            
        except Exception as e:
            print(f"❌ Error with patient preferences: {e}")
    
    async def test_appointment_reminders(self):
        """Test appointment reminder scheduling"""
        print("\n🔔 Testing Appointment Reminders...")
        
        try:
            # Schedule reminders for an appointment
            reminder_data = {
                "custom_reminders": [24, 2, 1]  # 24h, 2h, 1h before
            }
            
            response = await self.client.post(
                f"{SCHEDULING_API_URL}/api/notifications/reminders/appointment/{self.test_appointment_id}",
                json=reminder_data
            )
            response.raise_for_status()
            reminders = response.json()
            print(f"✅ Scheduled {len(reminders)} reminders for appointment {self.test_appointment_id}")
            
            # Get scheduled reminders
            response = await self.client.get(
                f"{SCHEDULING_API_URL}/api/notifications/reminders/appointment/{self.test_appointment_id}"
            )
            response.raise_for_status()
            reminders = response.json()
            print(f"✅ Retrieved {len(reminders)} reminders")
            
            for reminder in reminders:
                print(f"   - {reminder['reminder_type']} reminder at {reminder['reminder_time']} ({reminder['hours_before_appointment']}h before)")
            
        except Exception as e:
            print(f"❌ Error with appointment reminders: {e}")
    
    async def test_immediate_notifications(self):
        """Test immediate notification sending"""
        print("\n📧 Testing Immediate Notifications...")
        
        notification_types = ["confirmation", "cancellation", "reschedule"]
        
        for notification_type in notification_types:
            try:
                response = await self.client.post(
                    f"{SCHEDULING_API_URL}/api/notifications/send/appointment/{self.test_appointment_id}",
                    json={"notification_type": notification_type}
                )
                response.raise_for_status()
                result = response.json()
                print(f"✅ Sent {notification_type} notification: {result['notification_id']}")
                
            except Exception as e:
                print(f"❌ Error sending {notification_type} notification: {e}")
    
    async def test_notification_history(self):
        """Test notification history retrieval"""
        print("\n📊 Testing Notification History...")
        
        try:
            # Get notification history
            params = {
                "recipient_type": "PATIENT",
                "recipient_id": self.test_patient_id,
                "limit": 10,
                "offset": 0
            }
            
            response = await self.client.get(
                f"{SCHEDULING_API_URL}/api/notifications/history/",
                params=params
            )
            response.raise_for_status()
            history = response.json()
            print(f"✅ Retrieved {len(history)} notification history records")
            
            for record in history[:3]:  # Show first 3 records
                print(f"   - {record['notification_category']} ({record['notification_type']}) at {record['sent_at']}")
            
        except Exception as e:
            print(f"❌ Error with notification history: {e}")
    
    async def test_task_manager_integration(self):
        """Test TaskManager integration"""
        print("\n🔄 Testing TaskManager Integration...")
        
        try:
            # Check if TaskManager is running
            response = await self.client.get(f"{TASK_MANAGER_URL}/health")
            response.raise_for_status()
            print("✅ TaskManager is running")
            
            # Get TaskManager tasks
            response = await self.client.get(f"{TASK_MANAGER_URL}/tasks/")
            response.raise_for_status()
            tasks = response.json()
            print(f"✅ TaskManager has {len(tasks)} tasks")
            
            # Show recent tasks
            for task in tasks[:3]:
                print(f"   - Task {task['id']}: {task['name']} ({task['status']})")
            
        except Exception as e:
            print(f"❌ Error with TaskManager integration: {e}")
    
    async def test_notification_templates(self):
        """Test notification templates"""
        print("\n📝 Testing Notification Templates...")
        
        try:
            # Get templates
            response = await self.client.get(
                f"{SCHEDULING_API_URL}/api/notifications/templates/{self.test_organization_id}"
            )
            response.raise_for_status()
            templates = response.json()
            print("✅ Retrieved notification templates")
            
            print("   Email Templates:")
            for key, template in templates.get("email_templates", {}).items():
                print(f"     - {key}: {template[:50]}...")
            
            print("   SMS Templates:")
            for key, template in templates.get("sms_templates", {}).items():
                print(f"     - {key}: {template}")
            
        except Exception as e:
            print(f"❌ Error with notification templates: {e}")
    
    async def run_all_tests(self):
        """Run all notification integration tests"""
        print("🚀 Starting Notification & TaskManager Integration Tests")
        print("=" * 60)
        
        await self.test_organization_settings()
        await self.test_patient_preferences()
        await self.test_appointment_reminders()
        await self.test_immediate_notifications()
        await self.test_notification_history()
        await self.test_task_manager_integration()
        await self.test_notification_templates()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")

async def main():
    """Main test function"""
    async with NotificationIntegrationTest() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    print("Notification & TaskManager Integration Test Script")
    print("Make sure both Scheduling2.0 and TaskManager services are running!")
    print()
    
    # Run the tests
    asyncio.run(main()) 