import pytest
from fastapi.testclient import TestClient


def test_create_task(client: TestClient, sample_task_data):
    response = client.post("/api/v1/tasks/", json=sample_task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_task_data["name"]
    assert data["description"] == sample_task_data["description"]
    assert data["priority"] == sample_task_data["priority"]
    assert data["status"] == sample_task_data["status"]
    assert "id" in data
    assert "created_at" in data


def test_read_tasks(client: TestClient, sample_task_data):
    # Create a task first
    client.post("/api/v1/tasks/", json=sample_task_data)
    
    # Read tasks
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_task_data["name"]


def test_read_task(client: TestClient, sample_task_data):
    # Create a task
    create_response = client.post("/api/v1/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]
    
    # Read the task
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_task_data["name"]


def test_update_task(client: TestClient, sample_task_data):
    # Create a task
    create_response = client.post("/api/v1/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {"name": "Updated Task Name", "status": "completed"}
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Task Name"
    assert data["status"] == "completed"


def test_delete_task(client: TestClient, sample_task_data):
    # Create a task
    create_response = client.post("/api/v1/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_task_stats(client: TestClient, sample_task_data):
    # Create some tasks
    client.post("/api/v1/tasks/", json=sample_task_data)
    completed_task = {**sample_task_data, "status": "completed"}
    client.post("/api/v1/tasks/", json=completed_task)
    
    # Get stats
    response = client.get("/api/v1/tasks/stats/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 2
    assert data["completed_tasks"] == 1
    assert data["pending_tasks"] == 1


def test_task_validation(client: TestClient):
    # Test empty name
    invalid_data = {"name": "", "priority": "medium"}
    response = client.post("/api/v1/tasks/", json=invalid_data)
    assert response.status_code == 422
    
    # Test invalid priority
    invalid_data = {"name": "Test", "priority": "invalid"}
    response = client.post("/api/v1/tasks/", json=invalid_data)
    assert response.status_code == 422
