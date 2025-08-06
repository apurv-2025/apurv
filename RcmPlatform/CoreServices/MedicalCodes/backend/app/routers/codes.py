from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
from ..schemas import CPTCodeResponse, ICD10CodeResponse, HCPCSCodeResponse, ModifierCodeResponse

router = APIRouter(prefix="/api", tags=["codes"])

@router.get("/cpt/{code}", response_model=CPTCodeResponse)
async def get_cpt_code(code: str, db: Session = Depends(get_db)):
    cpt_code = db.query(CPTCode).filter(CPTCode.code == code.upper()).first()
    if not cpt_code:
        raise HTTPException(status_code=404, detail="CPT code not found")
    return cpt_code

@router.get("/icd10/{code}", response_model=ICD10CodeResponse)
async def get_icd10_code(code: str, db: Session = Depends(get_db)):
    icd10_code = db.query(ICD10Code).filter(ICD10Code.code == code.upper()).first()
    if not icd10_code:
        raise HTTPException(status_code=404, detail="ICD-10 code not found")
    return icd10_code

@router.get("/hcpcs/{code}", response_model=HCPCSCodeResponse)
async def get_hcpcs_code(code: str, db: Session = Depends(get_db)):
    hcpcs_code = db.query(HCPCSCode).filter(HCPCSCode.code == code.upper()).first()
    if not hcpcs_code:
        raise HTTPException(status_code=404, detail="HCPCS code not found")
    return hcpcs_code

@router.get("/modifier/{modifier}", response_model=ModifierCodeResponse)
async def get_modifier_code(modifier: str, db: Session = Depends(get_db)):
    modifier_code = db.query(ModifierCode).filter(ModifierCode.modifier == modifier.upper()).first()
    if not modifier_code:
        raise HTTPException(status_code=404, detail="Modifier code not found")
    return modifier_code 