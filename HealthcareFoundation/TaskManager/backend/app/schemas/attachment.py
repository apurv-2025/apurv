from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class AttachmentBase(BaseModel):
    file_name: str = Field(..., max_length=255)
    file_size: Optional[int] = None
    file_type: Optional[str] = Field(None, max_length=100)
    task_id: Optional[int] = None


# Properties to receive on attachment creation
class AttachmentCreate(AttachmentBase):
    file_path: str = Field(..., max_length=500)


# Properties shared by models stored in DB
class AttachmentInDBBase(AttachmentBase):
    id: int
    file_path: str
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Attachment(AttachmentInDBBase):
    url: str = ""


# Properties stored in DB
class AttachmentInDB(AttachmentInDBBase):
    pass

# app/schemas/response.py
from pydantic import BaseModel
from typing import Any, Optional, List, Generic, TypeVar

DataType = TypeVar('DataType')


class ResponseModel(BaseModel, Generic[DataType]):
    success: bool = True
    data: Optional[DataType] = None
    message: str = ""
    total: Optional[int] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[List[str]] = None


class PaginatedResponse(BaseModel, Generic[DataType]):
    items: List[DataType]
    total: int
    page: int = 1
    per_page: int = 10
    pages: int = 1
