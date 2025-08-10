# File: app/schemas/__init__.py
from .patient_information import (
    PatientInformationBase,
    PatientInformationCreate,
    PatientInformationUpdate,
    PatientInformation,
    PatientEDI275Response,
    InsuranceInfo,
    EmergencyContact,
    AllergyInfo,
    MedicalCondition,
    Medication
)

from .prior_authorization import (
    PriorAuthorizationRequestBase,
    PriorAuthorizationRequestCreate,
    PriorAuthorizationRequest,
    PriorAuthorizationResponse,
    AuthorizationDecision,
    PriorAuthorizationInquiryResponse,
    PriorAuthorizationDecisionResponse,
    ProcedureCodeInfo,
    DiagnosisCodeInfo,
    RequestType,
    CertificationType,
    ResponseCode,
    Gender,
    Priority
)

from .codes import (
    ServiceTypeCodeBase,
    ServiceTypeCodeCreate,
    ServiceTypeCode,
    ProcedureCodeBase,
    ProcedureCodeCreate,
    ProcedureCode,
    DiagnosisCodeBase,
    DiagnosisCodeCreate,
    DiagnosisCode
)

from .audit import (
    AuthorizationAuditBase,
    AuthorizationAuditCreate,
    AuthorizationAudit
)

from .common import (
    MessageResponse,
    ErrorResponse,
    PaginatedResponse,
    EDIResponse
)

__all__ = [
    # Patient schemas
    "PatientInformationBase",
    "PatientInformationCreate", 
    "PatientInformationUpdate",
    "PatientInformation",
    "PatientEDI275Response",
    "InsuranceInfo",
    "EmergencyContact",
    "AllergyInfo",
    "MedicalCondition",
    "Medication",
    
    # Prior authorization schemas
    "PriorAuthorizationRequestBase",
    "PriorAuthorizationRequestCreate",
    "PriorAuthorizationRequest",
    "PriorAuthorizationResponse", 
    "AuthorizationDecision",
    "PriorAuthorizationInquiryResponse",
    "PriorAuthorizationDecisionResponse",
    "ProcedureCodeInfo",
    "DiagnosisCodeInfo",
    "RequestType",
    "CertificationType",
    "ResponseCode",
    "Gender",
    "Priority",
    
    # Code schemas
    "ServiceTypeCodeBase",
    "ServiceTypeCodeCreate",
    "ServiceTypeCode",
    "ProcedureCodeBase",
    "ProcedureCodeCreate", 
    "ProcedureCode",
    "DiagnosisCodeBase",
    "DiagnosisCodeCreate",
    "DiagnosisCode",
    
    # Audit schemas
    "AuthorizationAuditBase",
    "AuthorizationAuditCreate",
    "AuthorizationAudit",
    
    # Common schemas
    "MessageResponse",
    "ErrorResponse", 
    "PaginatedResponse",
    "EDIResponse"
]

