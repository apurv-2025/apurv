# =============================================================================
# FILE: backend/app/agent/state.py
# =============================================================================
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class TaskType(str, Enum):
    """Types of tasks the agent can handle"""
    SCHEDULE_APPOINTMENT = "schedule_appointment"
    RESCHEDULE_APPOINTMENT = "reschedule_appointment"
    CANCEL_APPOINTMENT = "cancel_appointment"
    FIND_AVAILABILITY = "find_availability"
    ANALYZE_SCHEDULE = "analyze_schedule"
    GENERATE_REPORT = "generate_report"
    OPTIMIZE_SCHEDULE = "optimize_schedule"
    PATIENT_INQUIRY = "patient_inquiry"
    PRACTITIONER_INQUIRY = "practitioner_inquiry"
    WAITLIST_MANAGEMENT = "waitlist_management"
    GENERAL_QUERY = "general_query"

class AgentStatus(str, Enum):
    """Status of agent tasks"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SchedulingAgentState(BaseModel):
    """State management for the scheduling agent"""
    
    # Task identification
    task_id: str
    task_type: TaskType
    user_id: str
    
    # Task details
    description: str
    context: Dict[str, Any] = {}
    
    # Status and timing
    status: AgentStatus = AgentStatus.PENDING
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    # Processing state
    current_step: str = ""
    steps_completed: List[str] = []
    steps_remaining: List[str] = []
    
    # Results and outputs
    result: Optional[Dict[str, Any]] = None
    message: str = ""
    suggestions: List[str] = []
    next_actions: List[str] = []
    
    # Performance metrics
    confidence_score: float = 0.0
    processing_time: float = 0.0
    error_message: Optional[str] = None
    
    # Tool execution results
    tool_results: Dict[str, Any] = {}
    tool_errors: Dict[str, str] = {}
    
    # Context and memory
    conversation_history: List[Dict[str, Any]] = []
    user_preferences: Dict[str, Any] = {}
    
    class Config:
        arbitrary_types_allowed = True 