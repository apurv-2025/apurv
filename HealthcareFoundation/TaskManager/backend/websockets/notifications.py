# app/websockets/notifications.py
import json
from datetime import datetime
from typing import Dict, Any
from app.websockets.connection_manager import ConnectionManager


class NotificationManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    async def send_task_notification(self, user_id: int, event_type: str, task_data: Dict[str, Any]):
        """Send task-related notifications"""
        notification = {
            "type": "task_notification",
            "event": event_type,
            "data": task_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.connection_manager.send_to_user(
            json.dumps(notification), 
            user_id
        )

    async def send_system_notification(self, message: str, notification_type: str = "info"):
        """Send system-wide notifications"""
        notification = {
            "type": "system_notification",
            "level": notification_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.connection_manager.broadcast(json.dumps(notification))

    async def send_due_date_alert(self, user_id: int, task_id: int, task_name: str):
        """Send due date alerts"""
        await self.send_task_notification(
            user_id=user_id,
            event_type="due_date_alert",
            task_data={
                "task_id": task_id,
                "task_name": task_name,
                "message": f"Task '{task_name}' is due soon!"
            }
        )
