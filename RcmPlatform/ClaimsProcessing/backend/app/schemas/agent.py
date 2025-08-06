# =============================================================================
# FILE: backend/app/schemas/agent.py
# =============================================================================
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

class TaskType(str, Enum):
    PROCESS_CLAIM = "process_claim"
    VALIDATE_CLAIM = "validate_claim"
    ANALYZE_REJECTION = "analyze_rejection"
    RECONCILE_PAYMENT = "reconcile_payment"
    GENERATE_REPORT = "generate_report"
    ANSWER_QUESTION = "answer_question"
    TROUBLESHOOT = "troubleshoot"

class AgentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_HUMAN = "requires_human"

class AgentRequest(BaseModel):
    task_type: TaskType
    user_id: str = Field(..., description="ID of the user making the request")
    task_description: str = Field(..., description="Natural language description of the task")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Additional context for the task")
    claim_id: Optional[int] = Field(None, description="Claim ID if task is claim-specific")
    file_path: Optional[str] = Field(None, description="Path to uploaded file if applicable")
    priority: int = Field(default=5, description="Task priority 1-10 (10 highest)")

class AgentResponse(BaseModel):
    task_id: str
    status: AgentStatus
    result: Optional[Dict[str, Any]] = None
    message: str
    suggestions: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    processing_time: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class ClaimInsight(BaseModel):
    claim_id: int
    insight_type: str  # "error", "warning", "optimization", "pattern"
    message: str
    confidence: float
    suggested_actions: List[str]
    affected_fields: List[str] = Field(default_factory=list)
