# File: app/core/config.py - Updated Configuration
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "EDI 278/275 Prior Authorization System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@postgres:5432/prior_auth_db"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/tiff", "application/pdf"
    ]
    UPLOAD_DIRECTORY: str = "./uploads"
    
    # EDI Configuration
    EDI_SUBMITTER_ID: str = "PROVIDER001"
    EDI_RECEIVER_ID: str = "PAYER001"
    
    # Authorization Settings
    DEFAULT_AUTH_DAYS: int = 90
    MAX_UNITS_AUTO_APPROVE: int = 10
    REQUIRE_CLINICAL_INFO: bool = True

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
