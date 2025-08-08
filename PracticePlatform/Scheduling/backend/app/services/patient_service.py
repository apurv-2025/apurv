"""
Patient Service Integration
Handles API communication with the Patient microservice from HealthcareFoundation/CoreServices
"""

import httpx
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
import os

class PatientService:
    def __init__(self):
        self.base_url = os.getenv("PATIENT_SERVICE_URL", "http://patient-service:8000")
        self.timeout = 30.0
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to patient service"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Patient not found")
            elif e.response.status_code == 400:
                raise HTTPException(status_code=400, detail="Invalid request to patient service")
            else:
                raise HTTPException(status_code=500, detail=f"Patient service error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Patient service unavailable: {str(e)}")
    
    async def get_patients(self, skip: int = 0, limit: int = 10, active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get list of patients"""
        params = {"skip": skip, "limit": limit}
        if active is not None:
            params["active"] = active
        
        return await self._make_request("GET", "/patients", params=params)
    
    async def get_patient_by_id(self, patient_id: str) -> Dict[str, Any]:
        """Get patient by UUID"""
        return await self._make_request("GET", f"/patients/{patient_id}")
    
    async def get_patient_by_fhir_id(self, fhir_id: str) -> Dict[str, Any]:
        """Get patient by FHIR ID"""
        return await self._make_request("GET", f"/patients/fhir/{fhir_id}")
    
    async def create_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new patient"""
        return await self._make_request("POST", "/patients", json=patient_data)
    
    async def update_patient(self, patient_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing patient"""
        return await self._make_request("PUT", f"/patients/{patient_id}", json=patient_data)
    
    async def delete_patient(self, patient_id: str) -> Dict[str, Any]:
        """Delete a patient"""
        return await self._make_request("DELETE", f"/patients/{patient_id}")
    
    async def search_patients_by_name(self, family_name: Optional[str] = None, given_name: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search patients by name"""
        params = {"limit": limit}
        if family_name:
            params["family_name"] = family_name
        if given_name:
            params["given_name"] = given_name
        
        return await self._make_request("GET", "/patients/search/name", params=params)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check patient service health"""
        return await self._make_request("GET", "/health")

# Global instance
patient_service = PatientService() 