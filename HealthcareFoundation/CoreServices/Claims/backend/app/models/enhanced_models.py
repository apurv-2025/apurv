"""
Enhanced SQLAlchemy Models for Claims Service with DenialPrediction Integration

This module defines the additional database models needed for the integration
between the Claims Service and DenialPrediction system.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.database import Base
import uuid
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ResolutionStatus(str, Enum):
    """Resolution status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Prediction(Base):
    """Enhanced Predictions table for ML predictions"""
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String, ForeignKey("claims.id", ondelete="CASCADE"))
    model_version = Column(String, nullable=False)
    denial_probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # Using String instead of Enum for flexibility
    top_risk_factors = Column(JSON)
    recommended_actions = Column(JSON)
    shap_values = Column(JSON)
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    actual_outcome = Column(Boolean)
    feedback_received = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    claim = relationship("Claim", back_populates="predictions")

class DenialRecord(Base):
    """Enhanced Denial Records table"""
    __tablename__ = "denial_records"
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(String, ForeignKey("claims.id", ondelete="CASCADE"), unique=True, nullable=False)
    denial_date = Column(DateTime, nullable=False)
    denial_codes = Column(JSON)
    denial_reason_text = Column(Text)
    classification_result = Column(JSON)
    resolution_status = Column(String, default="pending")  # Using String instead of Enum for flexibility
    workflow_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claim = relationship("Claim", back_populates="denial_records")
    remediation_actions = relationship("RemediationAction", back_populates="denial_record")

class RemediationAction(Base):
    """Remediation Actions table"""
    __tablename__ = "remediation_actions"
    
    id = Column(Integer, primary_key=True)
    denial_record_id = Column(Integer, ForeignKey("denial_records.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String, nullable=False)
    action_data = Column(JSON)
    status = Column(String, default="pending")
    success_probability = Column(Float)
    executed_at = Column(DateTime)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    denial_record = relationship("DenialRecord", back_populates="remediation_actions")

class ModelVersion(Base):
    """Model Versions table for tracking ML models"""
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    mlflow_run_id = Column(String)
    performance_metrics = Column(JSON)
    training_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class FeatureStore(Base):
    """Feature Store table for caching computed features"""
    __tablename__ = "feature_store"
    
    id = Column(Integer, primary_key=True)
    entity_key = Column(String, nullable=False)  # e.g., "provider_id:PROV_123"
    feature_name = Column(String, nullable=False)
    feature_value = Column(Float, nullable=False)
    computed_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class AuditLog(Base):
    """Audit Log table for compliance"""
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Update the existing Claim model to include the new relationships
# This would be added to the existing fhir_models.py file
# For now, we'll define them here for reference

class ClaimEnhanced(Base):
    """Enhanced Claim model with additional fields and relationships"""
    __tablename__ = "claims"
    
    # All existing fields from the original Claim model...
    # (This is a reference - the actual fields are in fhir_models.py)
    
    # Additional ML prediction fields
    denial_probability = Column(Float)
    risk_level = Column(String)  # Using String instead of Enum for flexibility
    prediction_timestamp = Column(DateTime)
    model_version = Column(String)
    top_risk_factors = Column(JSON)
    recommended_actions = Column(JSON)
    shap_values = Column(JSON)
    
    # Denial information
    is_denied = Column(Boolean, default=False)
    denial_date = Column(DateTime)
    denial_codes = Column(JSON)
    denial_reason = Column(Text)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="claim")
    denial_records = relationship("DenialRecord", back_populates="claim")

# Pydantic models for API requests/responses

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PredictionCreate(BaseModel):
    """Pydantic model for creating a prediction"""
    claim_id: str = Field(..., description="Claim ID")
    model_version: str = Field(..., description="Model version")
    denial_probability: float = Field(..., ge=0, le=1, description="Denial probability")
    risk_level: str = Field(..., description="Risk level")
    top_risk_factors: Optional[List[str]] = Field(None, description="Top risk factors")
    recommended_actions: Optional[List[str]] = Field(None, description="Recommended actions")
    shap_values: Optional[Dict[str, Any]] = Field(None, description="SHAP values")

class PredictionResponse(BaseModel):
    """Pydantic model for prediction response"""
    id: str = Field(..., description="Prediction ID")
    claim_id: str = Field(..., description="Claim ID")
    model_version: str = Field(..., description="Model version")
    denial_probability: float = Field(..., description="Denial probability")
    risk_level: str = Field(..., description="Risk level")
    top_risk_factors: Optional[List[str]] = Field(None, description="Top risk factors")
    recommended_actions: Optional[List[str]] = Field(None, description="Recommended actions")
    prediction_timestamp: Optional[str] = Field(None, description="Prediction timestamp")
    actual_outcome: Optional[bool] = Field(None, description="Actual outcome")
    feedback_received: bool = Field(..., description="Feedback received")

class DenialRecordCreate(BaseModel):
    """Pydantic model for creating a denial record"""
    claim_id: str = Field(..., description="Claim ID")
    denial_date: str = Field(..., description="Denial date (ISO format)")
    denial_codes: Optional[List[str]] = Field(None, description="Denial codes")
    denial_reason_text: Optional[str] = Field(None, description="Denial reason text")
    classification_result: Optional[Dict[str, Any]] = Field(None, description="Classification result")
    resolution_status: str = Field("pending", description="Resolution status")
    workflow_id: Optional[str] = Field(None, description="Workflow ID")

class DenialRecordResponse(BaseModel):
    """Pydantic model for denial record response"""
    id: int = Field(..., description="Denial record ID")
    claim_id: str = Field(..., description="Claim ID")
    denial_date: str = Field(..., description="Denial date")
    denial_codes: Optional[List[str]] = Field(None, description="Denial codes")
    denial_reason_text: Optional[str] = Field(None, description="Denial reason text")
    classification_result: Optional[Dict[str, Any]] = Field(None, description="Classification result")
    resolution_status: str = Field(..., description="Resolution status")
    workflow_id: Optional[str] = Field(None, description="Workflow ID")
    created_at: str = Field(..., description="Created at")
    updated_at: str = Field(..., description="Updated at")

class RemediationActionCreate(BaseModel):
    """Pydantic model for creating a remediation action"""
    denial_record_id: int = Field(..., description="Denial record ID")
    action_type: str = Field(..., description="Action type")
    action_data: Optional[Dict[str, Any]] = Field(None, description="Action data")
    status: str = Field("pending", description="Status")
    success_probability: Optional[float] = Field(None, ge=0, le=1, description="Success probability")

class RemediationActionResponse(BaseModel):
    """Pydantic model for remediation action response"""
    id: int = Field(..., description="Remediation action ID")
    denial_record_id: int = Field(..., description="Denial record ID")
    action_type: str = Field(..., description="Action type")
    action_data: Optional[Dict[str, Any]] = Field(None, description="Action data")
    status: str = Field(..., description="Status")
    success_probability: Optional[float] = Field(None, description="Success probability")
    executed_at: Optional[str] = Field(None, description="Executed at")
    result: Optional[Dict[str, Any]] = Field(None, description="Result")
    created_at: str = Field(..., description="Created at")

class ModelVersionCreate(BaseModel):
    """Pydantic model for creating a model version"""
    model_name: str = Field(..., description="Model name")
    version: str = Field(..., description="Version")
    mlflow_run_id: Optional[str] = Field(None, description="MLflow run ID")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    is_active: bool = Field(False, description="Is active")

class ModelVersionResponse(BaseModel):
    """Pydantic model for model version response"""
    id: int = Field(..., description="Model version ID")
    model_name: str = Field(..., description="Model name")
    version: str = Field(..., description="Version")
    mlflow_run_id: Optional[str] = Field(None, description="MLflow run ID")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    training_date: str = Field(..., description="Training date")
    is_active: bool = Field(..., description="Is active")
    created_at: str = Field(..., description="Created at")

class FeatureStoreCreate(BaseModel):
    """Pydantic model for creating a feature store entry"""
    entity_key: str = Field(..., description="Entity key")
    feature_name: str = Field(..., description="Feature name")
    feature_value: float = Field(..., description="Feature value")
    expires_at: Optional[str] = Field(None, description="Expires at (ISO format)")

class FeatureStoreResponse(BaseModel):
    """Pydantic model for feature store response"""
    id: int = Field(..., description="Feature store ID")
    entity_key: str = Field(..., description="Entity key")
    feature_name: str = Field(..., description="Feature name")
    feature_value: float = Field(..., description="Feature value")
    computed_at: str = Field(..., description="Computed at")
    expires_at: Optional[str] = Field(None, description="Expires at")

class AuditLogCreate(BaseModel):
    """Pydantic model for creating an audit log entry"""
    user_id: Optional[str] = Field(None, description="User ID")
    action: str = Field(..., description="Action")
    resource_type: str = Field(..., description="Resource type")
    resource_id: Optional[str] = Field(None, description="Resource ID")
    details: Optional[Dict[str, Any]] = Field(None, description="Details")
    ip_address: Optional[str] = Field(None, description="IP address")

class AuditLogResponse(BaseModel):
    """Pydantic model for audit log response"""
    id: int = Field(..., description="Audit log ID")
    user_id: Optional[str] = Field(None, description="User ID")
    action: str = Field(..., description="Action")
    resource_type: str = Field(..., description="Resource type")
    resource_id: Optional[str] = Field(None, description="Resource ID")
    details: Optional[Dict[str, Any]] = Field(None, description="Details")
    ip_address: Optional[str] = Field(None, description="IP address")
    timestamp: str = Field(..., description="Timestamp")

# Statistics models

class ClaimsStats(BaseModel):
    """Pydantic model for claims statistics"""
    total_claims: int = Field(..., description="Total claims")
    active_claims: int = Field(..., description="Active claims")
    denied_claims: int = Field(..., description="Denied claims")
    high_risk_claims: int = Field(..., description="High risk claims")
    average_denial_probability: float = Field(..., description="Average denial probability")
    denial_rate: float = Field(..., description="Denial rate percentage")

class PredictionsStats(BaseModel):
    """Pydantic model for predictions statistics"""
    total_predictions: int = Field(..., description="Total predictions")
    high_risk_predictions: int = Field(..., description="High risk predictions")
    feedback_count: int = Field(..., description="Feedback count")
    average_denial_probability: float = Field(..., description="Average denial probability")
    model_versions: List[str] = Field(..., description="Model versions")
    feedback_coverage: float = Field(..., description="Feedback coverage percentage")

class DenialsStats(BaseModel):
    """Pydantic model for denials statistics"""
    total_denials: int = Field(..., description="Total denials")
    pending_denials: int = Field(..., description="Pending denials")
    resolved_denials: int = Field(..., description="Resolved denials")
    in_progress_denials: int = Field(..., description="In progress denials")
    resolution_rate: float = Field(..., description="Resolution rate percentage") 