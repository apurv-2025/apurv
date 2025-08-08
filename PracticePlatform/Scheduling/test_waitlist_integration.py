#!/usr/bin/env python3
"""
Waitlist Integration Test Script
Tests the complete waitlist functionality with Patient and Practitioner integration
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
PATIENT_SERVICE_URL = "http://localhost:8001"
PRACTITIONER_SERVICE_URL = "http://localhost:8002"

async def test_health_checks():
    """Test health endpoints"""
    print("🔍 Testing Health Checks...")
    
    async with aiohttp.ClientSession() as session:
        # Test main API health
        async with session.get(f"{BASE_URL}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Scheduling2.0 Health: {response.status}")
            else:
                print(f"❌ Scheduling2.0 Health: {response.status}")
        
        # Test patient service health
        async with session.get(f"{BASE_URL}/patients/health/check") as response:
            if response.status == 200:
                print(f"✅ Patient Service Health: {response.status}")
            else:
                print(f"❌ Patient Service Health: {response.status}")
        
        # Test practitioner service health
        async with session.get(f"{BASE_URL}/practitioners/health/check") as response:
            if response.status == 200:
                print(f"✅ Practitioner Service Health: {response.status}")
            else:
                print(f"❌ Practitioner Service Health: {response.status}")

async def test_waitlist_crud():
    """Test waitlist CRUD operations"""
    print("\n📋 Testing Waitlist CRUD Operations...")
    
    async with aiohttp.ClientSession() as session:
        # Create waitlist entry
        entry_data = {
            "service_type": "THERAPY",
            "priority": "HIGH",
            "preferred_dates": ["2025-08-10", "2025-08-12"],
            "preferred_times": ["09:00", "14:00"],
            "notes": "Test waitlist entry for integration testing"
        }
        
        async with session.post(f"{BASE_URL}/waitlist/", json=entry_data) as response:
            if response.status == 200:
                entry = await response.json()
                entry_id = entry["id"]
                print(f"✅ Created Waitlist Entry: {entry_id}")
            else:
                print(f"❌ Failed to create waitlist entry: {response.status}")
                return
        
        # Get waitlist entry
        async with session.get(f"{BASE_URL}/waitlist/{entry_id}") as response:
            if response.status == 200:
                entry = await response.json()
                print(f"✅ Retrieved Waitlist Entry: {entry_id}")
                print(f"   - Service Type: {entry['service_type']}")
                print(f"   - Priority: {entry['priority']}")
                print(f"   - Status: {entry['status']}")
            else:
                print(f"❌ Failed to retrieve waitlist entry: {response.status}")
        
        # Update waitlist entry
        update_data = {
            "priority": "URGENT",
            "notes": "Updated notes for urgent therapy session"
        }
        
        async with session.put(f"{BASE_URL}/waitlist/{entry_id}", json=update_data) as response:
            if response.status == 200:
                updated_entry = await response.json()
                print(f"✅ Updated Waitlist Entry: {entry_id}")
                print(f"   - New Priority: {updated_entry['priority']}")
            else:
                print(f"❌ Failed to update waitlist entry: {response.status}")
        
        # Schedule from waitlist
        async with session.post(f"{BASE_URL}/waitlist/{entry_id}/schedule") as response:
            if response.status == 200:
                result = await response.json()
                print(f"✅ Scheduled from Waitlist: {entry_id}")
                print(f"   - New Status: {result['status']}")
            else:
                print(f"❌ Failed to schedule from waitlist: {response.status}")
        
        # Delete waitlist entry
        async with session.delete(f"{BASE_URL}/waitlist/{entry_id}") as response:
            if response.status == 200:
                print(f"✅ Deleted Waitlist Entry: {entry_id}")
            else:
                print(f"❌ Failed to delete waitlist entry: {response.status}")

async def test_waitlist_with_patient_integration():
    """Test waitlist with patient integration"""
    print("\n👥 Testing Waitlist with Patient Integration...")
    
    async with aiohttp.ClientSession() as session:
        # First, get a patient
        async with session.get(f"{BASE_URL}/patients/?limit=1") as response:
            if response.status == 200:
                patients = await response.json()
                if patients:
                    patient = patients[0]
                    patient_id = patient["id"]
                    print(f"✅ Found Patient: {patient.get('family_name', 'Unknown')}")
                else:
                    print("❌ No patients found")
                    return
            else:
                print(f"❌ Failed to get patients: {response.status}")
                return
        
        # Create waitlist entry with patient
        entry_data = {
            "patient_id": patient_id,
            "service_type": "CONSULTATION",
            "priority": "NORMAL",
            "notes": "Waitlist entry with patient integration"
        }
        
        async with session.post(f"{BASE_URL}/waitlist/", json=entry_data) as response:
            if response.status == 200:
                entry = await response.json()
                entry_id = entry["id"]
                print(f"✅ Created Waitlist Entry with Patient: {entry_id}")
                print(f"   - Patient: {entry['patient_name']}")
            else:
                print(f"❌ Failed to create waitlist entry with patient: {response.status}")
                return
        
        # Search waitlist by patient
        async with session.get(f"{BASE_URL}/waitlist/search/patient/{patient_id}") as response:
            if response.status == 200:
                entries = await response.json()
                print(f"✅ Found {len(entries)} waitlist entries for patient")
            else:
                print(f"❌ Failed to search waitlist by patient: {response.status}")
        
        # Clean up
        async with session.delete(f"{BASE_URL}/waitlist/{entry_id}") as response:
            if response.status == 200:
                print(f"✅ Cleaned up waitlist entry: {entry_id}")

async def test_waitlist_with_practitioner_integration():
    """Test waitlist with practitioner integration"""
    print("\n👨‍⚕️ Testing Waitlist with Practitioner Integration...")
    
    async with aiohttp.ClientSession() as session:
        # First, get a practitioner
        async with session.get(f"{BASE_URL}/practitioners/?limit=1") as response:
            if response.status == 200:
                practitioners = await response.json()
                if practitioners:
                    practitioner = practitioners[0]
                    practitioner_id = practitioner["id"]
                    print(f"✅ Found Practitioner: {practitioner.get('name', 'Unknown')}")
                else:
                    print("❌ No practitioners found")
                    return
            else:
                print(f"❌ Failed to get practitioners: {response.status}")
                return
        
        # Create waitlist entry with practitioner
        entry_data = {
            "practitioner_id": practitioner_id,
            "service_type": "MENTAL_HEALTH",
            "priority": "HIGH",
            "notes": "Waitlist entry with practitioner integration"
        }
        
        async with session.post(f"{BASE_URL}/waitlist/", json=entry_data) as response:
            if response.status == 200:
                entry = await response.json()
                entry_id = entry["id"]
                print(f"✅ Created Waitlist Entry with Practitioner: {entry_id}")
                print(f"   - Practitioner: {entry['practitioner_name']}")
            else:
                print(f"❌ Failed to create waitlist entry with practitioner: {response.status}")
                return
        
        # Search waitlist by practitioner
        async with session.get(f"{BASE_URL}/waitlist/search/practitioner/{practitioner_id}") as response:
            if response.status == 200:
                entries = await response.json()
                print(f"✅ Found {len(entries)} waitlist entries for practitioner")
            else:
                print(f"❌ Failed to search waitlist by practitioner: {response.status}")
        
        # Clean up
        async with session.delete(f"{BASE_URL}/waitlist/{entry_id}") as response:
            if response.status == 200:
                print(f"✅ Cleaned up waitlist entry: {entry_id}")

async def test_waitlist_filtering():
    """Test waitlist filtering and pagination"""
    print("\n🔍 Testing Waitlist Filtering and Pagination...")
    
    async with aiohttp.ClientSession() as session:
        # Create multiple entries with different priorities and service types
        entries_data = [
            {"service_type": "THERAPY", "priority": "LOW", "notes": "Low priority therapy"},
            {"service_type": "CONSULTATION", "priority": "NORMAL", "notes": "Normal consultation"},
            {"service_type": "EMERGENCY", "priority": "URGENT", "notes": "Urgent emergency"},
            {"service_type": "ASSESSMENT", "priority": "HIGH", "notes": "High priority assessment"}
        ]
        
        created_ids = []
        for entry_data in entries_data:
            async with session.post(f"{BASE_URL}/waitlist/", json=entry_data) as response:
                if response.status == 200:
                    entry = await response.json()
                    created_ids.append(entry["id"])
                    print(f"✅ Created Entry {entry['id']}: {entry['service_type']} - {entry['priority']}")
        
        # Test filtering by priority
        async with session.get(f"{BASE_URL}/waitlist/?priority=URGENT") as response:
            if response.status == 200:
                entries = await response.json()
                print(f"✅ Found {len(entries)} urgent entries")
            else:
                print(f"❌ Failed to filter by priority: {response.status}")
        
        # Test filtering by service type
        async with session.get(f"{BASE_URL}/waitlist/?service_type=THERAPY") as response:
            if response.status == 200:
                entries = await response.json()
                print(f"✅ Found {len(entries)} therapy entries")
            else:
                print(f"❌ Failed to filter by service type: {response.status}")
        
        # Test pagination
        async with session.get(f"{BASE_URL}/waitlist/?skip=0&limit=2") as response:
            if response.status == 200:
                entries = await response.json()
                print(f"✅ Pagination test: {len(entries)} entries (limit 2)")
            else:
                print(f"❌ Failed to test pagination: {response.status}")
        
        # Clean up
        for entry_id in created_ids:
            async with session.delete(f"{BASE_URL}/waitlist/{entry_id}") as response:
                if response.status == 200:
                    print(f"✅ Cleaned up entry: {entry_id}")

async def test_waitlist_statistics():
    """Test waitlist statistics"""
    print("\n📊 Testing Waitlist Statistics...")
    
    async with aiohttp.ClientSession() as session:
        # Get initial stats
        async with session.get(f"{BASE_URL}/waitlist/stats/summary") as response:
            if response.status == 200:
                stats = await response.json()
                print(f"✅ Initial Stats:")
                print(f"   - Total Entries: {stats['total_entries']}")
                print(f"   - Active Entries: {stats['active_entries']}")
                print(f"   - Scheduled Entries: {stats['scheduled_entries']}")
            else:
                print(f"❌ Failed to get stats: {response.status}")

async def main():
    """Main test function"""
    print("🚀 Starting Waitlist Integration Tests")
    print("=" * 50)
    
    # Wait a bit for services to be ready
    print("⏳ Waiting for services to be ready...")
    await asyncio.sleep(5)
    
    # Run tests
    await test_health_checks()
    await test_waitlist_statistics()
    await test_waitlist_crud()
    await test_waitlist_with_patient_integration()
    await test_waitlist_with_practitioner_integration()
    await test_waitlist_filtering()
    await test_waitlist_statistics()
    
    print("\n" + "=" * 50)
    print("✅ Waitlist integration tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 