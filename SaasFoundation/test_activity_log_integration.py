#!/usr/bin/env python3
"""
Test script for ActivityLog Integration with SaaSFoundation
Tests the complete integration between SaaSFoundation and ActivityLog service
"""

import asyncio
import httpx
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
SAAS_FOUNDATION_URL = "http://localhost:8000"
ACTIVITY_LOG_URL = "http://localhost:8001"

class ActivityLogIntegrationTest:
    """Test class for ActivityLog integration"""
    
    def __init__(self):
        self.saas_client = httpx.AsyncClient(timeout=30.0)
        self.activity_client = httpx.AsyncClient(timeout=30.0)
        self.test_user_id = "test-user-123"
        self.test_email = "test@example.com"
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.saas_client.aclose()
        await self.activity_client.aclose()
    
    async def test_service_health(self):
        """Test if both services are running"""
        print("🏥 Testing Service Health...")
        
        try:
            # Test SaaSFoundation health
            response = await self.saas_client.get(f"{SAAS_FOUNDATION_URL}/api/v1/health")
            response.raise_for_status()
            print("✅ SaaSFoundation is running")
            
            # Test ActivityLog health
            response = await self.activity_client.get(f"{ACTIVITY_LOG_URL}/health")
            response.raise_for_status()
            print("✅ ActivityLog service is running")
            
            # Test ActivityLog integration health
            response = await self.saas_client.get(f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/health")
            response.raise_for_status()
            health_data = response.json()
            print(f"✅ ActivityLog integration health: {health_data['status']}")
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
        
        return True
    
    async def test_activity_logging(self):
        """Test basic activity logging"""
        print("\n📝 Testing Activity Logging...")
        
        try:
            # Log a custom activity
            activity_data = {
                "event_type": "test_activity",
                "event_category": "testing",
                "event_description": "Test activity from SaaSFoundation",
                "event_metadata": {
                    "test_id": "integration-test-001",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            response = await self.saas_client.post(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/log",
                json=activity_data,
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Custom activity logged: {result['event_id']}")
            
            # Wait a moment for the activity to be processed
            await asyncio.sleep(1)
            
            # Retrieve the logged activity
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            activities = response.json()
            
            if activities:
                print(f"✅ Retrieved {len(activities)} activities")
                latest_activity = activities[0]
                print(f"   Latest: {latest_activity.get('event', 'N/A')} - {latest_activity.get('date', 'N/A')}")
            else:
                print("⚠️  No activities found")
            
        except Exception as e:
            print(f"❌ Activity logging test failed: {e}")
    
    async def test_api_endpoint_logging(self):
        """Test automatic logging of API endpoints"""
        print("\n🔗 Testing API Endpoint Logging...")
        
        try:
            # Test various API endpoints to trigger automatic logging
            
            # Test health endpoint (should be excluded from logging)
            response = await self.saas_client.get(f"{SAAS_FOUNDATION_URL}/api/v1/health")
            response.raise_for_status()
            print("✅ Health endpoint accessed (should not be logged)")
            
            # Test pricing endpoint (should be logged)
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/pricing",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            print("✅ Pricing endpoint accessed (should be logged)")
            
            # Test organizations endpoint (should be logged)
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/organizations",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            print("✅ Organizations endpoint accessed (should be logged)")
            
            # Wait for activities to be processed
            await asyncio.sleep(2)
            
            # Check for logged activities
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            activities = response.json()
            
            print(f"✅ Found {len(activities)} total activities")
            
            # Check for specific activity types
            activity_types = [activity.get('eventType', '') for activity in activities]
            if 'pricing_view' in activity_types:
                print("✅ Pricing view activity logged")
            if 'organization_list' in activity_types:
                print("✅ Organization list activity logged")
            
        except Exception as e:
            print(f"❌ API endpoint logging test failed: {e}")
    
    async def test_activity_summary(self):
        """Test activity summary functionality"""
        print("\n📊 Testing Activity Summary...")
        
        try:
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/summary",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            summary = response.json()
            
            print(f"✅ Activity summary retrieved:")
            print(f"   Total events: {summary.get('total_events', 0)}")
            print(f"   Event types: {len(summary.get('event_types', {}))}")
            print(f"   Event categories: {len(summary.get('event_categories', {}))}")
            
            if summary.get('latest_activity'):
                latest = summary['latest_activity']
                print(f"   Latest activity: {latest.get('event', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Activity summary test failed: {e}")
    
    async def test_activity_statistics(self):
        """Test activity statistics functionality"""
        print("\n📈 Testing Activity Statistics...")
        
        try:
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/stats?period=7d",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            stats = response.json()
            
            print(f"✅ Activity statistics retrieved:")
            print(f"   Period: {stats.get('period', 'N/A')}")
            print(f"   Total events: {stats.get('total_events', 0)}")
            print(f"   Avg daily events: {stats.get('avg_daily_events', 0)}")
            print(f"   Unique days: {stats.get('unique_days', 0)}")
            
        except Exception as e:
            print(f"❌ Activity statistics test failed: {e}")
    
    async def test_activity_export(self):
        """Test activity export functionality"""
        print("\n📤 Testing Activity Export...")
        
        try:
            # Test JSON export
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/export?format=json",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            export_data = response.json()
            
            print(f"✅ JSON export successful:")
            print(f"   Format: {export_data.get('format', 'N/A')}")
            print(f"   Record count: {export_data.get('record_count', 0)}")
            
            # Test CSV export
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities/export?format=csv",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            csv_data = response.json()
            
            print(f"✅ CSV export successful:")
            print(f"   Format: {csv_data.get('format', 'N/A')}")
            print(f"   Record count: {csv_data.get('record_count', 0)}")
            
        except Exception as e:
            print(f"❌ Activity export test failed: {e}")
    
    async def test_activity_filtering(self):
        """Test activity filtering functionality"""
        print("\n🔍 Testing Activity Filtering...")
        
        try:
            # Test filtering by event type
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities?event_type=pricing_view",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            filtered_activities = response.json()
            
            print(f"✅ Event type filtering:")
            print(f"   Filter: pricing_view")
            print(f"   Results: {len(filtered_activities)} activities")
            
            # Test search functionality
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities?search=test",
                headers={"X-User-ID": self.test_user_id}
            )
            response.raise_for_status()
            search_results = response.json()
            
            print(f"✅ Search functionality:")
            print(f"   Search term: test")
            print(f"   Results: {len(search_results)} activities")
            
        except Exception as e:
            print(f"❌ Activity filtering test failed: {e}")
    
    async def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n⚠️  Testing Error Handling...")
        
        try:
            # Test with invalid user ID
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities",
                headers={"X-User-ID": "invalid-user"}
            )
            response.raise_for_status()
            print("✅ Invalid user ID handled gracefully")
            
            # Test with missing user ID
            response = await self.saas_client.get(
                f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities"
            )
            response.raise_for_status()
            print("✅ Missing user ID handled gracefully")
            
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
    
    async def test_performance(self):
        """Test performance with multiple concurrent requests"""
        print("\n⚡ Testing Performance...")
        
        try:
            start_time = time.time()
            
            # Make multiple concurrent requests
            tasks = []
            for i in range(10):
                task = self.saas_client.get(
                    f"{SAAS_FOUNDATION_URL}/api/v1/activity-log/activities",
                    headers={"X-User-ID": f"user-{i}"}
                )
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_time = time.time()
            duration = end_time - start_time
            
            successful_requests = sum(1 for r in responses if not isinstance(r, Exception))
            
            print(f"✅ Performance test completed:")
            print(f"   Total requests: 10")
            print(f"   Successful requests: {successful_requests}")
            print(f"   Duration: {duration:.2f} seconds")
            print(f"   Avg response time: {duration/10:.2f} seconds per request")
            
        except Exception as e:
            print(f"❌ Performance test failed: {e}")
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting ActivityLog Integration Tests")
        print("=" * 60)
        
        # Check if services are running
        if not await self.test_service_health():
            print("❌ Services are not running. Please start both SaaSFoundation and ActivityLog services.")
            return
        
        # Run all tests
        await self.test_activity_logging()
        await self.test_api_endpoint_logging()
        await self.test_activity_summary()
        await self.test_activity_statistics()
        await self.test_activity_export()
        await self.test_activity_filtering()
        await self.test_error_handling()
        await self.test_performance()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")

async def main():
    """Main test function"""
    async with ActivityLogIntegrationTest() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    print("ActivityLog Integration Test Script")
    print("Make sure both SaaSFoundation and ActivityLog services are running!")
    print(f"SaaSFoundation URL: {SAAS_FOUNDATION_URL}")
    print(f"ActivityLog URL: {ACTIVITY_LOG_URL}")
    print()
    
    # Run the tests
    asyncio.run(main()) 