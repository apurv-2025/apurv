# File: app/dao/__init__.py
from .patient_dao import PatientDAO
from .prior_authorization_dao import PriorAuthorizationRequestDAO, PriorAuthorizationResponseDAO
from .code_dao import ServiceTypeCodeDAO, ProcedureCodeDAO, DiagnosisCodeDAO
from .audit_dao import AuthorizationAuditDAO

# Create singleton instances
patient_dao = PatientDAO()
prior_auth_request_dao = PriorAuthorizationRequestDAO()
prior_auth_response_dao = PriorAuthorizationResponseDAO()
service_type_code_dao = ServiceTypeCodeDAO()
procedure_code_dao = ProcedureCodeDAO()
diagnosis_code_dao = DiagnosisCodeDAO()
authorization_audit_dao = AuthorizationAuditDAO()

__all__ = [
    "patient_dao",
    "prior_auth_request_dao", 
    "prior_auth_response_dao",
    "service_type_code_dao",
    "procedure_code_dao",
    "diagnosis_code_dao",
    "authorization_audit_dao",
    "PatientDAO",
    "PriorAuthorizationRequestDAO",
    "PriorAuthorizationResponseDAO",
    "ServiceTypeCodeDAO",
    "ProcedureCodeDAO",
    "DiagnosisCodeDAO",
    "AuthorizationAuditDAO"
]

