# Prior Authorization Service for Prior Authorization System
from typing import List, Optional
from sqlalchemy.orm import Session
from app.dao.prior_authorization_dao import EnhancedAuthorizationDAO
from app.schemas.prior_authorization import (
    PriorAuthorizationRequestCreate,
    PriorAuthorizationRequest,
    PriorAuthorizationResponse,
    AuthorizationDecision,
    AuthorizationSummary,
    AuthorizationSearchRequest
)
from app.services.edi_278_service import EDI278Service
import uuid


class PriorAuthService:
    def __init__(self):
        self.dao = EnhancedAuthorizationDAO()
        self.edi_service = EDI278Service()

    def create_authorization_request(
        self, 
        db: Session, 
        request_data: PriorAuthorizationRequestCreate
    ) -> PriorAuthorizationRequest:
        """Create a new prior authorization request"""
        # Generate unique request ID
        request_id = f"AUTH{uuid.uuid4().hex[:8].upper()}"
        
        # Create request record
        request_dict = request_data.model_dump()
        request_dict["request_id"] = request_id
        request_dict["status"] = "submitted"
        
        # Generate EDI 278 content
        edi_content = self.edi_service.generate_edi_278(request_data)
        request_dict["edi_278_content"] = edi_content
        
        return self.dao.create(db, obj_in=request_dict)

    def get_authorization_request(
        self, 
        db: Session, 
        request_id: str
    ) -> Optional[PriorAuthorizationRequest]:
        """Get authorization request by ID"""
        return self.dao.get_by_request_id(db, request_id)

    def update_authorization_request(
        self, 
        db: Session, 
        request_id: str, 
        request_update: dict
    ) -> Optional[PriorAuthorizationRequest]:
        """Update authorization request"""
        return self.dao.update(db, request_id, request_update)

    def search_authorizations(
        self, 
        db: Session, 
        search_request: AuthorizationSearchRequest
    ) -> List[AuthorizationSummary]:
        """Search authorization requests"""
        return self.dao.search_authorizations(db, search_request)

    def submit_decision(
        self, 
        db: Session, 
        request_id: str, 
        decision: AuthorizationDecision
    ) -> PriorAuthorizationResponse:
        """Submit authorization decision"""
        request = self.get_authorization_request(db, request_id)
        if not request:
            raise ValueError(f"Authorization request {request_id} not found")
        
        # Generate EDI 278 response
        edi_response = self.edi_service.generate_edi_278_response(request, decision)
        
        # Create response record
        response_data = {
            "request_id": request_id,
            "response_code": decision.response_code,
            "authorization_number": decision.authorization_number,
            "effective_date": decision.effective_date,
            "expiration_date": decision.expiration_date,
            "units_approved": decision.units_approved,
            "decision_reason": decision.decision_reason,
            "edi_278_response_content": edi_response
        }
        
        # Update request status
        status = "approved" if decision.response_code.value in ["A1", "A2"] else "denied"
        self.dao.update(db, request_id, {"status": status})
        
        return PriorAuthorizationResponse(**response_data)


# Create singleton instance
prior_auth_service = PriorAuthService() 