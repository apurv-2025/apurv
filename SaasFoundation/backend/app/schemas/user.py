from pydantic import BaseModel
from datetime import datetime
import uuid

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
