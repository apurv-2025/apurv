#!/usr/bin/env python3
"""
Test script for AI Agent Integration with InsuranceVerification
Tests the complete integration between InsuranceVerification and AI agent capabilities
"""

import asyncio
import httpx
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
INSURANCE_VERIFICATION_URL = "http://localhost:8000"
AGENTIC_CORE_PATH = "AIFoundation/AgenticFoundation/agentic-core"

class AgentIntegrationTest:
    """Test class for AI Agent integration with InsuranceVerification"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_user_id = "test-user-123"
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def test_service_health(self):
        """Test if InsuranceVerification service is running"""
        print("🏥 Testing Service Health...")
        
        try:
            # Test InsuranceVerification health
            response = await self.client.get(f"{INSURANCE_VERIFICATION_URL}/health")
            response.raise_for_status()
            print("✅ InsuranceVerification service is running")
            
            # Test AI agent health
            response = await self.client.get(f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/health")
            response.raise_for_status()
            health_data = response.json()
            print(f"✅ AI Agent health: {health_data['status']}")
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
        
        return True
    
    async def test_agent_chat(self):
        """Test AI agent chat functionality"""
        print("\n💬 Testing AI Agent Chat...")
        
        try:
            # Test chat with AI agent
            chat_data = {
                "message": "Can you help me verify insurance coverage?",
                "user_id": self.test_user_id,
                "context": {}
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/chat",
                json=chat_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Chat response received: {result.get('response', 'N/A')[:100]}...")
            
            # Test another chat message
            chat_data["message"] = "What tools do you have available?"
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/chat",
                json=chat_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Second chat response received: {result.get('response', 'N/A')[:100]}...")
            
        except Exception as e:
            print(f"❌ Chat test failed: {e}")
    
    async def test_insurance_verification(self):
        """Test insurance verification using AI agent"""
        print("\n🛡️ Testing Insurance Verification...")
        
        try:
            verification_data = {
                "member_id": "123456789",
                "provider_npi": "1234567890",
                "service_type": "30"
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/verify-insurance",
                json=verification_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Insurance verification completed:")
            print(f"   Member ID: {result.get('member_id', 'N/A')}")
            print(f"   Is Eligible: {result.get('is_eligible', 'N/A')}")
            print(f"   Coverage Details: {len(result.get('coverage_details', {}))} items")
            
        except Exception as e:
            print(f"❌ Insurance verification test failed: {e}")
    
    async def test_eligibility_check(self):
        """Test eligibility check using AI agent"""
        print("\n✅ Testing Eligibility Check...")
        
        try:
            eligibility_data = {
                "member_id": "123456789",
                "service_type": "30",
                "provider_npi": "1234567890"
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/check-eligibility",
                json=eligibility_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Eligibility check completed:")
            print(f"   Member ID: {result.get('member_id', 'N/A')}")
            print(f"   Service Type: {result.get('service_type', 'N/A')}")
            print(f"   Is Eligible: {result.get('is_eligible', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Eligibility check test failed: {e}")
    
    async def test_document_extraction(self):
        """Test document extraction using AI agent"""
        print("\n📄 Testing Document Extraction...")
        
        try:
            extraction_data = {
                "file_path": "/uploads/insurance_card.jpg",
                "file_type": "image"
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/extract-insurance-info",
                json=extraction_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Document extraction completed:")
            print(f"   File Path: {result.get('file_path', 'N/A')}")
            print(f"   Confidence Score: {result.get('confidence_score', 'N/A')}")
            print(f"   Extracted Info: {len(result.get('extracted_info', {}))} fields")
            
        except Exception as e:
            print(f"❌ Document extraction test failed: {e}")
    
    async def test_edi_analysis(self):
        """Test EDI analysis using AI agent"""
        print("\n📊 Testing EDI Analysis...")
        
        try:
            # Sample EDI 270 content
            edi_content = """ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *240115*1000*U*00401*000000001*0*P*>~GS*HS*SENDER*RECEIVER*20240115*1000*1*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20240115*1000~HL*1**20*1~NM1*PR*2*INSURANCE COMPANY*****PI*123456789~HL*2*1*21*1~NM1*1P*2*DR SMITH*****SV*1234567890~HL*3*2*22*0~TRN*1*123456789~NM1*IL*1*DOE*JOHN****MI*123456789~DMG*D8*19800101*M~DTP*291*D8*20240115~EQ*30~SE*13*0001~GE*1*1~IEA*1*000000001~"""
            
            edi_data = {
                "edi_content": edi_content,
                "transaction_type": "270"
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/analyze-edi",
                json=edi_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ EDI analysis completed:")
            print(f"   Transaction Type: {result.get('transaction_type', 'N/A')}")
            print(f"   Analysis: {len(result.get('analysis', {}))} items")
            print(f"   Validation: {result.get('validation', {}).get('is_valid', 'N/A')}")
            
        except Exception as e:
            print(f"❌ EDI analysis test failed: {e}")
    
    async def test_complex_verification(self):
        """Test complex verification with multiple service types"""
        print("\n🔄 Testing Complex Verification...")
        
        try:
            complex_data = {
                "member_id": "123456789",
                "provider_npi": "1234567890",
                "service_types": ["30", "35", "40"]
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/complex-verification",
                json=complex_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Complex verification completed:")
            print(f"   Member ID: {result.get('member_id', 'N/A')}")
            print(f"   Service Types: {len(result.get('verification_results', []))}")
            print(f"   Overall Eligible: {result.get('overall_eligible', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Complex verification test failed: {e}")
    
    async def test_available_tools(self):
        """Test getting available tools"""
        print("\n🛠️ Testing Available Tools...")
        
        try:
            response = await self.client.get(f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/tools")
            response.raise_for_status()
            tools = response.json()
            
            print(f"✅ Available tools retrieved: {len(tools)} tools")
            for tool in tools:
                print(f"   - {tool.get('name', 'N/A')}: {tool.get('description', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Available tools test failed: {e}")
    
    async def test_agent_metrics(self):
        """Test getting agent metrics"""
        print("\n📈 Testing Agent Metrics...")
        
        try:
            response = await self.client.get(f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/metrics")
            response.raise_for_status()
            metrics = response.json()
            
            print(f"✅ Agent metrics retrieved:")
            print(f"   Total Requests: {metrics.get('total_requests', 'N/A')}")
            print(f"   Successful Requests: {metrics.get('successful_requests', 'N/A')}")
            print(f"   Failed Requests: {metrics.get('failed_requests', 'N/A')}")
            print(f"   Average Response Time: {metrics.get('average_response_time', 'N/A')}s")
            
        except Exception as e:
            print(f"❌ Agent metrics test failed: {e}")
    
    async def test_batch_verification(self):
        """Test batch verification"""
        print("\n📦 Testing Batch Verification...")
        
        try:
            batch_data = [
                {
                    "member_id": "123456789",
                    "provider_npi": "1234567890",
                    "service_type": "30"
                },
                {
                    "member_id": "987654321",
                    "provider_npi": "0987654321",
                    "service_type": "35"
                }
            ]
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/batch-verification",
                json=batch_data
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Batch verification completed:")
            print(f"   Total Requests: {result.get('total_requests', 'N/A')}")
            print(f"   Successful Requests: {result.get('successful_requests', 'N/A')}")
            print(f"   Failed Requests: {result.get('failed_requests', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Batch verification test failed: {e}")
    
    async def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n⚠️ Testing Error Handling...")
        
        try:
            # Test with invalid data
            invalid_data = {
                "member_id": "",  # Empty member ID
                "provider_npi": "1234567890"
            }
            
            response = await self.client.post(
                f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/verify-insurance",
                json=invalid_data
            )
            
            if response.status_code == 400:
                print("✅ Invalid data handled correctly")
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
    
    async def test_performance(self):
        """Test performance with multiple concurrent requests"""
        print("\n⚡ Testing Performance...")
        
        try:
            start_time = time.time()
            
            # Make multiple concurrent requests
            tasks = []
            for i in range(5):
                task = self.client.get(f"{INSURANCE_VERIFICATION_URL}/api/v1/agent/health")
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            duration = end_time - start_time
            
            successful_requests = sum(1 for r in responses if not isinstance(r, Exception))
            
            print(f"✅ Performance test completed:")
            print(f"   Total requests: 5")
            print(f"   Successful requests: {successful_requests}")
            print(f"   Duration: {duration:.2f} seconds")
            print(f"   Avg response time: {duration/5:.2f} seconds per request")
            
        except Exception as e:
            print(f"❌ Performance test failed: {e}")
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting AI Agent Integration Tests for InsuranceVerification")
        print("=" * 70)
        
        # Check if service is running
        if not await self.test_service_health():
            print("❌ Service is not running. Please start the InsuranceVerification service.")
            return
        
        # Run all tests
        await self.test_agent_chat()
        await self.test_insurance_verification()
        await self.test_eligibility_check()
        await self.test_document_extraction()
        await self.test_edi_analysis()
        await self.test_complex_verification()
        await self.test_available_tools()
        await self.test_agent_metrics()
        await self.test_batch_verification()
        await self.test_error_handling()
        await self.test_performance()
        
        print("\n" + "=" * 70)
        print("✅ All AI Agent integration tests completed!")

async def main():
    """Main test function"""
    async with AgentIntegrationTest() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    print("AI Agent Integration Test Script for InsuranceVerification")
    print("Make sure the InsuranceVerification service is running!")
    print(f"InsuranceVerification URL: {INSURANCE_VERIFICATION_URL}")
    print(f"Agentic Core Location: {AGENTIC_CORE_PATH}")
    print()
    
    # Run the tests
    asyncio.run(main()) 