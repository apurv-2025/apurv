# File: app/crud/crud_eligibility.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.crud.base import CRUDBase
from app.models.models import EligibilityRequest, EligibilityResponse
from app.schemas.eligibility import EligibilityRequestCreate, EligibilityRequest as EligibilityRequestSchema


class CRUDEligibilityRequest(CRUDBase[EligibilityRequest, EligibilityRequestCreate, EligibilityRequestSchema]):
    """CRUD operations for EligibilityRequest."""
    
    def get_by_request_id(self, db: Session, *, request_id: str) -> Optional[EligibilityRequest]:
        """Get eligibility request by request ID."""
        return db.query(EligibilityRequest).filter(EligibilityRequest.request_id == request_id).first()
    
    def get_by_member_id(self, db: Session, *, member_id: str) -> List[EligibilityRequest]:
        """Get eligibility requests by member ID."""
        return (
            db.query(EligibilityRequest)
            .filter(EligibilityRequest.member_id == member_id)
            .order_by(desc(EligibilityRequest.created_at))
            .all()
        )
    
    def get_by_status(self, db: Session, *, status: str) -> List[EligibilityRequest]:
        """Get eligibility requests by status."""
        return (
            db.query(EligibilityRequest)
            .filter(EligibilityRequest.status == status)
            .order_by(desc(EligibilityRequest.created_at))
            .all()
        )
    
    def get_recent(self, db: Session, *, limit: int = 50) -> List[EligibilityRequest]:
        """Get most recent eligibility requests."""
        return (
            db.query(EligibilityRequest)
            .order_by(desc(EligibilityRequest.created_at))
            .limit(limit)
            .all()
        )
    
    def update_status(self, db: Session, *, request_id: str, status: str) -> Optional[EligibilityRequest]:
        """Update request status."""
        request = self.get_by_request_id(db, request_id=request_id)
        if request:
            request.status = status
            db.commit()
            db.refresh(request)
        return request


class CRUDEligibilityResponse(CRUDBase[EligibilityResponse, None, None]):
    """CRUD operations for EligibilityResponse."""
    
    def get_by_request_id(self, db: Session, *, request_id: str) -> Optional[EligibilityResponse]:
        """Get eligibility response by request ID."""
        return db.query(EligibilityResponse).filter(EligibilityResponse.request_id == request_id).first()
    
    def create_response(
        self, 
        db: Session, 
        *, 
        request_id: str, 
        edi_271_content: str, 
        is_eligible: bool, 
        benefits_info: dict = None,
        **kwargs
    ) -> Optional[EligibilityResponse]:
        """Create eligibility response."""
        try:
            response_data = {
                'request_id': request_id,
                'edi_271_content': edi_271_content,
                'is_eligible': is_eligible,
                'benefits_info': benefits_info or {},
                **kwargs
            }
            
            db_response = EligibilityResponse(**response_data)
            db.add(db_response)
            db.commit()
            db.refresh(db_response)
            return db_response
        except Exception as e:
            db.rollback()
            return None


eligibility_request = CRUDEligibilityRequest(EligibilityRequest)
eligibility_response = CRUDEligibilityResponse(EligibilityResponse)
