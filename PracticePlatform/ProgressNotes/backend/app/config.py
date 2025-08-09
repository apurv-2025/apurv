# backend/config.py - Simplified version for testing
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./mental_health_ehr.db"

    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # File upload settings
    upload_directory: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [
        "application/pdf",
        "image/jpeg", 
        "image/png",
        "text/plain",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    # CORS settings - simplified without validator for now
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Session settings
    session_timeout_minutes: int = 15

    # Audit settings
    enable_audit_logging: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
