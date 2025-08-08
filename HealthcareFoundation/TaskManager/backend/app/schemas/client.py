from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


# Shared properties
class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


# Properties to receive on client creation
class ClientCreate(ClientBase):
    pass


# Properties to receive on client update
class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


# Properties shared by models stored in DB
class ClientInDBBase(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Client(ClientInDBBase):
    task_count: int = 0


# Properties stored in DB
class ClientInDB(ClientInDBBase):
    pass

