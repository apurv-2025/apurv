# File: app/crud/crud_prior_authorization.py - CRUD Operations
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.crud.base import CRUDBase
from app.models.models import PriorAuthorizationRequest, PriorAuthorizationResponse
from app.schemas.prior_authorization import PriorAuthorizationRequestCreate


class CRUDPriorAuthorizationRequest(CRUDBase[PriorAuthorizationRequest, PriorAuthorizationRequestCreate, None]):
    """CRUD operations for Prior Authorization Requests."""
    
    def get_by_request_id(self, db: Session, *, request_id: str) -> Optional[PriorAuthorizationRequest]:
        """Get prior authorization request by request ID."""
        return db.query(PriorAuthorizationRequest).filter(
            PriorAuthorizationRequest.request_id == request_id
        ).first()
    
    def get_by_patient_id(self, db: Session, *, patient_id: str) -> List[PriorAuthorizationRequest]:
        """Get prior authorization requests by patient ID."""
        return (
            db.query(PriorAuthorizationRequest)
            .filter(PriorAuthorizationRequest.patient_id == patient_id)
            .order_by(desc(PriorAuthorizationRequest.created_at))
            .all()
        )
    
    def get_by_member_id(self, db: Session, *, member_id: str) -> List[PriorAuthorizationRequest]:
        """Get prior authorization requests by member ID."""
        return (
            db.query(PriorAuthorizationRequest)
            .filter(PriorAuthorizationRequest.member_id == member_id)
            .order_by(desc(PriorAuthorizationRequest.created_at))
            .all()
        )
    
    def get_by_status(self, db: Session, *, status: str) -> List[PriorAuthorizationRequest]:
        """Get prior authorization requests by status."""
        return (
            db.query(PriorAuthorizationRequest)
            .filter(PriorAuthorizationRequest.status == status)
            .order_by(desc(PriorAuthorizationRequest.created_at))
            .all()
        )
    
    def get_by_provider_npi(self, db: Session, *, provider_npi: str) -> List[PriorAuthorizationRequest]:
        """Get prior authorization requests by provider NPI."""
        return (
            db.query(PriorAuthorizationRequest)
            .filter(PriorAuthorizationRequest.requesting_provider_npi == provider_npi)
            .order_by(desc(PriorAuthorizationRequest.created_at))
            .all()
        )
    
    def update_status(self, db: Session, *, request_id: str, status: str) -> Optional[PriorAuthorizationRequest]:
        """Update request status."""
        request = self.get_by_request_id(db, request_id=request_id)
        if request:
            request.status = status
            db.commit()
            db.refresh(request)
        return request


class CRUDPriorAuthorizationResponse(CRUDBase[PriorAuthorizationResponse, None, None]):
    """CRUD operations for Prior Authorization Responses."""
    
    def get_by_request_id(self, db: Session, *, request_id: str) -> Optional[PriorAuthorizationResponse]:
        """Get prior authorization response by request ID."""
        return db.query(PriorAuthorizationResponse).filter(
            PriorAuthorizationResponse.request_id == request_id
        ).first()
    
    def create_response(
        self,
        db: Session,
        *,
        request_id: str,
        response_data: dict
    ) -> Optional[PriorAuthorizationResponse]:
        """Create prior authorization response."""
        try:
            db_response = PriorAuthorizationResponse(
                request_id=request_id,
                **response_data
            )
            db.add(db_response)
            db.commit()
            db.refresh(db_response)
            return db_response
        except Exception as e:
            db.rollback()
            return None


prior_authorization_request = CRUDPriorAuthorizationRequest(PriorAuthorizationRequest)
prior_authorization_response = CRUDPriorAuthorizationResponse(PriorAuthorizationResponse)
