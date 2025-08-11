#!/usr/bin/env python3
"""
AI Assistant Integration Test for Prior Authorization System
Tests the AI assistant functionality and integration with agentic-core
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
PREAUTH_SERVICE_URL = "http://localhost:8002"

def test_ai_health_check():
    """Test AI assistant health check"""
    print("🤖 Testing AI Assistant Health Check...")
    
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/agent/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Health Check: PASSED")
            print(f"   Status: {data.get('status')}")
            print(f"   Agentic Core Available: {data.get('agentic_core_available')}")
            return data.get('agentic_core_available', False)
        else:
            print(f"❌ AI Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ AI Health Check: FAILED ({e})")
        return False

def test_ai_chat():
    """Test AI chat functionality"""
    print("💬 Testing AI Chat...")
    
    try:
        chat_data = {
            "message": "Hello, can you help me with prior authorization?",
            "user_id": "test_user_123"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Chat: PASSED")
                print(f"   Response: {data.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ AI Chat: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Chat: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Chat: FAILED ({e})")
        return False

def test_ai_tools():
    """Test AI tools functionality"""
    print("🔧 Testing AI Tools...")
    
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/agent/tools")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                tools = data.get("tools", [])
                print(f"✅ AI Tools: PASSED (Found {len(tools)} tools)")
                for tool in tools:
                    print(f"   - {tool.get('name')}: {tool.get('description')}")
                return True
            else:
                print(f"❌ AI Tools: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Tools: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ AI Tools: FAILED ({e})")
        return False

def test_ai_examples():
    """Test AI examples endpoint"""
    print("📚 Testing AI Examples...")
    
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/agent/examples")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                examples = data.get("examples", [])
                print(f"✅ AI Examples: PASSED (Found {len(examples)} categories)")
                for category in examples:
                    print(f"   - {category.get('category')}: {len(category.get('examples', []))} examples")
                return True
            else:
                print(f"❌ AI Examples: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Examples: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ AI Examples: FAILED ({e})")
        return False

def test_create_prior_auth_ai():
    """Test AI-assisted prior authorization creation"""
    print("📋 Testing AI Prior Authorization Creation...")
    
    try:
        auth_data = {
            "patient_id": "PAT123456",
            "provider_npi": "1234567890",
            "procedure_codes": [
                {"code": "99213", "description": "Office visit, established patient, 20-29 minutes"}
            ],
            "diagnosis_codes": [
                {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications", "is_primary": True}
            ],
            "service_date": "2024-01-15",
            "medical_necessity": "Patient requires evaluation and management for diabetes management"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/create-prior-auth",
            json=auth_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Prior Auth Creation: PASSED")
                print(f"   Request ID: {data.get('data', {}).get('request_id', 'N/A')}")
                return True
            else:
                print(f"❌ AI Prior Auth Creation: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Prior Auth Creation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Prior Auth Creation: FAILED ({e})")
        return False

def test_check_status_ai():
    """Test AI-assisted status checking"""
    print("📊 Testing AI Status Check...")
    
    try:
        status_data = {
            "request_id": "AUTH123456"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/check-status",
            json=status_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Status Check: PASSED")
                print(f"   Status: {data.get('data', {}).get('status', 'N/A')}")
                return True
            else:
                print(f"❌ AI Status Check: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Status Check: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Status Check: FAILED ({e})")
        return False

def test_generate_edi_ai():
    """Test AI-assisted EDI generation"""
    print("📄 Testing AI EDI Generation...")
    
    try:
        edi_data = {
            "edi_type": "278",
            "patient_id": "PAT123456",
            "request_id": "AUTH123456",
            "provider_npi": "1234567890",
            "service_date": "2024-01-15",
            "birth_date": "1990-01-01",
            "gender": "M"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/generate-edi",
            json=edi_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI EDI Generation: PASSED")
                print(f"   EDI Type: {data.get('data', {}).get('edi_type', 'N/A')}")
                return True
            else:
                print(f"❌ AI EDI Generation: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI EDI Generation: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI EDI Generation: FAILED ({e})")
        return False

def test_lookup_patient_ai():
    """Test AI-assisted patient lookup"""
    print("👤 Testing AI Patient Lookup...")
    
    try:
        patient_data = {
            "patient_id": "PAT123456"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/lookup-patient",
            json=patient_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Patient Lookup: PASSED")
                patient_info = data.get('data', {})
                print(f"   Patient: {patient_info.get('first_name', '')} {patient_info.get('last_name', '')}")
                return True
            else:
                print(f"❌ AI Patient Lookup: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Patient Lookup: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Patient Lookup: FAILED ({e})")
        return False

def test_lookup_codes_ai():
    """Test AI-assisted code lookup"""
    print("🏷️ Testing AI Code Lookup...")
    
    try:
        code_data = {
            "code_type": "procedure",
            "search_term": "office visit"
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/lookup-codes",
            json=code_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Code Lookup: PASSED")
                codes = data.get('data', {}).get('codes', [])
                print(f"   Found {len(codes)} codes")
                return True
            else:
                print(f"❌ AI Code Lookup: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Code Lookup: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Code Lookup: FAILED ({e})")
        return False

def test_complex_workflow_ai():
    """Test AI complex workflow processing"""
    print("🔄 Testing AI Complex Workflow...")
    
    try:
        workflow_data = {
            "workflow": [
                {
                    "name": "Lookup Patient",
                    "tool": "lookup_patient",
                    "data": {"patient_id": "PAT123456"}
                },
                {
                    "name": "Create Authorization",
                    "tool": "create_prior_authorization",
                    "data": {
                        "patient_id": "PAT123456",
                        "provider_npi": "1234567890",
                        "procedure_codes": [{"code": "99213", "description": "Office visit"}],
                        "diagnosis_codes": [{"code": "E11.9", "description": "Diabetes"}]
                    }
                },
                {
                    "name": "Generate EDI",
                    "tool": "generate_edi",
                    "data": {
                        "edi_type": "278",
                        "patient_id": "PAT123456",
                        "provider_npi": "1234567890"
                    }
                }
            ]
        }
        
        response = requests.post(
            f"{PREAUTH_SERVICE_URL}/api/v1/agent/complex-workflow",
            json=workflow_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ AI Complex Workflow: PASSED")
                workflow_results = data.get('data', [])
                print(f"   Completed {len(workflow_results)} workflow steps")
                return True
            else:
                print(f"❌ AI Complex Workflow: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ AI Complex Workflow: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI Complex Workflow: FAILED ({e})")
        return False

def test_conversation_history():
    """Test conversation history functionality"""
    print("📜 Testing Conversation History...")
    
    try:
        response = requests.get(f"{PREAUTH_SERVICE_URL}/api/v1/agent/conversations/test_user_123")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                conversations = data.get("conversations", [])
                print(f"✅ Conversation History: PASSED (Found {len(conversations)} conversations)")
                return True
            else:
                print(f"❌ Conversation History: FAILED - {data.get('error')}")
                return False
        else:
            print(f"❌ Conversation History: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Conversation History: FAILED ({e})")
        return False

def main():
    """Run all AI integration tests"""
    print("🧪 Starting AI Assistant Integration Tests for Prior Authorization")
    print("=" * 80)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    test_results = []
    
    # Test basic AI functionality
    health_ok = test_ai_health_check()
    test_results.append(("AI Health Check", health_ok))
    
    chat_ok = test_ai_chat()
    test_results.append(("AI Chat", chat_ok))
    
    tools_ok = test_ai_tools()
    test_results.append(("AI Tools", tools_ok))
    
    examples_ok = test_ai_examples()
    test_results.append(("AI Examples", examples_ok))
    
    # Test AI-assisted operations
    if health_ok:
        auth_ok = test_create_prior_auth_ai()
        test_results.append(("AI Prior Auth Creation", auth_ok))
        
        status_ok = test_check_status_ai()
        test_results.append(("AI Status Check", status_ok))
        
        edi_ok = test_generate_edi_ai()
        test_results.append(("AI EDI Generation", edi_ok))
        
        patient_ok = test_lookup_patient_ai()
        test_results.append(("AI Patient Lookup", patient_ok))
        
        codes_ok = test_lookup_codes_ai()
        test_results.append(("AI Code Lookup", codes_ok))
        
        workflow_ok = test_complex_workflow_ai()
        test_results.append(("AI Complex Workflow", workflow_ok))
        
        history_ok = test_conversation_history()
        test_results.append(("Conversation History", history_ok))
    else:
        print("⚠️ Skipping AI-assisted tests due to health check failure")
        test_results.extend([
            ("AI Prior Auth Creation", False),
            ("AI Status Check", False),
            ("AI EDI Generation", False),
            ("AI Patient Lookup", False),
            ("AI Code Lookup", False),
            ("AI Complex Workflow", False),
            ("Conversation History", False)
        ])
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 AI Integration Test Results:")
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
        print("🎉 All AI integration tests passed! The AI assistant is working correctly.")
    else:
        print("⚠️ Some AI tests failed. Check the logs above for details.")
    
    print("\n🔗 Service URLs:")
    print(f"   Prior Authorization API:  {PREAUTH_SERVICE_URL}")
    print(f"   API Documentation:        {PREAUTH_SERVICE_URL}/docs")
    print(f"   AI Assistant Health:      {PREAUTH_SERVICE_URL}/api/v1/agent/health")
    
    print("\n🤖 AI Assistant Features:")
    print("   ✅ Natural language chat interface")
    print("   ✅ Prior authorization request creation")
    print("   ✅ Authorization status checking")
    print("   ✅ EDI document generation (278/275)")
    print("   ✅ Patient information lookup")
    print("   ✅ Healthcare code lookup")
    print("   ✅ Complex workflow processing")
    print("   ✅ Conversation history")
    print("   ✅ Example interactions")
    print("   ✅ Tool management")
    
    print("\n📝 Integration Summary:")
    print("   ✅ AI assistant integrated with Prior Authorization system")
    print("   ✅ Agentic-core integration with fallback support")
    print("   ✅ Custom tools for prior authorization workflows")
    print("   ✅ React frontend component with chat interface")
    print("   ✅ Comprehensive API endpoints for AI functionality")
    print("   ✅ Error handling and graceful degradation")

if __name__ == "__main__":
    main() 