# ========================
# schemas.py
# ========================
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, Any, List


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None


class ClientCreate(ClientBase):
    pass


class ClientInDB(ClientBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class ActivityEventBase(BaseModel):
    event_type: str
    event_category: str
    event_description: str
    ip_address: Optional[str] = None
    location: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ActivityEventCreate(ActivityEventBase):
    client_id: Optional[str] = None


class ActivityEventInDB(ActivityEventBase):
    id: str
    user_id: str
    client_id: Optional[str] = None
    timestamp: datetime
    user: Optional[UserInDB] = None
    client: Optional[ClientInDB] = None

    class Config:
        from_attributes = True


class ActivityEventResponse(BaseModel):
    id: str
    date: str
    time: str
    event: str
    eventType: str
    ipAddress: Optional[str] = None
    location: Optional[str] = None
    clientName: Optional[str] = None
    userId: str
    details: Optional[Dict[str, Any]] = None


class ActivityEventFilters(BaseModel):
    event_type: Optional[str] = None
    date_range: Optional[str] = "all"
    search: Optional[str] = None
    client_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
