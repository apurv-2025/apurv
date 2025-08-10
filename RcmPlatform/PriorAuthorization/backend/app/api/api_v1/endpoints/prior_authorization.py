# File: app/api/endpoints/prior_authorization.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import prior_auth_service
from app.schemas.prior_authorization import (
    PriorAuthorizationRequestCreate,
    PriorAuthorizationRequest,
    PriorAuthorizationResponse,
    AuthorizationDecision,
    PriorAuthorizationInquiryResponse,
    PriorAuthorizationDecisionResponse
)

router = APIRouter()


@router.post("/requests", response_model=PriorAuthorizationRequest)
def submit_authorization_request(
    request_data: PriorAuthorizationRequestCreate,
    db: Session = Depends(get_db)
):
    """Submit a new prior authorization request"""
    try:
        return prior_auth_service.submit_authorization_request(db, request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests/{request_id}", response_model=PriorAuthorizationRequest)
def get_authorization_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    """Get authorization request by ID"""
    request = prior_auth_service.get_authorization_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Authorization request not found")
    return request


@router.post("/requests/{request_id}/decision", response_model=PriorAuthorizationResponse)
def process_authorization_decision(
    request_id: str,
    decision: AuthorizationDecision,
    reviewer: Optional[str] = Query(None, description="Reviewer name"),
    db: Session = Depends(get_db)
):
    """Process authorization decision"""
    response = prior_auth_service.process_authorization_decision(
        db, request_id, decision, reviewer
    )
    if not response:
        raise HTTPException(status_code=404, detail="Authorization request not found")
    return response


@router.get("/requests", response_model=List[PriorAuthorizationRequest])
def search_authorization_requests(
    patient_name: Optional[str] = Query(None, description="Patient name"),
    member_id: Optional[str] = Query(None, description="Member ID"),
    provider_npi: Optional[str] = Query(None, description="Provider NPI"),
    status: Optional[str] = Query(None, description="Request status"),
    service_date_from: Optional[str] = Query(None, description="Service date from (YYYY-MM-DD)"),
    service_date_to: Optional[str] = Query(None, description="Service date to (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Search authorization requests"""
    return prior_auth_service.search_authorization_requests(
        db,
        patient_name=patient_name,
        member_id=member_id,
        provider_npi=provider_npi,
        status=status,
        service_date_from=service_date_from,
        service_date_to=service_date_to,
        skip=skip,
        limit=limit
    )


@router.get("/patients/{patient_id}/requests", response_model=List[PriorAuthorizationRequest])
def get_patient_authorizations(
    patient_id: str,
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all authorizations for a patient"""
    return prior_auth_service.get_patient_authorizations(
        db, patient_id, skip=skip, limit=limit, status=status
    )


@router.get("/providers/{provider_npi}/requests", response_model=List[PriorAuthorizationRequest])
def get_provider_authorizations(
    provider_npi: str,
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all authorizations for a provider"""
    return prior_auth_service.get_provider_authorizations(
        db, provider_npi, skip=skip, limit=limit, status=status
    )


@router.get("/pending", response_model=List[PriorAuthorizationRequest])
def get_pending_requests(
    priority: Optional[str] = Query(None, description="Filter by priority"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get pending authorization requests"""
    return prior_auth_service.get_pending_requests(
        db, skip=skip, limit=limit, priority=priority
    )


# EDI-specific endpoints
@router.post("/edi278/inquiry", response_model=PriorAuthorizationInquiryResponse)
def edi_278_inquiry(
    request_data: PriorAuthorizationRequestCreate,
    db: Session = Depends(get_db)
):
    """Process EDI 278 inquiry request"""
    try:
        # Submit the request
        auth_request = prior_auth_service.submit_authorization_request(db, request_data)
        
        return PriorAuthorizationInquiryResponse(
            request_id=auth_request.request_id,
            edi_278=auth_request.edi_278_content,
            status="submitted",
            message="Prior authorization request submitted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/edi278/decision", response_model=PriorAuthorizationDecisionResponse)
def edi_278_decision(
    request_id: str,
    decision: AuthorizationDecision,
    reviewer: Optional[str] = Query(None, description="Reviewer name"),
    db: Session = Depends(get_db)
):
    """Process EDI 278 decision response"""
    try:
        response = prior_auth_service.process_authorization_decision(
            db, request_id, decision, reviewer
        )
        if not response:
            raise HTTPException(status_code=404, detail="Authorization request not found")
        
        return PriorAuthorizationDecisionResponse(
            request_id=request_id,
            edi_278_response=response.edi_278_response_content,
            response_code=response.response_code,
            authorization_number=response.authorization_number,
            decision_details={
                "effective_date": response.effective_date.isoformat() if response.effective_date else None,
                "expiration_date": response.expiration_date.isoformat() if response.expiration_date else None,
                "units_approved": response.units_approved,
                "decision_reason": response.decision_reason
            },
            processed_at=response.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

