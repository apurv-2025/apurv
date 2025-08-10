# File: app/core/config.py (FIXED for Pydantic v2)
import os
from typing import List, Union, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator, computed_field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Health Insurance Verification API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database - Individual components
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "health_insurance_db"
    POSTGRES_PORT: str = "5432"
    
    # Allow DATABASE_URL to be set directly via environment
    DATABASE_URL: Optional[str] = None
    
    @computed_field
    @property
    def effective_database_url(self) -> str:
        """Get the effective database URL, preferring DATABASE_URL if set."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/tiff", "application/pdf"
    ]
    UPLOAD_DIRECTORY: str = "./uploads"
    
    # OCR Configuration
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    
    # EDI Configuration
    EDI_SUBMITTER_ID: str = "SUBMITTER"
    EDI_RECEIVER_ID: str = "RECEIVER"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # This fixes the "extra inputs not permitted" error
    }


settings = Settings()

# Alternative simpler configuration if the above doesn't work
class SimpleSettings(BaseSettings):
    """Simplified settings class for Pydantic v2 compatibility."""
    
    # Basic settings
    PROJECT_NAME: str = "Health Insurance Verification API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database URL - direct field (not computed)
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/health_insurance_db"
    
    # File settings
    MAX_UPLOAD_SIZE: int = 10485760
    UPLOAD_DIRECTORY: str = "./uploads"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


# Use the simple settings if needed
# settings = SimpleSettings()
