import asyncio
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Task, TaskExecution
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskExecutor:
    def __init__(self):
        self.running_tasks = {}
    
    async def execute_task(self, task_id: int):
        """Execute a task based on its type"""
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                logger.error(f"Task {task_id} not found")
                return
            
            # Create execution record
            execution = TaskExecution(
                task_id=task_id,
                status="running"
            )
            db.add(execution)
            task.status = "running"
            db.commit()
            db.refresh(execution)
            
            try:
                result = None
                if task.task_type == "email":
                    result = await self._send_email(task.payload)
                elif task.task_type == "sms":
                    result = await self._send_sms(task.payload)
                elif task.task_type == "webhook":
                    result = await self._call_webhook(task.payload)
                elif task.task_type == "reminder":
                    result = await self._send_reminder(task.payload)
                else:
                    raise ValueError(f"Unknown task type: {task.task_type}")
                
                # Mark as successful
                execution.status = "success"
                execution.result = result
                execution.completed_at = datetime.utcnow()
                task.status = "completed"
                
                # Call callback if provided
                if task.callback_url:
                    await self._call_callback(task.callback_url, {
                        "task_id": task_id,
                        "status": "success",
                        "result": result
                    })
                
            except Exception as e:
                logger.error(f"Task {task_id} failed: {str(e)}")
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                
                # Handle retries
                task.retry_count += 1
                if task.retry_count < task.max_retries:
                    task.status = "pending"
                    # Schedule retry (in real implementation, use proper job queue)
                    asyncio.create_task(self._retry_task(task_id, delay=60 * task.retry_count))
                else:
                    task.status = "failed"
                
                # Call callback with error
                if task.callback_url:
                    await self._call_callback(task.callback_url, {
                        "task_id": task_id,
                        "status": "failed",
                        "error": str(e)
                    })
            
            db.commit()
            
        finally:
            db.close()
    
    async def _send_email(self, payload: dict) -> dict:
        """Send email task"""
        # This is a simplified email sender
        # In production, use proper email service like SendGrid, SES, etc.
        
        to_email = payload.get("to_email")
        subject = payload.get("subject")
        body = payload.get("body")
        
        if not all([to_email, subject, body]):
            raise ValueError("Missing required email fields: to_email, subject, body")
        
        # Simulate email sending
        await asyncio.sleep(1)  # Simulate API call delay
        
        logger.info(f"Email sent to {to_email} with subject: {subject}")
        
        return {
            "to_email": to_email,
            "subject": subject,
            "sent_at": datetime.utcnow().isoformat(),
            "status": "delivered"
        }
    
    async def _send_sms(self, payload: dict) -> dict:
        """Send SMS task"""
        phone_number = payload.get("phone_number")
        message = payload.get("message")
        
        if not all([phone_number, message]):
            raise ValueError("Missing required SMS fields: phone_number, message")
        
        # Simulate SMS sending
        await asyncio.sleep(1)
        
        logger.info(f"SMS sent to {phone_number}: {message}")
        
        return {
            "phone_number": phone_number,
            "message": message,
            "sent_at": datetime.utcnow().isoformat(),
            "status": "delivered"
        }
    
    async def _call_webhook(self, payload: dict) -> dict:
        """Call webhook task"""
        url = payload.get("url")
        method = payload.get("method", "POST")
        data = payload.get("data", {})
        headers = payload.get("headers", {})
        
        if not url:
            raise ValueError("Missing required webhook field: url")
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            
            return {
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "response": response.text,
                "called_at": datetime.utcnow().isoformat()
            }
    
    async def _send_reminder(self, payload: dict) -> dict:
        """Send reminder task (could be email, SMS, or push notification)"""
        reminder_type = payload.get("type", "email")
        recipient = payload.get("recipient")
        message = payload.get("message")
        
        if not all([recipient, message]):
            raise ValueError("Missing required reminder fields: recipient, message")
        
        if reminder_type == "email":
            return await self._send_email({
                "to_email": recipient,
                "subject": "Reminder",
                "body": message
            })
        elif reminder_type == "sms":
            return await self._send_sms({
                "phone_number": recipient,
                "message": message
            })
        else:
            raise ValueError(f"Unsupported reminder type: {reminder_type}")
    
    async def _call_callback(self, callback_url: str, data: dict):
        """Call callback URL with task result"""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(callback_url, json=data, timeout=10.0)
        except Exception as e:
            logger.error(f"Failed to call callback URL {callback_url}: {str(e)}")
    
    async def _retry_task(self, task_id: int, delay: int):
        """Retry a failed task after delay"""
        await asyncio.sleep(delay)
        await self.execute_task(task_id)
    
    async def schedule_task(self, task_id: int, scheduled_time: datetime):
        """Schedule a task for future execution"""
        now = datetime.utcnow()
        delay = (scheduled_time - now).total_seconds()
        
        if delay > 0:
            await asyncio.sleep(delay)
        
        await self.execute_task(task_id)

