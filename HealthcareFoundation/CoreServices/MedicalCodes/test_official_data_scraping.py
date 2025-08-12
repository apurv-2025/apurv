#!/usr/bin/env python3
"""
Test script for official data scraping functionality
Demonstrates fetching data from the three official medical coding sources
"""

import requests
import json
import time
from datetime import datetime

def test_official_data_scraping():
    """Test the official data scraping functionality"""
    
    base_url = "http://localhost:8003"
    
    print("🔍 Testing Official Data Scraping Functionality")
    print("=" * 60)
    print()
    
    # Test 1: Check sync service health
    print("1️⃣ Testing Data Sync Service Health...")
    try:
        response = requests.get(f"{base_url}/api/sync/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   📊 Sources status:")
            for source, status in health_data['sources_status'].items():
                print(f"      - {source}: {status}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    print()
    
    # Test 2: Get official sources information
    print("2️⃣ Getting Official Sources Information...")
    try:
        response = requests.get(f"{base_url}/api/sync/sources")
        if response.status_code == 200:
            sources_data = response.json()
            print(f"   ✅ Found {sources_data['total_sources']} official sources:")
            for key, source in sources_data['sources'].items():
                print(f"      - {source['name']} ({source['type']})")
                print(f"        URL: {source['url']}")
                print(f"        Maintainer: {source['maintainer']}")
                print()
        else:
            print(f"   ❌ Failed to get sources: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Sources error: {e}")
    
    print()
    
    # Test 3: Test individual scraping endpoints
    print("3️⃣ Testing Individual Scraping Endpoints...")
    
    # Test CPT scraping
    print("   🏥 Testing CPT Code Scraping...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-cpt")
        if response.status_code == 200:
            cpt_data = response.json()
            print(f"      ✅ CPT scraping: {cpt_data['message']}")
            print(f"      📊 Codes found: {cpt_data['cpt_codes_count']}")
        else:
            print(f"      ❌ CPT scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ CPT scraping error: {e}")
    
    # Test ICD-10 scraping
    print("   📋 Testing ICD-10 Code Scraping...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-icd10")
        if response.status_code == 200:
            icd10_data = response.json()
            print(f"      ✅ ICD-10 scraping: {icd10_data['message']}")
            print(f"      📊 Codes found: {icd10_data['icd10_codes_count']}")
        else:
            print(f"      ❌ ICD-10 scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ ICD-10 scraping error: {e}")
    
    # Test HCPCS scraping
    print("   💊 Testing HCPCS Code Scraping...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-hcpcs")
        if response.status_code == 200:
            hcpcs_data = response.json()
            print(f"      ✅ HCPCS scraping: {hcpcs_data['message']}")
            print(f"      📊 Codes found: {hcpcs_data['hcpcs_codes_count']}")
        else:
            print(f"      ❌ HCPCS scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ HCPCS scraping error: {e}")
    
    print()
    
    # Test 4: Test comprehensive scraping
    print("4️⃣ Testing Comprehensive Data Scraping...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape")
        if response.status_code == 200:
            scrape_data = response.json()
            print(f"   ✅ Comprehensive scraping: {scrape_data['message']}")
            print(f"   📊 Total codes scraped: {scrape_data['total_codes']}")
            print(f"   📁 Data saved to: {scrape_data['filename']}")
            print(f"   📈 Breakdown:")
            print(f"      - CPT codes: {scrape_data['cpt_codes_count']}")
            print(f"      - ICD-10 codes: {scrape_data['icd10_codes_count']}")
            print(f"      - HCPCS codes: {scrape_data['hcpcs_codes_count']}")
        else:
            print(f"   ❌ Comprehensive scraping failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Comprehensive scraping error: {e}")
    
    print()
    
    # Test 5: Test sync status
    print("5️⃣ Testing Sync Status...")
    try:
        response = requests.get(f"{base_url}/api/sync/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Sync status: {status_data['status']}")
            print(f"   📅 Last sync: {status_data['last_sync']}")
            print(f"   💬 Message: {status_data['message']}")
        else:
            print(f"   ❌ Sync status failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Sync status error: {e}")
    
    print()
    print("=" * 60)
    print("🎉 Official Data Scraping Test Completed!")
    print()
    print("📚 Official Sources Tested:")
    print("   - AMA CPT: https://www.ama-assn.org/practice-management/cpt")
    print("   - CMS ICD-10: https://www.cms.gov/medicare/coding-billing/icd-10-codes")
    print("   - CMS HCPCS: https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system")
    print()
    print("🔗 API Documentation: http://localhost:8003/docs")
    print("🌐 Frontend Application: http://localhost:3003")

if __name__ == "__main__":
    test_official_data_scraping() 