# File: app/services/authorization_service.py - Business Logic Service
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any
import logging
import random
import string

from app.schemas.prior_authorization import (
    PriorAuthorizationRequestCreate,
    AuthorizationDecision,
    ResponseCode
)

logger = logging.getLogger(__name__)


class AuthorizationService:
    """Service for prior authorization business logic."""
    
    def __init__(self):
        self.auto_approval_procedures = [
            "99213", "99214", "99215",  # Office visits
            "90791", "90834", "90837",  # Mental health
            "36415",  # Blood draw
        ]
        self.high_value_procedures = [
            "27447",  # Knee replacement
            "23472",  # Shoulder surgery
            "64483",  # Injection procedures
        ]
    
    def generate_authorization_number(self) -> str:
        """Generate a unique authorization number."""
        prefix = "AUTH"
        random_part = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{random_part}"
    
    def evaluate_authorization_request(self, request: PriorAuthorizationRequestCreate) -> AuthorizationDecision:
        """Evaluate authorization request and make decision."""
        try:
            logger.info(f"Evaluating authorization request for {request.patient_first_name} {request.patient_last_name}")
            
            # Extract procedure codes
            procedure_codes = [proc.code for proc in request.procedure_codes]
            
            # Auto-approval logic
            if self._should_auto_approve(request, procedure_codes):
                return self._create_approval_decision(request, "Auto-approved based on criteria")
            
            # High-value procedure logic
            if any(code in self.high_value_procedures for code in procedure_codes):
                return self._create_pending_decision(request, "High-value procedure requires manual review")
            
            # Emergency/urgent priority
            if request.priority.value == "emergency":
                return self._create_approval_decision(request, "Approved due to emergency priority")
            
            # Default approval for demonstration
            return self._create_approval_decision(request, "Approved after review")
            
        except Exception as e:
            logger.error(f"Error evaluating authorization request: {str(e)}")
            return self._create_denial_decision(request, f"System error during evaluation: {str(e)}")
    
    def _should_auto_approve(self, request: PriorAuthorizationRequestCreate, procedure_codes: list) -> bool:
        """Determine if request should be auto-approved."""
        # Auto-approve if all procedures are in auto-approval list
        return all(code in self.auto_approval_procedures for code in procedure_codes)
    
    def _create_approval_decision(self, request: PriorAuthorizationRequestCreate, reason: str) -> AuthorizationDecision:
        """Create an approval decision."""
        auth_number = self.generate_authorization_number()
        effective_date = request.service_date_from
        expiration_date = effective_date + timedelta(days=90)  # 90-day authorization
        
        return AuthorizationDecision(
            response_code=ResponseCode.APPROVED,
            authorization_number=auth_number,
            effective_date=effective_date,
            expiration_date=expiration_date,
            units_approved=request.units_requested,
            decision_reason=reason
        )
    
    def _create_pending_decision(self, request: PriorAuthorizationRequestCreate, reason: str) -> AuthorizationDecision:
        """Create a pending decision."""
        return AuthorizationDecision(
            response_code=ResponseCode.PENDED,
            decision_reason=reason,
            additional_information_required="Please provide additional clinical documentation including recent lab results and physician notes."
        )
    
    def _create_denial_decision(self, request: PriorAuthorizationRequestCreate, reason: str) -> AuthorizationDecision:
        """Create a denial decision."""
        return AuthorizationDecision(
            response_code=ResponseCode.DENIED,
            decision_reason=reason
        )
    
    def _create_modified_decision(self, request: PriorAuthorizationRequestCreate, reason: str, approved_units: int) -> AuthorizationDecision:
        """Create a modified approval decision."""
        auth_number = self.generate_authorization_number()
        effective_date = request.service_date_from
        expiration_date = effective_date + timedelta(days=30)  # Shorter authorization for modified
        
        return AuthorizationDecision(
            response_code=ResponseCode.MODIFIED,
            authorization_number=auth_number,
            effective_date=effective_date,
            expiration_date=expiration_date,
            units_approved=approved_units,
            decision_reason=reason
        )
