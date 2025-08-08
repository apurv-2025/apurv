# app/background/tasks.py
from typing import List, Dict, Any
import asyncio
import aiofiles
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import task as task_crud
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def send_email_notification(
    to_email: str, 
    subject: str, 
    message: str
) -> bool:
    """
    Send email notification (placeholder - integrate with actual email service)
    """
    try:
        # Simulate email sending
        await asyncio.sleep(1)
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


async def cleanup_old_files(days_old: int = 30) -> int:
    """
    Clean up old uploaded files that are not referenced in database
    """
    try:
        upload_dir = Path(settings.UPLOAD_FOLDER)
        if not upload_dir.exists():
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        # Get all files in upload directory
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                # Check file age
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime < cutoff_date:
                    # Check if file is referenced in database
                    db = SessionLocal()
                    try:
                        from app.crud.crud_attachment import attachment
                        db_attachment = db.query(attachment.model).filter(
                            attachment.model.file_path == str(file_path)
                        ).first()
                        
                        if not db_attachment:
                            file_path.unlink()
                            deleted_count += 1
                            logger.info(f"Deleted orphaned file: {file_path}")
                    finally:
                        db.close()
        
        logger.info(f"Cleanup completed. Deleted {deleted_count} files.")
        return deleted_count
        
    except Exception as e:
        logger.error(f"File cleanup failed: {e}")
        return 0


async def generate_reports() -> Dict[str, Any]:
    """
    Generate daily/weekly reports
    """
    try:
        db = SessionLocal()
        try:
            # Get task statistics
            stats = task_crud.get_stats(db)
            
            # Get overdue tasks
            overdue_tasks = task_crud.get_overdue(db)
            
            # Get tasks due today
            due_today = task_crud.get_due_today(db)
            
            report = {
                "generated_at": datetime.utcnow().isoformat(),
                "stats": stats.dict(),
                "overdue_count": len(overdue_tasks),
                "due_today_count": len(due_today),
                "overdue_tasks": [
                    {"id": task.id, "name": task.name, "due_date": task.due_date.isoformat()}
                    for task in overdue_tasks[:10]  # Limit to first 10
                ]
            }
            
            # Save report to file
            report_file = Path("reports") / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
            report_file.parent.mkdir(exist_ok=True)
            
            import json
            async with aiofiles.open(report_file, 'w') as f:
                await f.write(json.dumps(report, indent=2, default=str))
            
            logger.info(f"Daily report generated: {report_file}")
            return report
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return {}


async def send_due_date_reminders():
    """
    Send reminders for tasks due tomorrow
    """
    try:
        db = SessionLocal()
        try:
            from datetime import date
            tomorrow = date.today() + timedelta(days=1)
            
            # Get tasks due tomorrow
            tasks_due_tomorrow = db.query(task_crud.model).filter(
                task_crud.model.due_date == tomorrow,
                task_crud.model.status != "completed"
            ).all()
            
            for task in tasks_due_tomorrow:
                if task.client and task.client.email:
                    await send_email_notification(
                        to_email=task.client.email,
                        subject=f"Task Reminder: {task.name}",
                        message=f"Your task '{task.name}' is due tomorrow."
                    )
            
            logger.info(f"Sent {len(tasks_due_tomorrow)} due date reminders")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Failed to send due date reminders: {e}")
