# File: tests/test_eligibility.py
import pytest
from datetime import date
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_eligibility_inquiry():
    """Test eligibility inquiry creation."""
    test_data = {
        "member_id": "TEST123456",
        "provider_npi": "1234567890",
        "service_type": "30",
        "subscriber_first_name": "John",
        "subscriber_last_name": "Doe",
        "subscriber_dob": "1980-01-01"
    }
    
    response = client.post("/api/v1/eligibility/inquiry", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "request_id" in data
    assert "edi_270" in data
    assert data["status"] == "submitted"


def test_get_eligibility_requests():
    """Test get eligibility requests endpoint."""
    response = client.get("/api/v1/eligibility/requests")
    assert response.status_code == 200
    assert "items" in response.json()
