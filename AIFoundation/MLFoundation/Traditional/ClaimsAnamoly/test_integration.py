#!/usr/bin/env python3
"""
Integration Test Script for ClaimsAnomaly + Claims Service

This script tests the integration between ClaimsAnomaly and the Claims service,
verifying that both systems work together seamlessly for ML anomaly detection.
"""

import asyncio
import httpx
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CLAIMS_ANOMALY_URL = "http://localhost:8002"
CLAIMS_SERVICE_URL = "http://localhost:8001"

# Sample claim data for testing
SAMPLE_CLAIM_DATA = {
    "claim_id": "TEST-001",
    "submission_date": "2024-01-15",
    "provider_id": "PROVIDER-123",
    "provider_specialty": "Cardiology",
    "patient_age": 45,
    "patient_gender": "M",
    "cpt_code": "99213",
    "icd_code": "I10",
    "units_of_service": 1,
    "billed_amount": 150.00,
    "paid_amount": 120.00,
    "place_of_service": "11",
    "prior_authorization": "N",
    "modifier": "",
    "is_anomaly": 0
}

SAMPLE_BATCH_DATA = [
    {
        "claim_id": "TEST-001",
        "submission_date": "2024-01-15",
        "provider_id": "PROVIDER-123",
        "provider_specialty": "Cardiology",
        "patient_age": 45,
        "patient_gender": "M",
        "cpt_code": "99213",
        "icd_code": "I10",
        "units_of_service": 1,
        "billed_amount": 150.00,
        "paid_amount": 120.00,
        "place_of_service": "11",
        "prior_authorization": "N",
        "modifier": "",
        "is_anomaly": 0
    },
    {
        "claim_id": "TEST-002",
        "submission_date": "2024-01-16",
        "provider_id": "PROVIDER-456",
        "provider_specialty": "Orthopedics",
        "patient_age": 32,
        "patient_gender": "F",
        "cpt_code": "99214",
        "icd_code": "M79.3",
        "units_of_service": 1,
        "billed_amount": 200.00,
        "paid_amount": 160.00,
        "place_of_service": "11",
        "prior_authorization": "Y",
        "modifier": "25",
        "is_anomaly": 0
    }
]

class IntegrationTester:
    """Test class for ClaimsAnomaly + Claims Service integration"""
    
    def __init__(self):
        self.claims_anomaly_client = httpx.AsyncClient(base_url=CLAIMS_ANOMALY_URL, timeout=30.0)
        self.claims_service_client = httpx.AsyncClient(base_url=CLAIMS_SERVICE_URL, timeout=30.0)
        self.test_results = []
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.claims_anomaly_client.aclose()
        await self.claims_service_client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {details}")
        
        if not success and data:
            logger.error(f"Error details: {data}")
    
    async def test_claims_service_health(self) -> bool:
        """Test Claims service health"""
        try:
            response = await self.claims_service_client.get("/health")
            response.raise_for_status()
            data = response.json()
            
            success = data.get("status") == "healthy"
            self.log_test("Claims Service Health", success, f"Status: {data.get('status')}", data)
            return success
            
        except Exception as e:
            self.log_test("Claims Service Health", False, f"Error: {str(e)}")
            return False
    
    async def test_claims_anomaly_health(self) -> bool:
        """Test ClaimsAnomaly health"""
        try:
            response = await self.claims_anomaly_client.get("/health")
            response.raise_for_status()
            data = response.json()
            
            success = data.get("status") in ["healthy", "degraded"]  # degraded is acceptable
            self.log_test("ClaimsAnomaly Health", success, f"Status: {data.get('status')}", data)
            return success
            
        except Exception as e:
            self.log_test("ClaimsAnomaly Health", False, f"Error: {str(e)}")
            return False
    
    async def test_integration_health(self) -> bool:
        """Test integration health endpoint"""
        try:
            response = await self.claims_anomaly_client.get("/api/v1/health/integration")
            response.raise_for_status()
            data = response.json()
            
            health_status = data.get("health_status", {})
            overall_status = health_status.get("overall_status")
            
            success = overall_status in ["healthy", "degraded"]  # degraded is acceptable for testing
            self.log_test("Integration Health", success, f"Overall status: {overall_status}", data)
            return success
            
        except Exception as e:
            self.log_test("Integration Health", False, f"Error: {str(e)}")
            return False
    
    async def test_single_claim_scoring(self) -> bool:
        """Test single claim scoring with integration"""
        try:
            response = await self.claims_anomaly_client.post(
                "/api/v1/score",
                json=SAMPLE_CLAIM_DATA,
                params={"use_fhir": True}
            )
            response.raise_for_status()
            data = response.json()
            
            integration_status = data.get("integration_status")
            stored_in_fhir = data.get("stored_in_fhir")
            
            success = integration_status in ["success", "fallback"] and "claim_id" in data
            self.log_test(
                "Single Claim Scoring", 
                success, 
                f"Integration status: {integration_status}, Stored in FHIR: {stored_in_fhir}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Single Claim Scoring", False, f"Error: {str(e)}")
            return False
    
    async def test_batch_claim_scoring(self) -> bool:
        """Test batch claim scoring with integration"""
        try:
            batch_request = {
                "claims": SAMPLE_BATCH_DATA,
                "use_fhir": True
            }
            
            response = await self.claims_anomaly_client.post(
                "/api/v1/score/batch",
                json=batch_request
            )
            response.raise_for_status()
            data = response.json()
            
            integration_status = data.get("integration_status")
            count = data.get("count", 0)
            
            success = integration_status in ["success", "fallback"] and count > 0
            self.log_test(
                "Batch Claim Scoring", 
                success, 
                f"Integration status: {integration_status}, Claims scored: {count}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Batch Claim Scoring", False, f"Error: {str(e)}")
            return False
    
    async def test_claims_service_crud(self) -> bool:
        """Test basic CRUD operations on Claims service"""
        try:
            # Test creating a claim
            claim_data = {
                "identifier": [{"system": "test-system", "value": "ANOMALY-TEST-001"}],
                "status": "active",
                "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "professional"}]},
                "use": "claim",
                "patient_id": "patient-123",
                "insurer_id": "insurer-456",
                "provider_id": "provider-789"
            }
            
            response = await self.claims_service_client.post("/api/v1/claims", json=claim_data)
            response.raise_for_status()
            created_claim = response.json()
            claim_id = created_claim.get("id")
            
            if not claim_id:
                self.log_test("Claims Service CRUD", False, "No claim ID returned")
                return False
            
            # Test getting the claim
            response = await self.claims_service_client.get(f"/api/v1/claims/{claim_id}")
            response.raise_for_status()
            retrieved_claim = response.json()
            
            # Test updating the claim
            update_data = {"status": "cancelled"}
            response = await self.claims_service_client.put(f"/api/v1/claims/{claim_id}", json=update_data)
            response.raise_for_status()
            updated_claim = response.json()
            
            # Test deleting the claim
            response = await self.claims_service_client.delete(f"/api/v1/claims/{claim_id}")
            response.raise_for_status()
            
            success = True
            self.log_test(
                "Claims Service CRUD", 
                success, 
                f"Successfully created, retrieved, updated, and deleted claim {claim_id}",
                {"claim_id": claim_id}
            )
            return success
            
        except Exception as e:
            self.log_test("Claims Service CRUD", False, f"Error: {str(e)}")
            return False
    
    async def test_model_info(self) -> bool:
        """Test model information endpoint"""
        try:
            response = await self.claims_anomaly_client.get("/api/v1/model/info")
            response.raise_for_status()
            data = response.json()
            
            integration_enabled = data.get("integration_enabled", False)
            enhanced_features = data.get("enhanced_features", [])
            
            success = integration_enabled and len(enhanced_features) > 0
            self.log_test(
                "Model Information", 
                success, 
                f"Integration enabled: {integration_enabled}, Features: {len(enhanced_features)}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Model Information", False, f"Error: {str(e)}")
            return False
    
    async def test_anomaly_statistics(self) -> bool:
        """Test anomaly statistics endpoint"""
        try:
            response = await self.claims_anomaly_client.get("/api/v1/stats/anomaly")
            response.raise_for_status()
            data = response.json()
            
            local_stats = data.get("local_stats", {})
            fhir_stats = data.get("fhir_stats")
            
            success = "model_loaded" in local_stats
            self.log_test(
                "Anomaly Statistics", 
                success, 
                f"Local stats available: {bool(local_stats)}, FHIR stats available: {bool(fhir_stats)}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Anomaly Statistics", False, f"Error: {str(e)}")
            return False
    
    async def test_claim_validation(self) -> bool:
        """Test claim validation endpoint"""
        try:
            response = await self.claims_anomaly_client.post(
                "/api/v1/validate/claim",
                json=SAMPLE_CLAIM_DATA
            )
            response.raise_for_status()
            data = response.json()
            
            overall_status = data.get("overall_status")
            ml_validation = data.get("ml_validation", {})
            fhir_validation = data.get("fhir_validation", {})
            
            success = overall_status in ["valid", "invalid"] and "claim_id" in data
            self.log_test(
                "Claim Validation", 
                success, 
                f"Overall status: {overall_status}, ML valid: {ml_validation.get('is_valid')}, FHIR valid: {fhir_validation.get('status')}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Claim Validation", False, f"Error: {str(e)}")
            return False
    
    async def test_example_endpoint(self) -> bool:
        """Test example endpoint"""
        try:
            response = await self.claims_anomaly_client.get("/api/v1/example")
            response.raise_for_status()
            data = response.json()
            
            example_claim = data.get("example_claim", {})
            
            success = "claim_id" in example_claim and "cpt_code" in example_claim
            self.log_test(
                "Example Endpoint", 
                success, 
                f"Example claim available with {len(example_claim)} fields",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Example Endpoint", False, f"Error: {str(e)}")
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting ClaimsAnomaly + Claims Service Integration Tests")
        logger.info("=" * 60)
        
        tests = [
            ("Claims Service Health", self.test_claims_service_health),
            ("ClaimsAnomaly Health", self.test_claims_anomaly_health),
            ("Integration Health", self.test_integration_health),
            ("Claims Service CRUD", self.test_claims_service_crud),
            ("Single Claim Scoring", self.test_single_claim_scoring),
            ("Batch Claim Scoring", self.test_batch_claim_scoring),
            ("Model Information", self.test_model_info),
            ("Anomaly Statistics", self.test_anomaly_statistics),
            ("Claim Validation", self.test_claim_validation),
            ("Example Endpoint", self.test_example_endpoint),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results[test_name] = result
            except Exception as e:
                logger.error(f"Test {test_name} failed with exception: {e}")
                results[test_name] = False
        
        # Calculate summary
        total_tests = len(tests)
        passed_tests = sum(1 for result in results.values() if result)
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            "results": results,
            "detailed_results": self.test_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("=" * 60)
        logger.info("📊 Integration Test Summary")
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {summary['success_rate']:.1f}%")
        
        if failed_tests == 0:
            logger.info("🎉 All tests passed! Integration is working correctly.")
        else:
            logger.warning(f"⚠️  {failed_tests} test(s) failed. Check the details above.")
        
        return summary

async def main():
    """Main test function"""
    print("ClaimsAnomaly + Claims Service Integration Test")
    print("=" * 60)
    print(f"ClaimsAnomaly URL: {CLAIMS_ANOMALY_URL}")
    print(f"Claims Service URL: {CLAIMS_SERVICE_URL}")
    print()
    
    async with IntegrationTester() as tester:
        summary = await tester.run_all_tests()
        
        # Save results to file
        with open("claims_anomaly_integration_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: claims_anomaly_integration_test_results.json")
        
        return summary

if __name__ == "__main__":
    asyncio.run(main()) 