from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    task_type: str
    payload: Dict[Any, Any]
    scheduled_time: datetime
    callback_url: Optional[str] = None
    max_retries: Optional[int] = 3

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    callback_url: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    task_type: str
    payload: Dict[Any, Any]
    status: str
    scheduled_time: datetime
    created_at: datetime
    updated_at: datetime
    callback_url: Optional[str]
    max_retries: int
    retry_count: int

    class Config:
        from_attributes = True

class TaskExecutionResponse(BaseModel):
    id: int
    task_id: int
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
    result: Optional[Dict[Any, Any]]
    error_message: Optional[str]

    class Config:
        from_attributes = True
