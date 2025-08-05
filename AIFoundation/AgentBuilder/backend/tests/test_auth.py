# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient

def test_register_user(client, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data

def test_register_duplicate_email(client, test_user):
    # Register first user
    client.post("/auth/register", json=test_user)
    
    # Try to register same email again
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    # Register user first
    client.post("/auth/register", json=test_user)
    
    # Login
    response = client.post("/auth/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/auth/token", data={
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_user(authenticated_client, test_user):
    response = authenticated_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
