from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums for validation
class NotificationType(str, Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"

class NotificationCategory(str, Enum):
    BILLING = "billing"
    TEAM = "team"
    SYSTEM = "system"
    SECURITY = "security"

# Base schemas
class NotificationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: NotificationType = NotificationType.INFO
    category: NotificationCategory = NotificationCategory.SYSTEM

class NotificationCreate(NotificationBase):
    user_id: int = Field(..., gt=0)

class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    type: Optional[NotificationType] = None
    category: Optional[NotificationCategory] = None
    read: Optional[bool] = None

class NotificationMarkRead(BaseModel):
    read: bool = True

class NotificationBulkRead(BaseModel):
    notification_ids: List[int] = Field(..., min_items=1)
    read: bool = True

class NotificationBulkDelete(BaseModel):
    notification_ids: List[int] = Field(..., min_items=1)

class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    read: bool
    created_at: datetime
    updated_at: datetime

class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    page: int
    page_size: int
    total_pages: int

# Preference schemas
class NotificationPreferenceBase(BaseModel):
    email: bool = True
    push: bool = True
    sms: bool = False
    weekly_digest: bool = True

class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: int = Field(..., gt=0)

class NotificationPreferenceUpdate(BaseModel):
    email: Optional[bool] = None
    push: Optional[bool] = None
    sms: Optional[bool] = None
    weekly_digest: Optional[bool] = None

class NotificationPreferenceResponse(NotificationPreferenceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

# Filter and query schemas
class NotificationFilters(BaseModel):
    category: Optional[NotificationCategory] = None
    read: Optional[bool] = None
    search: Optional[str] = Field(None, min_length=1)
    type: Optional[NotificationType] = None
    
class NotificationQuery(NotificationFilters):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    order_by: Optional[str] = Field("created_at", pattern="^(created_at|updated_at|title)$")
    order_direction: Optional[str] = Field("desc", pattern="^(asc|desc)$")

# Response schemas
class UnreadCountResponse(BaseModel):
    count: int

class BulkOperationResponse(BaseModel):
    success: bool
    affected_count: int
    message: str

class SuccessResponse(BaseModel):
    success: bool
    message: str

# User schema (if you don't already have one)
class UserBase(BaseModel):
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    username: Optional[str] = Field(None, min_length=3, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Template schemas (optional)
class NotificationTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    title_template: str = Field(..., min_length=1, max_length=255)
    message_template: str = Field(..., min_length=1)
    type: NotificationType = NotificationType.INFO
    category: NotificationCategory = NotificationCategory.SYSTEM

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    title_template: Optional[str] = Field(None, min_length=1, max_length=255)
    message_template: Optional[str] = Field(None, min_length=1)
    type: Optional[NotificationType] = None
    category: Optional[NotificationCategory] = None
    is_active: Optional[bool] = None

class NotificationTemplateResponse(NotificationTemplateBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int