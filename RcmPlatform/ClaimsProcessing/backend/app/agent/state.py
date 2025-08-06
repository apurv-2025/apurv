# =============================================================================
# FILE: backend/app/agent/state.py
# =============================================================================
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from app.schemas.agent import TaskType, AgentStatus

@dataclass
class ClaimsAgentState:
    """State object for the LangGraph agent"""
    
    # Core task information
    task_id: str
    task_type: TaskType
    user_id: str
    description: str
    status: AgentStatus = AgentStatus.PENDING
    
    # Context and data
    context: Dict[str, Any] = field(default_factory=dict)
    claim_data: Optional[Dict[str, Any]] = None
    processed_data: Dict[str, Any] = field(default_factory=dict)
    
    # Agent reasoning
    thoughts: List[str] = field(default_factory=list)
    actions_taken: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    
    # Results and outputs
    result: Optional[Dict[str, Any]] = None
    insights: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    
    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Metadata
    confidence_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_thought(self, thought: str):
        self.thoughts.append(f"[{datetime.utcnow().isoformat()}] {thought}")
        self.updated_at = datetime.utcnow()
    
    def add_action(self, action: str):
        self.actions_taken.append(f"[{datetime.utcnow().isoformat()}] {action}")
        self.updated_at = datetime.utcnow()
    
    def add_insight(self, insight_type: str, message: str, confidence: float = 0.5):
        self.insights.append({
            "type": insight_type,
            "message": message,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
