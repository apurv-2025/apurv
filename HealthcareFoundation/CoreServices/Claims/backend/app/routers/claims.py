# routers/claims.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from models.fhir_models import Claim, ClaimResponse, ExplanationOfBenefit, Coverage
from schemas.fhir_schemas import (
    ClaimCreate, ClaimUpdate, ClaimResponse as ClaimSchema,
    ClaimResponseCreate, ClaimResponseUpdate, ClaimResponseResponse,
    CoverageCreate, CoverageUpdate, CoverageResponse
)
from datetime import datetime

router = APIRouter()

# Claim endpoints
@router.post("/claims", response_model=ClaimSchema)
async def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    db_claim = Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

@router.get("/claims", response_model=List[ClaimSchema])
async def get_claims(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    patient_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Claim)
    
    if status:
        query = query.filter(Claim.status == status)
    if patient_id:
        query = query.filter(Claim.patient_id == patient_id)
    
    claims = query.offset(skip).limit(limit).all()
    return claims

@router.get("/claims/{claim_id}", response_model=ClaimSchema)
async def get_claim(claim_id: str, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@router.put("/claims/{claim_id}", response_model=ClaimSchema)
async def update_claim(claim_id: str, claim_update: ClaimUpdate, db: Session = Depends(get_db)):
    db_claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    update_data = claim_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_claim, key, value)
    
    db_claim.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_claim)
    return db_claim

@router.delete("/claims/{claim_id}")
async def delete_claim(claim_id: str, db: Session = Depends(get_db)):
    db_claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    db.delete(db_claim)
    db.commit()
    return {"message": "Claim deleted successfully"}

# ClaimResponse endpoints
@router.post("/claim-responses", response_model=ClaimResponseResponse)
async def create_claim_response(claim_response: ClaimResponseCreate, db: Session = Depends(get_db)):
    db_claim_response = ClaimResponse(**claim_response.dict())
    db.add(db_claim_response)
    db.commit()
    db.refresh(db_claim_response)
    return db_claim_response

@router.get("/claim-responses", response_model=List[ClaimResponseResponse])
async def get_claim_responses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    request_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ClaimResponse)
    
    if status:
        query = query.filter(ClaimResponse.status == status)
    if request_id:
        query = query.filter(ClaimResponse.request_id == request_id)
    
    responses = query.offset(skip).limit(limit).all()
    return responses

@router.get("/claim-responses/{response_id}", response_model=ClaimResponseResponse)
async def get_claim_response(response_id: str, db: Session = Depends(get_db)):
    response = db.query(ClaimResponse).filter(ClaimResponse.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="ClaimResponse not found")
    return response

@router.put("/claim-responses/{response_id}", response_model=ClaimResponseResponse)
async def update_claim_response(response_id: str, response_update: ClaimResponseUpdate, db: Session = Depends(get_db)):
    db_response = db.query(ClaimResponse).filter(ClaimResponse.id == response_id).first()
    if not db_response:
        raise HTTPException(status_code=404, detail="ClaimResponse not found")
    
    update_data = response_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_response, key, value)
    
    db_response.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_response)
    return db_response

@router.delete("/claim-responses/{response_id}")
async def delete_claim_response(response_id: str, db: Session = Depends(get_db)):
    db_response = db.query(ClaimResponse).filter(ClaimResponse.id == response_id).first()
    if not db_response:
        raise HTTPException(status_code=404, detail="ClaimResponse not found")
    
    db.delete(db_response)
    db.commit()
    return {"message": "ClaimResponse deleted successfully"}

# Coverage endpoints
@router.post("/coverages", response_model=CoverageResponse)
async def create_coverage(coverage: CoverageCreate, db: Session = Depends(get_db)):
    db_coverage = Coverage(**coverage.dict())
    db.add(db_coverage)
    db.commit()
    db.refresh(db_coverage)
    return db_coverage

@router.get("/coverages", response_model=List[CoverageResponse])
async def get_coverages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    beneficiary_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Coverage)
    
    if status:
        query = query.filter(Coverage.status == status)
    if beneficiary_id:
        query = query.filter(Coverage.beneficiary_id == beneficiary_id)
    
    coverages = query.offset(skip).limit(limit).all()
    return coverages

@router.get("/coverages/{coverage_id}", response_model=CoverageResponse)
async def get_coverage(coverage_id: str, db: Session = Depends(get_db)):
    coverage = db.query(Coverage).filter(Coverage.id == coverage_id).first()
    if not coverage:
        raise HTTPException(status_code=404, detail="Coverage not found")
    return coverage

@router.put("/coverages/{coverage_id}", response_model=CoverageResponse)
async def update_coverage(coverage_id: str, coverage_update: CoverageUpdate, db: Session = Depends(get_db)):
    db_coverage = db.query(Coverage).filter(Coverage.id == coverage_id).first()
    if not db_coverage:
        raise HTTPException(status_code=404, detail="Coverage not found")
    
    update_data = coverage_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_coverage, key, value)
    
    db_coverage.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_coverage)
    return db_coverage

@router.delete("/coverages/{coverage_id}")
async def delete_coverage(coverage_id: str, db: Session = Depends(get_db)):
    db_coverage = db.query(Coverage).filter(Coverage.id == coverage_id).first()
    if not db_coverage:
        raise HTTPException(status_code=404, detail="Coverage not found")
    
    db.delete(db_coverage)
    db.commit()
    return {"message": "Coverage deleted successfully"}

# Additional utility endpoints
@router.get("/claims/{claim_id}/responses", response_model=List[ClaimResponseResponse])
async def get_claim_responses_for_claim(claim_id: str, db: Session = Depends(get_db)):
    responses = db.query(ClaimResponse).filter(ClaimResponse.request_id == claim_id).all()
    return responses

@router.get("/patients/{patient_id}/claims", response_model=List[ClaimSchema])
async def get_patient_claims(patient_id: str, db: Session = Depends(get_db)):
    claims = db.query(Claim).filter(Claim.patient_id == patient_id).all()
    return claims

@router.get("/stats/claims")
async def get_claims_stats(db: Session = Depends(get_db)):
    total_claims = db.query(Claim).count()
    active_claims = db.query(Claim).filter(Claim.status == "active").count()
    draft_claims = db.query(Claim).filter(Claim.status == "draft").count()
    
    return {
        "total_claims": total_claims,
        "active_claims": active_claims,
        "draft_claims": draft_claims,
        "completed_claims": total_claims - active_claims - draft_claims
    }
