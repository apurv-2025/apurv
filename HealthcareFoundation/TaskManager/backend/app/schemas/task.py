# app/schemas/task.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum


class TaskPriority(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Shared properties
class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    priority: TaskPriority = TaskPriority.NONE
    status: TaskStatus = TaskStatus.TODO
    client_id: Optional[int] = None


# Properties to receive on task creation
class TaskCreate(TaskBase):
    pass


# Properties to receive on task update
class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    client_id: Optional[int] = None


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Task(TaskInDBBase):
    attachments: List["Attachment"] = []
    client: Optional["Client"] = None


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass


# For task statistics
class TaskStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    due_today: int
    completion_rate: float
