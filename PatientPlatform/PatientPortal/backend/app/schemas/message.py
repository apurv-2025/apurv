from pydantic import BaseModel
from datetime import datetime
from .doctor import DoctorResponse

class MessageBase(BaseModel):
    subject: str
    content: str

class MessageCreate(MessageBase):
    recipient_id: int

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    is_read: bool
    created_at: datetime
    sender: DoctorResponse

    class Config:
        from_attributes = True 