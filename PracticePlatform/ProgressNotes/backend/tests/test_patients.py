# backend/tests/test_patients.py
def test_create_patient(client, auth_headers):
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "medical_record_number": "MRN123456",
        "phone": "555-1234",
        "email": "john.doe@example.com"
    }
    response = client.post("/patients/", json=patient_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["medical_record_number"] == "MRN123456"

def test_get_patients(client, auth_headers):
    response = client.get("/patients/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_patient_missing_fields(client, auth_headers):
    patient_data = {
        "first_name": "John",
        # Missing required fields
    }
    response = client.post("/patients/", json=patient_data, headers=auth_headers)
    assert response.status_code == 422

