# Load testing script (tests/load_test.py)
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

class LoadTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        
    async def setup_session(self):
        self.session = aiohttp.ClientSession()
        
        # Login to get token
        async with self.session.post(f"{self.base_url}/auth/token", data={
            "username": "test@example.com",
            "password": "TestPassword123!"
        }) as resp:
            if resp.status == 200:
                data = await resp.json()
                self.token = data["access_token"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
    
    async def test_endpoint(self, endpoint, method="GET", data=None):
        try:
            async with self.session.request(method, f"{self.base_url}{endpoint}", json=data) as resp:
                return resp.status, await resp.text()
        except Exception as e:
            return 0, str(e)
    
    async def run_load_test(self, endpoint, concurrent_requests=10, total_requests=100):
        await self.setup_session()
        
        start_time = time.time()
        
        async def single_request():
            return await self.test_endpoint(endpoint)
        
        # Run concurrent requests
        tasks = []
        for _ in range(total_requests):
            task = asyncio.create_task(single_request())
            tasks.append(task)
            
            # Limit concurrent tasks
            if len(tasks) >= concurrent_requests:
                await asyncio.gather(*tasks)
                tasks = []
        
        # Wait for remaining tasks
        if tasks:
            await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        await self.session.close()
        
        return {
            "total_requests": total_requests,
            "duration": duration,
            "requests_per_second": total_requests / duration,
            "concurrent_requests": concurrent_requests
        }

# Run load test
async def main():
    tester = LoadTester()
    
    # Test different endpoints
    endpoints = [
        "/health",
        "/agents/",
        "/auth/me"
    ]
    
    for endpoint in endpoints:
        print(f"Testing {endpoint}...")
        results = await tester.run_load_test(endpoint, concurrent_requests=5, total_requests=50)
        print(f"Results: {results}")
        print("---")

if __name__ == "__main__":
    asyncio.run(main())
