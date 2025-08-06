"""
Agentic Core - Reusable AI Agent Framework

A comprehensive framework for building AI-powered applications with
integrated chat, task processing, and tool management capabilities.
"""

__version__ = "1.0.0"
__author__ = "Agentic Core Team"
__description__ = "Reusable AI Agent Framework"

# Core classes
from .core import (
    AgenticCore,
    create_agentic_core,
    get_agentic_core,
    initialize_agentic_core
)

from .manager import (
    AgentManager,
    get_agent_manager,
    initialize_agent_manager
)

# Schemas and models
from .schemas import (
    AgentRequest,
    AgentResponse,
    TaskType,
    AgentStatus,
    Message,
    Conversation,
    Task,
    Tool,
    User,
    ModelConfig,
    HealthStatus,
    PerformanceMetrics,
    ToolExecution,
    APIKey,
    Session,
    Metric,
    AuditLog,
    ChatRequest,
    ChatResponse,
    ToolInfo,
    BatchTaskRequest,
    BatchTaskResponse
)

# Model providers
from .models import (
    BaseModelProvider,
    OpenAIModelProvider,
    AnthropicModelProvider,
    MockModelProvider,
    CustomModelProvider,
    create_model_provider
)

# Tools
from .tools import (
    BaseTool,
    ToolRegistry,
    get_global_tool_registry,
    SearchTool,
    CalculatorTool,
    FileReadTool,
    DateTimeTool,
    WeatherTool,
    tool
)

# Configuration
from .config import (
    Settings,
    DevelopmentSettings,
    StagingSettings,
    ProductionSettings,
    get_settings,
    get_settings_instance
)

# Version info
VERSION = __version__
AUTHOR = __author__
DESCRIPTION = __description__

# Default exports
__all__ = [
    # Core
    "AgenticCore",
    "create_agentic_core",
    "get_agentic_core",
    "initialize_agentic_core",
    
    # Manager
    "AgentManager",
    "get_agent_manager",
    "initialize_agent_manager",
    
    # Schemas
    "AgentRequest",
    "AgentResponse",
    "TaskType",
    "AgentStatus",
    "Message",
    "Conversation",
    "Task",
    "Tool",
    "User",
    "ModelConfig",
    "HealthStatus",
    "PerformanceMetrics",
    "ToolExecution",
    "APIKey",
    "Session",
    "Metric",
    "AuditLog",
    "ChatRequest",
    "ChatResponse",
    "ToolInfo",
    "BatchTaskRequest",
    "BatchTaskResponse",
    
    # Models
    "BaseModelProvider",
    "OpenAIModelProvider",
    "AnthropicModelProvider",
    "MockModelProvider",
    "CustomModelProvider",
    "create_model_provider",
    
    # Tools
    "BaseTool",
    "ToolRegistry",
    "get_global_tool_registry",
    "SearchTool",
    "CalculatorTool",
    "FileReadTool",
    "DateTimeTool",
    "WeatherTool",
    "tool",
    
    # Configuration
    "Settings",
    "DevelopmentSettings",
    "StagingSettings",
    "ProductionSettings",
    "get_settings",
    "get_settings_instance",
    
    # Version info
    "VERSION",
    "AUTHOR",
    "DESCRIPTION"
] 