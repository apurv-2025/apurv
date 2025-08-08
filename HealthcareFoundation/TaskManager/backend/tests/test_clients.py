import pytest
from fastapi.testclient import TestClient


def test_create_client(client: TestClient, sample_client_data):
    response = client.post("/api/v1/clients/", json=sample_client_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_client_data["name"]
    assert data["email"] == sample_client_data["email"]
    assert "id" in data


def test_read_clients(client: TestClient, sample_client_data):
    # Create a client first
    client.post("/api/v1/clients/", json=sample_client_data)
    
    # Read clients
    response = client.get("/api/v1/clients/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_client_data["name"]


def test_duplicate_email(client: TestClient, sample_client_data):
    # Create first client
    client.post("/api/v1/clients/", json=sample_client_data)
    
    # Try to create another client with same email
    response = client.post("/api/v1/clients/", json=sample_client_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_client_validation(client: TestClient):
    # Test empty name
    invalid_data = {"name": "", "email": "test@example.com"}
    response = client.post("/api/v1/clients/", json=invalid_data)
    assert response.status_code == 422
    
    # Test invalid email
    invalid_data = {"name": "Test", "email": "invalid-email"}
    response = client.post("/api/v1/clients/", json=invalid_data)
    assert response.status_code == 422

# tests/test_api.py
def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Management System API" in response.json()["message"]


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_openapi_docs(client: TestClient):
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
