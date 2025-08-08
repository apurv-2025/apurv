#!/usr/bin/env python3
"""
Integration Test Script for Scheduling2.0 with Patient and Practitioner Services
"""

import asyncio
import httpx
import json
from datetime import datetime

# Configuration
SCHEDULING_API_URL = "http://localhost:8000"
PATIENT_SERVICE_URL = "http://localhost:8001"
PRACTITIONER_SERVICE_URL = "http://localhost:8002"

async def test_health_checks():
    """Test health check endpoints"""
    print("🔍 Testing Health Checks...")
    
    async with httpx.AsyncClient() as client:
        # Test Scheduling2.0 health
        try:
            response = await client.get(f"{SCHEDULING_API_URL}/health")
            print(f"✅ Scheduling2.0 Health: {response.status_code}")
        except Exception as e:
            print(f"❌ Scheduling2.0 Health Failed: {e}")
        
        # Test Patient service health
        try:
            response = await client.get(f"{SCHEDULING_API_URL}/patients/health/check")
            print(f"✅ Patient Service Health: {response.status_code}")
        except Exception as e:
            print(f"❌ Patient Service Health Failed: {e}")
        
        # Test Practitioner service health
        try:
            response = await client.get(f"{SCHEDULING_API_URL}/practitioners/health/check")
            print(f"✅ Practitioner Service Health: {response.status_code}")
        except Exception as e:
            print(f"❌ Practitioner Service Health Failed: {e}")

async def test_patient_integration():
    """Test patient service integration"""
    print("\n👥 Testing Patient Integration...")
    
    async with httpx.AsyncClient() as client:
        # Create a test patient
        test_patient = {
            "fhir_id": f"test-patient-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "family_name": "TestPatient",
            "given_names": ["John", "Doe"],
            "gender": "male",
            "birth_date": "1990-01-01",
            "active": True
        }
        
        try:
            response = await client.post(
                f"{SCHEDULING_API_URL}/patients/",
                json=test_patient
            )
            if response.status_code == 200:
                patient_data = response.json()
                patient_id = patient_data.get("id")
                print(f"✅ Created Patient: {patient_data.get('fhir_id')}")
                
                # Test getting the patient
                response = await client.get(f"{SCHEDULING_API_URL}/patients/{patient_id}")
                if response.status_code == 200:
                    print(f"✅ Retrieved Patient: {response.json().get('fhir_id')}")
                
                # Test searching patients
                response = await client.get(f"{SCHEDULING_API_URL}/patients/search/name?family_name=TestPatient")
                if response.status_code == 200:
                    patients = response.json()
                    print(f"✅ Found {len(patients)} patients by search")
                
            else:
                print(f"❌ Failed to create patient: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Patient integration test failed: {e}")

async def test_practitioner_integration():
    """Test practitioner service integration"""
    print("\n👨‍⚕️ Testing Practitioner Integration...")
    
    async with httpx.AsyncClient() as client:
        # Create a test practitioner
        test_practitioner = {
            "fhir_id": f"test-practitioner-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "family_name": "TestDoctor",
            "given_names": ["Dr. Jane", "Smith"],
            "gender": "female",
            "birth_date": "1980-05-15",
            "active": True,
            "qualifications": [
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0360/2.7",
                                "code": "MD",
                                "display": "Doctor of Medicine"
                            }
                        ]
                    }
                }
            ]
        }
        
        try:
            response = await client.post(
                f"{SCHEDULING_API_URL}/practitioners/",
                json=test_practitioner
            )
            if response.status_code == 200:
                practitioner_data = response.json()
                practitioner_id = practitioner_data.get("id")
                print(f"✅ Created Practitioner: {practitioner_data.get('fhir_id')}")
                
                # Test getting the practitioner
                response = await client.get(f"{SCHEDULING_API_URL}/practitioners/{practitioner_id}")
                if response.status_code == 200:
                    print(f"✅ Retrieved Practitioner: {response.json().get('fhir_id')}")
                
                # Test searching practitioners
                response = await client.get(f"{SCHEDULING_API_URL}/practitioners/search/name?family_name=TestDoctor")
                if response.status_code == 200:
                    practitioners = response.json()
                    print(f"✅ Found {len(practitioners)} practitioners by search")
                
            else:
                print(f"❌ Failed to create practitioner: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Practitioner integration test failed: {e}")

async def test_calendar_integration():
    """Test calendar integration with practitioners"""
    print("\n📅 Testing Calendar Integration...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test getting practitioners for calendar
            response = await client.get(f"{SCHEDULING_API_URL}/practitioners/")
            if response.status_code == 200:
                practitioners = response.json()
                print(f"✅ Calendar found {len(practitioners)} practitioners")
                
                # Display practitioner details
                for practitioner in practitioners[:3]:  # Show first 3
                    print(f"   - {practitioner.get('name')} ({practitioner.get('specialty')})")
            else:
                print(f"❌ Failed to get practitioners for calendar: {response.status_code}")
        except Exception as e:
            print(f"❌ Calendar integration test failed: {e}")

async def test_list_endpoints():
    """Test list endpoints"""
    print("\n📋 Testing List Endpoints...")
    
    async with httpx.AsyncClient() as client:
        # Test patients list
        try:
            response = await client.get(f"{SCHEDULING_API_URL}/patients/?limit=5")
            if response.status_code == 200:
                patients = response.json()
                print(f"✅ Patients list: {len(patients)} patients")
            else:
                print(f"❌ Failed to get patients list: {response.status_code}")
        except Exception as e:
            print(f"❌ Patients list test failed: {e}")
        
        # Test practitioners list
        try:
            response = await client.get(f"{SCHEDULING_API_URL}/practitioners/?limit=5")
            if response.status_code == 200:
                practitioners = response.json()
                print(f"✅ Practitioners list: {len(practitioners)} practitioners")
            else:
                print(f"❌ Failed to get practitioners list: {response.status_code}")
        except Exception as e:
            print(f"❌ Practitioners list test failed: {e}")

async def main():
    """Main test function"""
    print("🚀 Starting Scheduling2.0 Integration Tests")
    print("=" * 50)
    
    # Wait a bit for services to be ready
    print("⏳ Waiting for services to be ready...")
    await asyncio.sleep(5)
    
    # Run tests
    await test_health_checks()
    await test_patient_integration()
    await test_practitioner_integration()
    await test_calendar_integration()
    await test_list_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Integration tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 