"""
Patient API Router
Provides endpoints for patient management by integrating with the Patient microservice
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID

from app.services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["patients"])

# Pydantic models for request/response
class PatientSearchRequest(BaseModel):
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    limit: int = 10

class PatientCreateRequest(BaseModel):
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    active: Optional[bool] = True

class PatientUpdateRequest(BaseModel):
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    active: Optional[bool] = None

@router.get("/", response_model=List[Dict[str, Any]])
async def get_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Get list of patients from the Patient microservice
    """
    try:
        patients = await patient_service.get_patients(skip=skip, limit=limit, active=active)
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patients: {str(e)}")

@router.get("/{patient_id}", response_model=Dict[str, Any])
async def get_patient(patient_id: str):
    """
    Get a specific patient by UUID
    """
    try:
        patient = await patient_service.get_patient_by_id(patient_id)
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient: {str(e)}")

@router.get("/fhir/{fhir_id}", response_model=Dict[str, Any])
async def get_patient_by_fhir_id(fhir_id: str):
    """
    Get a specific patient by FHIR ID
    """
    try:
        patient = await patient_service.get_patient_by_fhir_id(fhir_id)
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch patient: {str(e)}")

@router.post("/", response_model=Dict[str, Any])
async def create_patient(patient_data: PatientCreateRequest):
    """
    Create a new patient
    """
    try:
        patient = await patient_service.create_patient(patient_data.dict())
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create patient: {str(e)}")

@router.put("/{patient_id}", response_model=Dict[str, Any])
async def update_patient(patient_id: str, patient_data: PatientUpdateRequest):
    """
    Update an existing patient
    """
    try:
        # Only include fields that are not None
        update_data = {k: v for k, v in patient_data.dict().items() if v is not None}
        patient = await patient_service.update_patient(patient_id, update_data)
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update patient: {str(e)}")

@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    """
    Delete a patient
    """
    try:
        result = await patient_service.delete_patient(patient_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete patient: {str(e)}")

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_patients(search_request: PatientSearchRequest):
    """
    Search patients by name
    """
    try:
        patients = await patient_service.search_patients_by_name(
            family_name=search_request.family_name,
            given_name=search_request.given_name,
            limit=search_request.limit
        )
        return patients
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search patients: {str(e)}")

@router.get("/search/name", response_model=List[Dict[str, Any]])
async def search_patients_by_name_endpoint(
    family_name: Optional[str] = Query(None, description="Family name to search for"),
    given_name: Optional[str] = Query(None, description="Given name to search for"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return")
):
    """
    Search patients by name using query parameters
    """
    try:
        patients = await patient_service.search_patients_by_name(
            family_name=family_name,
            given_name=given_name,
            limit=limit
        )
        return patients
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search patients: {str(e)}")

@router.get("/health/check")
async def check_patient_service_health():
    """
    Check the health of the Patient microservice
    """
    try:
        health = await patient_service.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Patient service health check failed: {str(e)}") 