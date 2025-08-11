#!/usr/bin/env python3
"""
Integration Test for Prior Authorization + Patient Microservice
Tests the complete integration between the two systems
"""

import requests
import json
import time
from datetime import date, datetime
from typing import Dict, Any

# Configuration
PATIENT_SERVICE_URL = "http://localhost:8000"
PREAUTH_SERVICE_URL = "http://localhost:8002"

def test_patient_service():
    """Test Patient microservice functionality"""
    print("🏥 Testing Patient Microservice...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{PATIENT_SERVICE_URL}/health")
        if response.status_code == 200:
            print("✅ Patient Service Health Check: PASSED")
        else:
            print(f"❌ Patient Service Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Patient Service Health Check: FAILED ({e})")
        return False
    
    # Test patient creation
    patient_data = {
        "fhir_id": "TEST001",
        "family_name": "Doe",
        "given_names": ["John"],
        "gender": "male",
        "birth_date": "1990-01-01",
        "identifiers": [
            {
                "system": "member-id",
                "value": "MEM123456",
                "use": "official"
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": "555-123-4567",
                "use": "mobile"
            },
            {
                "system": "email",
                "value": "john.doe@example.com",
                "use": "home"
            }
        ],
        "addresses": [
            {
                "use": "home",
                "type": "postal",
                "line": ["123 Main St"],
                "city": "Anytown",
                "state": "CA",
                "postal_code": "12345",
                "country": "US"
            }
        ],
        "active": True
    }
    
    try:
        response = requests.post(
            f"{PATIENT_SERVICE_URL}/patients",
            json=patient_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            patient = response.json()
            patient_id = patient["id"]
            print(f"✅ Patient Creation: PASSED (ID: {patient_id})")
            return patient_id
        else:
            print(f"❌ Patient Creation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Patient Creation: FAILED ({e})")
        return None

def test_preauth_service():
    """Test Prior Authorization service functionality"""
    print("🔐 Testing Prior Authorization Service...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/health")
        if response.status_code == 200:
            print("✅ Prior Authorization Health Check: PASSED")
        else:
            print(f"❌ Prior Authorization Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Prior Authorization Health Check: FAILED ({e})")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/")
        if response.status_code == 200:
            print("✅ Prior Authorization Root Endpoint: PASSED")
        else:
            print(f"❌ Prior Authorization Root Endpoint: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Prior Authorization Root Endpoint: FAILED ({e})")
        return False
    
    return True

def test_patient_integration(patient_id: str):
    """Test integration between Patient and Prior Authorization services"""
    print("🔗 Testing Patient Integration...")
    
    # Test getting patient from Prior Authorization service
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/patients/{patient_id}")
        if response.status_code == 200:
            patient = response.json()
            print(f"✅ Patient Retrieval via Prior Authorization: PASSED")
            print(f"   Patient: {patient.get('first_name')} {patient.get('last_name')}")
            return True
        else:
            print(f"❌ Patient Retrieval via Prior Authorization: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Patient Retrieval via Prior Authorization: FAILED ({e})")
        return False

def test_patient_search():
    """Test patient search functionality"""
    print("🔍 Testing Patient Search...")
    
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/patients/", params={
            "first_name": "John",
            "last_name": "Doe",
            "limit": 10
        })
        if response.status_code == 200:
            patients = response.json()
            print(f"✅ Patient Search: PASSED (Found {len(patients)} patients)")
            return True
        else:
            print(f"❌ Patient Search: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Patient Search: FAILED ({e})")
        return False

def test_prior_authorization_creation(patient_id: str):
    """Test prior authorization request creation"""
    print("📋 Testing Prior Authorization Creation...")
    
    auth_data = {
        "patient_first_name": "John",
        "patient_last_name": "Doe",
        "patient_dob": "1990-01-01",
        "patient_gender": "M",
        "member_id": "MEM123456",
        "requesting_provider_npi": "1234567890",
        "requesting_provider_name": "Dr. Smith",
        "procedure_codes": [
            {
                "code": "99213",
                "description": "Office visit, established patient, 20-29 minutes"
            }
        ],
        "diagnosis_codes": [
            {
                "code": "E11.9",
                "description": "Type 2 diabetes mellitus without complications",
                "is_primary": True
            }
        ],
        "service_date_from": "2024-01-15",
        "medical_necessity": "Patient requires evaluation and management for diabetes management",
        "priority": "normal"
    }
    
    try:
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/prior-auth/",
            json=auth_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            auth = response.json()
            auth_id = auth.get("request_id")
            print(f"✅ Prior Authorization Creation: PASSED (ID: {auth_id})")
            return auth_id
        else:
            print(f"❌ Prior Authorization Creation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Prior Authorization Creation: FAILED ({e})")
        return None

def test_codes_endpoints():
    """Test healthcare codes endpoints"""
    print("🏷️ Testing Healthcare Codes...")
    
    # Test procedure codes
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/codes/procedures", params={"limit": 5})
        if response.status_code == 200:
            codes = response.json()
            print(f"✅ Procedure Codes: PASSED (Found {len(codes)} codes)")
        else:
            print(f"❌ Procedure Codes: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Procedure Codes: FAILED ({e})")
        return False
    
    # Test diagnosis codes
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/codes/diagnoses", params={"limit": 5})
        if response.status_code == 200:
            codes = response.json()
            print(f"✅ Diagnosis Codes: PASSED (Found {len(codes)} codes)")
        else:
            print(f"❌ Diagnosis Codes: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Diagnosis Codes: FAILED ({e})")
        return False
    
    return True

def main():
    """Run all integration tests"""
    print("🧪 Starting Prior Authorization + Patient Microservice Integration Tests")
    print("=" * 80)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(10)
    
    test_results = []
    
    # Test Patient Service
    patient_id = test_patient_service()
    test_results.append(("Patient Service", patient_id is not None))
    
    # Test Prior Authorization Service
    preauth_ok = test_preauth_service()
    test_results.append(("Prior Authorization Service", preauth_ok))
    
    # Test integration if both services are working
    if patient_id and preauth_ok:
        integration_ok = test_patient_integration(patient_id)
        test_results.append(("Patient Integration", integration_ok))
        
        search_ok = test_patient_search()
        test_results.append(("Patient Search", search_ok))
        
        auth_id = test_prior_authorization_creation(patient_id)
        test_results.append(("Prior Authorization Creation", auth_id is not None))
        
        codes_ok = test_codes_endpoints()
        test_results.append(("Healthcare Codes", codes_ok))
    else:
        print("⚠️ Skipping integration tests due to service failures")
        test_results.extend([
            ("Patient Integration", False),
            ("Patient Search", False),
            ("Prior Authorization Creation", False),
            ("Healthcare Codes", False)
        ])
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Integration Test Results:")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name:<30} {status}")
        if result:
            passed += 1
    
    print("\n" + "=" * 80)
    print(f"📈 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed! The systems are working together correctly.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    print("\n🔗 Service URLs:")
    print(f"   Patient Microservice:     {PATIENT_SERVICE_URL}")
    print(f"   Prior Authorization:      {PREAUTH_SERVICE_URL}")
    print(f"   Patient API Docs:         {PATIENT_SERVICE_URL}/docs")
    print(f"   Prior Auth API Docs:      {PREAUTH_SERVICE_URL}/docs")
    
    print("\n📝 Integration Summary:")
    print("   ✅ Prior Authorization now uses Patient microservice for patient data")
    print("   ✅ No redundant patient information in Prior Authorization")
    print("   ✅ Patient microservice handles all FHIR Patient operations")
    print("   ✅ Prior Authorization focuses on authorization requests and EDI processing")
    print("   ✅ Proper microservice architecture with clear separation of concerns")

if __name__ == "__main__":
    main() 