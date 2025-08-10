# File: app/api/api_v1/endpoints/patient_information.py - Patient Information Endpoints
from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import EDIException
from app.services.edi_275_service import EDI275Service
from app.crud.crud_patient_information import patient_information
from app.schemas.patient_information import (
    PatientInformationCreate,
    PatientInformationUpdate,
    PatientInformation,
    PatientEDI275Response
)
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()
edi_275_service = EDI275Service()


@router.post("/", response_model=PatientInformation)
async def create_patient_information(
    *,
    db: Session = Depends(get_db),
    patient_data: PatientInformationCreate
) -> Any:
    """
    Create patient information record and generate EDI 275.
    
    - **first_name**: Patient first name
    - **last_name**: Patient last name
    - **date_of_birth**: Patient date of birth
    - **gender**: Patient gender (M/F/U)
    - **address information**: Patient contact details
    - **insurance_information**: Primary and secondary insurance
    - **medical_information**: Conditions, allergies, medications
    
    Returns patient information with generated EDI 275.
    """
    try:
        logger.info(f"Creating patient information for: {patient_data.first_name} {patient_data.last_name}")
        
        # Generate unique patient ID
        patient_id = str(uuid.uuid4())
        
        # Generate EDI 275
        edi_275_content, transaction_id = edi_275_service.generate_edi_275(patient_data)
        
        # Create database record
        from app.models.models import PatientInformation
        db_patient = PatientInformation(
            patient_id=patient_id,
            first_name=patient_data.first_name,
            last_name=patient_data.last_name,
            middle_name=patient_data.middle_name,
            date_of_birth=patient_data.date_of_birth,
            gender=patient_data.gender.value,
            ssn=patient_data.ssn,
            address_line1=patient_data.address_line1,
            address_line2=patient_data.address_line2,
            city=patient_data.city,
            state=patient_data.state,
            zip_code=patient_data.zip_code,
            phone_home=patient_data.phone_home,
            phone_work=patient_data.phone_work,
            phone_mobile=patient_data.phone_mobile,
            email=patient_data.email,
            primary_insurance=patient_data.primary_insurance.dict() if patient_data.primary_insurance else None,
            secondary_insurance=patient_data.secondary_insurance.dict() if patient_data.secondary_insurance else None,
            member_id_primary=patient_data.member_id_primary,
            member_id_secondary=patient_data.member_id_secondary,
            emergency_contact_name=patient_data.emergency_contact.name if patient_data.emergency_contact else None,
            emergency_contact_phone=patient_data.emergency_contact.phone if patient_data.emergency_contact else None,
            emergency_contact_relationship=patient_data.emergency_contact.relationship if patient_data.emergency_contact else None,
            primary_care_provider=patient_data.primary_care_provider,
            allergies=[allergy.dict() for allergy in patient_data.allergies] if patient_data.allergies else None,
            medical_conditions=[condition.dict() for condition in patient_data.medical_conditions] if patient_data.medical_conditions else None,
            medications=[med.dict() for med in patient_data.medications] if patient_data.medications else None,
            edi_275_content=edi_275_content,
            last_edi_update=datetime.utcnow(),
            hipaa_authorization=patient_data.hipaa_authorization,
            consent_date=patient_data.consent_date
        )
        
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        
        logger.info(f"Patient information created with ID: {patient_id}")
        return db_patient
        
    except EDIException as e:
        logger.error(f"EDI error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate EDI 275: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error creating patient information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create patient information: {str(e)}"
        )


@router.get("/edi-275/{patient_id}", response_model=PatientEDI275Response)
async def get_patient_edi_275(
    *,
    db: Session = Depends(get_db),
    patient_id: str
) -> Any:
    """
    Get EDI 275 transaction for a patient.
    
    - **patient_id**: The patient ID
    
    Returns EDI 275 content for the patient.
    """
    try:
        logger.info(f"Getting EDI 275 for patient: {patient_id}")
        
        # Get patient information
        patient = patient_information.get_by_patient_id(db=db, patient_id=patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Return existing EDI 275 or generate new one
        if patient.edi_275_content:
            edi_275_content = patient.edi_275_content
            generated_at = patient.last_edi_update or patient.created_at
        else:
            # Regenerate EDI 275 if not available
            patient_schema = PatientInformationCreate(
                first_name=patient.first_name,
                last_name=patient.last_name,
                middle_name=patient.middle_name,
                date_of_birth=patient.date_of_birth,
                gender=patient.gender,
                member_id_primary=patient.member_id_primary,
                # Add other fields as needed
            )
            edi_275_content, _ = edi_275_service.generate_edi_275(patient_schema)
            generated_at = datetime.utcnow()
            
            # Update patient record
            patient.edi_275_content = edi_275_content
            patient.last_edi_update = generated_at
            db.commit()
        
        return PatientEDI275Response(
            patient_id=patient_id,
            edi_275=edi_275_content,
            message="EDI 275 retrieved successfully",
            generated_at=generated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting EDI 275 for patient {patient_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get EDI 275 for patient: {str(e)}"
        )


@router.get("/", response_model=List[PatientInformation])
async def get_patients(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    first_name: str = Query(None, description="Filter by first name"),
    last_name: str = Query(None, description="Filter by last name"),
    member_id: str = Query(None, description="Filter by member ID")
) -> Any:
    """Get patients with optional filtering."""
    try:
        if member_id:
            patient = patient_information.get_by_member_id(db=db, member_id=member_id)
            return [patient] if patient else []
        elif first_name or last_name:
            patients = patient_information.search_by_name(
                db=db, 
                first_name=first_name, 
                last_name=last_name
            )
            return patients[skip:skip+limit]
        else:
            return patient_information.get_multi(db=db, skip=skip, limit=limit)
        
    except Exception as e:
        logger.error(f"Error retrieving patients: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve patients"
        )


@router.get("/{patient_id}", response_model=PatientInformation)
async def get_patient(
    *,
    db: Session = Depends(get_db),
    patient_id: str
) -> Any:
    """Get specific patient by ID."""
    try:
        patient = patient_information.get_by_patient_id(db=db, patient_id=patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        return patient
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve patient"
        )


@router.put("/{patient_id}", response_model=PatientInformation)
async def update_patient(
    *,
    db: Session = Depends(get_db),
    patient_id: str,
    patient_update: PatientInformationUpdate
) -> Any:
    """Update patient information."""
    try:
        patient = patient_information.get_by_patient_id(db=db, patient_id=patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        updated_patient = patient_information.update(
            db=db, 
            db_obj=patient, 
            obj_in=patient_update
        )
        
        return updated_patient
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating patient {patient_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update patient"
        )


