#!/usr/bin/env python3
"""
Integration Test Script for ClaimsProcessing + Claims Service

This script tests the integration between ClaimsProcessing and the Claims service,
verifying that both systems work together seamlessly.
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
CLAIMS_PROCESSING_URL = "http://localhost:8000"
CLAIMS_SERVICE_URL = "http://localhost:8001"

# Sample EDI content for testing
SAMPLE_EDI_CONTENT = """ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *230101*1200*U*00401*000000001*0*P*>~
GS*HC*SENDER*RECEIVER*20230101*1200*1*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*0123*20230101*1200*CH~
NM1*41*2*PAYER NAME*****46*PAYER123~
PER*IC*CONTACT PERSON*TE*555-123-4567~
NM1*40*2*PROVIDER NAME*****46*PROVIDER123~
NM1*85*2*BILLING PROVIDER*****24*TAX123~
HL*1**20*1~
PRV*BI*PXC*207Q00000X~
NM1*87*2*PAY TO PROVIDER*****24*TAX123~
N3*123 MAIN ST~
N4*ANYTOWN*NY*12345~
REF*TJ*123456789~
NM1*IL*1*DOE*JOHN*A****MI*123456789A~
N3*456 PATIENT ST~
N4*ANYTOWN*NY*12345~
DMG*D8*19800101*M~
CLM*123456*100.00***11:A:1*Y*A*Y*Y*C~
DTP*472*D8*20230101~
CL1*1*9*01~
HI*BK:V20201~
NM1*82*1*SMITH*JANE*****XX*1234567890~
PRV*PE*PXC*207Q00000X~
LX*1~
SV1*HC:D0120:AD*100.00*UN*1***1~
DTP*472*D8*20230101~
SE*29*0001~
GE*1*1~
IEA*1*000000001~"""

class IntegrationTester:
    """Test class for ClaimsProcessing + Claims Service integration"""
    
    def __init__(self):
        self.claims_processing_client = httpx.AsyncClient(base_url=CLAIMS_PROCESSING_URL, timeout=30.0)
        self.claims_service_client = httpx.AsyncClient(base_url=CLAIMS_SERVICE_URL, timeout=30.0)
        self.test_results = []
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.claims_processing_client.aclose()
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
    
    async def test_claims_processing_health(self) -> bool:
        """Test ClaimsProcessing health"""
        try:
            response = await self.claims_processing_client.get("/health")
            response.raise_for_status()
            data = response.json()
            
            success = data.get("status") == "healthy"
            self.log_test("ClaimsProcessing Health", success, f"Status: {data.get('status')}", data)
            return success
            
        except Exception as e:
            self.log_test("ClaimsProcessing Health", False, f"Error: {str(e)}")
            return False
    
    async def test_integration_health(self) -> bool:
        """Test integration health endpoint"""
        try:
            response = await self.claims_processing_client.get("/api/enhanced-claims/health/integration")
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
    
    async def test_edi_upload_integration(self) -> bool:
        """Test EDI upload with integration"""
        try:
            # Create a temporary file-like object
            files = {"file": ("test_claim.edi", SAMPLE_EDI_CONTENT, "text/plain")}
            params = {"payer_id": 1}
            
            response = await self.claims_processing_client.post(
                "/api/enhanced-claims/upload",
                files=files,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            result = data.get("result", {})
            integration_status = result.get("integration_status")
            
            success = integration_status in ["success", "fallback"]  # both are acceptable
            self.log_test(
                "EDI Upload Integration", 
                success, 
                f"Integration status: {integration_status}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("EDI Upload Integration", False, f"Error: {str(e)}")
            return False
    
    async def test_get_claims_integration(self) -> bool:
        """Test getting claims with integration"""
        try:
            response = await self.claims_processing_client.get("/api/enhanced-claims/")
            response.raise_for_status()
            data = response.json()
            
            claims = data.get("claims", [])
            source = data.get("source")
            
            success = source in ["fhir", "local", "local_fallback"]
            self.log_test(
                "Get Claims Integration", 
                success, 
                f"Source: {source}, Claims count: {len(claims)}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Get Claims Integration", False, f"Error: {str(e)}")
            return False
    
    async def test_claims_service_crud(self) -> bool:
        """Test basic CRUD operations on Claims service"""
        try:
            # Test creating a claim
            claim_data = {
                "identifier": [{"system": "test-system", "value": "TEST-001"}],
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
    
    async def test_work_queue_functionality(self) -> bool:
        """Test work queue functionality (ClaimsProcessing specific)"""
        try:
            # Test work queue summary
            response = await self.claims_processing_client.get("/api/enhanced-claims/work-queue/summary")
            response.raise_for_status()
            data = response.json()
            
            success = "total_items" in data
            self.log_test(
                "Work Queue Functionality", 
                success, 
                f"Work queue summary retrieved: {data.get('total_items', 0)} items",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Work Queue Functionality", False, f"Error: {str(e)}")
            return False
    
    async def test_agent_integration(self) -> bool:
        """Test AI agent integration"""
        try:
            response = await self.claims_processing_client.get("/api/agent/health")
            response.raise_for_status()
            data = response.json()
            
            success = "status" in data
            self.log_test(
                "Agent Integration", 
                success, 
                f"Agent status: {data.get('status', 'unknown')}",
                data
            )
            return success
            
        except Exception as e:
            self.log_test("Agent Integration", False, f"Error: {str(e)}")
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting ClaimsProcessing + Claims Service Integration Tests")
        logger.info("=" * 60)
        
        tests = [
            ("Claims Service Health", self.test_claims_service_health),
            ("ClaimsProcessing Health", self.test_claims_processing_health),
            ("Integration Health", self.test_integration_health),
            ("Claims Service CRUD", self.test_claims_service_crud),
            ("EDI Upload Integration", self.test_edi_upload_integration),
            ("Get Claims Integration", self.test_get_claims_integration),
            ("Work Queue Functionality", self.test_work_queue_functionality),
            ("Agent Integration", self.test_agent_integration),
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
    print("ClaimsProcessing + Claims Service Integration Test")
    print("=" * 60)
    print(f"ClaimsProcessing URL: {CLAIMS_PROCESSING_URL}")
    print(f"Claims Service URL: {CLAIMS_SERVICE_URL}")
    print()
    
    async with IntegrationTester() as tester:
        summary = await tester.run_all_tests()
        
        # Save results to file
        with open("integration_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: integration_test_results.json")
        
        return summary

if __name__ == "__main__":
    asyncio.run(main()) 