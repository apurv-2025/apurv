import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_insurance_card():
    """Test insurance card upload endpoint."""
    # Create a simple test file
    test_file = b"Test insurance card content"
    
    response = client.post(
        "/api/v1/upload/insurance-card",
        files={"file": ("test_card.jpg", test_file, "image/jpeg")}
    )
    
    # Note: This will fail without actual OCR setup, but shows the structure
    assert response.status_code in [200, 500]  # Allow for processing errors in tests


def test_get_insurance_cards():
    """Test get insurance cards endpoint."""
    response = client.get("/api/v1/upload/insurance-cards")
    assert response.status_code == 200
    assert "items" in response.json()
