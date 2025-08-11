# =============================================================================
# FILE: api/claims_service_client.py
# =============================================================================
"""
Claims Service Client for ClaimsAnomaly Integration

This module provides a client interface to communicate with the foundational
Claims service, enabling ClaimsAnomaly to use FHIR-based CRUD operations
while maintaining its ML anomaly detection capabilities.
"""

import httpx
import logging
from typing import Dict, List, Optional, Any
from fastapi import HTTPException
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ClaimsServiceClient:
    """Client for interacting with the Claims service API"""
    
    def __init__(self, base_url: str = "http://localhost:8001", timeout: int = 30):
        """
        Initialize the Claims service client
        
        Args:
            base_url: Base URL of the Claims service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """
        Make HTTP request to Claims service
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            HTTPException: If request fails
        """
        url = f"{self.base_url}/api/v1{endpoint}"
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Claims service HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Claims service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Claims service request error: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Claims service unavailable: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in Claims service client: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal error: {str(e)}"
            )
    
    # Claim CRUD Operations
    
    async def create_claim(self, claim_data: Dict) -> Dict:
        """Create a new claim in the Claims service"""
        return await self._make_request("POST", "/claims", data=claim_data)
    
    async def get_claim(self, claim_id: str) -> Dict:
        """Get a claim by ID from the Claims service"""
        return await self._make_request("GET", f"/claims/{claim_id}")
    
    async def get_claims(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        patient_id: Optional[str] = None
    ) -> List[Dict]:
        """Get list of claims with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if patient_id:
            params["patient_id"] = patient_id
            
        return await self._make_request("GET", "/claims", params=params)
    
    async def update_claim(self, claim_id: str, claim_data: Dict) -> Dict:
        """Update a claim in the Claims service"""
        return await self._make_request("PUT", f"/claims/{claim_id}", data=claim_data)
    
    async def delete_claim(self, claim_id: str) -> Dict:
        """Delete a claim from the Claims service"""
        return await self._make_request("DELETE", f"/claims/{claim_id}")
    
    # ClaimResponse Operations
    
    async def create_claim_response(self, response_data: Dict) -> Dict:
        """Create a new claim response"""
        return await self._make_request("POST", "/claim-responses", data=response_data)
    
    async def get_claim_response(self, response_id: str) -> Dict:
        """Get a claim response by ID"""
        return await self._make_request("GET", f"/claim-responses/{response_id}")
    
    async def get_claim_responses(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> List[Dict]:
        """Get list of claim responses with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if request_id:
            params["request_id"] = request_id
            
        return await self._make_request("GET", "/claim-responses", params=params)
    
    async def update_claim_response(self, response_id: str, response_data: Dict) -> Dict:
        """Update a claim response"""
        return await self._make_request("PUT", f"/claim-responses/{response_id}", data=response_data)
    
    async def delete_claim_response(self, response_id: str) -> Dict:
        """Delete a claim response"""
        return await self._make_request("DELETE", f"/claim-responses/{response_id}")
    
    # Coverage Operations
    
    async def create_coverage(self, coverage_data: Dict) -> Dict:
        """Create a new coverage"""
        return await self._make_request("POST", "/coverages", data=coverage_data)
    
    async def get_coverage(self, coverage_id: str) -> Dict:
        """Get a coverage by ID"""
        return await self._make_request("GET", f"/coverages/{coverage_id}")
    
    async def get_coverages(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        beneficiary_id: Optional[str] = None
    ) -> List[Dict]:
        """Get list of coverages with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if beneficiary_id:
            params["beneficiary_id"] = beneficiary_id
            
        return await self._make_request("GET", "/coverages", params=params)
    
    async def update_coverage(self, coverage_id: str, coverage_data: Dict) -> Dict:
        """Update a coverage"""
        return await self._make_request("PUT", f"/coverages/{coverage_id}", data=coverage_data)
    
    async def delete_coverage(self, coverage_id: str) -> Dict:
        """Delete a coverage"""
        return await self._make_request("DELETE", f"/coverages/{coverage_id}")
    
    # Relationship Operations
    
    async def get_claim_responses_for_claim(self, claim_id: str) -> List[Dict]:
        """Get all responses for a specific claim"""
        return await self._make_request("GET", f"/claims/{claim_id}/responses")
    
    async def get_patient_claims(self, patient_id: str) -> List[Dict]:
        """Get all claims for a specific patient"""
        return await self._make_request("GET", f"/patients/{patient_id}/claims")
    
    # Statistics
    
    async def get_claims_stats(self) -> Dict:
        """Get claims statistics"""
        return await self._make_request("GET", "/stats/claims")
    
    # Health Check
    
    async def health_check(self) -> Dict:
        """Check if Claims service is healthy"""
        try:
            return await self._make_request("GET", "/health")
        except Exception as e:
            logger.warning(f"Claims service health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}

# Data Transformation Utilities

class ClaimsDataTransformer:
    """Utility class for transforming data between ClaimsAnomaly and Claims service formats"""
    
    @staticmethod
    def anomaly_claim_to_fhir(anomaly_claim_data: Dict) -> Dict:
        """
        Transform ClaimsAnomaly claim data to FHIR format
        
        Args:
            anomaly_claim_data: Claim data in ClaimsAnomaly format
            
        Returns:
            Claim data in FHIR format for Claims service
        """
        # Extract basic claim information
        claim_id = anomaly_claim_data.get('claim_id', '')
        submission_date = anomaly_claim_data.get('submission_date', '')
        provider_id = anomaly_claim_data.get('provider_id', '')
        patient_age = anomaly_claim_data.get('patient_age', 0)
        billed_amount = anomaly_claim_data.get('billed_amount', 0)
        paid_amount = anomaly_claim_data.get('paid_amount', 0)
        
        # Map ClaimsAnomaly data to FHIR structure
        fhir_claim = {
            'identifier': [{'system': 'claim-id', 'value': claim_id}],
            'status': 'active',
            'type': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/claim-type', 'code': 'professional'}]},
            'use': 'claim',
            'patient_id': f"patient-{claim_id}",  # Generate patient ID from claim
            'insurer_id': 'default-insurer',  # Default insurer
            'provider_id': provider_id,
            'created': submission_date,
            'item': []
        }
        
        # Create FHIR item from ClaimsAnomaly data
        fhir_item = {
            'sequence': 1,
            'careTeamSequence': [],
            'diagnosisSequence': [],
            'procedureSequence': [],
            'informationSequence': [],
            'revenue': {
                'coding': [{
                    'system': 'http://terminology.hl7.org/CodeSystem/ex-revenue-center',
                    'code': '0300'
                }]
            },
            'productOrService': {
                'coding': [{
                    'system': 'http://www.ama-assn.org/go/cpt',
                    'code': anomaly_claim_data.get('cpt_code', ''),
                    'display': f"CPT Code: {anomaly_claim_data.get('cpt_code', '')}"
                }]
            },
            'servicedDate': submission_date,
            'quantity': {
                'value': anomaly_claim_data.get('units_of_service', 1),
                'unit': 'unit'
            },
            'unitPrice': {
                'value': float(billed_amount),
                'currency': 'USD'
            },
            'net': {
                'value': float(billed_amount),
                'currency': 'USD'
            }
        }
        
        fhir_claim['item'].append(fhir_item)
        
        # Add total amount
        if billed_amount:
            fhir_claim['total'] = {
                'value': float(billed_amount),
                'currency': 'USD'
            }
        
        # Add diagnosis information
        if anomaly_claim_data.get('icd_code'):
            fhir_claim['diagnosis'] = [{
                'sequence': 1,
                'diagnosisCodeableConcept': {
                    'coding': [{
                        'system': 'http://hl7.org/fhir/sid/icd-10',
                        'code': anomaly_claim_data.get('icd_code', ''),
                        'display': f"ICD Code: {anomaly_claim_data.get('icd_code', '')}"
                    }]
                }
            }]
        
        return fhir_claim
    
    @staticmethod
    def fhir_claim_to_anomaly(fhir_claim_data: Dict) -> Dict:
        """
        Transform FHIR claim data to ClaimsAnomaly format
        
        Args:
            fhir_claim_data: Claim data in FHIR format from Claims service
            
        Returns:
            Claim data in ClaimsAnomaly format
        """
        # Extract basic information
        claim_id = fhir_claim_data.get('id', '')
        status = fhir_claim_data.get('status', 'active')
        
        # Find claim ID from identifiers
        claim_identifier = ''
        for identifier in fhir_claim_data.get('identifier', []):
            if identifier.get('system') == 'claim-id':
                claim_identifier = identifier.get('value', '')
                break
        
        # Build ClaimsAnomaly claim structure
        anomaly_claim = {
            'claim_id': claim_identifier or claim_id,
            'submission_date': fhir_claim_data.get('created', ''),
            'provider_id': fhir_claim_data.get('provider_id', ''),
            'provider_specialty': 'Unknown',  # Default value
            'patient_age': 0,  # Default value
            'patient_gender': 'M',  # Default value
            'cpt_code': '',
            'icd_code': '',
            'units_of_service': 1,
            'billed_amount': 0,
            'paid_amount': 0,
            'place_of_service': '11',  # Default office
            'prior_authorization': 'N',  # Default no
            'modifier': '',
            'is_anomaly': 0  # Default not anomaly
        }
        
        # Extract data from FHIR items
        for item in fhir_claim_data.get('item', []):
            # Extract CPT code
            if 'productOrService' in item and 'coding' in item['productOrService']:
                for coding in item['productOrService']['coding']:
                    if coding.get('system') == 'http://www.ama-assn.org/go/cpt':
                        anomaly_claim['cpt_code'] = coding.get('code', '')
                        break
            
            # Extract amount
            if 'net' in item:
                anomaly_claim['billed_amount'] = item['net'].get('value', 0)
            
            # Extract quantity
            if 'quantity' in item:
                anomaly_claim['units_of_service'] = item['quantity'].get('value', 1)
        
        # Extract diagnosis information
        for diagnosis in fhir_claim_data.get('diagnosis', []):
            if 'diagnosisCodeableConcept' in diagnosis and 'coding' in diagnosis['diagnosisCodeableConcept']:
                for coding in diagnosis['diagnosisCodeableConcept']['coding']:
                    if coding.get('system') == 'http://hl7.org/fhir/sid/icd-10':
                        anomaly_claim['icd_code'] = coding.get('code', '')
                        break
        
        # Extract total amount
        if 'total' in fhir_claim_data:
            anomaly_claim['billed_amount'] = fhir_claim_data['total'].get('value', 0)
        
        return anomaly_claim
    
    @staticmethod
    def batch_anomaly_to_fhir(batch_claims: List[Dict]) -> List[Dict]:
        """
        Transform batch of ClaimsAnomaly claims to FHIR format
        
        Args:
            batch_claims: List of claim data in ClaimsAnomaly format
            
        Returns:
            List of claim data in FHIR format
        """
        return [ClaimsDataTransformer.anomaly_claim_to_fhir(claim) for claim in batch_claims]
    
    @staticmethod
    def batch_fhir_to_anomaly(batch_fhir_claims: List[Dict]) -> List[Dict]:
        """
        Transform batch of FHIR claims to ClaimsAnomaly format
        
        Args:
            batch_fhir_claims: List of claim data in FHIR format
            
        Returns:
            List of claim data in ClaimsAnomaly format
        """
        return [ClaimsDataTransformer.fhir_claim_to_anomaly(claim) for claim in batch_fhir_claims]

# Factory function for creating client instances

def create_claims_service_client(base_url: str = None) -> ClaimsServiceClient:
    """
    Factory function to create Claims service client
    
    Args:
        base_url: Optional base URL override
        
    Returns:
        Configured ClaimsServiceClient instance
    """
    if base_url is None:
        # Default to Claims service URL from environment or config
        base_url = "http://localhost:8001"
    
    return ClaimsServiceClient(base_url=base_url) 