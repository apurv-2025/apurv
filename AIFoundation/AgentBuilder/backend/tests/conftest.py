import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from models.database import get_db, Base
from models.user import User
from models.agent import Agent

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "practice_name": "Test Practice",
        "role": "admin"
    }

@pytest.fixture
def test_agent():
    return {
        "name": "Test Agent",
        "description": "A test agent for billing",
        "role": "billing",
        "persona": "Friendly and professional billing assistant",
        "instructions": "Help with billing inquiries while maintaining HIPAA compliance",
        "configuration": {"max_tokens": 500}
    }

@pytest.fixture
def authenticated_client(client, test_user):
    # Register user
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    
    # Login
    response = client.post("/auth/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
