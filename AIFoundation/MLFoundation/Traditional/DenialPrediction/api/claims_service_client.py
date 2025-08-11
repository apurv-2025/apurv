"""
Claims Service Client for DenialPrediction Integration

This module provides a client interface to communicate with the foundational
Claims service, enabling DenialPrediction to use FHIR-based CRUD operations
while maintaining its ML prediction capabilities.
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
        """Get a specific claim by ID"""
        return await self._make_request("GET", f"/claims/{claim_id}")
    
    async def get_claims(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        patient_id: Optional[str] = None,
        provider_id: Optional[str] = None
    ) -> List[Dict]:
        """Get claims with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if patient_id:
            params["patient_id"] = patient_id
        if provider_id:
            params["provider_id"] = provider_id
            
        return await self._make_request("GET", "/claims", params=params)
    
    async def update_claim(self, claim_id: str, claim_data: Dict) -> Dict:
        """Update an existing claim"""
        return await self._make_request("PUT", f"/claims/{claim_id}", data=claim_data)
    
    async def delete_claim(self, claim_id: str) -> Dict:
        """Delete a claim"""
        return await self._make_request("DELETE", f"/claims/{claim_id}")
    
    # Prediction-specific Operations
    
    async def get_claim_for_prediction(self, claim_id: str) -> Dict:
        """Get claim data in DenialPrediction format"""
        fhir_claim = await self.get_claim(claim_id)
        return ClaimsDataTransformer.fhir_claim_to_prediction(fhir_claim)
    
    async def update_claim_with_prediction(self, claim_id: str, prediction_data: Dict) -> Dict:
        """Update claim with prediction results"""
        update_data = {
            "denial_probability": prediction_data.get("denial_probability"),
            "risk_level": prediction_data.get("risk_level"),
            "prediction_timestamp": datetime.utcnow().isoformat(),
            "model_version": prediction_data.get("model_version"),
            "top_risk_factors": prediction_data.get("top_risk_factors"),
            "recommended_actions": prediction_data.get("recommended_actions"),
            "shap_values": prediction_data.get("shap_values")
        }
        return await self.update_claim(claim_id, update_data)
    
    async def create_prediction(self, prediction_data: Dict) -> Dict:
        """Create a new prediction record"""
        return await self._make_request("POST", "/predictions", data=prediction_data)
    
    async def get_predictions(
        self,
        skip: int = 0,
        limit: int = 100,
        claim_id: Optional[str] = None,
        model_version: Optional[str] = None
    ) -> List[Dict]:
        """Get predictions with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if claim_id:
            params["claim_id"] = claim_id
        if model_version:
            params["model_version"] = model_version
            
        return await self._make_request("GET", "/predictions", params=params)
    
    # Denial Record Operations
    
    async def create_denial_record(self, denial_data: Dict) -> Dict:
        """Create a denial record"""
        return await self._make_request("POST", "/denial-records", data=denial_data)
    
    async def get_denial_record(self, record_id: int) -> Dict:
        """Get a specific denial record"""
        return await self._make_request("GET", f"/denial-records/{record_id}")
    
    async def get_denial_records(
        self,
        skip: int = 0,
        limit: int = 100,
        claim_id: Optional[str] = None,
        resolution_status: Optional[str] = None
    ) -> List[Dict]:
        """Get denial records with optional filtering"""
        params = {"skip": skip, "limit": limit}
        if claim_id:
            params["claim_id"] = claim_id
        if resolution_status:
            params["resolution_status"] = resolution_status
            
        return await self._make_request("GET", "/denial-records", params=params)
    
    async def update_denial_record(self, record_id: int, denial_data: Dict) -> Dict:
        """Update a denial record"""
        return await self._make_request("PUT", f"/denial-records/{record_id}", data=denial_data)
    
    # Batch Operations
    
    async def get_claims_for_prediction(self, limit: int = 100, status: str = "active") -> List[Dict]:
        """Get claims ready for prediction processing"""
        claims = await self.get_claims(limit=limit, status=status)
        return [ClaimsDataTransformer.fhir_claim_to_prediction(claim) for claim in claims]
    
    async def batch_update_predictions(self, predictions: List[Dict]) -> List[Dict]:
        """Update multiple claims with predictions"""
        results = []
        for prediction in predictions:
            try:
                claim_id = prediction.get("claim_id")
                if claim_id:
                    result = await self.update_claim_with_prediction(claim_id, prediction)
                    results.append({"claim_id": claim_id, "status": "success", "result": result})
                else:
                    results.append({"claim_id": None, "status": "error", "error": "Missing claim_id"})
            except Exception as e:
                results.append({"claim_id": prediction.get("claim_id"), "status": "error", "error": str(e)})
        return results
    
    # Statistics and Analytics
    
    async def get_claims_stats(self) -> Dict:
        """Get claims statistics"""
        return await self._make_request("GET", "/stats/claims")
    
    async def get_prediction_stats(self) -> Dict:
        """Get prediction statistics"""
        return await self._make_request("GET", "/stats/predictions")
    
    async def get_denial_stats(self) -> Dict:
        """Get denial statistics"""
        return await self._make_request("GET", "/stats/denials")
    
    # Health and Status
    
    async def health_check(self) -> Dict:
        """Check Claims service health"""
        return await self._make_request("GET", "/health")


class ClaimsDataTransformer:
    """Transform data between Claims Service and DenialPrediction formats"""
    
    @staticmethod
    def fhir_claim_to_prediction(fhir_claim: Dict) -> Dict:
        """
        Convert FHIR claim to DenialPrediction format
        
        Args:
            fhir_claim: FHIR claim data from Claims service
            
        Returns:
            DenialPrediction format claim data
        """
        try:
            # Extract basic fields
            prediction_claim = {
                "claim_id": fhir_claim.get("id"),
                "provider_id": fhir_claim.get("provider_id"),
                "patient_id": fhir_claim.get("patient_id"),
                "payer_id": fhir_claim.get("insurer_id"),
                "claim_amount": ClaimsDataTransformer._extract_total_amount(fhir_claim),
                "submission_date": fhir_claim.get("created"),
                "service_date": ClaimsDataTransformer._extract_service_date(fhir_claim),
                "patient_age": ClaimsDataTransformer._extract_patient_age(fhir_claim),
                "patient_gender": ClaimsDataTransformer._extract_patient_gender(fhir_claim),
                "authorization_number": ClaimsDataTransformer._extract_auth_number(fhir_claim),
                "cpt_codes": ClaimsDataTransformer._extract_cpt_codes(fhir_claim),
                "icd_codes": ClaimsDataTransformer._extract_icd_codes(fhir_claim),
                "modifiers": ClaimsDataTransformer._extract_modifiers(fhir_claim),
                "place_of_service": ClaimsDataTransformer._extract_place_of_service(fhir_claim),
                "diagnosis_codes": ClaimsDataTransformer._extract_diagnosis_codes(fhir_claim)
            }
            
            # Add existing prediction data if available
            if fhir_claim.get("denial_probability") is not None:
                prediction_claim.update({
                    "denial_probability": fhir_claim.get("denial_probability"),
                    "risk_level": fhir_claim.get("risk_level"),
                    "prediction_timestamp": fhir_claim.get("prediction_timestamp"),
                    "model_version": fhir_claim.get("model_version"),
                    "top_risk_factors": fhir_claim.get("top_risk_factors"),
                    "recommended_actions": fhir_claim.get("recommended_actions")
                })
            
            # Add denial information if available
            if fhir_claim.get("is_denied"):
                prediction_claim.update({
                    "is_denied": fhir_claim.get("is_denied"),
                    "denial_date": fhir_claim.get("denial_date"),
                    "denial_codes": fhir_claim.get("denial_codes"),
                    "denial_reason": fhir_claim.get("denial_reason")
                })
            
            return prediction_claim
            
        except Exception as e:
            logger.error(f"Error transforming FHIR claim to prediction format: {e}")
            raise ValueError(f"Failed to transform claim data: {str(e)}")
    
    @staticmethod
    def prediction_to_fhir_claim(prediction_claim: Dict) -> Dict:
        """
        Convert DenialPrediction claim to FHIR format
        
        Args:
            prediction_claim: DenialPrediction format claim data
            
        Returns:
            FHIR format claim data
        """
        try:
            # Basic FHIR claim structure
            fhir_claim = {
                "resource_type": "Claim",
                "status": "active",
                "use": "claim",
                "patient_id": prediction_claim.get("patient_id"),
                "insurer_id": prediction_claim.get("payer_id"),
                "provider_id": prediction_claim.get("provider_id"),
                "created": prediction_claim.get("submission_date"),
                "total": {
                    "currency": "USD",
                    "value": prediction_claim.get("claim_amount", 0)
                },
                "item": ClaimsDataTransformer._create_fhir_items(prediction_claim),
                "diagnosis": ClaimsDataTransformer._create_fhir_diagnoses(prediction_claim),
                "insurance": [{"coverage": {"reference": f"Coverage/{prediction_claim.get('payer_id')}"}}]
            }
            
            # Add billable period if service date is available
            if prediction_claim.get("service_date"):
                fhir_claim["billable_period"] = {
                    "start": prediction_claim.get("service_date")
                }
            
            # Add prediction data
            if prediction_claim.get("denial_probability") is not None:
                fhir_claim.update({
                    "denial_probability": prediction_claim.get("denial_probability"),
                    "risk_level": prediction_claim.get("risk_level"),
                    "prediction_timestamp": prediction_claim.get("prediction_timestamp"),
                    "model_version": prediction_claim.get("model_version"),
                    "top_risk_factors": prediction_claim.get("top_risk_factors"),
                    "recommended_actions": prediction_claim.get("recommended_actions")
                })
            
            return fhir_claim
            
        except Exception as e:
            logger.error(f"Error transforming prediction claim to FHIR format: {e}")
            raise ValueError(f"Failed to transform claim data: {str(e)}")
    
    # Helper methods for data extraction
    
    @staticmethod
    def _extract_total_amount(fhir_claim: Dict) -> float:
        """Extract total amount from FHIR claim"""
        total = fhir_claim.get("total", {})
        if isinstance(total, dict):
            return total.get("value", 0.0)
        return 0.0
    
    @staticmethod
    def _extract_service_date(fhir_claim: Dict) -> str:
        """Extract service date from FHIR claim"""
        billable_period = fhir_claim.get("billable_period", {})
        if isinstance(billable_period, dict):
            return billable_period.get("start", "")
        return ""
    
    @staticmethod
    def _extract_patient_age(fhir_claim: Dict) -> int:
        """Extract patient age from FHIR claim (placeholder)"""
        # This would need to be calculated from patient birth date
        # For now, return a default value
        return 45
    
    @staticmethod
    def _extract_patient_gender(fhir_claim: Dict) -> str:
        """Extract patient gender from FHIR claim (placeholder)"""
        # This would need to be extracted from patient resource
        # For now, return a default value
        return "M"
    
    @staticmethod
    def _extract_auth_number(fhir_claim: Dict) -> str:
        """Extract authorization number from FHIR claim"""
        # This would be in supporting info or other fields
        return ""
    
    @staticmethod
    def _extract_cpt_codes(fhir_claim: Dict) -> List[str]:
        """Extract CPT codes from FHIR claim items"""
        codes = []
        items = fhir_claim.get("item", [])
        for item in items:
            if isinstance(item, dict):
                product_service = item.get("productOrService", {})
                if isinstance(product_service, dict):
                    coding = product_service.get("coding", [])
                    for code in coding:
                        if isinstance(code, dict) and code.get("system") == "http://www.ama-assn.org/go/cpt":
                            codes.append(code.get("code", ""))
        return codes
    
    @staticmethod
    def _extract_icd_codes(fhir_claim: Dict) -> List[str]:
        """Extract ICD codes from FHIR claim diagnoses"""
        codes = []
        diagnoses = fhir_claim.get("diagnosis", [])
        for diagnosis in diagnoses:
            if isinstance(diagnosis, dict):
                diagnosis_concept = diagnosis.get("diagnosisCodeableConcept", {})
                if isinstance(diagnosis_concept, dict):
                    coding = diagnosis_concept.get("coding", [])
                    for code in coding:
                        if isinstance(code, dict) and "icd" in code.get("system", "").lower():
                            codes.append(code.get("code", ""))
        return codes
    
    @staticmethod
    def _extract_modifiers(fhir_claim: Dict) -> List[str]:
        """Extract modifiers from FHIR claim items"""
        modifiers = []
        items = fhir_claim.get("item", [])
        for item in items:
            if isinstance(item, dict):
                modifier = item.get("modifier")
                if modifier:
                    modifiers.append(modifier)
        return modifiers
    
    @staticmethod
    def _extract_place_of_service(fhir_claim: Dict) -> str:
        """Extract place of service from FHIR claim items"""
        items = fhir_claim.get("item", [])
        for item in items:
            if isinstance(item, dict):
                location = item.get("locationCodeableConcept", {})
                if isinstance(location, dict):
                    coding = location.get("coding", [])
                    for code in coding:
                        if isinstance(code, dict):
                            return code.get("code", "")
        return ""
    
    @staticmethod
    def _extract_diagnosis_codes(fhir_claim: Dict) -> List[str]:
        """Extract diagnosis codes (same as ICD codes)"""
        return ClaimsDataTransformer._extract_icd_codes(fhir_claim)
    
    @staticmethod
    def _create_fhir_items(prediction_claim: Dict) -> List[Dict]:
        """Create FHIR items from prediction claim data"""
        items = []
        cpt_codes = prediction_claim.get("cpt_codes", [])
        modifiers = prediction_claim.get("modifiers", [])
        
        for i, cpt_code in enumerate(cpt_codes):
            item = {
                "sequence": i + 1,
                "productOrService": {
                    "coding": [{
                        "system": "http://www.ama-assn.org/go/cpt",
                        "code": cpt_code
                    }]
                }
            }
            
            # Add modifier if available
            if i < len(modifiers):
                item["modifier"] = modifiers[i]
            
            # Add place of service if available
            place_of_service = prediction_claim.get("place_of_service")
            if place_of_service:
                item["locationCodeableConcept"] = {
                    "coding": [{
                        "system": "https://www.cms.gov/Medicare/Coding/place-of-service-codes/Place_of_Service_Code_Set",
                        "code": place_of_service
                    }]
                }
            
            items.append(item)
        
        return items
    
    @staticmethod
    def _create_fhir_diagnoses(prediction_claim: Dict) -> List[Dict]:
        """Create FHIR diagnoses from prediction claim data"""
        diagnoses = []
        icd_codes = prediction_claim.get("icd_codes", [])
        
        for i, icd_code in enumerate(icd_codes):
            diagnosis = {
                "sequence": i + 1,
                "diagnosisCodeableConcept": {
                    "coding": [{
                        "system": "http://hl7.org/fhir/sid/icd-10",
                        "code": icd_code
                    }]
                }
            }
            diagnoses.append(diagnosis)
        
        return diagnoses


def create_claims_service_client(base_url: str = None) -> ClaimsServiceClient:
    """
    Create a Claims Service client instance
    
    Args:
        base_url: Base URL of the Claims service (defaults to env var)
        
    Returns:
        ClaimsServiceClient instance
    """
    import os
    
    if base_url is None:
        base_url = os.getenv('CLAIMS_SERVICE_URL', 'http://localhost:8001')
    
    return ClaimsServiceClient(base_url) 