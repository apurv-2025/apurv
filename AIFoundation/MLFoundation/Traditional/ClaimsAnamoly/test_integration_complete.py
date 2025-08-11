#!/usr/bin/env python3
"""
Complete Integration Test for ClaimsAnamoly + Claims Service

This script tests the full integration between ClaimsAnamoly (ML anomaly detection)
and Claims Service (FHIR-compliant CRUD operations).
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationTester:
    """Test the complete integration between ClaimsAnamoly and Claims Service"""
    
    def __init__(self):
        self.claims_service_url = "http://localhost:8002"
        self.claims_anomaly_url = "http://localhost:8003"
        self.timeout = 30
        
    async def test_health_checks(self) -> bool:
        """Test health checks for both services"""
        logger.info("🔍 Testing health checks...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Test Claims Service health
                response = await client.get(f"{self.claims_service_url}/health")
                if response.status_code == 200:
                    logger.info("✅ Claims Service health check passed")
                else:
                    logger.error(f"❌ Claims Service health check failed: {response.status_code}")
                    return False
                
                # Test ClaimsAnamoly health
                response = await client.get(f"{self.claims_anomaly_url}/health")
                if response.status_code == 200:
                    logger.info("✅ ClaimsAnamoly health check passed")
                else:
                    logger.error(f"❌ ClaimsAnamoly health check failed: {response.status_code}")
                    return False
                
                # Test integration health
                response = await client.get(f"{self.claims_anomaly_url}/api/v1/health/integration")
                if response.status_code == 200:
                    logger.info("✅ Integration health check passed")
                else:
                    logger.error(f"❌ Integration health check failed: {response.status_code}")
                    return False
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Health check error: {e}")
                return False
    
    async def test_claims_service_crud(self) -> bool:
        """Test basic CRUD operations on Claims Service"""
        logger.info("🔍 Testing Claims Service CRUD operations...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Create a test claim
                test_claim = {
                    "patient_id": "TEST_PATIENT_001",
                    "provider_id": "TEST_PROVIDER_001",
                    "status": "active",
                    "type": "professional",
                    "use": "claim",
                    "created": "2024-01-15T10:00:00Z",
                    "insurer_id": "TEST_INSURER_001",
                    "priority": "normal",
                    "funds_reserve": "none",
                    "related": [],
                    "prescription": False,
                    "original_prescription": False,
                    "payee": None,
                    "referral": None,
                    "facility": None,
                    "care_team": [],
                    "insurance": [],
                    "accident": None,
                    "employment_impacted": None,
                    "hospitalization": None,
                    "item": [],
                    "total": {
                        "currency": "USD",
                        "value": 150.00
                    }
                }
                
                # Create claim
                response = await client.post(
                    f"{self.claims_service_url}/api/v1/claims",
                    json=test_claim
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to create claim: {response.status_code}")
                    return False
                
                created_claim = response.json()
                claim_id = created_claim.get('id')
                logger.info(f"✅ Created claim with ID: {claim_id}")
                
                # Read claim
                response = await client.get(f"{self.claims_service_url}/api/v1/claims/{claim_id}")
                if response.status_code != 200:
                    logger.error(f"❌ Failed to read claim: {response.status_code}")
                    return False
                
                logger.info("✅ Successfully read claim")
                
                # Update claim
                update_data = {"status": "completed"}
                response = await client.put(
                    f"{self.claims_service_url}/api/v1/claims/{claim_id}",
                    json=update_data
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to update claim: {response.status_code}")
                    return False
                
                logger.info("✅ Successfully updated claim")
                
                # Delete claim
                response = await client.delete(f"{self.claims_service_url}/api/v1/claims/{claim_id}")
                if response.status_code != 200:
                    logger.error(f"❌ Failed to delete claim: {response.status_code}")
                    return False
                
                logger.info("✅ Successfully deleted claim")
                return True
                
            except Exception as e:
                logger.error(f"❌ CRUD test error: {e}")
                return False
    
    async def test_claims_anomaly_scoring(self) -> bool:
        """Test ClaimsAnamoly scoring functionality"""
        logger.info("🔍 Testing ClaimsAnamoly scoring...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Test single claim scoring
                test_claim = {
                    "claim_id": "TEST_CLM_001",
                    "submission_date": "2024-01-15",
                    "provider_id": "TEST_PROV_001",
                    "provider_specialty": "Cardiology",
                    "patient_age": 45,
                    "patient_gender": "M",
                    "cpt_code": "99213",
                    "icd_code": "I10",
                    "units_of_service": 1,
                    "billed_amount": 150.00,
                    "paid_amount": 120.00,
                    "place_of_service": "11",
                    "prior_authorization": "N"
                }
                
                response = await client.post(
                    f"{self.claims_anomaly_url}/api/v1/score",
                    json=test_claim,
                    params={"use_fhir": "true"}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to score claim: {response.status_code}")
                    return False
                
                result = response.json()
                logger.info(f"✅ Successfully scored claim. Risk score: {result.get('risk_score')}")
                logger.info(f"   Classification: {result.get('classification')}")
                logger.info(f"   FHIR ID: {result.get('fhir_claim_id')}")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Scoring test error: {e}")
                return False
    
    async def test_integration_features(self) -> bool:
        """Test integration-specific features"""
        logger.info("🔍 Testing integration features...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Test getting claims from service
                response = await client.get(
                    f"{self.claims_anomaly_url}/api/v1/claims/from-service",
                    params={"limit": 5}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to get claims from service: {response.status_code}")
                    return False
                
                claims_data = response.json()
                logger.info(f"✅ Retrieved {len(claims_data.get('claims', []))} claims from service")
                
                # Test scoring claims from service
                response = await client.post(
                    f"{self.claims_anomaly_url}/api/v1/score/from-service",
                    params={"limit": 3}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to score claims from service: {response.status_code}")
                    return False
                
                scoring_result = response.json()
                logger.info(f"✅ Scored {scoring_result.get('count', 0)} claims from service")
                
                # Test anomaly statistics
                response = await client.get(
                    f"{self.claims_anomaly_url}/api/v1/stats/anomaly",
                    params={"use_fhir": "true"}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to get anomaly statistics: {response.status_code}")
                    return False
                
                stats = response.json()
                logger.info("✅ Retrieved anomaly statistics with FHIR integration")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Integration test error: {e}")
                return False
    
    async def test_model_info(self) -> bool:
        """Test model information endpoints"""
        logger.info("🔍 Testing model information...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Test model info
                response = await client.get(f"{self.claims_anomaly_url}/api/v1/model/info")
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to get model info: {response.status_code}")
                    return False
                
                model_info = response.json()
                logger.info(f"✅ Model info retrieved. Type: {model_info.get('model_type')}")
                logger.info(f"   Integration enabled: {model_info.get('integration_enabled')}")
                logger.info(f"   Claims service URL: {model_info.get('claims_service_url')}")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Model info test error: {e}")
                return False
    
    async def test_example_data(self) -> bool:
        """Test example data endpoints"""
        logger.info("🔍 Testing example data...")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Test example claim
                response = await client.get(f"{self.claims_anomaly_url}/api/v1/example")
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to get example data: {response.status_code}")
                    return False
                
                example_data = response.json()
                logger.info("✅ Retrieved example claim data")
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Example data test error: {e}")
                return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all integration tests"""
        logger.info("🚀 Starting complete integration tests...")
        logger.info("=" * 60)
        
        test_results = {}
        
        # Test 1: Health checks
        test_results['health_checks'] = await self.test_health_checks()
        
        # Test 2: Claims Service CRUD
        test_results['claims_service_crud'] = await self.test_claims_service_crud()
        
        # Test 3: ClaimsAnamoly scoring
        test_results['claims_anomaly_scoring'] = await self.test_claims_anomaly_scoring()
        
        # Test 4: Integration features
        test_results['integration_features'] = await self.test_integration_features()
        
        # Test 5: Model information
        test_results['model_info'] = await self.test_model_info()
        
        # Test 6: Example data
        test_results['example_data'] = await self.test_example_data()
        
        # Summary
        logger.info("=" * 60)
        logger.info("📊 Test Results Summary:")
        logger.info("=" * 60)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1
        
        logger.info("=" * 60)
        logger.info(f"Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("🎉 All tests passed! Integration is working correctly.")
        else:
            logger.error("⚠️  Some tests failed. Check the logs above for details.")
        
        return test_results

async def main():
    """Main function to run the integration tests"""
    tester = IntegrationTester()
    
    try:
        results = await tester.run_all_tests()
        
        # Exit with appropriate code
        if all(results.values()):
            exit(0)
        else:
            exit(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Tests interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 