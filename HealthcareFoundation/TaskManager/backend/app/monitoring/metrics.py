# app/monitoring/metrics.py
import time
import psutil
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Task, Client, TaskAttachment


class MetricsCollector:
    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        """Collect system performance metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
    
    @staticmethod
    def get_database_metrics(db: Session) -> Dict[str, Any]:
        """Collect database metrics"""
        return {
            "total_tasks": db.query(Task).count(),
            "total_clients": db.query(Client).count(),
            "total_attachments": db.query(TaskAttachment).count(),
            "completed_tasks": db.query(Task).filter(Task.status == "completed").count(),
            "pending_tasks": db.query(Task).filter(Task.status.in_(["todo", "in_progress"])).count(),
        }
