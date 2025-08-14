# main.py
from fastapi import FastAPI, Depends, HTTPException, Query, Path, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.database import get_db  # Fixed import path
from app.models.models import Charge, Provider, Patient, Encounter, ChargeTemplate, ChargeValidationRule
from app.services import ChargeService, ChargeTemplateService, ReportingService
from app.schemas import (
    ChargeCreate, ChargeUpdate, ChargeResponse, ChargeSearchParams, ChargeSearchResponse,
    ChargeTemplateCreate, ChargeTemplateResponse, BatchChargeCreate, BatchChargeResponse,
    ChargeValidation, ChargeMetrics, ProviderMetrics, EncounterResponse, PatientResponse
)
from app.api.agent import router as agent_router

app = FastAPI(title="Charge Capture API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get current user (implement based on your auth system)
def get_current_user():
    # This should return the current authenticated user
    # For now, returning a mock user ID
    return uuid.uuid4()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include AI Agent routes
app.include_router(agent_router)

# Charge endpoints
@app.post("/charges", response_model=ChargeResponse)
async def create_charge(
    charge_data: ChargeCreate,
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user)
):
    """Create a new charge"""
    try:
        charge_service = ChargeService(db)
        charge = charge_service.create_charge(charge_data, current_user)
        return ChargeResponse.from_orm(charge)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/charges/{charge_id}", response_model=ChargeResponse)
async def get_charge(
    charge_id: uuid.UUID = Path(..., description="Charge ID"),
    db: Session = Depends(get_db)
):
    """Get a specific charge by ID"""
    charge_service = ChargeService(db)
    charge = charge_service.get_charge(charge_id)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    return ChargeResponse.from_orm(charge)

@app.put("/charges/{charge_id}", response_model=ChargeResponse)
async def update_charge(
    charge_id: uuid.UUID = Path(..., description="Charge ID"),
    charge_data: ChargeUpdate = ...,
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user)
):
    """Update an existing charge"""
    charge_service = ChargeService(db)
    charge = charge_service.update_charge(charge_id, charge_data, current_user)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    return ChargeResponse.from_orm(charge)

@app.get("/charges", response_model=ChargeSearchResponse)
async def search_charges(
    patient_id: Optional[uuid.UUID] = Query(None),
    provider_id: Optional[uuid.UUID] = Query(None),
    encounter_id: Optional[uuid.UUID] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    cpt_code: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search and filter charges"""
    params = ChargeSearchParams(
        patient_id=patient_id,
        provider_id=provider_id,
        encounter_id=encounter_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
        cpt_code=cpt_code,
        specialty=specialty,
        page=page,
        page_size=page_size
    )
    
    charge_service = ChargeService(db)
    charges, total_count = charge_service.search_charges(params)
    
    return ChargeSearchResponse(
        charges=[ChargeResponse.from_orm(charge) for charge in charges],
        total_count=total_count,
        page=page,
        page_size=page_size,
        total_pages=(total_count + page_size - 1) // page_size
    )

@app.post("/charges/validate", response_model=ChargeValidation)
async def validate_charge(
    charge_data: ChargeCreate,
    db: Session = Depends(get_db)
):
    """Validate charge data without creating it"""
    charge_service = ChargeService(db)
    return charge_service.validate_charge(charge_data)

@app.post("/charges/batch", response_model=BatchChargeResponse)
async def create_batch_charges(
    batch_data: BatchChargeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user)
):
    """Create multiple charges in batch"""
    charge_service = ChargeService(db)
    created_charges = []
    errors = []
    
    for i, charge_data in enumerate(batch_data.charges):
        try:
            charge = charge_service.create_charge(charge_data, current_user)
            created_charges.append(ChargeResponse.from_orm(charge))
        except Exception as e:
            errors.append({
                "index": i,
                "charge_data": charge_data.dict(),
                "error": str(e)
            })
    
    return BatchChargeResponse(
        success_count=len(created_charges),
        error_count=len(errors),
        created_charges=created_charges,
        errors=errors
    )

@app.post("/charges/{charge_id}/submit")
async def submit_charge_to_billing(
    charge_id: uuid.UUID = Path(..., description="Charge ID"),
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user)
):
    """Submit charge to billing system"""
    charge_service = ChargeService(db)
    charge = charge_service.get_charge(charge_id)
    
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    
    if charge.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft charges can be submitted")
    
    # Update charge status
    update_data = ChargeUpdate(status="submitted")
    updated_charge = charge_service.update_charge(charge_id, update_data, current_user)
    
    # Here you would integrate with your billing system
    # billing_service.submit_charge(charge)
    
    return {"message": "Charge submitted to billing", "charge_id": str(charge_id)}

# Template endpoints
@app.post("/templates", response_model=ChargeTemplateResponse)
async def create_template(
    template_data: ChargeTemplateCreate,
    db: Session = Depends(get_db),
    current_user: uuid.UUID = Depends(get_current_user)
):
    """Create a new charge template"""
    template_service = ChargeTemplateService(db)
    template = template_service.create_template(template_data)
    return ChargeTemplateResponse.from_orm(template)

@app.get("/templates", response_model=List[ChargeTemplateResponse])
async def get_templates(
    provider_id: Optional[uuid.UUID] = Query(None),
    specialty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get templates for a provider or specialty"""
    template_service = ChargeTemplateService(db)
    
    if provider_id and specialty:
        templates = template_service.get_templates_for_provider(provider_id, specialty)
    else:
        # Get all active templates
        templates = db.query(ChargeTemplate).filter(ChargeTemplate.is_active == True).all()
    
    return [ChargeTemplateResponse.from_orm(template) for template in templates]

@app.put("/templates/{template_id}", response_model=ChargeTemplateResponse)
async def update_template(
    template_id: uuid.UUID = Path(..., description="Template ID"),
    updates: dict = ...,
    db: Session = Depends(get_db)
):
    """Update a template"""
    template_service = ChargeTemplateService(db)
    template = template_service.update_template(template_id, updates)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return ChargeTemplateResponse.from_orm(template)

# Encounter endpoints
@app.get("/encounters/{encounter_id}/charges", response_model=List[ChargeResponse])
async def get_encounter_charges(
    encounter_id: uuid.UUID = Path(..., description="Encounter ID"),
    db: Session = Depends(get_db)
):
    """Get all charges for a specific encounter"""
    charges = db.query(Charge).filter(Charge.encounter_id == encounter_id).all()
    return [ChargeResponse.from_orm(charge) for charge in charges]

@app.get("/encounters/without-charges")
async def get_encounters_without_charges(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    specialty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get encounters without charges (missed charges)"""
    charge_service = ChargeService(db)
    missed_charges = charge_service.get_missed_charges(date_from, date_to)
    
    if specialty:
        missed_charges = [mc for mc in missed_charges if mc.get('specialty') == specialty]
    
    return {
        "missed_charges": missed_charges,
        "count": len(missed_charges),
        "date_range": {"from": date_from, "to": date_to}
    }

# Reporting endpoints
@app.get("/reports/charge-metrics", response_model=ChargeMetrics)
async def get_charge_metrics(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    specialty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get charge capture metrics"""
    reporting_service = ReportingService(db)
    metrics = reporting_service.get_charge_metrics(date_from, date_to, specialty)
    return ChargeMetrics(**metrics)

@app.get("/reports/provider-metrics")
async def get_provider_metrics(
    date_from: datetime = Query(..., description="Start date"),
    date_to: datetime = Query(..., description="End date"),
    provider_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """Get provider-specific metrics"""
    # Implementation for provider metrics
    query = db.query(Provider)
    if provider_id:
        query = query.filter(Provider.id == provider_id)
    
    providers = query.all()
    metrics = []
    
    for provider in providers:
        # Calculate metrics for each provider
        provider_charges = db.query(Charge)\
            .filter(
                Charge.provider_id == provider.id,
                Charge.captured_at.between(date_from, date_to)
            ).all()
        
        total_charges = len(provider_charges)
        
        # Calculate encounters for this provider
        encounters = db.query(Encounter)\
            .filter(
                Encounter.provider_id == provider.id,
                Encounter.encounter_date.between(date_from, date_to),
                Encounter.status == "completed"
            ).count()
        
        avg_charges_per_encounter = total_charges / encounters if encounters > 0 else 0
        charge_capture_rate = (total_charges / encounters * 100) if encounters > 0 else 0
        
        # Calculate average time to capture
        capture_times = []
        for charge in provider_charges:
            if charge.encounter and charge.encounter.encounter_date:
                time_diff = (charge.captured_at - charge.encounter.encounter_date).total_seconds() / 60
                capture_times.append(time_diff)
        
        avg_time_to_capture = sum(capture_times) / len(capture_times) if capture_times else None
        
        metrics.append(ProviderMetrics(
            provider_id=provider.id,
            provider_name=f"{provider.first_name} {provider.last_name}",
            specialty=provider.specialty,
            total_charges=total_charges,
            avg_charges_per_encounter=avg_charges_per_encounter,
            charge_capture_rate=charge_capture_rate,
            avg_time_to_capture=avg_time_to_capture
        ))
    
    return metrics

# Medical code integration endpoints
@app.get("/codes/cpt/search")
async def search_cpt_codes(
    query: str = Query(..., description="Search term"),
    specialty: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50)
):
    """Search CPT codes - integrates with your existing medical code service"""
    # This would call your existing MedicalCode Service
    # medical_code_service.search_cpt_codes(query, specialty, limit)
    
    # Mock response for now
    return {
        "codes": [
            {"code": "99213", "description": "Office visit, established patient"},
            {"code": "99214", "description": "Office visit, established patient, detailed"},
        ],
        "total": 2
    }

@app.get("/codes/icd/search")
async def search_icd_codes(
    query: str = Query(..., description="Search term"),
    limit: int = Query(10, ge=1, le=50)
):
    """Search ICD codes"""
    # Integration with your medical code service
    return {
        "codes": [
            {"code": "Z00.00", "description": "Encounter for general adult medical examination"},
            {"code": "M79.3", "description": "Panniculitis, unspecified"},
        ],
        "total": 2
    }

@app.get("/codes/favorites/{provider_id}")
async def get_provider_favorite_codes(
    provider_id: uuid.UUID = Path(..., description="Provider ID"),
    db: Session = Depends(get_db)
):
    """Get frequently used codes for a provider"""
    # Query most used codes by this provider
    frequent_cpt = db.query(Charge.cpt_code, func.count(Charge.cpt_code).label('count'))\
        .filter(Charge.provider_id == provider_id)\
        .group_by(Charge.cpt_code)\
        .order_by(func.count(Charge.cpt_code).desc())\
        .limit(10)\
        .all()
    
    frequent_icd = db.query(Charge.icd_code, func.count(Charge.icd_code).label('count'))\
        .filter(Charge.provider_id == provider_id)\
        .group_by(Charge.icd_code)\
        .order_by(func.count(Charge.icd_code).desc())\
        .limit(10)\
        .all()
    
    return {
        "cpt_codes": [{"code": code, "usage_count": count} for code, count in frequent_cpt],
        "icd_codes": [{"code": code, "usage_count": count} for code, count in frequent_icd]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
