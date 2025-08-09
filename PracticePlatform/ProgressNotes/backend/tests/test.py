# backend/tests/conftest.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import User
from app.auth import get_password_hash

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("testpassword"),
        first_name="Test",
        last_name="User",
        role="clinician"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": test_user.email, "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# backend/tests/test_auth.py
def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": test_user.email, "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == test_user.email

def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_unauthorized_access(client):
    response = client.get("/auth/me")
    assert response.status_code == 401

# backend/tests/test_patients.py
def test_create_patient(client, auth_headers):
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "medical_record_number": "MRN123456",
        "phone": "555-1234",
        "email": "john.doe@example.com"
    }
    response = client.post("/patients/", json=patient_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["medical_record_number"] == "MRN123456"

def test_get_patients(client, auth_headers):
    response = client.get("/patients/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_patient_missing_fields(client, auth_headers):
    patient_data = {
        "first_name": "John",
        # Missing required fields
    }
    response = client.post("/patients/", json=patient_data, headers=auth_headers)
    assert response.status_code == 422

# backend/tests/test_notes.py
import uuid
from datetime import datetime

def test_create_note(client, auth_headers):
    # First create a patient
    patient_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1985-05-15",
        "medical_record_number": "MRN789012"
    }
    patient_response = client.post("/patients/", json=patient_data, headers=auth_headers)
    patient_id = patient_response.json()["id"]
    
    # Create note
    note_data = {
        "patient_id": patient_id,
        "note_type": "SOAP",
        "session_date": "2024-01-15T10:00:00",
        "content": {
            "subjective": "Patient reports feeling anxious",
            "objective": "Patient appears restless",
            "assessment": "Generalized anxiety",
            "plan": "Continue therapy sessions"
        }
    }
    response = client.post("/notes/", json=note_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["note_type"] == "SOAP"
    assert data["patient_id"] == patient_id

def test_get_notes(client, auth_headers):
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_sign_note(client, auth_headers):
    # Create patient and note first
    patient_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "date_of_birth": "1980-03-20",
        "medical_record_number": "MRN345678"
    }
    patient_response = client.post("/patients/", json=patient_data, headers=auth_headers)
    patient_id = patient_response.json()["id"]
    
    note_data = {
        "patient_id": patient_id,
        "note_type": "SOAP",
        "session_date": "2024-01-15T14:00:00",
        "content": {"subjective": "Test note", "objective": "", "assessment": "", "plan": ""}
    }
    note_response = client.post("/notes/", json=note_data, headers=auth_headers)
    note_id = note_response.json()["id"]
    
    # Sign the note
    response = client.post(f"/notes/{note_id}/sign", headers=auth_headers, json={})
    assert response.status_code == 200
    data = response.json()
    assert data["is_signed"] == True
    assert data["is_locked"] == True

# backend/middleware.py
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
import time
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request timing."""
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

# backend/utils/validators.py
import re
from typing import Optional
from datetime import datetime, date

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's 10 or 11 digits (with or without country code)
    return len(digits_only) in [10, 11]

def validate_medical_record_number(mrn: str) -> bool:
    """Validate medical record number format."""
    # MRN should be alphanumeric and at least 6 characters
    pattern = r'^[A-Za-z0-9]{6,}$'
    return re.match(pattern, mrn) is not None

def validate_date_of_birth(dob: date) -> bool:
    """Validate date of birth (must be in the past and reasonable)."""
    today = date.today()
    if dob >= today:
        return False
    
    # Check if age is reasonable (between 0 and 150 years)
    age = today.year - dob.year
    if age < 0 or age > 150:
        return False
    
    return True

def validate_session_date(session_date: datetime) -> bool:
    """Validate session date (should not be too far in the future)."""
    now = datetime.now()
    # Allow sessions up to 1 week in the future
    max_future = now.replace(day=now.day + 7) if now.day <= 24 else now.replace(month=now.month + 1, day=now.day - 24)
    return session_date <= max_future

# backend/utils/encryption.py
from cryptography.fernet import Fernet
from typing import Optional
import base64
import os

class EncryptionService:
    """Service for encrypting/decrypting sensitive data."""
    
    def __init__(self):
        # In production, store this in environment variables or key management service
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            # Generate a key for development (don't do this in production)
            key = Fernet.generate_key()
        else:
            key = key.encode()
        
        self.cipher_suite = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        if not data:
            return data
        
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string."""
        if not encrypted_data:
            return encrypted_data
        
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception:
            # Return original data if decryption fails (for backward compatibility)
            return encrypted_data

# Global instance
encryption_service = EncryptionService()

# backend/utils/audit.py
from typing import Dict, Any, Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from models import AuditLog

class AuditLogger:
    """Enhanced audit logging utility."""
    
    @staticmethod
    def log_user_action(
        db: Session,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """Log a user action with detailed context."""
        
        # Sanitize sensitive data
        if old_values:
            old_values = AuditLogger._sanitize_data(old_values)
        if new_values:
            new_values = AuditLogger._sanitize_data(new_values)
        
        # Add additional context if provided
        if additional_context:
            if new_values:
                new_values.update(additional_context)
            else:
                new_values = additional_context
        
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(audit_log)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            # Log the error but don't fail the main operation
            print(f"Failed to log audit entry: {e}")
    
    @staticmethod
    def _sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive fields from audit data."""
        sensitive_fields = [
            'password', 'password_hash', 'secret_key', 'token',
            'access_token', 'refresh_token', 'api_key'
        ]
        
        sanitized = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = AuditLogger._sanitize_data(value)
            else:
                sanitized[key] = value
        
        return sanitized

# backend/utils/file_handler.py
import os
import uuid
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from pathlib import Path
import magic

class FileHandler:
    """Handle file uploads and management."""
    
    def __init__(self, upload_directory: str = "./uploads", max_size: int = 10 * 1024 * 1024):
        self.upload_directory = Path(upload_directory)
        self.max_size = max_size
        self.allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/gif',
            'text/plain',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        # Create upload directory if it doesn't exist
        self.upload_directory.mkdir(parents=True, exist_ok=True)
    
    async def save_file(self, file: UploadFile, subfolder: str = "") -> dict:
        """Save uploaded file and return file info."""
        
        # Validate file size
        content = await file.read()
        if len(content) > self.max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {self.max_size} bytes"
            )
        
        # Validate file type
        mime_type = magic.from_buffer(content, mime=True)
        if mime_type not in self.allowed_types:
            raise HTTPException(
                status_code=415,
                detail=f"File type {mime_type} not allowed"
            )
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Create subfolder if specified
        save_directory = self.upload_directory / subfolder if subfolder else self.upload_directory
        save_directory.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = save_directory / unique_filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "filename": file.filename,
            "saved_filename": unique_filename,
            "file_path": str(file_path),
            "file_size": len(content),
            "mime_type": mime_type
        }
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get file information."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                stat = path.stat()
                return {
                    "filename": path.name,
                    "file_size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime
                }
            return None
        except Exception:
            return None

# backend/utils/exceptions.py
from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BusinessLogicException(Exception):
    """Custom exception for business logic errors."""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationException(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

def create_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized HTTP exception."""
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )

# Common HTTP exceptions
def not_found_exception(resource: str = "Resource") -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found"
    )

def permission_denied_exception(action: str = "perform this action") -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Not enough permissions to {action}"
    )

def validation_exception(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )

def conflict_exception(message: str) -> HTTPException:
    return create_http_exception(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )

# backend/utils/response_models.py
from pydantic import BaseModel
from typing import Any, Optional, List, Dict

class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    """Standard error response model."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

class PaginatedAPIResponse(APIResponse):
    """Paginated API response model."""
    meta: Optional[PaginationMeta] = None

def create_success_response(
    data: Any = None,
    message: str = "Operation successful"
) -> APIResponse:
    """Create a success response."""
    return APIResponse(
        success=True,
        message=message,
        data=data
    )

def create_error_response(
    message: str,
    error_code: str = None,
    details: Dict[str, Any] = None
) -> ErrorResponse:
    """Create an error response."""
    return ErrorResponse(
        success=False,
        message=message,
        error_code=error_code,
        details=details
    )
