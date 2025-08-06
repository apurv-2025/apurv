# =============================================================================
# FILE: backend/app/api/routes/payers.py
# =============================================================================
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...database.models import Payer
from ...schemas.claims import Payer as PayerSchema, PayerCreate

router = APIRouter()

@router.post("/", response_model=PayerSchema)
def create_payer(payer: PayerCreate, db: Session = Depends(get_db)):
    """Create a new payer"""
    
    db_payer = Payer(**payer.dict())
    db.add(db_payer)
    db.commit()
    db.refresh(db_payer)
    
    return db_payer

@router.get("/", response_model=List[PayerSchema])
def get_payers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of payers"""
    
    payers = db.query(Payer).filter(Payer.is_active == True).offset(skip).limit(limit).all()
    return payers

@router.get("/{payer_id}", response_model=PayerSchema)
def get_payer(payer_id: int, db: Session = Depends(get_db)):
    """Get a specific payer by ID"""
    
    payer = db.query(Payer).filter(Payer.id == payer_id).first()
    if not payer:
        raise HTTPException(status_code=404, detail="Payer not found")
    
    return payer

@router.get("/{payer_id}/rules")
def get_payer_rules(payer_id: int, db: Session = Depends(get_db)):
    """Get validation rules for a specific payer"""
    
    payer = db.query(Payer).filter(Payer.id == payer_id).first()
    if not payer:
        raise HTTPException(status_code=404, detail="Payer not found")
    
    return {
        "payer_id": payer.id,
        "payer_name": payer.name,
        "validation_rules": payer.validation_rules or {},
        "companion_guide_url": payer.companion_guide_url
    }
