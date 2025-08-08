from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    task_type = Column(String, nullable=False)  # 'email', 'sms', 'webhook', 'reminder'
    payload = Column(JSON)  # Task-specific data
    status = Column(String, default="pending")  # pending, running, completed, failed
    scheduled_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    callback_url = Column(String)  # Optional webhook URL for completion notification
    max_retries = Column(Integer, default=3)
    retry_count = Column(Integer, default=0)
    
    executions = relationship("TaskExecution", back_populates="task")

class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    status = Column(String)  # running, success, failed
    result = Column(JSON)  # Execution result
    error_message = Column(Text)
    
    task = relationship("Task", back_populates="executions")
