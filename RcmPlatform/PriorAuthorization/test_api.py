#!/usr/bin/env python3
"""
Test script for Prior Authorization API
"""

import requests
import json
import time
from datetime import date, datetime

BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_patients_endpoint():
    """Test patients endpoint"""
    print("🔍 Testing patients endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/patients/")
        if response.status_code == 200:
            print("✅ Patients endpoint passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Patients endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Patients endpoint failed: {e}")
        return False

def test_prior_auth_endpoint():
    """Test prior authorization endpoint"""
    print("🔍 Testing prior authorization endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/prior-auth/")
        if response.status_code == 200:
            print("✅ Prior authorization endpoint passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Prior authorization endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Prior authorization endpoint failed: {e}")
        return False

def test_codes_endpoint():
    """Test codes endpoint"""
    print("🔍 Testing codes endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/codes/procedures")
        if response.status_code == 200:
            print("✅ Codes endpoint passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Codes endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Codes endpoint failed: {e}")
        return False

def test_create_patient():
    """Test creating a patient"""
    print("🔍 Testing patient creation...")
    
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "M",
        "address_line1": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "phone_mobile": "555-123-4567",
        "email": "john.doe@example.com",
        "primary_insurance": {
            "carrier_name": "Blue Cross Blue Shield",
            "policy_number": "POL123456",
            "group_number": "GRP789",
            "effective_date": "2024-01-01"
        },
        "member_id_primary": "MEM123456",
        "emergency_contact": {
            "name": "Jane Doe",
            "phone": "555-987-6543",
            "relationship": "Spouse"
        },
        "hipaa_authorization": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/patients/",
            json=patient_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("✅ Patient creation passed")
            patient = response.json()
            print(f"   Created patient ID: {patient.get('patient_id')}")
            return patient.get('patient_id')
        else:
            print(f"❌ Patient creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Patient creation failed: {e}")
        return None

def test_create_prior_auth(patient_id):
    """Test creating a prior authorization request"""
    print("🔍 Testing prior authorization creation...")
    
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
            f"{BASE_URL}/api/v1/prior-auth/",
            json=auth_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("✅ Prior authorization creation passed")
            auth = response.json()
            print(f"   Created request ID: {auth.get('request_id')}")
            return auth.get('request_id')
        else:
            print(f"❌ Prior authorization creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Prior authorization creation failed: {e}")
        return None

def main():
    """Run all tests"""
    print("🧪 Starting Prior Authorization API Tests")
    print("=" * 50)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    tests = [
        test_health,
        test_root,
        test_patients_endpoint,
        test_prior_auth_endpoint,
        test_codes_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Test data creation
    print("📝 Testing data creation...")
    patient_id = test_create_patient()
    if patient_id:
        passed += 1
        print()
        
        request_id = test_create_prior_auth(patient_id)
        if request_id:
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total + 2} tests passed")
    
    if passed == total + 2:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    print("\n🔗 API Documentation: http://localhost:8002/docs")
    print("🌐 Frontend: http://localhost:3002")

if __name__ == "__main__":
    main() 