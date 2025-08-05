# tests/test_agents.py
import pytest

def test_create_agent(authenticated_client, test_agent):
    response = authenticated_client.post("/agents/", json=test_agent)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_agent["name"]
    assert data["role"] == test_agent["role"]
    assert "id" in data

def test_get_agents(authenticated_client, test_agent):
    # Create an agent first
    authenticated_client.post("/agents/", json=test_agent)
    
    # Get all agents
    response = authenticated_client.get("/agents/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_agent["name"]

def test_get_agent_by_id(authenticated_client, test_agent):
    # Create an agent
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Get agent by ID
    response = authenticated_client.get(f"/agents/{agent_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == agent_id
    assert data["name"] == test_agent["name"]

def test_update_agent(authenticated_client, test_agent):
    # Create an agent
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Update agent
    update_data = {"name": "Updated Agent Name"}
    response = authenticated_client.put(f"/agents/{agent_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Agent Name"

def test_delete_agent(authenticated_client, test_agent):
    # Create an agent
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Delete agent
    response = authenticated_client.delete(f"/agents/{agent_id}")
    assert response.status_code == 200
    
    # Verify agent is deleted
    response = authenticated_client.get(f"/agents/{agent_id}")
    assert response.status_code == 404

def test_chat_with_agent(authenticated_client, test_agent):
    # Create an agent
    create_response = authenticated_client.post("/agents/", json=test_agent)
    agent_id = create_response.json()["id"]
    
    # Chat with agent (this will fail without proper LLM setup, but tests the endpoint)
    chat_data = {"agent_id": agent_id, "message": "Hello, can you help me?"}
    response = authenticated_client.post("/agents/chat", json=chat_data)
    
    # Should return some response even if LLM fails
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "confidence" in data
