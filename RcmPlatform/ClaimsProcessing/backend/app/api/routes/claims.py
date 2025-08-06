# =============================================================================
# FILE: backend/app/api/routes/claims.py
# =============================================================================
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...database.models import Claim, ClaimStatus
from ...schemas.claims import Claim as ClaimSchema, ClaimCreate, ClaimUpdate
from ...services.claim_processor import ClaimProcessor

router = APIRouter()

@router.post("/", response_model=ClaimSchema)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    """Create a new claim"""
    processor = ClaimProcessor(db)
    
    # Convert Pydantic model to dict for processing
    claim_dict = claim.dict()
    
    # This is a simplified version - in real implementation,
    # you'd need to generate EDI from the structured data
    return {"message": "Claim creation from structured data not yet implemented"}

@router.post("/upload", response_model=ClaimSchema)
async def upload_claim_file(
    file: UploadFile = File(...),
    payer_id: int = 1,
    db: Session = Depends(get_db)
):
    """Upload and process an EDI claim file"""
    
    if not file.filename.endswith(('.edi', '.txt', '.x12')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload .edi, .txt, or .x12 files")
    
    try:
        content = await file.read()
        edi_content = content.decode('utf-8')
        
        processor = ClaimProcessor(db)
        claim = processor.create_claim_from_edi(edi_content, payer_id)
        
        return claim
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/", response_model=List[ClaimSchema])
def get_claims(
    skip: int = 0,
    limit: int = 100,
    status: ClaimStatus = None,
    db: Session = Depends(get_db)
):
    """Get list of claims with optional filtering"""
    
    query = db.query(Claim)
    
    if status:
        query = query.filter(Claim.status == status)
    
    claims = query.offset(skip).limit(limit).all()
    return claims

@router.get("/{claim_id}", response_model=ClaimSchema)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    """Get a specific claim by ID"""
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return claim

@router.patch("/{claim_id}", response_model=ClaimSchema)
def update_claim(claim_id: int, claim_update: ClaimUpdate, db: Session = Depends(get_db)):
    """Update a claim"""
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    for field, value in claim_update.dict(exclude_unset=True).items():
        setattr(claim, field, value)
    
    db.commit()
    db.refresh(claim)
    
    return claim

@router.post("/{claim_id}/validate")
def validate_claim(claim_id: int, db: Session = Depends(get_db)):
    """Validate a claim"""
    
    processor = ClaimProcessor(db)
    
    try:
        result = processor.validate_claim(claim_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{claim_id}/submit")
def submit_claim(claim_id: int, db: Session = Depends(get_db)):
    """Submit a validated claim to payer"""
    
    processor = ClaimProcessor(db)
    
    try:
        # This would implement actual submission logic
        # For now, just update status
        claim = db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        if claim.status != ClaimStatus.VALIDATED:
            raise HTTPException(status_code=400, detail="Claim must be validated before submission")
        
        claim.status = ClaimStatus.SENT
        db.commit()
        
        return {"success": True, "message": "Claim submitted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
