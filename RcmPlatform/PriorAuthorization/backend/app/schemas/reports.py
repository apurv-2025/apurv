# File: app/schemas/reports.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class ReportType(str, Enum):
    AUTHORIZATION_SUMMARY = "authorization_summary"
    PROVIDER_PERFORMANCE = "provider_performance"
    PATIENT_DEMOGRAPHICS = "patient_demographics"
    AUDIT_TRAIL = "audit_trail"
    EDI_TRANSACTION_LOG = "edi_transaction_log"


class ReportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    EXCEL = "excel"


class ReportRequest(BaseModel):
    """Report generation request schema"""
    report_type: ReportType
    format: ReportFormat = ReportFormat.JSON
    date_from: date
    date_to: date
    filters: Optional[Dict[str, Any]] = None
    include_details: bool = False
    
    @field_validator('date_to')
    @classmethod
    def validate_date_range(cls, v, info):
        if 'date_from' in info.data and v < info.data['date_from']:
            raise ValueError('End date must be after start date')
        return v


class ReportMetadata(BaseModel):
    """Report metadata schema"""
    report_id: str
    report_type: ReportType
    format: ReportFormat
    status: str  # generating, completed, failed
    date_from: date
    date_to: date
    record_count: Optional[int] = None
    file_size_bytes: Optional[int] = None
    download_url: Optional[str] = None
    error_message: Optional[str] = None
    requested_by: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class ReportResponse(BaseModel):
    """Report response schema"""
    metadata: ReportMetadata
    data: Optional[Dict[str, Any]] = None
    message: str


# Update the __init__.py imports
from .statistics import (
    AuthorizationStatistics,
    ProviderStatistics,
    PatientStatistics,
    SystemStatistics
)

from .reports import (
    ReportType,
    ReportFormat,
    ReportRequest,
    ReportMetadata,
    ReportResponse
)
