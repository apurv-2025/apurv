# File: app/api/api_v1/endpoints/upload.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.post("/insurance-card")
async def upload_insurance_card(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    """Upload and process insurance card."""
    try:
        # Simple file validation
        if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Read file content
        content = await file.read()
        
        # Mock OCR extraction
        extracted_data = {
            "patient_name": "John Doe",
            "member_id": "123456789",
            "insurance_company": "Sample Insurance"
        }
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "size": len(content),
            "extracted_data": extracted_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insurance-cards")
async def get_insurance_cards(db: Session = Depends(get_db)):
    """Get all processed insurance cards."""
    return {"message": "Insurance cards endpoint", "cards": []}
