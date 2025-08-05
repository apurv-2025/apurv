from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Text, UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import uuid
import os
from contextlib import contextmanager

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/fhir_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class AllergyIntolerance(Base):
    __tablename__ = "allergy_intolerances"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    clinical_status = Column(String(50))
    verification_status = Column(String(50))
    type = Column(String(50))
    categories = Column(ARRAY(Text))
    criticality = Column(String(50))
    code = Column(JSONB)
    patient_id = Column(UUID(as_uuid=True), nullable=False)
    encounter_id = Column(UUID(as_uuid=True))
    onset_date_time = Column(DateTime(timezone=True))
    onset_age = Column(JSONB)
    onset_period = Column(JSONB)
    onset_range = Column(JSONB)
    onset_string = Column(String(500))
    recorded_date = Column(DateTime(timezone=True))
    recorder = Column(UUID(as_uuid=True))
    asserter = Column(UUID(as_uuid=True))
    last_occurrence = Column(DateTime(timezone=True))
    notes = Column(JSONB)
    reactions = Column(JSONB)
    fhir_resource = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic Models (THIS is where the validator goes)
class AllergyIntoleranceBase(BaseModel):
    fhir_id: str
    clinical_status: Optional[str] = None
    verification_status: Optional[str] = None
    type: Optional[str] = None
    categories: Optional[List[str]] = None
    criticality: Optional[str] = None
    code: Optional[Dict[str, Any]] = None
    patient_id: str
    encounter_id: Optional[str] = None
    onset_date_time: Optional[datetime] = None
    onset_age: Optional[Dict[str, Any]] = None
    onset_period: Optional[Dict[str, Any]] = None
    onset_range: Optional[Dict[str, Any]] = None
    onset_string: Optional[str] = None
    recorded_date: Optional[datetime] = None
    recorder: Optional[str] = None
    asserter: Optional[str] = None
    last_occurrence: Optional[datetime] = None
    notes: Optional[List[Dict[str, Any]]] = None
    reactions: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None
    
    @field_validator('recorded_date', mode='before')  # ✅ INSIDE the Pydantic class
    @classmethod
    def parse_recorded_date(cls, v):
        if isinstance(v, str):
            # Handle date-only strings from UI
            if len(v) == 10 and v.count('-') == 2:  # "2025-07-01" format
                try:
                    # Convert to datetime at midnight
                    return datetime.strptime(v, "%Y-%m-%d")
                except ValueError:
                    pass
        return v




class AllergyIntoleranceCreate(AllergyIntoleranceBase):
    pass

class AllergyIntoleranceUpdate(AllergyIntoleranceBase):
    pass


class AllergyIntoleranceResponse(AllergyIntoleranceBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="FHIR AllergyIntolerance API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    
# CRUD Operations
@app.post("/allergies", response_model=AllergyIntoleranceResponse)
def create_allergy(allergy: AllergyIntoleranceCreate, db: Session = Depends(get_db)):
    # Check if fhir_id already exists
    existing = db.query(AllergyIntolerance).filter(AllergyIntolerance.fhir_id == allergy.fhir_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="AllergyIntolerance with this FHIR ID already exists")
    
    db_allergy = AllergyIntolerance(**allergy.dict())
    db.add(db_allergy)
    db.commit()
    db.refresh(db_allergy)
    
    # Convert UUID to string for response
    response_data = {
        **{k: v for k, v in db_allergy.__dict__.items() if not k.startswith('_')},
        'id': str(db_allergy.id),
        'patient_id': str(db_allergy.patient_id),
        'encounter_id': str(db_allergy.encounter_id) if db_allergy.encounter_id else None,
        'recorder': str(db_allergy.recorder) if db_allergy.recorder else None,
        'asserter': str(db_allergy.asserter) if db_allergy.asserter else None,
    }
    return AllergyIntoleranceResponse(**response_data)

@app.get("/allergies", response_model=List[AllergyIntoleranceResponse])
def get_allergies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: Optional[str] = None,
    clinical_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AllergyIntolerance)
    
    if patient_id:
        query = query.filter(AllergyIntolerance.patient_id == patient_id)
    if clinical_status:
        query = query.filter(AllergyIntolerance.clinical_status == clinical_status)
    
    allergies = query.offset(skip).limit(limit).all()
    
    response_list = []
    for allergy in allergies:
        response_data = {
            **{k: v for k, v in allergy.__dict__.items() if not k.startswith('_')},
            'id': str(allergy.id),
            'patient_id': str(allergy.patient_id),
            'encounter_id': str(allergy.encounter_id) if allergy.encounter_id else None,
            'recorder': str(allergy.recorder) if allergy.recorder else None,
            'asserter': str(allergy.asserter) if allergy.asserter else None,
        }
        response_list.append(AllergyIntoleranceResponse(**response_data))
    
    return response_list

@app.get("/allergies/{allergy_id}", response_model=AllergyIntoleranceResponse)
def get_allergy(allergy_id: str, db: Session = Depends(get_db)):
    allergy = db.query(AllergyIntolerance).filter(AllergyIntolerance.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="AllergyIntolerance not found")
    
    response_data = {
        **{k: v for k, v in allergy.__dict__.items() if not k.startswith('_')},
        'id': str(allergy.id),
        'patient_id': str(allergy.patient_id),
        'encounter_id': str(allergy.encounter_id) if allergy.encounter_id else None,
        'recorder': str(allergy.recorder) if allergy.recorder else None,
        'asserter': str(allergy.asserter) if allergy.asserter else None,
    }
    return AllergyIntoleranceResponse(**response_data)

@app.put("/allergies/{allergy_id}", response_model=AllergyIntoleranceResponse)
def update_allergy(allergy_id: str, allergy_update: AllergyIntoleranceUpdate, db: Session = Depends(get_db)):
    allergy = db.query(AllergyIntolerance).filter(AllergyIntolerance.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="AllergyIntolerance not found")
    
    update_data = allergy_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(allergy, field, value)
    
    allergy.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(allergy)
    
    response_data = {
        **{k: v for k, v in allergy.__dict__.items() if not k.startswith('_')},
        'id': str(allergy.id),
        'patient_id': str(allergy.patient_id),
        'encounter_id': str(allergy.encounter_id) if allergy.encounter_id else None,
        'recorder': str(allergy.recorder) if allergy.recorder else None,
        'asserter': str(allergy.asserter) if allergy.asserter else None,
    }
    return AllergyIntoleranceResponse(**response_data)

@app.delete("/allergies/{allergy_id}")
def delete_allergy(allergy_id: str, db: Session = Depends(get_db)):
    allergy = db.query(AllergyIntolerance).filter(AllergyIntolerance.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="AllergyIntolerance not found")
    
    db.delete(allergy)
    db.commit()
    return {"message": "AllergyIntolerance deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
