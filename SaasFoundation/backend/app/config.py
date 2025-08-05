from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/saas_app"
    
    # JWT
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: Optional[str] = None
    email_password: Optional[str] = None
    
    # CORS
    allowed_origins: list = ["http://localhost:3000"]
    
    # App
    app_name: str = "SaaS Platform API"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False
        
        # Map environment variables
        env_prefix = ""
        fields = {
            'database_url': {'env': 'DATABASE_URL'},
            'jwt_secret': {'env': 'JWT_SECRET'},
            'email_user': {'env': 'EMAIL_USER'},
            'email_password': {'env': 'EMAIL_PASSWORD'},
        }

settings = Settings()
