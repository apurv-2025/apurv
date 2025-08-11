# Patient Service Client for Prior Authorization System
# This client communicates with the Patient microservice instead of managing patients locally

import httpx
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import date, datetime
import os

# Configuration
PATIENT_SERVICE_URL = os.getenv('PATIENT_SERVICE_URL', 'http://localhost:8000')


class PatientClientError(Exception):
    """Custom exception for patient client errors"""
    pass


class PatientIdentifier(BaseModel):
    use: Optional[str] = None
    type: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional[Dict[str, str]] = None


class PatientTelecom(BaseModel):
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None
    rank: Optional[int] = None
    period: Optional[Dict[str, str]] = None


class PatientAddress(BaseModel):
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    period: Optional[Dict[str, str]] = None


class PatientCreate(BaseModel):
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[PatientIdentifier]] = None
    telecom: Optional[List[PatientTelecom]] = None
    addresses: Optional[List[PatientAddress]] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    active: Optional[bool] = True


class PatientUpdate(BaseModel):
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[PatientIdentifier]] = None
    telecom: Optional[List[PatientTelecom]] = None
    addresses: Optional[List[PatientAddress]] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    active: Optional[bool] = None


class PatientResponse(BaseModel):
    id: str
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    telecom: Optional[List[Dict[str, Any]]] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    active: Optional[bool] = None
    created_at: datetime
    updated_at: datetime


class PatientClient:
    """Client for communicating with the Patient microservice"""
    
    def __init__(self, base_url: str = PATIENT_SERVICE_URL):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to patient service"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PatientClientError(f"Patient not found: {e.response.text}")
            elif e.response.status_code == 400:
                raise PatientClientError(f"Bad request: {e.response.text}")
            else:
                raise PatientClientError(f"HTTP error {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise PatientClientError(f"Request failed: {str(e)}")
    
    async def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        """Create a new patient"""
        data = patient_data.model_dump(exclude_none=True)
        result = await self._make_request("POST", "/patients", json=data)
        return PatientResponse(**result)
    
    async def get_patient(self, patient_id: str) -> Optional[PatientResponse]:
        """Get patient by ID"""
        try:
            result = await self._make_request("GET", f"/patients/{patient_id}")
            return PatientResponse(**result)
        except PatientClientError as e:
            if "not found" in str(e).lower():
                return None
            raise
    
    async def get_patient_by_fhir_id(self, fhir_id: str) -> Optional[PatientResponse]:
        """Get patient by FHIR ID"""
        try:
            result = await self._make_request("GET", f"/patients/fhir/{fhir_id}")
            return PatientResponse(**result)
        except PatientClientError as e:
            if "not found" in str(e).lower():
                return None
            raise
    
    async def update_patient(self, patient_id: str, patient_update: PatientUpdate) -> Optional[PatientResponse]:
        """Update patient information"""
        try:
            data = patient_update.model_dump(exclude_none=True)
            result = await self._make_request("PUT", f"/patients/{patient_id}", json=data)
            return PatientResponse(**result)
        except PatientClientError as e:
            if "not found" in str(e).lower():
                return None
            raise
    
    async def search_patients(
        self,
        skip: int = 0,
        limit: int = 100,
        active: Optional[bool] = None,
        gender: Optional[str] = None
    ) -> List[PatientResponse]:
        """Search patients"""
        params = {"skip": skip, "limit": limit}
        if active is not None:
            params["active"] = active
        if gender is not None:
            params["gender"] = gender
        
        result = await self._make_request("GET", "/patients", params=params)
        return [PatientResponse(**patient) for patient in result]
    
    async def search_patients_by_name(
        self,
        family_name: Optional[str] = None,
        given_name: Optional[str] = None,
        limit: int = 100
    ) -> List[PatientResponse]:
        """Search patients by name"""
        params = {"limit": limit}
        if family_name:
            params["family_name"] = family_name
        if given_name:
            params["given_name"] = given_name
        
        result = await self._make_request("GET", "/patients/search/name", params=params)
        return [PatientResponse(**patient) for patient in result]
    
    async def get_patient_by_identifier(self, identifier_value: str, identifier_system: Optional[str] = None) -> Optional[PatientResponse]:
        """Get patient by identifier (e.g., member ID)"""
        # First get all patients and filter by identifier
        patients = await self.search_patients(limit=1000)
        
        for patient in patients:
            if patient.identifiers:
                for identifier in patient.identifiers:
                    if identifier.get('value') == identifier_value:
                        if identifier_system is None or identifier.get('system') == identifier_system:
                            return patient
        return None
    
    async def health_check(self) -> bool:
        """Check if patient service is healthy"""
        try:
            await self._make_request("GET", "/health")
            return True
        except PatientClientError:
            return False


# Synchronous wrapper for compatibility with existing code
class PatientClientSync:
    """Synchronous wrapper for PatientClient"""
    
    def __init__(self, base_url: str = PATIENT_SERVICE_URL):
        self.base_url = base_url
    
    def _run_async(self, coro):
        """Run async function in sync context"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(coro)
    
    def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        """Create a new patient (sync)"""
        async def _create():
            async with PatientClient(self.base_url) as client:
                return await client.create_patient(patient_data)
        return self._run_async(_create())
    
    def get_patient(self, patient_id: str) -> Optional[PatientResponse]:
        """Get patient by ID (sync)"""
        async def _get():
            async with PatientClient(self.base_url) as client:
                return await client.get_patient(patient_id)
        return self._run_async(_get())
    
    def get_patient_by_fhir_id(self, fhir_id: str) -> Optional[PatientResponse]:
        """Get patient by FHIR ID (sync)"""
        async def _get():
            async with PatientClient(self.base_url) as client:
                return await client.get_patient_by_fhir_id(fhir_id)
        return self._run_async(_get())
    
    def update_patient(self, patient_id: str, patient_update: PatientUpdate) -> Optional[PatientResponse]:
        """Update patient information (sync)"""
        async def _update():
            async with PatientClient(self.base_url) as client:
                return await client.update_patient(patient_id, patient_update)
        return self._run_async(_update())
    
    def search_patients(
        self,
        skip: int = 0,
        limit: int = 100,
        active: Optional[bool] = None,
        gender: Optional[str] = None
    ) -> List[PatientResponse]:
        """Search patients (sync)"""
        async def _search():
            async with PatientClient(self.base_url) as client:
                return await client.search_patients(skip, limit, active, gender)
        return self._run_async(_search())
    
    def search_patients_by_name(
        self,
        family_name: Optional[str] = None,
        given_name: Optional[str] = None,
        limit: int = 100
    ) -> List[PatientResponse]:
        """Search patients by name (sync)"""
        async def _search():
            async with PatientClient(self.base_url) as client:
                return await client.search_patients_by_name(family_name, given_name, limit)
        return self._run_async(_search())
    
    def get_patient_by_identifier(self, identifier_value: str, identifier_system: Optional[str] = None) -> Optional[PatientResponse]:
        """Get patient by identifier (sync)"""
        async def _get():
            async with PatientClient(self.base_url) as client:
                return await client.get_patient_by_identifier(identifier_value, identifier_system)
        return self._run_async(_get())
    
    def health_check(self) -> bool:
        """Check if patient service is healthy (sync)"""
        async def _check():
            async with PatientClient(self.base_url) as client:
                return await client.health_check()
        return self._run_async(_check())


# Create singleton instance
patient_client = PatientClientSync() 