"""
Pydantic schemas for Agentic Core
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Task types for agent operations."""
    CHAT = "chat"
    ANALYZE_CLAIM = "analyze_claim"
    ANALYZE_REJECTION = "analyze_rejection"
    GENERATE_REPORT = "generate_report"
    SEARCH_CLAIMS = "search_claims"
    VALIDATE_CLAIM = "validate_claim"
    ANSWER_QUESTION = "answer_question"


class AgentStatus(str, Enum):
    """Agent status values."""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ERROR = "error"


class Message(BaseModel):
    """Message model for chat conversations."""
    id: Optional[str] = None
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    """Conversation model."""
    id: Optional[str] = None
    user_id: str = Field(..., description="User identifier")
    title: Optional[str] = None
    messages: List[Message] = Field(default_factory=list)
    model: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    conversation_id: Optional[str] = None


class Task(BaseModel):
    """Task model for agent tasks."""
    id: Optional[str] = None
    user_id: str = Field(..., description="User identifier")
    task_type: TaskType = Field(..., description="Type of task")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Task status")
    data: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class Tool(BaseModel):
    """Tool model for agent tools."""
    id: Optional[str] = None
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    version: str = Field(default="1.0.0", description="Tool version")
    config: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True, description="Whether tool is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User(BaseModel):
    """User model."""
    id: Optional[str] = None
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True, description="Whether user is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ModelConfig(BaseModel):
    """Model configuration."""
    name: str = Field(..., description="Model name")
    provider: str = Field(..., description="Model provider")
    model_id: str = Field(..., description="Model identifier")
    config: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True, description="Whether model is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentRequest(BaseModel):
    """Request model for agent operations."""
    task_type: TaskType = Field(..., description="Type of task")
    user_id: str = Field(..., description="User identifier")
    task_description: str = Field(..., description="Task description")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Task context")
    task_id: Optional[str] = None
    conversation_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Response model for agent operations."""
    task_id: str = Field(..., description="Task identifier")
    task_type: TaskType = Field(..., description="Type of task")
    status: AgentStatus = Field(..., description="Task status")
    response: str = Field(..., description="Agent response")
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class HealthStatus(BaseModel):
    """Health status model."""
    status: str = Field(..., description="Overall status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0.0", description="Application version")
    uptime: Optional[str] = None
    active_tasks: int = Field(default=0, description="Number of active tasks")
    model_connected: bool = Field(default=True, description="Model connection status")
    database_connected: bool = Field(default=True, description="Database connection status")
    tools_count: int = Field(default=0, description="Number of available tools")


class PerformanceMetrics(BaseModel):
    """Performance metrics model."""
    total_requests: int = Field(default=0, description="Total requests")
    average_response_time: float = Field(default=0.0, description="Average response time")
    success_rate: float = Field(default=0.0, description="Success rate percentage")
    active_tasks: int = Field(default=0, description="Active tasks count")
    completed_tasks: int = Field(default=0, description="Completed tasks count")
    error_rate: float = Field(default=0.0, description="Error rate percentage")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ToolExecution(BaseModel):
    """Tool execution model."""
    id: Optional[str] = None
    task_id: str = Field(..., description="Task identifier")
    tool_id: str = Field(..., description="Tool identifier")
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[int] = None
    status: str = Field(default="pending", description="Execution status")
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class APIKey(BaseModel):
    """API key model."""
    id: Optional[str] = None
    user_id: str = Field(..., description="User identifier")
    name: str = Field(..., description="API key name")
    key_hash: str = Field(..., description="Hashed API key")
    permissions: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True, description="Whether key is active")
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Session(BaseModel):
    """Session model."""
    id: Optional[str] = None
    user_id: str = Field(..., description="User identifier")
    session_token: str = Field(..., description="Session token")
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = Field(default=True, description="Whether session is active")
    expires_at: datetime = Field(..., description="Session expiration")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)


class Metric(BaseModel):
    """Metric model."""
    id: Optional[str] = None
    metric_name: str = Field(..., description="Metric name")
    metric_value: float = Field(..., description="Metric value")
    metric_unit: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditLog(BaseModel):
    """Audit log model."""
    id: Optional[str] = None
    user_id: Optional[str] = None
    action: str = Field(..., description="Action performed")
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Additional schemas for specific use cases
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="User message")
    user_id: str = Field(..., description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Chat context")
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="Agent response")
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ToolInfo(BaseModel):
    """Tool information model."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    type: str = Field(..., description="Tool type")
    parameters: Optional[Dict[str, Any]] = None


class BatchTaskRequest(BaseModel):
    """Batch task request model."""
    tasks: List[AgentRequest] = Field(..., description="List of tasks")
    user_id: str = Field(..., description="User identifier")
    max_concurrent: int = Field(default=3, description="Maximum concurrent tasks")


class BatchTaskResponse(BaseModel):
    """Batch task response model."""
    batch_id: str = Field(..., description="Batch identifier")
    total_tasks: int = Field(..., description="Total number of tasks")
    results: List[Dict[str, Any]] = Field(..., description="Task results")
    created_at: datetime = Field(default_factory=datetime.utcnow) 