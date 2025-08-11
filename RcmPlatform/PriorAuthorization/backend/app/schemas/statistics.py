# Statistics Schemas for Prior Authorization System
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import date, datetime


class AuthorizationStatistics(BaseModel):
    """Authorization statistics"""
    total_requests: int = Field(..., description="Total number of requests")
    approved_requests: int = Field(..., description="Number of approved requests")
    denied_requests: int = Field(..., description="Number of denied requests")
    pending_requests: int = Field(..., description="Number of pending requests")
    approval_rate: float = Field(..., description="Approval rate percentage")
    average_processing_time: float = Field(..., description="Average processing time in hours")
    requests_by_status: Dict[str, int] = Field(..., description="Requests grouped by status")
    requests_by_month: Dict[str, int] = Field(..., description="Requests grouped by month")


class ProviderStatistics(BaseModel):
    """Provider-specific statistics"""
    provider_npi: str = Field(..., description="Provider NPI")
    provider_name: str = Field(..., description="Provider name")
    total_requests: int = Field(..., description="Total requests from this provider")
    approved_requests: int = Field(..., description="Approved requests from this provider")
    denied_requests: int = Field(..., description="Denied requests from this provider")
    approval_rate: float = Field(..., description="Provider approval rate")
    average_processing_time: float = Field(..., description="Average processing time for this provider")
    top_procedures: List[Dict[str, Any]] = Field(..., description="Most common procedures")
    top_diagnoses: List[Dict[str, Any]] = Field(..., description="Most common diagnoses")


class PatientStatistics(BaseModel):
    """Patient-specific statistics"""
    patient_id: str = Field(..., description="Patient ID")
    patient_name: str = Field(..., description="Patient name")
    total_requests: int = Field(..., description="Total requests for this patient")
    approved_requests: int = Field(..., description="Approved requests for this patient")
    denied_requests: int = Field(..., description="Denied requests for this patient")
    approval_rate: float = Field(..., description="Patient approval rate")
    total_units_requested: int = Field(..., description="Total units requested")
    total_units_approved: int = Field(..., description="Total units approved")
    last_request_date: Optional[date] = Field(None, description="Date of last request")


class SystemStatistics(BaseModel):
    """Overall system statistics"""
    total_patients: int = Field(..., description="Total number of patients")
    total_providers: int = Field(..., description="Total number of providers")
    total_requests: int = Field(..., description="Total number of requests")
    system_approval_rate: float = Field(..., description="Overall system approval rate")
    average_response_time: float = Field(..., description="Average response time in hours")
    requests_today: int = Field(..., description="Requests submitted today")
    requests_this_week: int = Field(..., description="Requests submitted this week")
    requests_this_month: int = Field(..., description="Requests submitted this month")
    top_denial_reasons: List[Dict[str, Any]] = Field(..., description="Most common denial reasons")
    top_procedures: List[Dict[str, Any]] = Field(..., description="Most common procedures")
    top_diagnoses: List[Dict[str, Any]] = Field(..., description="Most common diagnoses")
