from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
from ..schemas import CategoriesResponse, StatsResponse

router = APIRouter(prefix="/api", tags=["utils"])

@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(db: Session = Depends(get_db)):
    cpt_categories = db.query(CPTCode.category).distinct().all()
    icd10_chapters = db.query(ICD10Code.chapter).distinct().all()
    hcpcs_categories = db.query(HCPCSCode.category).distinct().all()
    
    return CategoriesResponse(
        cpt_categories=[cat[0] for cat in cpt_categories if cat[0]],
        icd10_chapters=[chap[0] for chap in icd10_chapters if chap[0]],
        hcpcs_categories=[cat[0] for cat in hcpcs_categories if cat[0]]
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    return StatsResponse(
        total_cpt_codes=db.query(CPTCode).count(),
        total_icd10_codes=db.query(ICD10Code).count(),
        total_hcpcs_codes=db.query(HCPCSCode).count(),
        total_modifier_codes=db.query(ModifierCode).count(),
        active_cpt_codes=db.query(CPTCode).filter(CPTCode.is_active == 'Y').count(),
        active_icd10_codes=db.query(ICD10Code).filter(ICD10Code.is_active == 'Y').count(),
        active_hcpcs_codes=db.query(HCPCSCode).filter(HCPCSCode.is_active == 'Y').count()
    ) 