from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime, date
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/records", tags=["records"])

# Mock health records data
MOCK_RECORDS = [
    {
        "id": 1,
        "type": "visit",
        "category": "Office Visit",
        "title": "Annual Physical Examination",
        "date": "2024-02-15",
        "provider": "Dr. Sarah Johnson",
        "specialty": "Internal Medicine",
        "facility": "Main Medical Center",
        "status": "Final",
        "summary": "Comprehensive annual physical examination with routine preventive care.",
        "chiefComplaint": "Annual wellness exam",
        "diagnosis": [
            {"code": "Z00.00", "description": "Encounter for general adult medical examination without abnormal findings"}
        ],
        "vitals": {
            "bloodPressure": "118/76",
            "heartRate": "68",
            "temperature": "98.4°F",
            "weight": "165 lbs",
            "height": "5'8\"",
            "bmi": "25.1"
        },
        "assessment": "Patient is in good health overall. Continue current exercise routine and healthy diet.",
        "plan": [
            "Continue current medications",
            "Return in 1 year for routine follow-up",
            "Annual mammogram recommended",
            "Colonoscopy due in 2 years"
        ],
        "medications": ["Lisinopril 10mg daily", "Metformin 500mg twice daily"],
        "allergies": ["Penicillin - Rash"],
        "notes": "Patient reports feeling well. No acute concerns. Discussed preventive care measures.",
        "downloadUrl": "/records/visit-2024-02-15.pdf"
    },
    {
        "id": 2,
        "type": "visit",
        "category": "Cardiology Consultation",
        "title": "Hypertension Follow-up",
        "date": "2024-01-20",
        "provider": "Dr. Sarah Johnson",
        "specialty": "Cardiology",
        "facility": "Cardiology Associates",
        "status": "Final",
        "summary": "Follow-up visit for blood pressure management.",
        "chiefComplaint": "Blood pressure check",
        "diagnosis": [
            {"code": "I10", "description": "Essential hypertension"}
        ],
        "vitals": {
            "bloodPressure": "128/82",
            "heartRate": "72",
            "weight": "167 lbs"
        },
        "assessment": "Blood pressure well controlled on current regimen.",
        "plan": [
            "Continue Lisinopril 10mg daily",
            "Follow-up in 3 months",
            "Home blood pressure monitoring"
        ],
        "medications": ["Lisinopril 10mg daily"],
        "allergies": ["Penicillin - Rash"],
        "downloadUrl": "/records/visit-2024-01-20.pdf"
    },
    {
        "id": 3,
        "type": "immunization",
        "category": "Vaccination",
        "title": "COVID-19 Vaccine (Booster)",
        "date": "2024-01-15",
        "provider": "Dr. Michael Chen",
        "specialty": "Internal Medicine",
        "facility": "Vaccination Clinic",
        "status": "Administered",
        "vaccine": {
            "name": "COVID-19 mRNA Vaccine",
            "manufacturer": "Pfizer-BioNTech",
            "lotNumber": "FF9899",
            "dose": "Booster (3rd dose)",
            "site": "Left deltoid",
            "route": "Intramuscular"
        },
        "nextDue": "2024-07-15",
        "reactions": "None reported",
        "notes": "Patient tolerated vaccine well. No immediate adverse reactions observed.",
        "downloadUrl": "/records/immunization-2024-01-15.pdf"
    },
    {
        "id": 4,
        "type": "immunization",
        "category": "Vaccination",
        "title": "Influenza Vaccine",
        "date": "2023-10-01",
        "provider": "Dr. Michael Chen",
        "specialty": "Internal Medicine",
        "facility": "Main Medical Center",
        "status": "Administered",
        "vaccine": {
            "name": "Influenza Vaccine (Quadrivalent)",
            "manufacturer": "Sanofi Pasteur",
            "lotNumber": "UJ015AA",
            "dose": "Annual dose",
            "site": "Right deltoid",
            "route": "Intramuscular"
        },
        "nextDue": "2024-09-01",
        "reactions": "Mild soreness at injection site",
        "notes": "Annual influenza vaccination. Patient advised to expect mild local reaction.",
        "downloadUrl": "/records/immunization-2023-10-01.pdf"
    },
    {
        "id": 5,
        "type": "allergy",
        "category": "Allergy",
        "title": "Drug Allergy - Penicillin",
        "date": "2020-03-15",
        "provider": "Dr. Emily Davis",
        "specialty": "Allergy & Immunology",
        "facility": "Allergy Center",
        "status": "Active",
        "allergen": "Penicillin",
        "reaction": "Skin rash, hives",
        "severity": "Moderate",
        "onset": "Childhood",
        "notes": "Patient developed rash and hives after taking penicillin as a child. Avoid all penicillin-based antibiotics.",
        "alternatives": ["Cephalexin", "Azithromycin", "Ciprofloxacin"],
        "downloadUrl": "/records/allergy-penicillin.pdf"
    },
    {
        "id": 6,
        "type": "condition",
        "category": "Medical Condition",
        "title": "Type 2 Diabetes Mellitus",
        "date": "2022-06-10",
        "provider": "Dr. Michael Chen",
        "specialty": "Endocrinology",
        "facility": "Diabetes Center",
        "status": "Active",
        "condition": "Type 2 Diabetes Mellitus",
        "icd10": "E11.9",
        "severity": "Mild to Moderate",
        "onset": "2022-06-10",
        "management": "Diet, exercise, and medication",
        "currentMedications": ["Metformin 500mg twice daily"],
        "monitoring": "Quarterly HbA1c, annual eye exam, annual foot exam",
        "notes": "Well-controlled diabetes with lifestyle modifications and metformin.",
        "downloadUrl": "/records/condition-diabetes.pdf"
    },
    {
        "id": 7,
        "type": "imaging",
        "category": "Radiology",
        "title": "Mammogram Screening",
        "date": "2024-01-25",
        "provider": "Dr. Jennifer Wilson",
        "specialty": "Radiology",
        "facility": "Imaging Center",
        "status": "Final",
        "procedure": "Bilateral Diagnostic Mammography",
        "findings": "No suspicious masses or calcifications identified.",
        "impression": "BIRADS Category 1 - Negative",
        "recommendation": "Continue routine annual screening",
        "notes": "Normal screening mammogram. Next screening due in 12 months.",
        "downloadUrl": "/records/imaging-2024-01-25.pdf"
    },
    {
        "id": 8,
        "type": "procedure",
        "category": "Procedure",
        "title": "Colonoscopy Screening",
        "date": "2023-08-15",
        "provider": "Dr. Robert Smith",
        "specialty": "Gastroenterology",
        "facility": "Endoscopy Center",
        "status": "Complete",
        "procedure": "Screening Colonoscopy",
        "indication": "Routine screening - age 50+",
        "findings": "Two small polyps removed from sigmoid colon",
        "pathology": "Benign adenomatous polyps",
        "complications": "None",
        "recommendation": "Repeat colonoscopy in 5 years",
        "postOpInstructions": "Resume normal diet, follow-up if any concerning symptoms",
        "downloadUrl": "/records/procedure-2023-08-15.pdf"
    },
    {
        "id": 9,
        "type": "lab",
        "category": "Laboratory",
        "title": "Hemoglobin A1C",
        "date": "2024-02-10",
        "provider": "Dr. Michael Chen",
        "specialty": "Endocrinology",
        "facility": "Lab Corp",
        "status": "Final",
        "results": [
            {"test": "Hemoglobin A1C", "value": "6.8", "unit": "%", "range": "<7.0", "status": "normal"}
        ],
        "interpretation": "Good diabetes control. Continue current management.",
        "notes": "Patient continues to show excellent diabetes management.",
        "downloadUrl": "/records/lab-2024-02-10.pdf"
    }
]

@router.get("/")
async def get_health_records(
    record_type: Optional[str] = None,
    provider: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all health records for the current user with optional filtering"""
    try:
        records = MOCK_RECORDS.copy()
        
        # Filter by record type
        if record_type and record_type != "all":
            records = [r for r in records if r["type"] == record_type]
        
        # Filter by provider
        if provider and provider != "all":
            records = [r for r in records if r["provider"] == provider]
        
        # Filter by date range
        if date_from:
            records = [r for r in records if r["date"] >= date_from]
        if date_to:
            records = [r for r in records if r["date"] <= date_to]
        
        # Search functionality
        if search:
            search_lower = search.lower()
            records = [
                r for r in records 
                if (search_lower in r["title"].lower() or
                    search_lower in r["category"].lower() or
                    search_lower in r["provider"].lower() or
                    search_lower in r.get("specialty", "").lower() or
                    search_lower in r.get("summary", "").lower() or
                    search_lower in r.get("notes", "").lower())
            ]
        
        # Sort by date (newest first)
        records.sort(key=lambda x: x["date"], reverse=True)
        
        return records
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching health records: {str(e)}")

@router.get("/visits")
async def get_visit_summaries(current_user: User = Depends(get_current_user)):
    """Get all visit summaries"""
    try:
        visits = [r for r in MOCK_RECORDS if r["type"] == "visit"]
        visits.sort(key=lambda x: x["date"], reverse=True)
        return visits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching visit summaries: {str(e)}")

@router.get("/immunizations")
async def get_immunizations(current_user: User = Depends(get_current_user)):
    """Get all immunization records"""
    try:
        immunizations = [r for r in MOCK_RECORDS if r["type"] == "immunization"]
        immunizations.sort(key=lambda x: x["date"], reverse=True)
        return immunizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching immunizations: {str(e)}")

@router.get("/allergies")
async def get_allergies(current_user: User = Depends(get_current_user)):
    """Get all allergy records"""
    try:
        allergies = [r for r in MOCK_RECORDS if r["type"] == "allergy"]
        allergies.sort(key=lambda x: x["date"], reverse=True)
        return allergies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching allergies: {str(e)}")

@router.get("/conditions")
async def get_medical_conditions(current_user: User = Depends(get_current_user)):
    """Get all medical condition records"""
    try:
        conditions = [r for r in MOCK_RECORDS if r["type"] == "condition"]
        conditions.sort(key=lambda x: x["date"], reverse=True)
        return conditions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching medical conditions: {str(e)}")

@router.get("/summary")
async def get_records_summary(current_user: User = Depends(get_current_user)):
    """Get summary statistics for all health records"""
    try:
        total_records = len(MOCK_RECORDS)
        visits = len([r for r in MOCK_RECORDS if r["type"] == "visit"])
        immunizations = len([r for r in MOCK_RECORDS if r["type"] == "immunization"])
        active_allergies = len([r for r in MOCK_RECORDS if r["type"] == "allergy" and r["status"] == "Active"])
        active_conditions = len([r for r in MOCK_RECORDS if r["type"] == "condition" and r["status"] == "Active"])
        
        # Get recent records (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        recent_records = [r for r in MOCK_RECORDS if r["date"] >= thirty_days_ago]
        
        return {
            "totalRecords": total_records,
            "visits": visits,
            "immunizations": immunizations,
            "activeAllergies": active_allergies,
            "activeConditions": active_conditions,
            "recentRecords": len(recent_records),
            "lastUpdated": max([r["date"] for r in MOCK_RECORDS]) if MOCK_RECORDS else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching records summary: {str(e)}")

@router.get("/{record_id}")
async def get_record_detail(record_id: int, current_user: User = Depends(get_current_user)):
    """Get detailed information for a specific health record"""
    try:
        record = next((r for r in MOCK_RECORDS if r["id"] == record_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching record detail: {str(e)}")

@router.get("/download/{record_id}")
async def download_record(record_id: int, current_user: User = Depends(get_current_user)):
    """Download a specific health record as PDF"""
    try:
        record = next((r for r in MOCK_RECORDS if r["id"] == record_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # In a real implementation, this would generate and return a PDF file
        return {
            "downloadUrl": record.get("downloadUrl", f"/records/record-{record_id}.pdf"),
            "filename": f"{record['title'].replace(' ', '_')}_{record['date']}.pdf",
            "message": "PDF generation would be handled here"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading record: {str(e)}")

@router.get("/download/all")
async def download_all_records(current_user: User = Depends(get_current_user)):
    """Download all health records as a comprehensive PDF"""
    try:
        # In a real implementation, this would compile all records into a single PDF
        return {
            "downloadUrl": "/records/complete_health_record.pdf",
            "filename": f"Complete_Health_Record_{datetime.now().strftime('%Y%m%d')}.pdf",
            "recordCount": len(MOCK_RECORDS),
            "message": "Complete health record PDF compilation would be handled here"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading all records: {str(e)}")

@router.get("/providers")
async def get_providers(current_user: User = Depends(get_current_user)):
    """Get list of all providers from health records"""
    try:
        providers = list(set([r["provider"] for r in MOCK_RECORDS]))
        providers.sort()
        return {"providers": providers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching providers: {str(e)}")

@router.get("/types")
async def get_record_types(current_user: User = Depends(get_current_user)):
    """Get list of all record types"""
    try:
        types = list(set([r["type"] for r in MOCK_RECORDS]))
        type_info = [
            {"value": "all", "label": "All Records"},
            {"value": "visit", "label": "Visit Summaries"},
            {"value": "immunization", "label": "Immunizations"},
            {"value": "allergy", "label": "Allergies"},
            {"value": "condition", "label": "Medical Conditions"},
            {"value": "lab", "label": "Lab Results"},
            {"value": "imaging", "label": "Imaging"},
            {"value": "procedure", "label": "Procedures"}
        ]
        return {"types": type_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching record types: {str(e)}")