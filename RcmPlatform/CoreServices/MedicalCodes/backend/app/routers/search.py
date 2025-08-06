from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
from ..schemas import SearchResults

router = APIRouter(prefix="/api", tags=["search"])

@router.get("/search", response_model=SearchResults)
async def search_codes(
    query: str = Query(..., min_length=1, description="Search query"),
    code_type: Optional[str] = Query(None, description="Filter by code type: cpt, icd10, hcpcs, modifier"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results per code type"),
    db: Session = Depends(get_db)
):
    results = SearchResults(
        cpt_codes=[],
        icd10_codes=[],
        hcpcs_codes=[],
        modifier_codes=[],
        total_results=0
    )
    
    search_term = f"%{query.upper()}%"
    
    # Search CPT codes
    if not code_type or code_type == "cpt":
        cpt_query = db.query(CPTCode).filter(
            (CPTCode.code.ilike(search_term)) |
            (CPTCode.description.ilike(search_term))
        )
        if category:
            cpt_query = cpt_query.filter(CPTCode.category.ilike(f"%{category}%"))
        
        results.cpt_codes = cpt_query.limit(limit).all()
    
    # Search ICD-10 codes
    if not code_type or code_type == "icd10":
        icd10_query = db.query(ICD10Code).filter(
            (ICD10Code.code.ilike(search_term)) |
            (ICD10Code.description.ilike(search_term))
        )
        if category:
            icd10_query = icd10_query.filter(ICD10Code.chapter.ilike(f"%{category}%"))
        
        results.icd10_codes = icd10_query.limit(limit).all()
    
    # Search HCPCS codes
    if not code_type or code_type == "hcpcs":
        hcpcs_query = db.query(HCPCSCode).filter(
            (HCPCSCode.code.ilike(search_term)) |
            (HCPCSCode.description.ilike(search_term))
        )
        if category:
            hcpcs_query = hcpcs_query.filter(HCPCSCode.category.ilike(f"%{category}%"))
        
        results.hcpcs_codes = hcpcs_query.limit(limit).all()
    
    # Search Modifier codes
    if not code_type or code_type == "modifier":
        modifier_query = db.query(ModifierCode).filter(
            (ModifierCode.modifier.ilike(search_term)) |
            (ModifierCode.description.ilike(search_term))
        )
        if category:
            modifier_query = modifier_query.filter(ModifierCode.category.ilike(f"%{category}%"))
        
        results.modifier_codes = modifier_query.limit(limit).all()
    
    results.total_results = (
        len(results.cpt_codes) +
        len(results.icd10_codes) +
        len(results.hcpcs_codes) +
        len(results.modifier_codes)
    )
    
    return results 