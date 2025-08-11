# File: app/api/endpoints/patient.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import patient_service
from app.schemas.patient_information import (
    PatientInformationCreate,
    PatientInformationUpdate,
    PatientInformation,
    PatientSummary,
    PatientSearchRequest,
    PatientEDI275Response
)

router = APIRouter()


@router.post("/", response_model=PatientInformation)
def create_patient(
    patient_data: PatientInformationCreate,
    db: Session = Depends(get_db)
):
    """Create a new patient record via Patient microservice"""
    print("Creating new Patient via Patient microservice")
    try:
        return patient_service.create_patient(db, patient_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{patient_id}", response_model=PatientInformation)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """Get patient by patient ID from Patient microservice"""
    try:
        patient = patient_service.get_patient(db, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{patient_id}", response_model=PatientInformation)
def update_patient(
    patient_id: str,
    patient_update: PatientInformationUpdate,
    db: Session = Depends(get_db)
):
    """Update patient information via Patient microservice"""
    try:
        patient = patient_service.update_patient(db, patient_id, patient_update)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/member/{member_id}", response_model=PatientInformation)
def get_patient_by_member_id(
    member_id: str,
    db: Session = Depends(get_db)
):
    """Get patient by member ID from Patient microservice"""
    try:
        patient = patient_service.get_patient_by_member_id(db, member_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[PatientSummary])
def search_patients(
    first_name: Optional[str] = Query(None, description="Patient first name"),
    last_name: Optional[str] = Query(None, description="Patient last name"),
    date_of_birth: Optional[str] = Query(None, description="Date of birth (YYYY-MM-DD)"),
    member_id: Optional[str] = Query(None, description="Member ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Search patients by criteria via Patient microservice"""
    try:
        # Create search request object
        search_request = PatientSearchRequest(
            first_name=first_name,
            last_name=last_name,
            member_id=member_id,
            limit=limit,
            offset=skip
        )
        
        return patient_service.search_patients(db, search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}/edi275", response_model=PatientEDI275Response)
def generate_patient_edi275(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """Generate EDI 275 for patient information from Patient microservice"""
    try:
        edi_content = patient_service.generate_edi_275(db, patient_id)
        if not edi_content:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return edi_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

