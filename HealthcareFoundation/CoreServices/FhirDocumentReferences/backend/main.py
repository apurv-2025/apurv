from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Text, UUID, ARRAY, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import uuid
import os
from contextlib import asynccontextmanager

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/fhir_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class DocumentReference(Base):
    __tablename__ = "document_references"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    master_identifier = Column(JSONB)
    identifiers = Column(JSONB)
    status = Column(String(50), nullable=False)
    doc_status = Column(String(50))
    type = Column(JSONB)
    categories = Column(JSONB)
    subject_patient_id = Column(UUID(as_uuid=True), nullable=False)
    date_time = Column(TIMESTAMP(timezone=True))
    authors = Column(JSONB)
    authenticator = Column(UUID(as_uuid=True))
    custodian = Column(UUID(as_uuid=True))
    relates_to = Column(JSONB)
    description = Column(Text)
    security_labels = Column(JSONB)
    content = Column(JSONB, nullable=False)
    context = Column(JSONB)
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

class Questionnaire(Base):
    __tablename__ = "questionnaires"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    url = Column(String(500))
    identifiers = Column(JSONB)
    version = Column(String(100))
    name = Column(String(255))
    title = Column(String(500))
    derived_from = Column(ARRAY(Text))
    status = Column(String(50), nullable=False)
    experimental = Column(Boolean, default=False)
    subject_types = Column(ARRAY(Text))
    date_time = Column(TIMESTAMP(timezone=True))
    publisher = Column(String(500))
    contacts = Column(JSONB)
    description = Column(Text)
    use_contexts = Column(JSONB)
    jurisdictions = Column(JSONB)
    purpose = Column(Text)
    copyright = Column(Text)
    approval_date = Column(DateTime)
    last_review_date = Column(DateTime)
    effective_period = Column(JSONB)
    codes = Column(JSONB)
    items = Column(JSONB, nullable=False)
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

class QuestionnaireResponse(Base):
    __tablename__ = "questionnaire_responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fhir_id = Column(String(255), unique=True, nullable=False)
    identifier = Column(JSONB)
    based_on = Column(JSONB)
    part_of = Column(JSONB)
    questionnaire_id = Column(UUID(as_uuid=True))
    questionnaire_canonical = Column(String(500))
    status = Column(String(50), nullable=False)
    subject_patient_id = Column(UUID(as_uuid=True), nullable=False)
    encounter_id = Column(UUID(as_uuid=True))
    authored = Column(TIMESTAMP(timezone=True))
    author_patient_id = Column(UUID(as_uuid=True))
    author_practitioner_id = Column(UUID(as_uuid=True))
    author_device_id = Column(UUID(as_uuid=True))
    author_organization_id = Column(UUID(as_uuid=True))
    source_patient_id = Column(UUID(as_uuid=True))
    source_practitioner_id = Column(UUID(as_uuid=True))
    source_related_person_id = Column(UUID(as_uuid=True))
    items = Column(JSONB)
    fhir_resource = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

# Pydantic Models
class DocumentReferenceCreate(BaseModel):
    fhir_id: str
    master_identifier: Optional[Dict[str, Any]] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    status: str
    doc_status: Optional[str] = None
    type: Optional[Dict[str, Any]] = None
    categories: Optional[List[Dict[str, Any]]] = None
    subject_patient_id: str
    date_time: Optional[datetime] = None
    authors: Optional[List[Dict[str, Any]]] = None
    authenticator: Optional[str] = None
    custodian: Optional[str] = None
    relates_to: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None
    security_labels: Optional[List[Dict[str, Any]]] = None
    content: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

    @validator('subject_patient_id')
    def validate_patient_id(cls, v):
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError('subject_patient_id must be a valid UUID')

    @validator('authenticator')
    def validate_authenticator(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('authenticator must be a valid UUID')
        return v

    @validator('custodian')
    def validate_custodian(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('custodian must be a valid UUID')
        return v

class DocumentReferenceUpdate(BaseModel):
    master_identifier: Optional[Dict[str, Any]] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    doc_status: Optional[str] = None
    type: Optional[Dict[str, Any]] = None
    categories: Optional[List[Dict[str, Any]]] = None
    date_time: Optional[datetime] = None
    authors: Optional[List[Dict[str, Any]]] = None
    authenticator: Optional[str] = None
    custodian: Optional[str] = None
    relates_to: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None
    security_labels: Optional[List[Dict[str, Any]]] = None
    content: Optional[List[Dict[str, Any]]] = None
    context: Optional[Dict[str, Any]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class QuestionnaireCreate(BaseModel):
    fhir_id: str
    url: Optional[str] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    version: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    derived_from: Optional[List[str]] = None
    status: str
    experimental: Optional[bool] = False
    subject_types: Optional[List[str]] = None
    date_time: Optional[datetime] = None
    publisher: Optional[str] = None
    contacts: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None
    use_contexts: Optional[List[Dict[str, Any]]] = None
    jurisdictions: Optional[List[Dict[str, Any]]] = None
    purpose: Optional[str] = None
    copyright: Optional[str] = None
    approval_date: Optional[datetime] = None
    last_review_date: Optional[datetime] = None
    effective_period: Optional[Dict[str, Any]] = None
    codes: Optional[List[Dict[str, Any]]] = None
    items: List[Dict[str, Any]]
    fhir_resource: Optional[Dict[str, Any]] = None

class QuestionnaireResponseCreate(BaseModel):
    fhir_id: str
    identifier: Optional[Dict[str, Any]] = None
    based_on: Optional[List[Dict[str, Any]]] = None
    part_of: Optional[List[Dict[str, Any]]] = None
    questionnaire_id: Optional[str] = None
    questionnaire_canonical: Optional[str] = None
    status: str
    subject_patient_id: str
    encounter_id: Optional[str] = None
    authored: Optional[datetime] = None
    author_patient_id: Optional[str] = None
    author_practitioner_id: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

    @validator('subject_patient_id')
    def validate_patient_id(cls, v):
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError('subject_patient_id must be a valid UUID')

    @validator('questionnaire_id')
    def validate_questionnaire_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('questionnaire_id must be a valid UUID')
        return v

    @validator('encounter_id')
    def validate_encounter_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('encounter_id must be a valid UUID')
        return v

    @validator('author_patient_id')
    def validate_author_patient_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('author_patient_id must be a valid UUID')
        return v

    @validator('author_practitioner_id')
    def validate_author_practitioner_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
                return v
            except ValueError:
                raise ValueError('author_practitioner_id must be a valid UUID')
        return v

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield

# FastAPI app
app = FastAPI(
    title="FHIR Document Management API",
    description="CRUD operations for FHIR DocumentReference, Questionnaire, and QuestionnaireResponse resources",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DocumentReference endpoints
@app.post("/document-references/", response_model=dict)
def create_document_reference(doc_ref: DocumentReferenceCreate, db: Session = Depends(get_db)):
    db_doc_ref = DocumentReference(**doc_ref.dict())
    db_doc_ref.updated_at = datetime.utcnow()
    db.add(db_doc_ref)
    db.commit()
    db.refresh(db_doc_ref)
    return {"id": str(db_doc_ref.id), "fhir_id": db_doc_ref.fhir_id}

@app.get("/document-references/")
def get_document_references(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(DocumentReference)
    if patient_id:
        query = query.filter(DocumentReference.subject_patient_id == patient_id)
    doc_refs = query.offset(skip).limit(limit).all()
    return [{"id": str(dr.id), "fhir_id": dr.fhir_id, "status": dr.status, 
             "description": dr.description, "created_at": dr.created_at} for dr in doc_refs]

@app.get("/document-references/{doc_ref_id}")
def get_document_reference(doc_ref_id: str, db: Session = Depends(get_db)):
    doc_ref = db.query(DocumentReference).filter(DocumentReference.id == doc_ref_id).first()
    if not doc_ref:
        raise HTTPException(status_code=404, detail="Document reference not found")
    return doc_ref

@app.put("/document-references/{doc_ref_id}")
def update_document_reference(doc_ref_id: str, doc_ref_update: DocumentReferenceUpdate, db: Session = Depends(get_db)):
    doc_ref = db.query(DocumentReference).filter(DocumentReference.id == doc_ref_id).first()
    if not doc_ref:
        raise HTTPException(status_code=404, detail="Document reference not found")
    
    update_data = doc_ref_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doc_ref, field, value)
    
    doc_ref.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Document reference updated successfully"}

@app.delete("/document-references/{doc_ref_id}")
def delete_document_reference(doc_ref_id: str, db: Session = Depends(get_db)):
    doc_ref = db.query(DocumentReference).filter(DocumentReference.id == doc_ref_id).first()
    if not doc_ref:
        raise HTTPException(status_code=404, detail="Document reference not found")
    
    db.delete(doc_ref)
    db.commit()
    return {"message": "Document reference deleted successfully"}

# Questionnaire endpoints
@app.post("/questionnaires/", response_model=dict)
def create_questionnaire(questionnaire: QuestionnaireCreate, db: Session = Depends(get_db)):
    db_questionnaire = Questionnaire(**questionnaire.dict())
    db_questionnaire.updated_at = datetime.utcnow()
    db.add(db_questionnaire)
    db.commit()
    db.refresh(db_questionnaire)
    return {"id": str(db_questionnaire.id), "fhir_id": db_questionnaire.fhir_id}

@app.get("/questionnaires/")
def get_questionnaires(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questionnaires = db.query(Questionnaire).offset(skip).limit(limit).all()
    return [{"id": str(q.id), "fhir_id": q.fhir_id, "title": q.title, 
             "status": q.status, "created_at": q.created_at} for q in questionnaires]

@app.get("/questionnaires/{questionnaire_id}")
def get_questionnaire(questionnaire_id: str, db: Session = Depends(get_db)):
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == questionnaire_id).first()
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire

@app.delete("/questionnaires/{questionnaire_id}")
def delete_questionnaire(questionnaire_id: str, db: Session = Depends(get_db)):
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == questionnaire_id).first()
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    
    db.delete(questionnaire)
    db.commit()
    return {"message": "Questionnaire deleted successfully"}

# QuestionnaireResponse endpoints
@app.post("/questionnaire-responses/", response_model=dict)
def create_questionnaire_response(response: QuestionnaireResponseCreate, db: Session = Depends(get_db)):
    db_response = QuestionnaireResponse(**response.dict())
    db_response.updated_at = datetime.utcnow()
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return {"id": str(db_response.id), "fhir_id": db_response.fhir_id}

@app.get("/questionnaire-responses/")
def get_questionnaire_responses(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(QuestionnaireResponse)
    if patient_id:
        query = query.filter(QuestionnaireResponse.subject_patient_id == patient_id)
    responses = query.offset(skip).limit(limit).all()
    return [{"id": str(r.id), "fhir_id": r.fhir_id, "status": r.status, 
             "authored": r.authored, "created_at": r.created_at} for r in responses]

@app.get("/questionnaire-responses/{response_id}")
def get_questionnaire_response(response_id: str, db: Session = Depends(get_db)):
    response = db.query(QuestionnaireResponse).filter(QuestionnaireResponse.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Questionnaire response not found")
    return response

@app.delete("/questionnaire-responses/{response_id}")
def delete_questionnaire_response(response_id: str, db: Session = Depends(get_db)):
    response = db.query(QuestionnaireResponse).filter(QuestionnaireResponse.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Questionnaire response not found")
    
    db.delete(response)
    db.commit()
    return {"message": "Questionnaire response deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
