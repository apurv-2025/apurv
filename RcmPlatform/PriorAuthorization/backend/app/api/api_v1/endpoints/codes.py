# File: app/api/endpoints/codes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dao import service_type_code_dao, procedure_code_dao, diagnosis_code_dao
from app.models.health_insurance import ServiceTypeCode, ProcedureCode, DiagnosisCode

router = APIRouter()


@router.get("/service-types", response_model=List[dict])
def get_service_type_codes(
    active_only: bool = Query(True, description="Return only active codes"),
    requires_auth: Optional[bool] = Query(None, description="Filter by authorization requirement"),
    db: Session = Depends(get_db)
):
    """Get service type codes"""
    if active_only:
        codes = service_type_code_dao.get_active_codes(db)
    else:
        codes = service_type_code_dao.get_multi(db)
    
    if requires_auth is not None:
        codes = [code for code in codes if code.requires_authorization == requires_auth]
    
    return [
        {
            "code": code.code,
            "description": code.description,
            "category": code.category,
            "requires_authorization": code.requires_authorization
        }
        for code in codes
    ]


@router.get("/service-types/{code}")
def get_service_type_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific service type code"""
    service_code = service_type_code_dao.get_by_code(db, code)
    if not service_code:
        raise HTTPException(status_code=404, detail="Service type code not found")
    
    return {
        "code": service_code.code,
        "description": service_code.description,
        "category": service_code.category,
        "requires_authorization": service_code.requires_authorization
    }


@router.get("/procedures", response_model=List[dict])
def get_procedure_codes(
    code_type: Optional[str] = Query(None, description="Code type (CPT, HCPCS)"),
    category: Optional[str] = Query(None, description="Procedure category"),
    requires_auth: Optional[bool] = Query(None, description="Filter by authorization requirement"),
    search: Optional[str] = Query(None, description="Search in description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get procedure codes"""
    if search:
        codes = procedure_code_dao.search_by_description(db, search)
    elif code_type:
        codes = procedure_code_dao.get_by_type(db, code_type)
    elif category:
        codes = procedure_code_dao.get_by_category(db, category)
    else:
        codes = procedure_code_dao.get_multi(db, skip=skip, limit=limit, filters={"is_active": True})
    
    if requires_auth is not None:
        codes = [code for code in codes if code.requires_authorization == requires_auth]
    
    # Apply pagination if not already done
    if not (search or code_type or category):
        codes = codes[skip:skip + limit]
    
    return [
        {
            "code": code.code,
            "description": code.description,
            "code_type": code.code_type,
            "category": code.category,
            "requires_authorization": code.requires_authorization
        }
        for code in codes
    ]


@router.get("/procedures/{code}")
def get_procedure_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific procedure code"""
    procedure = procedure_code_dao.get_by_code(db, code)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure code not found")
    
    return {
        "code": procedure.code,
        "description": procedure.description,
        "code_type": procedure.code_type,
        "category": procedure.category,
        "requires_authorization": procedure.requires_authorization
    }


@router.get("/diagnoses", response_model=List[dict])
def get_diagnosis_codes(
    category: Optional[str] = Query(None, description="Diagnosis category"),
    search: Optional[str] = Query(None, description="Search in description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get diagnosis codes"""
    if search:
        codes = diagnosis_code_dao.search_by_description(db, search)
    elif category:
        codes = diagnosis_code_dao.get_by_category(db, category)
    else:
        codes = diagnosis_code_dao.get_multi(db, skip=skip, limit=limit, filters={"is_active": True})
    
    # Apply pagination if not already done
    if not (search or category):
        codes = codes[skip:skip + limit]
    
    return [
        {
            "code": code.code,
            "description": code.description,
            "category": code.category
        }
        for code in codes
    ]


@router.get("/diagnoses/{code}")
def get_diagnosis_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific diagnosis code"""
    diagnosis = diagnosis_code_dao.get_by_code(db, code)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis code not found")
    
    return {
        "code": diagnosis.code,
        "description": diagnosis.description,
        "category": diagnosis.category
    }

