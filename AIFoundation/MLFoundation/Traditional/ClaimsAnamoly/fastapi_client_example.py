#!/usr/bin/env python3
"""
FastAPI Client Example for Claims Anomaly Detection System

This script demonstrates how to use the FastAPI endpoints.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("=== Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_example():
    """Test getting an example claim structure"""
    print("\n=== Get Example Claim ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/example")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()['example_claim']
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_single_claim_scoring(claim_data):
    """Test scoring a single claim"""
    print("\n=== Single Claim Scoring ===")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/score",
            json=claim_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_batch_claim_scoring(claims_data):
    """Test scoring multiple claims"""
    print("\n=== Batch Claim Scoring ===")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/score/batch",
            json={'claims': claims_data},
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Processed {result.get('count', 0)} claims")
        print(f"Sample Results: {json.dumps(result.get('results', [])[:2], indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_model_info():
    """Test getting model information"""
    print("\n=== Model Information ===")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/model/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_docs():
    """Test accessing API documentation"""
    print("\n=== API Documentation ===")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ API documentation is accessible at http://localhost:8000/docs")
            print("✅ ReDoc is available at http://localhost:8000/redoc")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Claims Anomaly Detection FastAPI Client Example")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Health check failed. Make sure the FastAPI server is running:")
        print("   python3 run_fastapi.py")
        return
    
    # Test 2: Get example claim
    example_claim = test_get_example()
    if not example_claim:
        print("❌ Failed to get example claim")
        return
    
    # Test 3: Score single claim
    test_single_claim_scoring(example_claim)
    
    # Test 4: Score suspicious claim
    suspicious_claim = example_claim.copy()
    suspicious_claim['claim_id'] = 'SUSPICIOUS_001'
    suspicious_claim['billed_amount'] = 1500.0  # Suspiciously high
    test_single_claim_scoring(suspicious_claim)
    
    # Test 5: Batch scoring
    batch_claims = [
        example_claim,
        suspicious_claim,
        {**example_claim, 'claim_id': 'BATCH_003', 'billed_amount': 300.0},
        {**example_claim, 'claim_id': 'BATCH_004', 'billed_amount': 50.0}
    ]
    test_batch_claim_scoring(batch_claims)
    
    # Test 6: Model info
    test_model_info()
    
    # Test 7: API documentation
    test_api_docs()
    
    print("\n✅ All FastAPI tests completed!")
    print("\n🌐 You can now visit:")
    print("   http://localhost:8000/docs     - Interactive API documentation")
    print("   http://localhost:8000/redoc    - Alternative documentation")

if __name__ == "__main__":
    main() 