# File: app/api/endpoints/codes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.codes_service import codes_service

router = APIRouter()


@router.get("/service-types", response_model=List[dict])
def get_service_type_codes(
    active_only: bool = Query(True, description="Return only active codes"),
    requires_auth: Optional[bool] = Query(None, description="Filter by authorization requirement"),
    db: Session = Depends(get_db)
):
    """Get service type codes"""
    try:
        return codes_service.get_service_type_codes(db, active_only, requires_auth)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/service-types/{code}")
def get_service_type_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific service type code"""
    try:
        service_code = codes_service.get_service_type_code(db, code)
        if not service_code:
            raise HTTPException(status_code=404, detail="Service type code not found")
        return service_code
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        return codes_service.get_procedure_codes(
            db, code_type, category, requires_auth, search, skip, limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/procedures/{code}")
def get_procedure_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific procedure code"""
    try:
        procedure_code = codes_service.get_procedure_code(db, code)
        if not procedure_code:
            raise HTTPException(status_code=404, detail="Procedure code not found")
        return procedure_code
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnoses", response_model=List[dict])
def get_diagnosis_codes(
    category: Optional[str] = Query(None, description="Diagnosis category"),
    search: Optional[str] = Query(None, description="Search in description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get diagnosis codes"""
    try:
        return codes_service.get_diagnosis_codes(db, category, search, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnoses/{code}")
def get_diagnosis_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get specific diagnosis code"""
    try:
        diagnosis_code = codes_service.get_diagnosis_code(db, code)
        if not diagnosis_code:
            raise HTTPException(status_code=404, detail="Diagnosis code not found")
        return diagnosis_code
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[dict])
def search_codes(
    query: str = Query(..., description="Search query"),
    code_type: Optional[str] = Query(None, description="Code type (procedure, diagnosis)"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Search codes by query"""
    try:
        return codes_service.search_codes(db, query, code_type, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

