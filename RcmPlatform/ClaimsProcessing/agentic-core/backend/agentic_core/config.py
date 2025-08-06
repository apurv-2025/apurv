"""
Configuration management for Agentic Core
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = Field(default="Agentic Core", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # AI Model Configuration
    AI_MODEL_PROVIDER: str = Field(default="openai", env="AI_MODEL_PROVIDER")
    AI_MODEL_NAME: str = Field(default="gpt-4", env="AI_MODEL_NAME")
    AI_API_KEY: Optional[str] = Field(default=None, env="AI_API_KEY")
    AI_MAX_TOKENS: int = Field(default=1000, env="AI_MAX_TOKENS")
    AI_TEMPERATURE: float = Field(default=0.7, env="AI_TEMPERATURE")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://user:pass@localhost/agentic_core",
        env="DATABASE_URL"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    JWT_SECRET: str = Field(default="your-jwt-secret-here", env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION: int = Field(default=3600, env="JWT_EXPIRATION")
    
    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        env="CORS_ORIGINS"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")
    
    # API Configuration
    API_PREFIX: str = Field(default="/api", env="API_PREFIX")
    API_V1_STR: str = Field(default="/v1", env="API_V1_STR")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    # Logging
    LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # File Upload
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["txt", "pdf", "doc", "docx", "csv", "json"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # External Services
    EXTERNAL_API_TIMEOUT: int = Field(default=30, env="EXTERNAL_API_TIMEOUT")
    EXTERNAL_API_RETRIES: int = Field(default=3, env="EXTERNAL_API_RETRIES")
    
    # Task Processing
    MAX_CONCURRENT_TASKS: int = Field(default=10, env="MAX_CONCURRENT_TASKS")
    TASK_TIMEOUT: int = Field(default=300, env="TASK_TIMEOUT")  # 5 minutes
    TASK_RETENTION_DAYS: int = Field(default=30, env="TASK_RETENTION_DAYS")
    
    # Conversation
    MAX_CONVERSATION_LENGTH: int = Field(default=100, env="MAX_CONVERSATION_LENGTH")
    CONVERSATION_RETENTION_DAYS: int = Field(default=90, env="CONVERSATION_RETENTION_DAYS")
    
    # Tools
    ENABLE_DEFAULT_TOOLS: bool = Field(default=True, env="ENABLE_DEFAULT_TOOLS")
    TOOL_EXECUTION_TIMEOUT: int = Field(default=60, env="TOOL_EXECUTION_TIMEOUT")
    
    # Cache
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    CACHE_MAX_SIZE: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Email (if needed)
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = Field(default=True, env="SMTP_USE_TLS")
    
    # Claims Processing Specific
    CLAIMS_PROCESSING_ENABLED: bool = Field(default=True, env="CLAIMS_PROCESSING_ENABLED")
    ENABLE_CLAIM_ANALYSIS: bool = Field(default=True, env="ENABLE_CLAIM_ANALYSIS")
    ENABLE_REJECTION_ANALYSIS: bool = Field(default=True, env="ENABLE_REJECTION_ANALYSIS")
    ENABLE_REPORT_GENERATION: bool = Field(default=True, env="ENABLE_REPORT_GENERATION")
    ENABLE_CLAIMS_SEARCH: bool = Field(default=True, env="ENABLE_CLAIMS_SEARCH")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Get allowed file types as a list."""
        if isinstance(self.ALLOWED_FILE_TYPES, str):
            return [ft.strip() for ft in self.ALLOWED_FILE_TYPES.split(",")]
        return self.ALLOWED_FILE_TYPES


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings."""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    AI_MODEL_PROVIDER: str = "mock"  # Use mock provider for development


class StagingSettings(Settings):
    """Staging environment settings."""
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    AI_MODEL_PROVIDER: str = "openai"


class ProductionSettings(Settings):
    """Production environment settings."""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    AI_MODEL_PROVIDER: str = "openai"
    RATE_LIMIT_REQUESTS: int = 50  # More restrictive in production


def get_settings() -> Settings:
    """Get settings based on environment."""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "staging":
        return StagingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
_settings: Optional[Settings] = None


def get_settings_instance() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings 