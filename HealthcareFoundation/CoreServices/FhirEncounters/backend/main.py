# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, DECIMAL, UUID, Text, Time, ForeignKey, CheckConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from uuid import UUID as PyUUID, uuid4
import os

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/fhir_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Encounter(Base):
    __tablename__ = "encounters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False)
    class_ = Column("class", JSONB)
    type = Column(JSONB)
    service_type = Column(JSONB)
    priority = Column(JSONB)
    subject_patient_id = Column(UUID(as_uuid=True), nullable=False)
    episode_of_care = Column(JSONB)
    incoming_referral = Column(JSONB)
    participants = Column(JSONB)
    appointment = Column(UUID(as_uuid=True))
    period_start = Column(TIMESTAMP(timezone=True))
    period_end = Column(TIMESTAMP(timezone=True))
    length_value = Column(DECIMAL)
    length_unit = Column(String(50))
    reason_code = Column(JSONB)
    reason_reference = Column(JSONB)
    diagnosis = Column(JSONB)
    account = Column(JSONB)
    hospitalization = Column(JSONB)
    locations = Column(JSONB)
    service_provider = Column(UUID(as_uuid=True))
    part_of = Column(UUID(as_uuid=True))
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled', 'entered-in-error', 'unknown')"),
        Index('idx_encounters_fhir_id', 'fhir_id'),
        Index('idx_encounters_patient', 'subject_patient_id'),
        Index('idx_encounters_status', 'status'),
        Index('idx_encounters_period', 'period_start', 'period_end'),
    )

class Observation(Base):
    __tablename__ = "observations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False)
    category = Column(JSONB)
    code = Column(JSONB, nullable=False)
    subject_patient_id = Column(UUID(as_uuid=True), nullable=False)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey('encounters.id'))
    effective_date_time = Column(TIMESTAMP(timezone=True))
    effective_period_start = Column(TIMESTAMP(timezone=True))
    effective_period_end = Column(TIMESTAMP(timezone=True))
    effective_instant = Column(TIMESTAMP(timezone=True))
    issued = Column(TIMESTAMP(timezone=True))
    performers = Column(JSONB)
    value_quantity_value = Column(DECIMAL)
    value_quantity_unit = Column(String(100))
    value_quantity_system = Column(String(500))
    value_quantity_code = Column(String(100))
    value_codeable_concept = Column(JSONB)
    value_string = Column(Text)
    value_boolean = Column(Boolean)
    value_integer = Column(Integer)
    value_range = Column(JSONB)
    value_ratio = Column(JSONB)
    value_sampled_data = Column(JSONB)
    value_time = Column(Time)
    value_date_time = Column(TIMESTAMP(timezone=True))
    value_period = Column(JSONB)
    data_absent_reason = Column(JSONB)
    interpretation = Column(JSONB)
    notes = Column(JSONB)
    body_site = Column(JSONB)
    method = Column(JSONB)
    specimen = Column(UUID(as_uuid=True))
    device = Column(UUID(as_uuid=True))
    reference_ranges = Column(JSONB)
    has_member = Column(JSONB)
    derived_from = Column(JSONB)
    components = Column(JSONB)
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    encounter = relationship("Encounter", backref="observations")
    
    __table_args__ = (
        CheckConstraint("status IN ('registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown')"),
        Index('idx_observations_fhir_id', 'fhir_id'),
        Index('idx_observations_patient', 'subject_patient_id'),
        Index('idx_observations_encounter', 'encounter_id'),
        Index('idx_observations_effective', 'effective_date_time'),
        Index('idx_observations_status', 'status'),
    )

class Condition(Base):
    __tablename__ = "conditions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    clinical_status = Column(String(50))
    verification_status = Column(String(50))
    category = Column(JSONB)
    severity = Column(JSONB)
    code = Column(JSONB)
    body_sites = Column(JSONB)
    subject_patient_id = Column(UUID(as_uuid=True), nullable=False)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey('encounters.id'))
    onset_date_time = Column(TIMESTAMP(timezone=True))
    onset_age = Column(JSONB)
    onset_period = Column(JSONB)
    onset_range = Column(JSONB)
    onset_string = Column(String(500))
    abatement_date_time = Column(TIMESTAMP(timezone=True))
    abatement_age = Column(JSONB)
    abatement_period = Column(JSONB)
    abatement_range = Column(JSONB)
    abatement_string = Column(String(500))
    abatement_boolean = Column(Boolean)
    recorded_date = Column(DateTime)
    recorder = Column(UUID(as_uuid=True))
    asserter = Column(UUID(as_uuid=True))
    stages = Column(JSONB)
    evidence = Column(JSONB)
    notes = Column(JSONB)
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    encounter = relationship("Encounter", backref="conditions")
    
    __table_args__ = (
        CheckConstraint("clinical_status IN ('active', 'recurrence', 'relapse', 'inactive', 'remission', 'resolved', 'unknown')"),
        CheckConstraint("verification_status IN ('unconfirmed', 'provisional', 'differential', 'confirmed', 'refuted', 'entered-in-error')"),
    )

# Pydantic Models
class EncounterBase(BaseModel):
    fhir_id: str
    status: str
    class_: Optional[Dict[str, Any]] = Field(None, alias="class")
    type: Optional[List[Dict[str, Any]]] = None
    service_type: Optional[Dict[str, Any]] = None
    priority: Optional[Dict[str, Any]] = None
    subject_patient_id: PyUUID
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    length_value: Optional[float] = None
    length_unit: Optional[str] = None
    reason_code: Optional[List[Dict[str, Any]]] = None
    diagnosis: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class EncounterCreate(EncounterBase):
    pass

class EncounterUpdate(BaseModel):
    status: Optional[str] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    diagnosis: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class EncounterResponse(EncounterBase):
    id: PyUUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ObservationBase(BaseModel):
    fhir_id: str
    status: str
    category: Optional[List[Dict[str, Any]]] = None
    code: Dict[str, Any]
    subject_patient_id: PyUUID
    encounter_id: Optional[PyUUID] = None
    effective_date_time: Optional[datetime] = None
    value_quantity_value: Optional[float] = None
    value_quantity_unit: Optional[str] = None
    value_string: Optional[str] = None
    value_boolean: Optional[bool] = None
    interpretation: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class ObservationCreate(ObservationBase):
    pass

class ObservationUpdate(BaseModel):
    status: Optional[str] = None
    effective_date_time: Optional[datetime] = None
    value_quantity_value: Optional[float] = None
    value_quantity_unit: Optional[str] = None
    value_string: Optional[str] = None
    interpretation: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class ObservationResponse(ObservationBase):
    id: PyUUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConditionBase(BaseModel):
    fhir_id: str
    clinical_status: Optional[str] = None
    verification_status: Optional[str] = None
    category: Optional[List[Dict[str, Any]]] = None
    severity: Optional[Dict[str, Any]] = None
    code: Optional[Dict[str, Any]] = None
    subject_patient_id: PyUUID
    encounter_id: Optional[PyUUID] = None
    onset_date_time: Optional[datetime] = None
    recorded_date: Optional[date] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class ConditionCreate(ConditionBase):
    pass

class ConditionUpdate(BaseModel):
    clinical_status: Optional[str] = None
    verification_status: Optional[str] = None
    severity: Optional[Dict[str, Any]] = None
    onset_date_time: Optional[datetime] = None
    recorded_date: Optional[date] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class ConditionResponse(ConditionBase):
    id: PyUUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(title="FHIR Microservice", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Encounter Endpoints
@app.post("/encounters/", response_model=EncounterResponse)
def create_encounter(encounter: EncounterCreate, db: Session = Depends(get_db)):
    db_encounter = Encounter(**encounter.dict())
    db.add(db_encounter)
    db.commit()
    db.refresh(db_encounter)
    return db_encounter

@app.get("/encounters/", response_model=List[EncounterResponse])
def read_encounters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    encounters = db.query(Encounter).offset(skip).limit(limit).all()
    return encounters

@app.get("/encounters/{encounter_id}", response_model=EncounterResponse)
def read_encounter(encounter_id: PyUUID, db: Session = Depends(get_db)):
    encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if encounter is None:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return encounter

@app.put("/encounters/{encounter_id}", response_model=EncounterResponse)
def update_encounter(encounter_id: PyUUID, encounter: EncounterUpdate, db: Session = Depends(get_db)):
    db_encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if db_encounter is None:
        raise HTTPException(status_code=404, detail="Encounter not found")
    
    for key, value in encounter.dict(exclude_unset=True).items():
        setattr(db_encounter, key, value)
    
    db.commit()
    db.refresh(db_encounter)
    return db_encounter

@app.delete("/encounters/{encounter_id}")
def delete_encounter(encounter_id: PyUUID, db: Session = Depends(get_db)):
    db_encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if db_encounter is None:
        raise HTTPException(status_code=404, detail="Encounter not found")
    
    db.delete(db_encounter)
    db.commit()
    return {"message": "Encounter deleted successfully"}

# Observation Endpoints
@app.post("/observations/", response_model=ObservationResponse)
def create_observation(observation: ObservationCreate, db: Session = Depends(get_db)):
    db_observation = Observation(**observation.dict())
    db.add(db_observation)
    db.commit()
    db.refresh(db_observation)
    return db_observation

@app.get("/observations/", response_model=List[ObservationResponse])
def read_observations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    observations = db.query(Observation).offset(skip).limit(limit).all()
    return observations

@app.get("/observations/{observation_id}", response_model=ObservationResponse)
def read_observation(observation_id: PyUUID, db: Session = Depends(get_db)):
    observation = db.query(Observation).filter(Observation.id == observation_id).first()
    if observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")
    return observation

@app.put("/observations/{observation_id}", response_model=ObservationResponse)
def update_observation(observation_id: PyUUID, observation: ObservationUpdate, db: Session = Depends(get_db)):
    db_observation = db.query(Observation).filter(Observation.id == observation_id).first()
    if db_observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")
    
    for key, value in observation.dict(exclude_unset=True).items():
        setattr(db_observation, key, value)
    
    db.commit()
    db.refresh(db_observation)
    return db_observation

@app.delete("/observations/{observation_id}")
def delete_observation(observation_id: PyUUID, db: Session = Depends(get_db)):
    db_observation = db.query(Observation).filter(Observation.id == observation_id).first()
    if db_observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")
    
    db.delete(db_observation)
    db.commit()
    return {"message": "Observation deleted successfully"}

# Condition Endpoints
@app.post("/conditions/", response_model=ConditionResponse)
def create_condition(condition: ConditionCreate, db: Session = Depends(get_db)):
    db_condition = Condition(**condition.dict())
    db.add(db_condition)
    db.commit()
    db.refresh(db_condition)
    return db_condition

@app.get("/conditions/", response_model=List[ConditionResponse])
def read_conditions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conditions = db.query(Condition).offset(skip).limit(limit).all()
    return conditions

@app.get("/conditions/{condition_id}", response_model=ConditionResponse)
def read_condition(condition_id: PyUUID, db: Session = Depends(get_db)):
    condition = db.query(Condition).filter(Condition.id == condition_id).first()
    if condition is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return condition

@app.put("/conditions/{condition_id}", response_model=ConditionResponse)
def update_condition(condition_id: PyUUID, condition: ConditionUpdate, db: Session = Depends(get_db)):
    db_condition = db.query(Condition).filter(Condition.id == condition_id).first()
    if db_condition is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    
    for key, value in condition.dict(exclude_unset=True).items():
        setattr(db_condition, key, value)
    
    db.commit()
    db.refresh(db_condition)
    return db_condition

@app.delete("/conditions/{condition_id}")
def delete_condition(condition_id: PyUUID, db: Session = Depends(get_db)):
    db_condition = db.query(Condition).filter(Condition.id == condition_id).first()
    if db_condition is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    
    db.delete(db_condition)
    db.commit()
    return {"message": "Condition deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
