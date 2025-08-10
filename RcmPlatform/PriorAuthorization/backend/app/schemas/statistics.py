# File: app/schemas/statistics.py
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime, date


class AuthorizationStatistics(BaseModel):
    """Authorization statistics schema"""
    total_requests: int
    approved_requests: int
    denied_requests: int
    pending_requests: int
    approval_rate: float
    average_processing_time_hours: float
    by_priority: Dict[str, int]
    by_status: Dict[str, int]
    by_provider: List[Dict[str, Any]]
    period_start: date
    period_end: date
    generated_at: datetime


class ProviderStatistics(BaseModel):
    """Provider statistics schema"""
    provider_npi: str
    provider_name: Optional[str] = None
    total_requests: int
    approved_requests: int
    denied_requests: int
    approval_rate: float
    average_processing_time_hours: float
    common_procedures: List[Dict[str, Any]]
    common_diagnoses: List[Dict[str, Any]]


class PatientStatistics(BaseModel):
    """Patient statistics schema"""
    total_patients: int
    patients_with_authorizations: int
    average_authorizations_per_patient: float
    by_gender: Dict[str, int]
    by_age_group: Dict[str, int]
    by_insurance_type: Dict[str, int]
    generated_at: datetime


class SystemStatistics(BaseModel):
    """System-wide statistics schema"""
    authorization_stats: AuthorizationStatistics
    patient_stats: PatientStatistics
    top_providers: List[ProviderStatistics]
    edi_transaction_volume: Dict[str, int]
    system_uptime_hours: float
    database_size_mb: float
    generated_at: datetime
