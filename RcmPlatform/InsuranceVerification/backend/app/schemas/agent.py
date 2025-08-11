"""
Agent schemas for InsuranceVerification AI functionality
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class TaskType(str, Enum):
    """Task types for insurance verification"""
    CHAT = "chat"
    VERIFY_INSURANCE = "verify_insurance"
    EXTRACT_INSURANCE_INFO = "extract_insurance_info"
    CHECK_ELIGIBILITY = "check_eligibility"
    ANALYZE_EDI = "analyze_edi"
    COMPLEX_VERIFICATION = "complex_verification"


class AgentRequest(BaseModel):
    """Base request for AI agent"""
    task_type: TaskType
    user_id: str
    context: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Base response from AI agent"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request for chat with AI agent"""
    message: str
    user_id: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response from chat with AI agent"""
    response: str
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.now)


class InsuranceVerificationRequest(BaseModel):
    """Request for insurance verification"""
    member_id: str = Field(..., description="Member ID to verify")
    provider_npi: str = Field(..., description="Provider NPI")
    service_type: str = Field(default="30", description="Service type code")
    additional_info: Optional[Dict[str, Any]] = None


class InsuranceVerificationResponse(BaseModel):
    """Response from insurance verification"""
    member_id: str
    provider_npi: str
    service_type: str
    is_eligible: bool
    coverage_details: Dict[str, Any]
    benefits: Dict[str, Any]
    verification_date: datetime = Field(default_factory=datetime.now)


class InsuranceExtractionRequest(BaseModel):
    """Request for insurance information extraction"""
    file_path: str = Field(..., description="Path to the uploaded file")
    file_type: str = Field(..., description="Type of file (image, pdf, etc.)")
    extraction_options: Optional[Dict[str, Any]] = None


class InsuranceExtractionResponse(BaseModel):
    """Response from insurance information extraction"""
    file_path: str
    file_type: str
    extracted_info: Dict[str, Any]
    confidence_score: float
    extraction_date: datetime = Field(default_factory=datetime.now)


class EligibilityCheckRequest(BaseModel):
    """Request for eligibility check"""
    member_id: str = Field(..., description="Member ID to check")
    service_type: str = Field(..., description="Service type code")
    provider_npi: Optional[str] = Field(None, description="Provider NPI")
    service_date: Optional[datetime] = None


class EligibilityCheckResponse(BaseModel):
    """Response from eligibility check"""
    member_id: str
    service_type: str
    provider_npi: Optional[str]
    is_eligible: bool
    eligibility_date: datetime = Field(default_factory=datetime.now)
    service_details: Dict[str, Any]


class EDIAnalysisRequest(BaseModel):
    """Request for EDI analysis"""
    edi_content: str = Field(..., description="EDI transaction content")
    transaction_type: str = Field(default="270", description="Transaction type (270/271)")
    analysis_options: Optional[Dict[str, Any]] = None


class EDIAnalysisResponse(BaseModel):
    """Response from EDI analysis"""
    transaction_type: str
    edi_content: str
    analysis: Dict[str, Any]
    validation: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class ComplexVerificationRequest(BaseModel):
    """Request for complex verification with multiple service types"""
    member_id: str = Field(..., description="Member ID to verify")
    provider_npi: str = Field(..., description="Provider NPI")
    service_types: List[str] = Field(default=["30"], description="List of service types to verify")
    verification_options: Optional[Dict[str, Any]] = None


class ComplexVerificationResponse(BaseModel):
    """Response from complex verification"""
    member_id: str
    provider_npi: str
    verification_results: List[Dict[str, Any]]
    overall_eligible: bool
    timestamp: datetime = Field(default_factory=datetime.now)


class ToolInfo(BaseModel):
    """Information about available tools"""
    name: str
    description: str
    parameters: Dict[str, str]


class AgentHealthResponse(BaseModel):
    """Health check response for AI agent"""
    status: str
    model_provider: str
    available_tools: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentMetricsResponse(BaseModel):
    """Metrics response for AI agent"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    most_used_tools: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.now)


# Insurance-specific schemas

class InsuranceCardInfo(BaseModel):
    """Insurance card information"""
    patient_name: str
    member_id: str
    group_number: Optional[str] = None
    plan_name: Optional[str] = None
    insurance_company: Optional[str] = None
    effective_date: Optional[str] = None
    phone_number: Optional[str] = None


class CoverageDetails(BaseModel):
    """Insurance coverage details"""
    deductible: str
    copay: str
    coinsurance: str
    out_of_pocket_max: Optional[str] = None
    coverage_period: Optional[str] = None


class BenefitsInfo(BaseModel):
    """Insurance benefits information"""
    office_visits: str
    specialist_visits: str
    preventive_care: str
    prescription_drugs: str
    emergency_services: Optional[str] = None
    hospitalization: Optional[str] = None


class ServiceDetails(BaseModel):
    """Service-specific details"""
    service_description: str
    coverage_level: str
    authorization_required: bool
    benefit_percentage: str
    limitations: Optional[List[str]] = None


class EDISegmentInfo(BaseModel):
    """EDI segment information"""
    segment_type: str
    segment_data: Dict[str, Any]
    position: int


class EDIMemberInfo(BaseModel):
    """EDI member information"""
    member_id: str
    subscriber_name: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    relationship_code: Optional[str] = None


class EDIProviderInfo(BaseModel):
    """EDI provider information"""
    provider_npi: str
    provider_name: str
    provider_type: Optional[str] = None
    address: Optional[Dict[str, str]] = None


class EDIAnalysisResult(BaseModel):
    """Complete EDI analysis result"""
    transaction_type: str
    segments_found: List[str]
    member_info: EDIMemberInfo
    provider_info: EDIProviderInfo
    service_type: str
    request_date: datetime = Field(default_factory=datetime.now)
    validation_errors: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)


class VerificationSummary(BaseModel):
    """Summary of verification results"""
    total_verifications: int
    successful_verifications: int
    failed_verifications: int
    average_processing_time: float
    most_common_service_types: List[str]
    verification_date_range: Dict[str, datetime] 