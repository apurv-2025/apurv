"""
Agentic Core Configuration for Claims Processing
Configuration settings for integrating Agentic Core with the claims processing system
"""

import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field


class AgenticConfig(BaseSettings):
    """Configuration for Agentic Core integration"""
    
    # AI Model Configuration
    AI_MODEL_PROVIDER: str = Field(default="openai", env="AI_MODEL_PROVIDER")
    AI_MODEL_NAME: str = Field(default="gpt-4", env="AI_MODEL_NAME")
    AI_API_KEY: Optional[str] = Field(default=None, env="AI_API_KEY")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://user:pass@localhost/claims_processing",
        env="DATABASE_URL"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # Application Configuration
    APP_NAME: str = Field(default="Claims Processing with Agentic Core", env="APP_NAME")
    APP_VERSION: str = Field(default="3.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Security Configuration
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    JWT_SECRET: str = Field(default="your-jwt-secret-here", env="JWT_SECRET")
    
    # CORS Configuration
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        env="CORS_ORIGINS"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")
    
    # Claims Processing Specific Configuration
    CLAIMS_PROCESSING_ENABLED: bool = Field(default=True, env="CLAIMS_PROCESSING_ENABLED")
    EDI_PARSER_ENABLED: bool = Field(default=True, env="EDI_PARSER_ENABLED")
    VALIDATOR_ENABLED: bool = Field(default=True, env="VALIDATOR_ENABLED")
    
    # Agentic Tools Configuration
    ENABLE_CLAIM_ANALYSIS: bool = Field(default=True, env="ENABLE_CLAIM_ANALYSIS")
    ENABLE_REJECTION_ANALYSIS: bool = Field(default=True, env="ENABLE_REJECTION_ANALYSIS")
    ENABLE_REPORT_GENERATION: bool = Field(default=True, env="ENABLE_REPORT_GENERATION")
    ENABLE_CLAIMS_SEARCH: bool = Field(default=True, env="ENABLE_CLAIMS_SEARCH")
    
    # Performance Configuration
    MAX_CONCURRENT_TASKS: int = Field(default=5, env="MAX_CONCURRENT_TASKS")
    TASK_TIMEOUT_SECONDS: int = Field(default=300, env="TASK_TIMEOUT_SECONDS")
    CHAT_TIMEOUT_SECONDS: int = Field(default=60, env="CHAT_TIMEOUT_SECONDS")
    
    # Monitoring Configuration
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    ENABLE_HEALTH_CHECKS: bool = Field(default=True, env="ENABLE_HEALTH_CHECKS")
    METRICS_RETENTION_HOURS: int = Field(default=168, env="METRICS_RETENTION_HOURS")
    
    # Conversation Configuration
    ENABLE_CONVERSATION_HISTORY: bool = Field(default=True, env="ENABLE_CONVERSATION_HISTORY")
    MAX_CONVERSATION_LENGTH: int = Field(default=100, env="MAX_CONVERSATION_LENGTH")
    CONVERSATION_RETENTION_DAYS: int = Field(default=90, env="CONVERSATION_RETENTION_DAYS")
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    UPLOAD_PATH: str = Field(default="/app/uploads", env="UPLOAD_PATH")
    ALLOWED_FILE_TYPES: str = Field(
        default="pdf,doc,docx,txt,csv,xlsx",
        env="ALLOWED_FILE_TYPES"
    )
    
    # External Services Configuration
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    LOGGLY_TOKEN: Optional[str] = Field(default=None, env="LOGGLY_TOKEN")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_cors_origins_list(self) -> list:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def get_allowed_file_types_list(self) -> list:
        """Get allowed file types as a list"""
        return [ft.strip() for ft in self.ALLOWED_FILE_TYPES.split(",")]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "ai_model_provider": self.AI_MODEL_PROVIDER,
            "ai_model_name": self.AI_MODEL_NAME,
            "database_url": self.DATABASE_URL,
            "redis_url": self.REDIS_URL,
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "debug": self.DEBUG,
            "log_level": self.LOG_LEVEL,
            "cors_origins": self.get_cors_origins_list(),
            "rate_limit_requests": self.RATE_LIMIT_REQUESTS,
            "rate_limit_window": self.RATE_LIMIT_WINDOW,
            "claims_processing_enabled": self.CLAIMS_PROCESSING_ENABLED,
            "edi_parser_enabled": self.EDI_PARSER_ENABLED,
            "validator_enabled": self.VALIDATOR_ENABLED,
            "enable_claim_analysis": self.ENABLE_CLAIM_ANALYSIS,
            "enable_rejection_analysis": self.ENABLE_REJECTION_ANALYSIS,
            "enable_report_generation": self.ENABLE_REPORT_GENERATION,
            "enable_claims_search": self.ENABLE_CLAIMS_SEARCH,
            "max_concurrent_tasks": self.MAX_CONCURRENT_TASKS,
            "task_timeout_seconds": self.TASK_TIMEOUT_SECONDS,
            "chat_timeout_seconds": self.CHAT_TIMEOUT_SECONDS,
            "enable_metrics": self.ENABLE_METRICS,
            "enable_health_checks": self.ENABLE_HEALTH_CHECKS,
            "metrics_retention_hours": self.METRICS_RETENTION_HOURS,
            "enable_conversation_history": self.ENABLE_CONVERSATION_HISTORY,
            "max_conversation_length": self.MAX_CONVERSATION_LENGTH,
            "conversation_retention_days": self.CONVERSATION_RETENTION_DAYS,
            "max_file_size": self.MAX_FILE_SIZE,
            "upload_path": self.UPLOAD_PATH,
            "allowed_file_types": self.get_allowed_file_types_list(),
        }


# Global configuration instance
_agentic_config: Optional[AgenticConfig] = None


def get_agentic_config() -> AgenticConfig:
    """Get the global AgenticConfig instance"""
    global _agentic_config
    if _agentic_config is None:
        _agentic_config = AgenticConfig()
    return _agentic_config


def initialize_agentic_config(config_dict: Optional[Dict[str, Any]] = None) -> AgenticConfig:
    """Initialize the global AgenticConfig instance"""
    global _agentic_config
    
    if config_dict:
        _agentic_config = AgenticConfig(**config_dict)
    else:
        _agentic_config = AgenticConfig()
    
    return _agentic_config


# Claims Processing Specific Configuration
class ClaimsProcessingConfig:
    """Claims processing specific configuration"""
    
    def __init__(self, agentic_config: AgenticConfig):
        self.agentic_config = agentic_config
    
    @property
    def enabled_tools(self) -> list:
        """Get list of enabled tools"""
        tools = []
        
        if self.agentic_config.ENABLE_CLAIM_ANALYSIS:
            tools.append("analyze_claim")
        
        if self.agentic_config.ENABLE_REJECTION_ANALYSIS:
            tools.append("analyze_rejection")
        
        if self.agentic_config.ENABLE_REPORT_GENERATION:
            tools.append("generate_report")
        
        if self.agentic_config.ENABLE_CLAIMS_SEARCH:
            tools.append("search_claims")
        
        return tools
    
    @property
    def tool_config(self) -> Dict[str, Any]:
        """Get tool configuration"""
        return {
            "analyze_claim": {
                "enabled": self.agentic_config.ENABLE_CLAIM_ANALYSIS,
                "timeout": self.agentic_config.TASK_TIMEOUT_SECONDS,
                "max_retries": 3
            },
            "analyze_rejection": {
                "enabled": self.agentic_config.ENABLE_REJECTION_ANALYSIS,
                "timeout": self.agentic_config.TASK_TIMEOUT_SECONDS,
                "max_retries": 3
            },
            "generate_report": {
                "enabled": self.agentic_config.ENABLE_REPORT_GENERATION,
                "timeout": self.agentic_config.TASK_TIMEOUT_SECONDS,
                "max_retries": 2
            },
            "search_claims": {
                "enabled": self.agentic_config.ENABLE_CLAIMS_SEARCH,
                "timeout": 30,
                "max_retries": 2
            }
        }
    
    @property
    def performance_config(self) -> Dict[str, Any]:
        """Get performance configuration"""
        return {
            "max_concurrent_tasks": self.agentic_config.MAX_CONCURRENT_TASKS,
            "task_timeout_seconds": self.agentic_config.TASK_TIMEOUT_SECONDS,
            "chat_timeout_seconds": self.agentic_config.CHAT_TIMEOUT_SECONDS,
            "enable_metrics": self.agentic_config.ENABLE_METRICS,
            "metrics_retention_hours": self.agentic_config.METRICS_RETENTION_HOURS
        }
    
    @property
    def conversation_config(self) -> Dict[str, Any]:
        """Get conversation configuration"""
        return {
            "enable_history": self.agentic_config.ENABLE_CONVERSATION_HISTORY,
            "max_length": self.agentic_config.MAX_CONVERSATION_LENGTH,
            "retention_days": self.agentic_config.CONVERSATION_RETENTION_DAYS
        }


def get_claims_processing_config() -> ClaimsProcessingConfig:
    """Get claims processing configuration"""
    agentic_config = get_agentic_config()
    return ClaimsProcessingConfig(agentic_config)


# Environment-specific configurations
class DevelopmentConfig(AgenticConfig):
    """Development environment configuration"""
    
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    AI_MODEL_NAME: str = "gpt-3.5-turbo"  # Use cheaper model for development
    ENABLE_METRICS: bool = False  # Disable metrics in development


class StagingConfig(AgenticConfig):
    """Staging environment configuration"""
    
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    ENABLE_HEALTH_CHECKS: bool = True


class ProductionConfig(AgenticConfig):
    """Production environment configuration"""
    
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    ENABLE_METRICS: bool = True
    ENABLE_HEALTH_CHECKS: bool = True
    MAX_CONCURRENT_TASKS: int = 10
    TASK_TIMEOUT_SECONDS: int = 600  # 10 minutes
    CHAT_TIMEOUT_SECONDS: int = 120  # 2 minutes


def get_environment_config(environment: str = None) -> AgenticConfig:
    """Get configuration for specific environment"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig
    }
    
    config_class = config_map.get(environment.lower(), DevelopmentConfig)
    return config_class()


# Configuration validation
def validate_config(config: AgenticConfig) -> bool:
    """Validate configuration settings"""
    errors = []
    
    # Check required settings
    if not config.AI_API_KEY:
        errors.append("AI_API_KEY is required")
    
    if not config.DATABASE_URL:
        errors.append("DATABASE_URL is required")
    
    if not config.SECRET_KEY or config.SECRET_KEY == "your-secret-key-here":
        errors.append("SECRET_KEY must be set to a secure value")
    
    if not config.JWT_SECRET or config.JWT_SECRET == "your-jwt-secret-here":
        errors.append("JWT_SECRET must be set to a secure value")
    
    # Check numeric ranges
    if config.RATE_LIMIT_REQUESTS <= 0:
        errors.append("RATE_LIMIT_REQUESTS must be positive")
    
    if config.RATE_LIMIT_WINDOW <= 0:
        errors.append("RATE_LIMIT_WINDOW must be positive")
    
    if config.MAX_CONCURRENT_TASKS <= 0:
        errors.append("MAX_CONCURRENT_TASKS must be positive")
    
    if config.TASK_TIMEOUT_SECONDS <= 0:
        errors.append("TASK_TIMEOUT_SECONDS must be positive")
    
    if config.CHAT_TIMEOUT_SECONDS <= 0:
        errors.append("CHAT_TIMEOUT_SECONDS must be positive")
    
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    return True 