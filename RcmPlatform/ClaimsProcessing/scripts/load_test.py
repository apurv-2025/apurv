# =============================================================================
# FILE: scripts/load_test.py
# =============================================================================
#!/usr/bin/env python3

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict
import argparse
import json

class LoadTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_agent_chat(self, user_id: str, message: str) -> Dict:
        """Test agent chat endpoint"""
        start_time = time.time()
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/agent/chat",
                json={
                    "message": message,
                    "user_id": user_id,
                    "context": {}
                }
            ) as response:
                end_time = time.time()
                
                return {
                    "status": response.status,
                    "response_time": end_time - start_time,
                    "success": response.status == 200,
                    "endpoint": "chat"
                }
        except Exception as e:
            return {
                "status": 500,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e),
                "endpoint": "chat"
            }
    
    async def test_claim_analysis(self, user_id: str, claim_id: int) -> Dict:
        """Test claim analysis endpoint"""
        start_time = time.time()
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/agent/tasks/analyze-claim/{claim_id}",
                json={"user_id": user_id}
            ) as response:
                end_time = time.time()
                
                return {
                    "status": response.status,
                    "response_time": end_time - start_time,
                    "success": response.status == 200,
                    "endpoint": "analyze_claim"
                }
        except Exception as e:
            return {
                "status": 500,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e),
                "endpoint": "analyze_claim"
            }
    
    async def test_dashboard_stats(self) -> Dict:
        """Test dashboard stats endpoint"""
        start_time = time.time()
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/reports/dashboard"
            ) as response:
                end_time = time.time()
                
                return {
                    "status": response.status,
                    "response_time": end_time - start_time,
                    "success": response.status == 200,
                    "endpoint": "dashboard_stats"
                }
        except Exception as e:
            return {
                "status": 500,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e),
                "endpoint": "dashboard_stats"
            }
    
    async def run_load_test(self, concurrent_users: int, requests_per_user: int) -> List[Dict]:
        """Run load test with specified parameters"""
        
        test_scenarios = [
            ("chat", "What is the status of recent claims?"),
            ("chat", "Generate a financial summary report"),
            ("chat", "Show me rejected claims from this week"),
            ("analyze_claim", 123),
            ("analyze_claim", 456),
            ("dashboard_stats", None)
        ]
        
        async def user_session(user_id: int):
            results = []
            
            for request_num in range(requests_per_user):
                # Randomly select a test scenario
                scenario_type, param = test_scenarios[request_num % len(test_scenarios)]
                
                if scenario_type == "chat":
                    result = await self.test_agent_chat(f"user_{user_id}", param)
                elif scenario_type == "analyze_claim":
                    result = await self.test_claim_analysis(f"user_{user_id}", param)
                elif scenario_type == "dashboard_stats":
                    result = await self.test_dashboard_stats()
                
                result["user_id"] = user_id
                result["request_num"] = request_num
                results.append(result)
                
                # Small delay between requests
                await asyncio.sleep(0.1)
            
            return results
        
        # Run concurrent user sessions
        tasks = [user_session(user_id) for user_id in range(concurrent_users)]
        user_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results
        all_results = []
        for user_result in user_results:
            if isinstance(user_result, list):
                all_results.extend(user_result)
            else:
                print(f"Error in user session: {user_result}")
        
        return all_results

def analyze_results(results: List[Dict]):
    """Analyze load test results"""
    
    if not results:
        print("No results to analyze")
        return
    
    # Overall statistics
    total_requests = len(results)
    successful_requests = sum(1 for r in results if r["success"])
    success_rate = (successful_requests / total_requests) * 100
    
    response_times = [r["response_time"] for r in results if r["success"]]
    
    if response_times:
        avg_response_time = statistics.mean(response_times)
        median_response_time = statistics.median(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else max(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
    else:
        avg_response_time = median_response_time = p95_response_time = min_response_time = max_response_time = 0
    
    # Per-endpoint statistics
    endpoint_stats = {}
    for result in results:
        endpoint = result["endpoint"]
        if endpoint not in endpoint_stats:
            endpoint_stats[endpoint] = {"total": 0, "successful": 0, "response_times": []}
        
        endpoint_stats[endpoint]["total"] += 1
        if result["success"]:
            endpoint_stats[endpoint]["successful"] += 1
            endpoint_stats[endpoint]["response_times"].append(result["response_time"])
    
    # Print results
    print("\n" + "="*60)
    print("LOAD TEST RESULTS")
    print("="*60)
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Failed Requests: {total_requests - successful_requests}")
    
    print(f"\nResponse Time Statistics:")
    print(f"  Average: {avg_response_time:.3f}s")
    print(f"  Median: {median_response_time:.3f}s")
    print(f"  95th Percentile: {p95_response_time:.3f}s")
    print(f"  Min: {min_response_time:.3f}s")
    print(f"  Max: {max_response_time:.3f}s")
    
    print(f"\nPer-Endpoint Statistics:")
    for endpoint, stats in endpoint_stats.items():
        total = stats["total"]
        successful = stats["successful"]
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        times = stats["response_times"]
        if times:
            avg_time = statistics.mean(times)
            p95_time = statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times)
        else:
            avg_time = p95_time = 0
        
        print(f"  {endpoint}:")
        print(f"    Requests: {total}")
        print(f"    Success Rate: {success_rate:.2f}%")
        print(f"    Avg Response Time: {avg_time:.3f}s")
        print(f"    95th Percentile: {p95_time:.3f}s")
    
    # Throughput calculation
    if response_times:
        total_time = max(response_times)
        throughput = total_requests / total_time if total_time > 0 else 0
        print(f"\nThroughput: {throughput:.2f} requests/second")

async def main():
    parser = argparse.ArgumentParser(description="Load test the EDI Claims API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for the API")
    parser.add_argument("--concurrent", type=int, default=10, help="Number of concurrent users")
    parser.add_argument("--requests", type=int, default=100, help="Total number of requests")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    requests_per_user = args.requests // args.concurrent
    
    print(f"Starting load test:")
    print(f"  URL: {args.url}")
    print(f"  Concurrent Users: {args.concurrent}")
    print(f"  Requests per User: {requests_per_user}")
    print(f"  Total Requests: {args.concurrent * requests_per_user}")
    
    async with LoadTester(args.url) as tester:
        print("\nRunning load test...")
        start_time = time.time()
        
        results = await tester.run_load_test(args.concurrent, requests_per_user)
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        print(f"\nLoad test completed in {total_duration:.2f} seconds")
        
        # Analyze and display results
        analyze_results(results)
        
        # Save results if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump({
                    "test_config": {
                        "url": args.url,
                        "concurrent_users": args.concurrent,
                        "requests_per_user": requests_per_user,
                        "total_duration": total_duration
                    },
                    "results": results
                }, f, indent=2)
            print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    asyncio.run(main())
