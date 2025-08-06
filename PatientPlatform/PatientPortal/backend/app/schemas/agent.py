"""
Agent schemas for PatientPortal AI functionality
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Task types for patient portal agent operations."""
    CHAT = "chat"
    SCHEDULE_APPOINTMENT = "schedule_appointment"
    CHECK_MEDICATIONS = "check_medications"
    VIEW_LAB_RESULTS = "view_lab_results"
    GENERATE_HEALTH_SUMMARY = "generate_health_summary"
    SETUP_MEDICATION_REMINDER = "setup_medication_reminder"
    FIND_DOCTOR = "find_doctor"
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


# Patient Portal specific schemas
class AppointmentSchedulingRequest(BaseModel):
    """Request model for appointment scheduling."""
    patient_id: str = Field(..., description="Patient identifier")
    appointment_type: str = Field(..., description="Type of appointment")
    preferred_date: Optional[str] = Field(None, description="Preferred date and time")
    preferred_doctor: Optional[str] = Field(None, description="Preferred doctor")
    location: Optional[str] = Field(None, description="Preferred location")
    notes: Optional[str] = Field(None, description="Additional notes")


class MedicationCheckRequest(BaseModel):
    """Request model for medication checking."""
    patient_id: str = Field(..., description="Patient identifier")
    include_refills: bool = Field(default=True, description="Include refill information")
    include_interactions: bool = Field(default=True, description="Include drug interaction information")


class LabResultsRequest(BaseModel):
    """Request model for lab results analysis."""
    patient_id: str = Field(..., description="Patient identifier")
    lab_result_id: Optional[str] = Field(None, description="Specific lab result ID")
    include_interpretation: bool = Field(default=True, description="Include AI interpretation")
    date_range: Optional[Dict[str, str]] = Field(None, description="Date range for results")


class HealthSummaryRequest(BaseModel):
    """Request model for health summary generation."""
    patient_id: str = Field(..., description="Patient identifier")
    report_type: str = Field(default="comprehensive", description="Type of health summary")
    include_recommendations: bool = Field(default=True, description="Include AI recommendations")
    include_trends: bool = Field(default=True, description="Include health trends")


class MedicationReminderRequest(BaseModel):
    """Request model for medication reminder setup."""
    patient_id: str = Field(..., description="Patient identifier")
    medication_id: str = Field(..., description="Medication identifier")
    reminder_time: str = Field(..., description="Reminder time")
    frequency: str = Field(default="daily", description="Reminder frequency")
    notification_method: str = Field(default="email", description="Notification method")


class DoctorSearchRequest(BaseModel):
    """Request model for doctor search."""
    specialty: str = Field(..., description="Medical specialty")
    location: Optional[str] = Field(None, description="Preferred location")
    insurance: Optional[str] = Field(None, description="Insurance provider")
    availability: Optional[str] = Field(None, description="Preferred availability")
    rating_min: Optional[float] = Field(None, description="Minimum rating") 