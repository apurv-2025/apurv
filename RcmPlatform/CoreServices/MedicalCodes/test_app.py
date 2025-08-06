#!/usr/bin/env python3
"""
Simple test script to verify the Medical Codes application is working
"""

import requests
import time
import sys

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Backend API...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Please start the backend server first.")
        return False
    
    # Test stats endpoint
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats endpoint working - Found {stats.get('total_cpt_codes', 0)} CPT codes")
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
        return False
    
    # Test search endpoint
    try:
        response = requests.get(f"{base_url}/api/search?query=office&limit=5")
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Search endpoint working - Found {results.get('total_results', 0)} results")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
        return False
    
    return True

def test_frontend():
    """Test the frontend application"""
    frontend_url = "http://localhost:3000"
    
    print("\nTesting Frontend...")
    
    try:
        response = requests.get(frontend_url)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running. Please start the frontend server first.")
        return False

def main():
    """Main test function"""
    print("Medical Codes Application Test")
    print("=" * 40)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 40)
    if backend_ok and frontend_ok:
        print("🎉 All tests passed! Application is working correctly.")
        print("\nAccess the application at:")
        print("- Frontend: http://localhost:3000")
        print("- Backend API: http://localhost:8000")
        print("- API Documentation: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 