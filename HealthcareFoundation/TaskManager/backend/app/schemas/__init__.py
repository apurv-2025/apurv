# app/schemas/__init__.py
from .task import Task, TaskCreate, TaskUpdate, TaskInDB
from .client import Client, ClientCreate, ClientUpdate, ClientInDB
from .attachment import Attachment, AttachmentCreate, AttachmentInDB
from .response import ResponseModel, ErrorResponse
