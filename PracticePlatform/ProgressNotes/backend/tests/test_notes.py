# backend/tests/test_notes.py
import uuid
from datetime import datetime

def test_create_note(client, auth_headers):
    # First create a patient
    patient_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1985-05-15",
        "medical_record_number": "MRN789012"
    }
    patient_response = client.post("/patients/", json=patient_data, headers=auth_headers)
    patient_id = patient_response.json()["id"]

    # Create note
    note_data = {
        "patient_id": patient_id,
        "note_type": "SOAP",
        "session_date": "2024-01-15T10:00:00",
        "content": {
            "subjective": "Patient reports feeling anxious",
            "objective": "Patient appears restless",
            "assessment": "Generalized anxiety",
            "plan": "Continue therapy sessions"
        }
    }
    response = client.post("/notes/", json=note_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["note_type"] == "SOAP"
    assert data["patient_id"] == patient_id

def test_get_notes(client, auth_headers):
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_sign_note(client, auth_headers):
    # Create patient and note first
    patient_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "date_of_birth": "1980-03-20",
        "medical_record_number": "MRN345678"
    }
    patient_response = client.post("/patients/", json=patient_data, headers=auth_headers)
    patient_id = patient_response.json()["id"]

    note_data = {
        "patient_id": patient_id,
        "note_type": "SOAP",
        "session_date": "2024-01-15T14:00:00",
        "content": {"subjective": "Test note", "objective": "", "assessment": "", "plan": ""}
    }
    note_response = client.post("/notes/", json=note_data, headers=auth_headers)
    note_id = note_response.json()["id"]

    # Sign the note
    response = client.post(f"/notes/{note_id}/sign", headers=auth_headers, json={})
    assert response.status_code == 200
    data = response.json()
    assert data["is_signed"] == True
    assert data["is_locked"] == True
