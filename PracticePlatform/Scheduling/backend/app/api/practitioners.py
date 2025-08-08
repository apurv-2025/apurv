"""
Practitioner API Router
Provides endpoints for practitioner management by integrating with the Practitioner microservice
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID

from app.services.practitioner_service import practitioner_service

router = APIRouter(prefix="/practitioners", tags=["practitioners"])

# Pydantic models for request/response
class PractitionerSearchRequest(BaseModel):
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    limit: int = 10

class PractitionerCreateRequest(BaseModel):
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    qualifications: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = True

class PractitionerUpdateRequest(BaseModel):
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    qualifications: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = None

@router.get("/", response_model=List[Dict[str, Any]])
async def get_practitioners(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Get list of practitioners from the Practitioner microservice
    """
    try:
        practitioners = await practitioner_service.get_practitioners(skip=skip, limit=limit, active=active)
        return practitioners
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch practitioners: {str(e)}")

@router.get("/{practitioner_id}", response_model=Dict[str, Any])
async def get_practitioner(practitioner_id: str):
    """
    Get a specific practitioner by UUID
    """
    try:
        practitioner = await practitioner_service.get_practitioner_by_id(practitioner_id)
        return practitioner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch practitioner: {str(e)}")

@router.get("/fhir/{fhir_id}", response_model=Dict[str, Any])
async def get_practitioner_by_fhir_id(fhir_id: str):
    """
    Get a specific practitioner by FHIR ID
    """
    try:
        practitioner = await practitioner_service.get_practitioner_by_fhir_id(fhir_id)
        return practitioner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch practitioner: {str(e)}")

@router.post("/", response_model=Dict[str, Any])
async def create_practitioner(practitioner_data: PractitionerCreateRequest):
    """
    Create a new practitioner
    """
    try:
        practitioner = await practitioner_service.create_practitioner(practitioner_data.dict())
        return practitioner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create practitioner: {str(e)}")

@router.put("/{practitioner_id}", response_model=Dict[str, Any])
async def update_practitioner(practitioner_id: str, practitioner_data: PractitionerUpdateRequest):
    """
    Update an existing practitioner
    """
    try:
        # Only include fields that are not None
        update_data = {k: v for k, v in practitioner_data.dict().items() if v is not None}
        practitioner = await practitioner_service.update_practitioner(practitioner_id, update_data)
        return practitioner
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update practitioner: {str(e)}")

@router.delete("/{practitioner_id}")
async def delete_practitioner(practitioner_id: str):
    """
    Delete a practitioner
    """
    try:
        result = await practitioner_service.delete_practitioner(practitioner_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete practitioner: {str(e)}")

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_practitioners(search_request: PractitionerSearchRequest):
    """
    Search practitioners by name
    """
    try:
        practitioners = await practitioner_service.search_practitioners_by_name(
            family_name=search_request.family_name,
            given_name=search_request.given_name,
            limit=search_request.limit
        )
        return practitioners
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search practitioners: {str(e)}")

@router.get("/search/name", response_model=List[Dict[str, Any]])
async def search_practitioners_by_name_endpoint(
    family_name: Optional[str] = Query(None, description="Family name to search for"),
    given_name: Optional[str] = Query(None, description="Given name to search for"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return")
):
    """
    Search practitioners by name using query parameters
    """
    try:
        practitioners = await practitioner_service.search_practitioners_by_name(
            family_name=family_name,
            given_name=given_name,
            limit=limit
        )
        return practitioners
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search practitioners: {str(e)}")

@router.get("/search/identifier", response_model=List[Dict[str, Any]])
async def search_practitioners_by_identifier(
    identifier_value: str = Query(..., description="Identifier value to search for"),
    identifier_system: Optional[str] = Query(None, description="Identifier system"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return")
):
    """
    Search practitioners by identifier
    """
    try:
        practitioners = await practitioner_service.search_practitioners_by_identifier(
            identifier_value=identifier_value,
            identifier_system=identifier_system,
            limit=limit
        )
        return practitioners
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search practitioners: {str(e)}")

@router.get("/health/check")
async def check_practitioner_service_health():
    """
    Check the health of the Practitioner microservice
    """
    try:
        health = await practitioner_service.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Practitioner service health check failed: {str(e)}") 