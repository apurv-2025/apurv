# =============================================================================
# FILE: backend/app/config.py
# =============================================================================
import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        # Fallback for very old versions
        from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/edi_claims")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # App settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    class Config:
        env_file = ".env"

class AgentSettings(BaseSettings):
    """Configuration for the AI agent"""
    
    # Model configuration
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "openai")  # openai, anthropic, custom
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
    MODEL_MAX_TOKENS: int = int(os.getenv("MODEL_MAX_TOKENS", "2000"))
    
    # Custom model settings
    CUSTOM_MODEL_ENDPOINT: Optional[str] = os.getenv("CUSTOM_MODEL_ENDPOINT")
    CUSTOM_MODEL_API_KEY: Optional[str] = os.getenv("CUSTOM_MODEL_API_KEY")
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Anthropic settings
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Agent behavior
    MAX_TOOL_RETRIES: int = int(os.getenv("MAX_TOOL_RETRIES", "3"))
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "300"))  # 5 minutes
    ENABLE_AGENT_LOGGING: bool = os.getenv("ENABLE_AGENT_LOGGING", "true").lower() == "true"
    
    # LangGraph settings
    GRAPH_RECURSION_LIMIT: int = int(os.getenv("GRAPH_RECURSION_LIMIT", "50"))
    
    class Config:
        env_file = ".env"

# Global settings instances
settings = Settings()
agent_settings = AgentSettings()
