from pydantic import BaseModel
from typing import Optional


class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str
    url: str


class FileDeleteResponse(BaseModel):
    success: bool
    message: str = "File deleted successfully"

# Update task.py to handle forward references
# Add this at the bottom of app/schemas/task.py

# Resolve forward references
from . import client, attachment
Task.model_rebuild()
attachment.Attachment.model_rebuild()
client.Client.model_rebuild()
