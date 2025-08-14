"""
AI Agent schemas for ChargeCapture
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class TaskType(str, Enum):
    """AI agent task types"""
    CAPTURE_CHARGE = "capture_charge"
    VALIDATE_CHARGE = "validate_charge"
    GET_TEMPLATE = "get_template"
    ANALYZE_CHARGES = "analyze_charges"
    CHAT = "chat"


class AgentRequest(BaseModel):
    """Request for AI agent task"""
    model_config = ConfigDict(from_attributes=True)
    
    task_type: TaskType
    context: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    conversation_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Response from AI agent task"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request with AI assistant"""
    model_config = ConfigDict(from_attributes=True)
    
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response from AI assistant"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    response: str
    conversation_id: str
    tools_used: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChargeCaptureRequest(BaseModel):
    """Request for charge capture with AI assistance"""
    model_config = ConfigDict(from_attributes=True)
    
    encounter_id: str
    patient_id: str
    provider_id: str
    cpt_code: Optional[str] = None
    icd_code: Optional[str] = None
    modifiers: Optional[List[str]] = []
    charge_amount: Optional[float] = None
    capture_method: str = Field(default="ai_assistant")


class ChargeCaptureResponse(BaseModel):
    """Response from charge capture with AI assistance"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    charge_id: str
    encounter_id: str
    patient_id: str
    provider_id: str
    cpt_code: str
    icd_code: str
    status: str
    capture_method: str
    captured_at: datetime
    validation_errors: List[str] = []
    suggestions: List[str] = []
    message: str


class ChargeValidationRequest(BaseModel):
    """Request for charge validation"""
    model_config = ConfigDict(from_attributes=True)
    
    cpt_code: str = Field(..., min_length=5, max_length=10)
    icd_code: str = Field(..., min_length=3, max_length=10)
    modifiers: Optional[List[str]] = []
    charge_amount: Optional[float] = None
    specialty: Optional[str] = None


class ChargeValidationResponse(BaseModel):
    """Response from charge validation"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    cpt_code: str
    icd_code: str
    modifiers: List[str]
    charge_amount: Optional[float]
    is_valid: bool
    validation_errors: List[str] = []
    warnings: List[str] = []
    recommendations: List[str] = []
    compliance_score: int
    validation_date: datetime
    message: str


class ChargeTemplateRequest(BaseModel):
    """Request for charge templates"""
    model_config = ConfigDict(from_attributes=True)
    
    specialty: Optional[str] = None
    procedure_type: Optional[str] = None
    provider_id: Optional[str] = None


class ChargeTemplateResponse(BaseModel):
    """Response with charge templates"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    specialty: str
    procedure_type: str
    templates: List[Dict[str, Any]]
    suggestions: List[str] = []
    message: str


class ChargeAnalysisRequest(BaseModel):
    """Request for charge analysis"""
    model_config = ConfigDict(from_attributes=True)
    
    provider_id: Optional[str] = None
    date_range: str = Field(default="30_days")
    specialty: Optional[str] = None


class ChargeAnalysisResponse(BaseModel):
    """Response with charge analysis"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    provider_id: Optional[str]
    date_range: str
    total_charges: int
    total_amount: float
    average_charge: float
    top_cpt_codes: List[Dict[str, Any]]
    top_icd_codes: List[Dict[str, Any]]
    rejection_rate: float
    common_rejection_reasons: List[str]
    recommendations: List[str]
    analysis_date: datetime
    message: str


class ToolInfo(BaseModel):
    """Information about available AI tools"""
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    description: str
    parameters: List[str]
    examples: List[str] = []


class AgentHealthResponse(BaseModel):
    """Health check response for AI agent"""
    model_config = ConfigDict(from_attributes=True)
    
    status: str
    agentic_core_available: bool
    tools_available: List[str]
    last_updated: datetime


class AgentMetricsResponse(BaseModel):
    """Metrics response for AI agent"""
    model_config = ConfigDict(from_attributes=True)
    
    total_conversations: int
    total_charges_captured: int
    total_validations: int
    average_response_time: float
    success_rate: float
    most_used_tools: List[Dict[str, Any]]
    last_updated: datetime


class ConversationHistory(BaseModel):
    """Conversation history item"""
    model_config = ConfigDict(from_attributes=True)
    
    conversation_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    tools_used: List[str] = [] 