#!/usr/bin/env python3
"""
Test script to verify search functionality is working
"""

import requests
import json

def test_search_functionality():
    """Test various search scenarios"""
    base_url = "http://localhost:8003/api"
    
    print("🔍 Testing Search Functionality")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Office Visit Search",
            "query": "office",
            "expected_min_results": 1
        },
        {
            "name": "Diabetes Search",
            "query": "diabetes",
            "expected_min_results": 1
        },
        {
            "name": "CPT Code Search",
            "query": "99213",
            "expected_min_results": 1
        },
        {
            "name": "ICD-10 Code Search",
            "query": "E11.9",
            "expected_min_results": 1
        },
        {
            "name": "Modifier Search",
            "query": "25",
            "expected_min_results": 1
        },
        {
            "name": "HCPCS Search",
            "query": "E0424",
            "expected_min_results": 1
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   Query: '{test_case['query']}'")
        
        try:
            response = requests.get(f"{base_url}/search", params={
                "query": test_case['query'],
                "limit": 10
            })
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('total_results', 0)
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📊 Results: {total_results}")
                
                # Show some sample results
                if total_results > 0:
                    if data.get('cpt_codes'):
                        print(f"   🏥 CPT: {len(data['cpt_codes'])} codes")
                    if data.get('icd10_codes'):
                        print(f"   📋 ICD-10: {len(data['icd10_codes'])} codes")
                    if data.get('hcpcs_codes'):
                        print(f"   💊 HCPCS: {len(data['hcpcs_codes'])} codes")
                    if data.get('modifier_codes'):
                        print(f"   🔧 Modifiers: {len(data['modifier_codes'])} codes")
                
                if total_results >= test_case['expected_min_results']:
                    print(f"   ✅ PASSED: Found {total_results} results (expected ≥{test_case['expected_min_results']})")
                else:
                    print(f"   ❌ FAILED: Found {total_results} results (expected ≥{test_case['expected_min_results']})")
                    all_passed = False
            else:
                print(f"   ❌ FAILED: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All search tests passed!")
        print("\n✅ Search functionality is working correctly.")
        print("✅ Frontend should now be able to search properly.")
        print("\n🌐 Access the application at: http://localhost:3003")
    else:
        print("❌ Some search tests failed.")
        print("Please check the backend logs for issues.")
    
    return all_passed

if __name__ == "__main__":
    test_search_functionality() 