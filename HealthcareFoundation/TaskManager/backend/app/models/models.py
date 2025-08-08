from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    tasks = relationship("Task", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True, index=True)
    due_time = Column(Time, nullable=True)
    priority = Column(String(20), default="none", nullable=False, index=True)
    status = Column(String(20), default="todo", nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True, index=True)

    # Relationships
    client = relationship("Client", back_populates="tasks")
    attachments = relationship("TaskAttachment", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}')>"

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.status == "completed":
            return False
        
        due_datetime = datetime.combine(
            self.due_date, 
            self.due_time or datetime.min.time()
        )
        return due_datetime < datetime.now()


class TaskAttachment(Base, TimestampMixin):
    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(100), nullable=True)
    uploaded_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    task = relationship("Task", back_populates="attachments")

    def __repr__(self):
        return f"<TaskAttachment(id={self.id}, file_name='{self.file_name}')>"
