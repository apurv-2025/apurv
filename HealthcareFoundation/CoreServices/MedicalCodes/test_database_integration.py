#!/usr/bin/env python3
"""
Test script for enhanced database integration functionality
Demonstrates scraping and saving data directly to the database
"""

import requests
import json
import time
from datetime import datetime

def test_database_integration():
    """Test the enhanced database integration functionality"""
    
    base_url = "http://localhost:8003"
    
    print("🗄️ Testing Enhanced Database Integration")
    print("=" * 60)
    print()
    
    # Test 1: Check current database stats
    print("1️⃣ Checking Current Database Statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   📊 Current database contents:")
            print(f"      - CPT codes: {stats.get('total_cpt_codes', 0)}")
            print(f"      - ICD-10 codes: {stats.get('total_icd10_codes', 0)}")
            print(f"      - HCPCS codes: {stats.get('total_hcpcs_codes', 0)}")
            print(f"      - Modifier codes: {stats.get('total_modifier_codes', 0)}")
        else:
            print(f"   ❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Stats error: {e}")
    
    print()
    
    # Test 2: Test enhanced scraping with database integration
    print("2️⃣ Testing Enhanced Scraping with Database Integration...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-to-database?save_to_db=true&save_to_file=true")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Enhanced scraping completed")
            print(f"   📊 Results:")
            print(f"      - Database saved: {result.get('database_saved', False)}")
            print(f"      - File saved: {result.get('file_saved', False)}")
            print(f"      - Filename: {result.get('filename', 'N/A')}")
            print(f"   📈 Database counts:")
            db_counts = result.get('database_counts', {})
            print(f"      - CPT codes saved: {db_counts.get('cpt', 0)}")
            print(f"      - ICD-10 codes saved: {db_counts.get('icd10', 0)}")
            print(f"      - HCPCS codes saved: {db_counts.get('hcpcs', 0)}")
            print(f"   📈 Scraped counts:")
            scraped_counts = result.get('scraped_counts', {})
            print(f"      - CPT codes scraped: {scraped_counts.get('cpt', 0)}")
            print(f"      - ICD-10 codes scraped: {scraped_counts.get('icd10', 0)}")
            print(f"      - HCPCS codes scraped: {scraped_counts.get('hcpcs', 0)}")
        else:
            print(f"   ❌ Enhanced scraping failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Enhanced scraping error: {e}")
    
    print()
    
    # Test 3: Test individual code type scraping to database
    print("3️⃣ Testing Individual Code Type Scraping to Database...")
    
    # Test CPT scraping to database
    print("   🏥 Testing CPT Scraping to Database...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-cpt-to-database")
        if response.status_code == 200:
            result = response.json()
            print(f"      ✅ CPT scraping: {result.get('message', 'Success')}")
            print(f"      📊 Scraped: {result.get('scraped_count', 0)}, Saved: {result.get('saved_count', 0)}")
        else:
            print(f"      ❌ CPT scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ CPT scraping error: {e}")
    
    # Test ICD-10 scraping to database
    print("   📋 Testing ICD-10 Scraping to Database...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-icd10-to-database")
        if response.status_code == 200:
            result = response.json()
            print(f"      ✅ ICD-10 scraping: {result.get('message', 'Success')}")
            print(f"      📊 Scraped: {result.get('scraped_count', 0)}, Saved: {result.get('saved_count', 0)}")
        else:
            print(f"      ❌ ICD-10 scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ ICD-10 scraping error: {e}")
    
    # Test HCPCS scraping to database
    print("   💊 Testing HCPCS Scraping to Database...")
    try:
        response = requests.post(f"{base_url}/api/sync/scrape-hcpcs-to-database")
        if response.status_code == 200:
            result = response.json()
            print(f"      ✅ HCPCS scraping: {result.get('message', 'Success')}")
            print(f"      📊 Scraped: {result.get('scraped_count', 0)}, Saved: {result.get('saved_count', 0)}")
        else:
            print(f"      ❌ HCPCS scraping failed: {response.status_code}")
    except Exception as e:
        print(f"      ❌ HCPCS scraping error: {e}")
    
    print()
    
    # Test 4: Check updated database stats
    print("4️⃣ Checking Updated Database Statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   📊 Updated database contents:")
            print(f"      - CPT codes: {stats.get('total_cpt_codes', 0)}")
            print(f"      - ICD-10 codes: {stats.get('total_icd10_codes', 0)}")
            print(f"      - HCPCS codes: {stats.get('total_hcpcs_codes', 0)}")
            print(f"      - Modifier codes: {stats.get('total_modifier_codes', 0)}")
        else:
            print(f"   ❌ Failed to get updated stats: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Updated stats error: {e}")
    
    print()
    
    # Test 5: Test search functionality with new data
    print("5️⃣ Testing Search Functionality with New Data...")
    try:
        # Test search for office visits
        response = requests.get(f"{base_url}/api/search?query=office")
        if response.status_code == 200:
            search_result = response.json()
            print(f"   🔍 Office visit search: {search_result.get('total_results', 0)} results found")
        else:
            print(f"   ❌ Search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Search error: {e}")
    
    print()
    print("=" * 60)
    print("🎉 Database Integration Test Completed!")
    print()
    print("📚 Available Database Integration Endpoints:")
    print("   - POST /api/sync/scrape-to-database - Scrape all and save to DB")
    print("   - POST /api/sync/scrape-cpt-to-database - Scrape CPT and save to DB")
    print("   - POST /api/sync/scrape-icd10-to-database - Scrape ICD-10 and save to DB")
    print("   - POST /api/sync/scrape-hcpcs-to-database - Scrape HCPCS and save to DB")
    print()
    print("🔗 API Documentation: http://localhost:8003/docs")
    print("🌐 Frontend Application: http://localhost:3003")

if __name__ == "__main__":
    test_database_integration() 