#!/usr/bin/env python3
"""
Comprehensive test script for the Activity Log System
Tests all major functionality including API endpoints and data flow
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3001"
HEADERS = {"Authorization": "Bearer mock-token", "Content-Type": "application/json"}

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_api_documentation():
    """Test API documentation accessibility"""
    print("🔍 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
            return True
        else:
            print(f"❌ API documentation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API documentation error: {e}")
        return False

def test_get_activity_events():
    """Test getting activity events"""
    print("🔍 Testing get activity events...")
    try:
        response = requests.get(f"{BASE_URL}/api/activity-events", headers=HEADERS)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Retrieved {len(events)} activity events")
            return True
        else:
            print(f"❌ Get activity events failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get activity events error: {e}")
        return False

def test_create_activity_event():
    """Test creating an activity event"""
    print("🔍 Testing create activity event...")
    try:
        event_data = {
            "event_type": "test_event",
            "event_category": "test",
            "event_description": "Test event from automated test",
            "ip_address": "127.0.0.1"
        }
        response = requests.post(f"{BASE_URL}/api/activity-events", 
                               headers=HEADERS, 
                               json=event_data)
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Created activity event: {event['id']}")
            return True
        else:
            print(f"❌ Create activity event failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Create activity event error: {e}")
        return False

def test_sign_in_event():
    """Test sign-in event endpoint"""
    print("🔍 Testing sign-in event...")
    try:
        response = requests.post(f"{BASE_URL}/api/events/sign-in?success=true", 
                               headers=HEADERS)
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Created sign-in event: {event['id']}")
            return True
        else:
            print(f"❌ Sign-in event failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Sign-in event error: {e}")
        return False

def test_hipaa_audit_event():
    """Test HIPAA audit event endpoint"""
    print("🔍 Testing HIPAA audit event...")
    try:
        response = requests.post(f"{BASE_URL}/api/events/hipaa-audit?action=viewed&resource=test%20records&client_id=client-1", 
                               headers=HEADERS)
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Created HIPAA audit event: {event['id']}")
            return True
        else:
            print(f"❌ HIPAA audit event failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HIPAA audit event error: {e}")
        return False

def test_get_clients():
    """Test getting clients"""
    print("🔍 Testing get clients...")
    try:
        response = requests.get(f"{BASE_URL}/api/clients", headers=HEADERS)
        if response.status_code == 200:
            clients = response.json()
            print(f"✅ Retrieved {len(clients)} clients")
            return True
        else:
            print(f"❌ Get clients failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get clients error: {e}")
        return False

def test_frontend_accessibility():
    """Test frontend accessibility"""
    print("🔍 Testing frontend accessibility...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def test_database_connection():
    """Test database connection through API"""
    print("🔍 Testing database connection...")
    try:
        # Try to get events which requires database access
        response = requests.get(f"{BASE_URL}/api/activity-events", headers=HEADERS)
        if response.status_code == 200:
            print("✅ Database connection working")
            return True
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Activity Log System Tests")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_api_documentation,
        test_database_connection,
        test_get_clients,
        test_get_activity_events,
        test_create_activity_event,
        test_sign_in_event,
        test_hipaa_audit_event,
        test_frontend_accessibility
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the system.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 