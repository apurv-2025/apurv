from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from datetime import datetime, date
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/forms", tags=["forms"])

# Mock forms and uploads data
MOCK_AVAILABLE_FORMS = [
    {
        "id": 1,
        "title": "Patient Registration Form",
        "category": "Registration",
        "description": "Complete patient intake form for new patients",
        "estimatedTime": "10-15 minutes",
        "required": True,
        "status": "available",
        "fields": [
            {"name": "personalInfo", "label": "Personal Information", "type": "section"},
            {"name": "firstName", "label": "First Name", "type": "text", "required": True},
            {"name": "lastName", "label": "Last Name", "type": "text", "required": True},
            {"name": "dateOfBirth", "label": "Date of Birth", "type": "date", "required": True},
            {"name": "gender", "label": "Gender", "type": "select", "options": ["Male", "Female", "Other", "Prefer not to say"], "required": True},
            {"name": "phone", "label": "Phone Number", "type": "tel", "required": True},
            {"name": "email", "label": "Email Address", "type": "email", "required": True},
            {"name": "address", "label": "Address", "type": "textarea", "required": True},
            {"name": "emergencyContact", "label": "Emergency Contact", "type": "section"},
            {"name": "emergencyName", "label": "Emergency Contact Name", "type": "text", "required": True},
            {"name": "emergencyPhone", "label": "Emergency Contact Phone", "type": "tel", "required": True},
            {"name": "emergencyRelation", "label": "Relationship", "type": "text", "required": True}
        ]
    },
    {
        "id": 2,
        "title": "Medical History Questionnaire",
        "category": "Medical History",
        "description": "Comprehensive medical and family history form",
        "estimatedTime": "20-25 minutes",
        "required": True,
        "status": "available",
        "fields": [
            {"name": "currentMedications", "label": "Current Medications", "type": "section"},
            {"name": "medications", "label": "List all current medications", "type": "textarea", "placeholder": "Include dosage and frequency"},
            {"name": "allergies", "label": "Known Allergies", "type": "textarea", "placeholder": "Include drug, food, and environmental allergies"},
            {"name": "medicalHistory", "label": "Medical History", "type": "section"},
            {"name": "previousSurgeries", "label": "Previous Surgeries", "type": "textarea"},
            {"name": "chronicConditions", "label": "Chronic Medical Conditions", "type": "textarea"},
            {"name": "familyHistory", "label": "Family Medical History", "type": "textarea"},
            {"name": "lifestyle", "label": "Lifestyle Information", "type": "section"},
            {"name": "smoking", "label": "Smoking Status", "type": "select", "options": ["Never", "Former", "Current"]},
            {"name": "alcohol", "label": "Alcohol Use", "type": "select", "options": ["Never", "Occasional", "Regular", "Daily"]},
            {"name": "exercise", "label": "Exercise Frequency", "type": "select", "options": ["None", "1-2 times/week", "3-4 times/week", "Daily"]}
        ]
    },
    {
        "id": 3,
        "title": "Insurance Information Form",
        "category": "Insurance",
        "description": "Update insurance and billing information",
        "estimatedTime": "5-10 minutes",
        "required": False,
        "status": "available",
        "fields": [
            {"name": "primaryInsurance", "label": "Primary Insurance", "type": "section"},
            {"name": "insuranceCompany", "label": "Insurance Company", "type": "text", "required": True},
            {"name": "policyNumber", "label": "Policy Number", "type": "text", "required": True},
            {"name": "groupNumber", "label": "Group Number", "type": "text"},
            {"name": "subscriberName", "label": "Subscriber Name", "type": "text", "required": True},
            {"name": "secondaryInsurance", "label": "Secondary Insurance (if applicable)", "type": "section"},
            {"name": "secondaryCompany", "label": "Secondary Insurance Company", "type": "text"},
            {"name": "secondaryPolicy", "label": "Secondary Policy Number", "type": "text"}
        ]
    },
    {
        "id": 4,
        "title": "Pre-Visit Symptom Checker",
        "category": "Symptoms",
        "description": "Document current symptoms before your appointment",
        "estimatedTime": "5-8 minutes",
        "required": False,
        "status": "available",
        "fields": [
            {"name": "chiefComplaint", "label": "Main Concern", "type": "textarea", "placeholder": "What brings you in today?", "required": True},
            {"name": "symptomDuration", "label": "How long have you had these symptoms?", "type": "select", "options": ["Less than 1 day", "1-3 days", "1 week", "2-4 weeks", "More than 1 month"]},
            {"name": "painLevel", "label": "Pain Level (0-10)", "type": "range", "min": 0, "max": 10},
            {"name": "additionalSymptoms", "label": "Additional Symptoms", "type": "textarea"},
            {"name": "medications", "label": "Medications taken for this issue", "type": "textarea"}
        ]
    },
    {
        "id": 5,
        "title": "COVID-19 Screening Form",
        "category": "Screening",
        "description": "Required COVID-19 health screening",
        "estimatedTime": "2-3 minutes",
        "required": True,
        "status": "available",
        "fields": [
            {"name": "symptoms", "label": "COVID-19 Symptoms", "type": "section"},
            {"name": "fever", "label": "Have you had a fever in the last 14 days?", "type": "radio", "options": ["Yes", "No"], "required": True},
            {"name": "cough", "label": "Do you have a new or worsening cough?", "type": "radio", "options": ["Yes", "No"], "required": True},
            {"name": "breathing", "label": "Do you have difficulty breathing?", "type": "radio", "options": ["Yes", "No"], "required": True},
            {"name": "exposure", "label": "Have you been exposed to COVID-19?", "type": "radio", "options": ["Yes", "No", "Unknown"], "required": True},
            {"name": "travel", "label": "Have you traveled recently?", "type": "radio", "options": ["Yes", "No"], "required": True}
        ]
    }
]

MOCK_COMPLETED_FORMS = [
    {
        "id": 101,
        "formId": 1,
        "title": "Patient Registration Form",
        "completedDate": "2024-02-01",
        "status": "submitted",
        "submittedBy": "John Smith",
        "reviewedBy": "Dr. Sarah Johnson",
        "reviewDate": "2024-02-02",
        "responses": {
            "firstName": "John",
            "lastName": "Smith",
            "dateOfBirth": "1985-05-15",
            "gender": "Male",
            "phone": "555-0123",
            "email": "john.smith@email.com"
        }
    },
    {
        "id": 102,
        "formId": 5,
        "title": "COVID-19 Screening Form",
        "completedDate": "2024-02-15",
        "status": "approved",
        "submittedBy": "John Smith",
        "reviewedBy": "Clinic Staff",
        "reviewDate": "2024-02-15",
        "responses": {
            "fever": "No",
            "cough": "No",
            "breathing": "No",
            "exposure": "No",
            "travel": "No"
        }
    }
]

MOCK_UPLOADED_DOCUMENTS = [
    {
        "id": 201,
        "fileName": "Insurance_Card_Front.jpg",
        "category": "Insurance",
        "fileType": "image/jpeg",
        "fileSize": "2.1 MB",
        "uploadDate": "2024-02-10",
        "uploadedBy": "John Smith",
        "status": "verified",
        "description": "Primary insurance card - front side",
        "tags": ["insurance", "primary", "blue-cross"]
    },
    {
        "id": 202,
        "fileName": "Insurance_Card_Back.jpg",
        "category": "Insurance",
        "fileType": "image/jpeg",
        "fileSize": "1.8 MB",
        "uploadDate": "2024-02-10",
        "uploadedBy": "John Smith",
        "status": "verified",
        "description": "Primary insurance card - back side",
        "tags": ["insurance", "primary", "blue-cross"]
    },
    {
        "id": 203,
        "fileName": "Drivers_License.jpg",
        "category": "Identification",
        "fileType": "image/jpeg",
        "fileSize": "1.5 MB",
        "uploadDate": "2024-02-05",
        "uploadedBy": "John Smith",
        "status": "verified",
        "description": "Photo identification",
        "tags": ["id", "drivers-license"]
    },
    {
        "id": 204,
        "fileName": "Lab_Results_Jan2024.pdf",
        "category": "Medical Records",
        "fileType": "application/pdf",
        "fileSize": "856 KB",
        "uploadDate": "2024-01-25",
        "uploadedBy": "John Smith",
        "status": "reviewed",
        "description": "Lab results from previous provider",
        "tags": ["lab-results", "external", "blood-work"]
    }
]

MOCK_PENDING_FORMS = [
    {
        "id": 301,
        "formId": 2,
        "title": "Medical History Questionnaire",
        "assignedDate": "2024-02-01",
        "dueDate": "2024-02-20",
        "status": "pending",
        "priority": "high",
        "assignedBy": "Dr. Sarah Johnson",
        "reminder": True
    },
    {
        "id": 302,
        "formId": 4,
        "title": "Pre-Visit Symptom Checker",
        "assignedDate": "2024-02-12",
        "dueDate": "2024-02-18",
        "status": "in-progress",
        "priority": "medium",
        "assignedBy": "Dr. Michael Chen",
        "reminder": False,
        "progress": 60
    }
]

@router.get("/available")
async def get_available_forms(
    category: Optional[str] = None,
    required_only: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all available forms for completion"""
    try:
        forms = MOCK_AVAILABLE_FORMS.copy()
        
        # Filter by category
        if category and category != "all":
            forms = [f for f in forms if f["category"] == category]
        
        # Filter by required status
        if required_only is not None:
            forms = [f for f in forms if f["required"] == required_only]
        
        return forms
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching available forms: {str(e)}")

@router.get("/completed")
async def get_completed_forms(
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all completed forms"""
    try:
        forms = MOCK_COMPLETED_FORMS.copy()
        
        # Filter by status
        if status and status != "all":
            forms = [f for f in forms if f["status"] == status]
        
        # Filter by date range
        if date_from:
            forms = [f for f in forms if f["completedDate"] >= date_from]
        if date_to:
            forms = [f for f in forms if f["completedDate"] <= date_to]
        
        # Sort by completed date (newest first)
        forms.sort(key=lambda x: x["completedDate"], reverse=True)
        
        return forms
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching completed forms: {str(e)}")

@router.get("/pending")
async def get_pending_forms(current_user: User = Depends(get_current_user)):
    """Get all pending forms assigned to the user"""
    try:
        forms = MOCK_PENDING_FORMS.copy()
        # Sort by due date
        forms.sort(key=lambda x: x["dueDate"])
        return forms
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pending forms: {str(e)}")

@router.get("/templates/{form_id}")
async def get_form_template(form_id: int, current_user: User = Depends(get_current_user)):
    """Get form template with fields for completion"""
    try:
        form = next((f for f in MOCK_AVAILABLE_FORMS if f["id"] == form_id), None)
        if not form:
            raise HTTPException(status_code=404, detail="Form template not found")
        return form
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching form template: {str(e)}")

@router.post("/submit")
async def submit_form(
    form_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Submit a completed form"""
    try:
        # In a real implementation, this would save to database
        new_submission = {
            "id": len(MOCK_COMPLETED_FORMS) + 101,
            "formId": form_data.get("formId"),
            "title": form_data.get("title"),
            "completedDate": datetime.now().strftime("%Y-%m-%d"),
            "status": "submitted",
            "submittedBy": f"{current_user.first_name} {current_user.last_name}",
            "responses": form_data.get("responses", {})
        }
        
        MOCK_COMPLETED_FORMS.append(new_submission)
        
        return {
            "message": "Form submitted successfully",
            "submissionId": new_submission["id"],
            "status": "submitted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting form: {str(e)}")

@router.post("/save-draft")
async def save_form_draft(
    form_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Save form as draft for later completion"""
    try:
        # In a real implementation, this would save to database
        draft_id = f"draft_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "message": "Draft saved successfully",
            "draftId": draft_id,
            "savedAt": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving draft: {str(e)}")

@router.get("/documents")
async def get_uploaded_documents(
    category: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all uploaded documents"""
    try:
        documents = MOCK_UPLOADED_DOCUMENTS.copy()
        
        # Filter by category
        if category and category != "all":
            documents = [d for d in documents if d["category"] == category]
        
        # Filter by status
        if status and status != "all":
            documents = [d for d in documents if d["status"] == status]
        
        # Sort by upload date (newest first)
        documents.sort(key=lambda x: x["uploadDate"], reverse=True)
        
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documents: {str(e)}")

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Upload a document"""
    try:
        # In a real implementation, this would save the file and store metadata
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        file_size_mb = round(len(await file.read()) / (1024 * 1024), 2)
        
        # Reset file pointer
        await file.seek(0)
        
        new_document = {
            "id": len(MOCK_UPLOADED_DOCUMENTS) + 201,
            "fileName": file.filename,
            "category": category or "Other",
            "fileType": file.content_type,
            "fileSize": f"{file_size_mb} MB",
            "uploadDate": datetime.now().strftime("%Y-%m-%d"),
            "uploadedBy": f"{current_user.first_name} {current_user.last_name}",
            "status": "pending",
            "description": description or "",
            "tags": tags.split(',') if tags else []
        }
        
        MOCK_UPLOADED_DOCUMENTS.append(new_document)
        
        return {
            "message": "Document uploaded successfully",
            "documentId": new_document["id"],
            "fileName": file.filename,
            "fileSize": new_document["fileSize"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, current_user: User = Depends(get_current_user)):
    """Delete an uploaded document"""
    try:
        document_index = next((i for i, doc in enumerate(MOCK_UPLOADED_DOCUMENTS) if doc["id"] == document_id), None)
        if document_index is None:
            raise HTTPException(status_code=404, detail="Document not found")
        
        deleted_document = MOCK_UPLOADED_DOCUMENTS.pop(document_index)
        return {
            "message": "Document deleted successfully",
            "deletedDocument": deleted_document
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@router.get("/documents/{document_id}/download")
async def download_document(document_id: int, current_user: User = Depends(get_current_user)):
    """Download a document"""
    try:
        document = next((doc for doc in MOCK_UPLOADED_DOCUMENTS if doc["id"] == document_id), None)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # In a real implementation, this would return the actual file
        return {
            "downloadUrl": f"/downloads/documents/{document['fileName']}",
            "fileName": document["fileName"],
            "fileType": document["fileType"],
            "message": "File download would be handled here"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")

@router.get("/summary")
async def get_forms_summary(current_user: User = Depends(get_current_user)):
    """Get summary statistics for forms and documents"""
    try:
        available_count = len(MOCK_AVAILABLE_FORMS)
        pending_count = len(MOCK_PENDING_FORMS)
        completed_count = len(MOCK_COMPLETED_FORMS)
        documents_count = len(MOCK_UPLOADED_DOCUMENTS)
        
        # Get required forms that are not completed
        required_forms = [f for f in MOCK_AVAILABLE_FORMS if f["required"]]
        completed_form_ids = [f["formId"] for f in MOCK_COMPLETED_FORMS]
        outstanding_required = len([f for f in required_forms if f["id"] not in completed_form_ids])
        
        return {
            "availableForms": available_count,
            "pendingForms": pending_count,
            "completedForms": completed_count,
            "uploadedDocuments": documents_count,
            "outstandingRequired": outstanding_required,
            "completionRate": round((completed_count / available_count) * 100, 1) if available_count > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forms summary: {str(e)}")

@router.get("/categories")
async def get_form_categories(current_user: User = Depends(get_current_user)):
    """Get list of all form categories"""
    try:
        categories = list(set([f["category"] for f in MOCK_AVAILABLE_FORMS]))
        categories.sort()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching form categories: {str(e)}")

@router.get("/document-categories")
async def get_document_categories(current_user: User = Depends(get_current_user)):
    """Get list of all document categories"""
    try:
        categories = [
            "Insurance",
            "Identification", 
            "Medical Records",
            "Lab Results",
            "Prescriptions",
            "Other"
        ]
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching document categories: {str(e)}")