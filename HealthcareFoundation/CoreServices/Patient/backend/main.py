from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from uuid import UUID, uuid4
from datetime import datetime, date
from enum import Enum
import asyncpg
import os
from contextlib import asynccontextmanager
import json

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fhir_db")

# Global database pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    # Startup
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    # Shutdown
    await db_pool.close()

app = FastAPI(
    title="FHIR Patient Microservice",
    description="CRUD operations for FHIR Patient resources",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    unknown = "unknown"

# Pydantic models
class Identifier(BaseModel):
    use: Optional[str] = None
    type: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional[Dict[str, str]] = None

class Telecom(BaseModel):
    system: Optional[str] = None  # phone, fax, email, etc.
    value: Optional[str] = None
    use: Optional[str] = None  # home, work, mobile, etc.
    rank: Optional[int] = None
    period: Optional[Dict[str, str]] = None

class Address(BaseModel):
    use: Optional[str] = None  # home, work, temp, old
    type: Optional[str] = None  # postal, physical, both
    text: Optional[str] = None
    line: Optional[List[str]] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    period: Optional[Dict[str, str]] = None

class MaritalStatus(BaseModel):
    code: Optional[str] = None
    display: Optional[str] = None
    system: Optional[str] = None

class Communication(BaseModel):
    language: Optional[Dict[str, Any]] = None
    preferred: Optional[bool] = None

class PatientCreate(BaseModel):
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Identifier]] = None
    telecom: Optional[List[Telecom]] = None
    addresses: Optional[List[Address]] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    deceased_boolean: Optional[bool] = False
    deceased_date_time: Optional[datetime] = None
    marital_status_code: Optional[str] = None
    marital_status_display: Optional[str] = None
    communication: Optional[List[Communication]] = None
    general_practitioner: Optional[List[Dict[str, Any]]] = None
    managing_organization: Optional[UUID] = None
    photo: Optional[List[Dict[str, Any]]] = None
    links: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = True
    fhir_resource: Optional[Dict[str, Any]] = None

class PatientUpdate(BaseModel):
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Identifier]] = None
    telecom: Optional[List[Telecom]] = None
    addresses: Optional[List[Address]] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    deceased_boolean: Optional[bool] = None
    deceased_date_time: Optional[datetime] = None
    marital_status_code: Optional[str] = None
    marital_status_display: Optional[str] = None
    communication: Optional[List[Communication]] = None
    general_practitioner: Optional[List[Dict[str, Any]]] = None
    managing_organization: Optional[UUID] = None
    photo: Optional[List[Dict[str, Any]]] = None
    links: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class PatientResponse(BaseModel):
    id: UUID
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    telecom: Optional[List[Dict[str, Any]]] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    deceased_boolean: Optional[bool] = None
    deceased_date_time: Optional[datetime] = None
    marital_status_code: Optional[str] = None
    marital_status_display: Optional[str] = None
    communication: Optional[List[Dict[str, Any]]] = None
    general_practitioner: Optional[List[Dict[str, Any]]] = None
    managing_organization: Optional[UUID] = None
    photo: Optional[List[Dict[str, Any]]] = None
    links: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = None
    fhir_resource: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

# Helper function to parse JSON fields from database
def parse_json_field(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
    return value

# Helper function to convert database row to PatientResponse
def row_to_patient_response(row):
    row_dict = dict(row)
    
    # Parse JSON fields
    json_fields = ['identifiers', 'telecom', 'addresses', 'communication', 
                   'general_practitioner', 'photo', 'links', 'fhir_resource']
    
    for field in json_fields:
        if field in row_dict:
            row_dict[field] = parse_json_field(row_dict[field])
    
    return PatientResponse(**row_dict)

# Database operations
async def get_db_connection():
    return await db_pool.acquire()

async def release_db_connection(conn):
    await db_pool.release(conn)

# API Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/patients", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    conn = await get_db_connection()
    try:
        # Convert Pydantic models to JSON for database storage
        identifiers_json = [id.dict() for id in patient.identifiers] if patient.identifiers else None
        telecom_json = [t.dict() for t in patient.telecom] if patient.telecom else None
        addresses_json = [a.dict() for a in patient.addresses] if patient.addresses else None
        communication_json = [c.dict() for c in patient.communication] if patient.communication else None
        
        query = """
        INSERT INTO patients (
            fhir_id, family_name, given_names, prefix, suffix, identifiers,
            telecom, addresses, gender, birth_date, deceased_boolean, deceased_date_time,
            marital_status_code, marital_status_display, communication, general_practitioner,
            managing_organization, photo, links, active, fhir_resource
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
        RETURNING *
        """
        
        result = await conn.fetchrow(
            query,
            patient.fhir_id, patient.family_name, patient.given_names, patient.prefix, patient.suffix,
            json.dumps(identifiers_json) if identifiers_json else None,
            json.dumps(telecom_json) if telecom_json else None,
            json.dumps(addresses_json) if addresses_json else None,
            patient.gender, patient.birth_date, patient.deceased_boolean, patient.deceased_date_time,
            patient.marital_status_code, patient.marital_status_display,
            json.dumps(communication_json) if communication_json else None,
            json.dumps(patient.general_practitioner) if patient.general_practitioner else None,
            patient.managing_organization,
            json.dumps(patient.photo) if patient.photo else None,
            json.dumps(patient.links) if patient.links else None,
            patient.active,
            json.dumps(patient.fhir_resource) if patient.fhir_resource else None
        )
        
        return row_to_patient_response(result)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Patient with this FHIR ID already exists")
    finally:
        await release_db_connection(conn)

@app.get("/patients", response_model=List[PatientResponse])
async def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active: Optional[bool] = None,
    gender: Optional[GenderEnum] = None
):
    conn = await get_db_connection()
    try:
        where_conditions = []
        params = []
        param_count = 0
        
        if active is not None:
            param_count += 1
            where_conditions.append(f"active = ${param_count}")
            params.append(active)
            
        if gender is not None:
            param_count += 1
            where_conditions.append(f"gender = ${param_count}")
            params.append(gender)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        query = f"""
        SELECT * FROM patients 
        {where_clause}
        ORDER BY created_at DESC 
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, skip])
        results = await conn.fetch(query, *params)
        
        return [row_to_patient_response(row) for row in results]
    finally:
        await release_db_connection(conn)

@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM patients WHERE id = $1", patient_id)
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return row_to_patient_response(result)
    finally:
        await release_db_connection(conn)

@app.get("/patients/fhir/{fhir_id}", response_model=PatientResponse)
async def get_patient_by_fhir_id(fhir_id: str):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM patients WHERE fhir_id = $1", fhir_id)
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return row_to_patient_response(result)
    finally:
        await release_db_connection(conn)

@app.put("/patients/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: UUID, patient_update: PatientUpdate):
    conn = await get_db_connection()
    try:
        # Check if patient exists
        existing = await conn.fetchrow("SELECT * FROM patients WHERE id = $1", patient_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Build update query dynamically
        update_fields = []
        params = []
        param_count = 0
        
        update_data = patient_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            param_count += 1
            if field in ['identifiers', 'telecom', 'addresses', 'communication', 'general_practitioner', 'photo', 'links', 'fhir_resource']:
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps(value) if value else None)
            else:
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            return PatientResponse(**dict(existing))
        
        # Add updated_at
        param_count += 1
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.utcnow())
        
        # Add patient_id for WHERE clause
        param_count += 1
        params.append(patient_id)
        
        query = f"""
        UPDATE patients 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING *
        """
        
        result = await conn.fetchrow(query, *params)
        return row_to_patient_response(result)
    finally:
        await release_db_connection(conn)

@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("DELETE FROM patients WHERE id = $1 RETURNING id", patient_id)
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully", "patient_id": str(patient_id)}
    finally:
        await release_db_connection(conn)

# Search endpoints
@app.get("/patients/search/name", response_model=List[PatientResponse])
async def search_patients_by_name(
    family_name: Optional[str] = None,
    given_name: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100)
):
    conn = await get_db_connection()
    try:
        where_conditions = []
        params = []
        param_count = 0
        
        if family_name:
            param_count += 1
            where_conditions.append(f"family_name ILIKE ${param_count}")
            params.append(f"%{family_name}%")
            
        if given_name:
            param_count += 1
            where_conditions.append(f"${param_count} = ANY(given_names)")
            params.append(given_name)
        
        if not where_conditions:
            raise HTTPException(status_code=400, detail="At least one search parameter is required")
        
        where_clause = "WHERE " + " AND ".join(where_conditions)
        
        query = f"""
        SELECT * FROM patients 
        {where_clause}
        ORDER BY family_name, given_names
        LIMIT ${param_count + 1}
        """
        
        params.append(limit)
        results = await conn.fetch(query, *params)
        
        return [row_to_patient_response(row) for row in results]
    finally:
        await release_db_connection(conn)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
