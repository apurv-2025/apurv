# client_examples/python_client.py
"""
Python client example for Task Management API
"""
import requests
import json
from typing import Dict, List, Optional
from datetime import date, time


class TaskManagerClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/v1"
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def login(self, username: str, password: str) -> str:
        """Login and get access token"""
        response = self.session.post(
            f"{self.api_base}/auth/login",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data["access_token"]
        
        # Update session headers
        self.session.headers.update({"Authorization": f"Bearer {access_token}"})
        
        return access_token
    
    # Task methods
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        response = self.session.post(f"{self.api_base}/tasks/", json=task_data)
        response.raise_for_status()
        return response.json()
    
    def get_tasks(self, **filters) -> List[Dict]:
        """Get tasks with optional filters"""
        response = self.session.get(f"{self.api_base}/tasks/", params=filters)
        response.raise_for_status()
        return response.json()
    
    def get_task(self, task_id: int) -> Dict:
        """Get a specific task"""
        response = self.session.get(f"{self.api_base}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()
    
    def update_task(self, task_id: int, task_data: Dict) -> Dict:
        """Update a task"""
        response = self.session.put(f"{self.api_base}/tasks/{task_id}", json=task_data)
        response.raise_for_status()
        return response.json()
    
    def delete_task(self, task_id: int) -> Dict:
        """Delete a task"""
        response = self.session.delete(f"{self.api_base}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()
    
    # Client methods
    def create_client(self, client_data: Dict) -> Dict:
        """Create a new client"""
        response = self.session.post(f"{self.api_base}/clients/", json=client_data)
        response.raise_for_status()
        return response.json()
    
    def get_clients(self, **filters) -> List[Dict]:
        """Get clients with optional filters"""
        response = self.session.get(f"{self.api_base}/clients/", params=filters)
        response.raise_for_status()
        return response.json()
    
    # File upload methods
    def upload_file(self, file_path: str, task_id: Optional[int] = None) -> Dict:
        """Upload a file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {}
            if task_id:
                data['task_id'] = task_id
            
            response = self.session.post(
                f"{self.api_base}/attachments/upload",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def download_file(self, attachment_id: int, save_path: str):
        """Download a file"""
        response = self.session.get(f"{self.api_base}/attachments/{attachment_id}/download")
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
    
    # Statistics
    def get_task_stats(self) -> Dict:
        """Get task statistics"""
        response = self.session.get(f"{self.api_base}/tasks/stats/overview")
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = TaskManagerClient()
    
    try:
        # Login (if authentication is enabled)
        # token = client.login("username", "password")
        # print(f"Logged in with token: {token}")
        
        # Create a client
        new_client = client.create_client({
            "name": "John Doe",
            "email": "john@example.com",
            "company": "Acme Corp"
        })
        print(f"Created client: {new_client}")
        
        # Create a task
        new_task = client.create_task({
            "name": "Complete API integration",
            "description": "Integrate with the new task management API",
            "priority": "high",
            "client_id": new_client["id"]
        })
        print(f"Created task: {new_task}")
        
        # Get all tasks
        tasks = client.get_tasks()
        print(f"Total tasks: {len(tasks)}")
        
        # Get task statistics
        stats = client.get_task_stats()
        print(f"Task statistics: {stats}")
        
        # Update task status
        updated_task = client.update_task(new_task["id"], {"status": "completed"})
        print(f"Updated task: {updated_task}")
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
