"""
Practitioner Service Integration
Handles API communication with the Practitioner microservice from HealthcareFoundation/CoreServices
"""

import httpx
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
import os

class PractitionerService:
    def __init__(self):
        self.base_url = os.getenv("PRACTITIONER_SERVICE_URL", "http://practitioner-service:8000")
        self.timeout = 30.0
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to practitioner service"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Practitioner not found")
            elif e.response.status_code == 400:
                raise HTTPException(status_code=400, detail="Invalid request to practitioner service")
            else:
                raise HTTPException(status_code=500, detail=f"Practitioner service error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Practitioner service unavailable: {str(e)}")
    
    async def get_practitioners(self, skip: int = 0, limit: int = 10, active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get list of practitioners"""
        params = {"skip": skip, "limit": limit}
        if active is not None:
            params["active"] = active
        
        return await self._make_request("GET", "/practitioners", params=params)
    
    async def get_practitioner_by_id(self, practitioner_id: str) -> Dict[str, Any]:
        """Get practitioner by UUID"""
        return await self._make_request("GET", f"/practitioners/{practitioner_id}")
    
    async def get_practitioner_by_fhir_id(self, fhir_id: str) -> Dict[str, Any]:
        """Get practitioner by FHIR ID"""
        return await self._make_request("GET", f"/practitioners/fhir/{fhir_id}")
    
    async def create_practitioner(self, practitioner_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new practitioner"""
        return await self._make_request("POST", "/practitioners", json=practitioner_data)
    
    async def update_practitioner(self, practitioner_id: str, practitioner_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing practitioner"""
        return await self._make_request("PUT", f"/practitioners/{practitioner_id}", json=practitioner_data)
    
    async def delete_practitioner(self, practitioner_id: str) -> Dict[str, Any]:
        """Delete a practitioner"""
        return await self._make_request("DELETE", f"/practitioners/{practitioner_id}")
    
    async def search_practitioners_by_name(self, family_name: Optional[str] = None, given_name: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search practitioners by name"""
        params = {"limit": limit}
        if family_name:
            params["family_name"] = family_name
        if given_name:
            params["given_name"] = given_name
        
        return await self._make_request("GET", "/practitioners/search/name", params=params)
    
    async def search_practitioners_by_identifier(self, identifier_value: str, identifier_system: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search practitioners by identifier"""
        params = {"identifier_value": identifier_value, "limit": limit}
        if identifier_system:
            params["identifier_system"] = identifier_system
        
        return await self._make_request("GET", "/practitioners/search/identifier", params=params)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check practitioner service health"""
        return await self._make_request("GET", "/health")

# Global instance
practitioner_service = PractitionerService() 