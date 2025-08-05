import pytest
import io

def test_upload_document(authenticated_client, test_agent):
    # Create an agent first
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Create a fake file
    file_content = b"This is a test document for the knowledge base."
    file_data = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    # Upload document
    response = authenticated_client.post(f"/knowledge/upload/{agent_id}", files=file_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Document uploaded successfully"

def test_get_knowledge_base(authenticated_client, test_agent):
    # Create an agent
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Get knowledge base (should be empty initially)
    response = authenticated_client.get(f"/knowledge/{agent_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
