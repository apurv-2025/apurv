# =============================================================================
# FILE: backend/app/services/claims_service_client.py
# =============================================================================
"""
Claims Service Client for ClaimsProcessing Integration

This module provides a client interface to communicate with the foundational
Claims service, enabling ClaimsProcessing to use FHIR-based CRUD operations
while maintaining its high-level business logic and AI capabilities.
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
    """Utility class for transforming data between ClaimsProcessing and Claims service formats"""
    
    @staticmethod
    def edi_claim_to_fhir(edi_claim_data: Dict) -> Dict:
        """
        Transform EDI claim data to FHIR format
        
        Args:
            edi_claim_data: Claim data in EDI format from ClaimsProcessing
            
        Returns:
            Claim data in FHIR format for Claims service
        """
        # Extract basic claim information
        claim_number = edi_claim_data.get('claim_number', '')
        claim_type = edi_claim_data.get('claim_type', '837P')
        status = edi_claim_data.get('status', 'active')
        
        # Map EDI claim type to FHIR type
        fhir_type_mapping = {
            '837P': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/claim-type', 'code': 'professional'}]},
            '837D': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/claim-type', 'code': 'dental'}]},
            '837I': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/claim-type', 'code': 'institutional'}]}
        }
        
        # Build FHIR claim structure
        fhir_claim = {
            'identifier': [{'system': 'claim-number', 'value': claim_number}],
            'status': status,
            'type': fhir_type_mapping.get(claim_type, fhir_type_mapping['837P']),
            'use': 'claim',
            'patient_id': edi_claim_data.get('patient_id', ''),
            'insurer_id': edi_claim_data.get('payer_id', ''),
            'provider_id': edi_claim_data.get('provider_npi', ''),
            'created': datetime.utcnow().isoformat(),
            'item': []
        }
        
        # Transform service lines to FHIR items
        if 'service_lines' in edi_claim_data:
            for line in edi_claim_data['service_lines']:
                fhir_item = {
                    'sequence': line.get('line_number', 1),
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
                            'code': line.get('procedure_code', ''),
                            'display': line.get('procedure_description', '')
                        }]
                    },
                    'servicedDate': line.get('service_date_from', ''),
                    'quantity': {
                        'value': line.get('units', 1),
                        'unit': 'unit'
                    },
                    'unitPrice': {
                        'value': float(line.get('charge_amount', 0)),
                        'currency': 'USD'
                    },
                    'net': {
                        'value': float(line.get('charge_amount', 0)),
                        'currency': 'USD'
                    }
                }
                fhir_claim['item'].append(fhir_item)
        
        # Add total amount
        total_amount = edi_claim_data.get('total_charge', 0)
        if total_amount:
            fhir_claim['total'] = {
                'value': float(total_amount),
                'currency': 'USD'
            }
        
        return fhir_claim
    
    @staticmethod
    def fhir_claim_to_edi(fhir_claim_data: Dict) -> Dict:
        """
        Transform FHIR claim data to EDI format
        
        Args:
            fhir_claim_data: Claim data in FHIR format from Claims service
            
        Returns:
            Claim data in EDI format for ClaimsProcessing
        """
        # Extract basic information
        claim_id = fhir_claim_data.get('id', '')
        status = fhir_claim_data.get('status', 'active')
        
        # Find claim number from identifiers
        claim_number = ''
        for identifier in fhir_claim_data.get('identifier', []):
            if identifier.get('system') == 'claim-number':
                claim_number = identifier.get('value', '')
                break
        
        # Map FHIR type to EDI type
        edi_type_mapping = {
            'professional': '837P',
            'dental': '837D',
            'institutional': '837I'
        }
        
        claim_type = '837P'  # default
        if 'type' in fhir_claim_data and 'coding' in fhir_claim_data['type']:
            for coding in fhir_claim_data['type']['coding']:
                if coding.get('code') in edi_type_mapping:
                    claim_type = edi_type_mapping[coding['code']]
                    break
        
        # Build EDI claim structure
        edi_claim = {
            'id': claim_id,
            'claim_number': claim_number,
            'claim_type': claim_type,
            'status': status,
            'patient_id': fhir_claim_data.get('patient_id', ''),
            'provider_npi': fhir_claim_data.get('provider_id', ''),
            'payer_id': fhir_claim_data.get('insurer_id', ''),
            'service_lines': [],
            'created_at': fhir_claim_data.get('created', ''),
            'updated_at': fhir_claim_data.get('updated_at', '')
        }
        
        # Transform FHIR items to service lines
        for item in fhir_claim_data.get('item', []):
            service_line = {
                'line_number': item.get('sequence', 1),
                'procedure_code': '',
                'procedure_description': '',
                'charge_amount': 0,
                'units': 1
            }
            
            # Extract procedure code
            if 'productOrService' in item and 'coding' in item['productOrService']:
                for coding in item['productOrService']['coding']:
                    if coding.get('system') == 'http://www.ama-assn.org/go/cpt':
                        service_line['procedure_code'] = coding.get('code', '')
                        service_line['procedure_description'] = coding.get('display', '')
                        break
            
            # Extract amount
            if 'net' in item:
                service_line['charge_amount'] = item['net'].get('value', 0)
            
            # Extract quantity
            if 'quantity' in item:
                service_line['units'] = item['quantity'].get('value', 1)
            
            edi_claim['service_lines'].append(service_line)
        
        # Extract total amount
        if 'total' in fhir_claim_data:
            edi_claim['total_charge'] = fhir_claim_data['total'].get('value', 0)
        
        return edi_claim

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