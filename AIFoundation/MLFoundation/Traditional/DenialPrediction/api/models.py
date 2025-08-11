"""
Pydantic models for API request and response schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ClaimData(BaseModel):
    """Request model for claim prediction"""
    claim_id: str = Field(..., description="Unique claim identifier")
    provider_id: str = Field(..., description="Provider identifier")
    payer_id: str = Field(..., description="Payer identifier")
    patient_id: str = Field(..., description="Patient identifier")
    cpt_codes: List[str] = Field(..., description="CPT procedure codes")
    icd_codes: List[str] = Field(..., description="ICD diagnosis codes")
    claim_amount: float = Field(..., gt=0, description="Claim amount in dollars")
    service_date: str = Field(..., description="Service date (YYYY-MM-DD)")
    patient_age: int = Field(..., ge=0, le=120, description="Patient age")
    patient_gender: str = Field(..., pattern="^[MF]$", description="Patient gender (M/F)")
    authorization_number: Optional[str] = Field(None, description="Prior authorization number")
    modifiers: List[str] = Field(default=[], description="Procedure modifiers")
    place_of_service: str = Field(..., description="Place of service code")

class RiskFactor(BaseModel):
    """Risk factor model"""
    factor: str = Field(..., description="Risk factor description")
    impact: str = Field(..., description="How the factor affects risk (increases/decreases)")
    magnitude: float = Field(..., description="Impact magnitude")
    rank: int = Field(..., description="Rank of the risk factor")

class PredictionResponse(BaseModel):
    """Response model for claim prediction"""
    claim_id: str = Field(..., description="Claim identifier")
    denial_probability: float = Field(..., ge=0, le=1, description="Predicted denial probability")
    risk_level: str = Field(..., description="Risk level (LOW, MEDIUM, HIGH)")
    top_risk_factors: List[RiskFactor] = Field(..., description="Top risk factors")
    recommended_actions: List[str] = Field(..., description="Recommended actions")
    model_version: str = Field(..., description="Model version used")
    prediction_timestamp: str = Field(..., description="Prediction timestamp")

class BatchPredictionRequest(BaseModel):
    """Request model for batch predictions"""
    claims: List[ClaimData] = Field(..., description="List of claims to predict")

class BatchSummary(BaseModel):
    """Summary statistics for batch predictions"""
    total_claims: int = Field(..., description="Total number of claims")
    successful_predictions: int = Field(..., description="Number of successful predictions")
    high_risk_claims: int = Field(..., description="Number of high-risk claims")
    average_risk_score: float = Field(..., description="Average risk score")
    processing_time_seconds: float = Field(..., description="Processing time in seconds")

class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions"""
    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    summary: BatchSummary = Field(..., description="Summary statistics")

class FeedbackRequest(BaseModel):
    """Request model for prediction feedback"""
    claim_id: str = Field(..., description="Claim identifier")
    actual_outcome: bool = Field(..., description="Actual denial outcome")
    feedback_notes: Optional[str] = Field(None, description="Additional feedback notes")

class ModelPerformanceResponse(BaseModel):
    """Response model for model performance metrics"""
    period_days: int = Field(..., description="Period in days")
    total_predictions: int = Field(..., description="Total predictions made")
    actual_denial_rate: float = Field(..., description="Actual denial rate")
    avg_predicted_probability: float = Field(..., description="Average predicted probability")
    feedback_coverage: float = Field(..., description="Percentage of predictions with feedback")
    model_version: str = Field(..., description="Model version")
    last_updated: str = Field(..., description="Last update timestamp")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: str = Field(..., description="Error timestamp")

# Denial classification models (for Phase 2)
class DenialInput(BaseModel):
    """Input model for denial classification"""
    claim_id: str = Field(..., description="Claim identifier")
    denial_codes: List[str] = Field(..., description="Denial codes")
    denial_reason_text: str = Field(..., description="Denial reason text")
    raw_edi_segment: Optional[str] = Field(None, description="Raw EDI segment")
    claim_data: Dict[str, Any] = Field(..., description="Original claim data")

class ClassificationResponse(BaseModel):
    """Response model for denial classification"""
    claim_id: str = Field(..., description="Claim identifier")
    cause_category: str = Field(..., description="Denial cause category")
    confidence: float = Field(..., ge=0, le=1, description="Classification confidence")
    subcategory: str = Field(..., description="Denial subcategory")
    resolution_workflow: str = Field(..., description="Recommended resolution workflow")
    appeal_success_probability: float = Field(..., ge=0, le=1, description="Appeal success probability")
    recommended_actions: List[str] = Field(..., description="Recommended actions")
    priority_score: int = Field(..., ge=1, le=10, description="Priority score (1-10)")
    estimated_resolution_time: int = Field(..., description="Estimated resolution time in hours")
    automated_actions_available: bool = Field(..., description="Whether automated actions are available")

class RemediationRequest(BaseModel):
    """Request model for remediation execution"""
    denial_record_id: int = Field(..., description="Denial record ID")
    execute_automated_actions: bool = Field(True, description="Whether to execute automated actions")
    override_workflow: Optional[str] = Field(None, description="Override workflow type")

class RemediationResponse(BaseModel):
    """Response model for remediation execution"""
    denial_record_id: int = Field(..., description="Denial record ID")
    status: str = Field(..., description="Remediation status")
    workflow_type: str = Field(..., description="Workflow type executed")
    actions_taken: List[str] = Field(..., description="Actions taken")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    success_probability: float = Field(..., ge=0, le=1, description="Success probability")

class DenialStatusResponse(BaseModel):
    """Response model for denial status"""
    denial_record_id: int = Field(..., description="Denial record ID")
    status: str = Field(..., description="Current status")
    workflow_progress: float = Field(..., ge=0, le=100, description="Workflow progress percentage")
    last_action: str = Field(..., description="Last action taken")
    next_action: Optional[str] = Field(None, description="Next action")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    actions_log: List[Dict[str, Any]] = Field(..., description="Action history") 