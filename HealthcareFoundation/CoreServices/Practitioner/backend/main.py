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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fhir_practitioner_db")

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
    title="FHIR Practitioner Microservice",
    description="CRUD operations for FHIR Practitioner resources",
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

class Qualification(BaseModel):
    identifier: Optional[List[Dict[str, Any]]] = None
    code: Optional[Dict[str, Any]] = None  # CodeableConcept for degree/certification
    period: Optional[Dict[str, str]] = None
    issuer: Optional[Dict[str, Any]] = None  # Organization reference

class Communication(BaseModel):
    language: Optional[Dict[str, Any]] = None
    preferred: Optional[bool] = None

class PractitionerCreate(BaseModel):
    fhir_id: str
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    telecom: Optional[List[Dict[str, Any]]] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[str] = None  # Using string for date input
    qualifications: Optional[List[Dict[str, Any]]] = None
    communication: Optional[List[Dict[str, Any]]] = None
    photo: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = True
    fhir_resource: Optional[Dict[str, Any]] = None

class PractitionerUpdate(BaseModel):
    family_name: Optional[str] = None
    given_names: Optional[List[str]] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    identifiers: Optional[List[Dict[str, Any]]] = None
    telecom: Optional[List[Dict[str, Any]]] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[str] = None
    qualifications: Optional[List[Dict[str, Any]]] = None
    communication: Optional[List[Dict[str, Any]]] = None
    photo: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class PractitionerResponse(BaseModel):
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
    qualifications: Optional[List[Dict[str, Any]]] = None
    communication: Optional[List[Dict[str, Any]]] = None
    photo: Optional[List[Dict[str, Any]]] = None
    active: Optional[bool] = None
    fhir_resource: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

# Helper function to convert objects to JSON-serializable format
def serialize_for_json(obj):
    if obj is None:
        return None
    if hasattr(obj, 'dict'):
        obj_dict = obj.dict()
        # Convert date objects to ISO format strings
        for key, value in obj_dict.items():
            if isinstance(value, date):
                obj_dict[key] = value.isoformat()
            elif isinstance(value, datetime):
                obj_dict[key] = value.isoformat()
        return obj_dict
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_for_json(value) for key, value in obj.items()}
    return obj

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

# Helper function to convert database row to PractitionerResponse
def row_to_practitioner_response(row):
    row_dict = dict(row)
    
    # Parse JSON fields
    json_fields = ['identifiers', 'telecom', 'addresses', 'qualifications', 
                   'communication', 'photo', 'fhir_resource']
    
    for field in json_fields:
        if field in row_dict:
            row_dict[field] = parse_json_field(row_dict[field])
    
    return PractitionerResponse(**row_dict)

# Database operations
async def get_db_connection():
    return await db_pool.acquire()

async def release_db_connection(conn):
    await db_pool.release(conn)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ============================================================================
# Practitioner CRUD Operations
# ============================================================================

@app.post("/practitioners", response_model=PractitionerResponse)
async def create_practitioner(practitioner: PractitionerCreate):
    conn = await get_db_connection()
    try:
        # Parse birth_date if provided
        birth_date = None
        if practitioner.birth_date:
            try:
                from dateutil import parser
                birth_date = parser.parse(practitioner.birth_date).date()
            except Exception as e:
                print(f"Date parsing error: {e}")
        
        query = """
        INSERT INTO practitioners (
            fhir_id, family_name, given_names, prefix, suffix, identifiers,
            telecom, addresses, gender, birth_date, qualifications, communication,
            photo, active, fhir_resource
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        RETURNING *
        """
        
        result = await conn.fetchrow(
            query,
            practitioner.fhir_id,
            practitioner.family_name,
            practitioner.given_names,
            practitioner.prefix,
            practitioner.suffix,
            json.dumps(practitioner.identifiers) if practitioner.identifiers else None,
            json.dumps(practitioner.telecom) if practitioner.telecom else None,
            json.dumps(practitioner.addresses) if practitioner.addresses else None,
            practitioner.gender,
            birth_date,
            json.dumps(practitioner.qualifications) if practitioner.qualifications else None,
            json.dumps(practitioner.communication) if practitioner.communication else None,
            json.dumps(practitioner.photo) if practitioner.photo else None,
            practitioner.active,
            json.dumps(practitioner.fhir_resource) if practitioner.fhir_resource else None
        )
        
        return row_to_practitioner_response(result)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Practitioner with this FHIR ID already exists")
    except Exception as e:
        print(f"Error creating practitioner: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        await release_db_connection(conn)

@app.get("/practitioners", response_model=List[PractitionerResponse])
async def get_practitioners(
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
        SELECT * FROM practitioners 
        {where_clause}
        ORDER BY created_at DESC 
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, skip])
        results = await conn.fetch(query, *params)
        
        return [row_to_practitioner_response(row) for row in results]
    finally:
        await release_db_connection(conn)

@app.get("/practitioners/{practitioner_id}", response_model=PractitionerResponse)
async def get_practitioner(practitioner_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM practitioners WHERE id = $1", practitioner_id)
        if not result:
            raise HTTPException(status_code=404, detail="Practitioner not found")
        return row_to_practitioner_response(result)
    finally:
        await release_db_connection(conn)

@app.get("/practitioners/fhir/{fhir_id}", response_model=PractitionerResponse)
async def get_practitioner_by_fhir_id(fhir_id: str):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM practitioners WHERE fhir_id = $1", fhir_id)
        if not result:
            raise HTTPException(status_code=404, detail="Practitioner not found")
        return row_to_practitioner_response(result)
    finally:
        await release_db_connection(conn)

@app.put("/practitioners/{practitioner_id}", response_model=PractitionerResponse)
async def update_practitioner(practitioner_id: UUID, practitioner_update: PractitionerUpdate):
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow("SELECT * FROM practitioners WHERE id = $1", practitioner_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Practitioner not found")
        
        update_fields = []
        params = []
        param_count = 0
        
        update_data = practitioner_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            param_count += 1
            
            if field == 'birth_date' and value:
                # Parse birth_date
                try:
                    from dateutil import parser
                    birth_date = parser.parse(value).date()
                    update_fields.append(f"{field} = ${param_count}")
                    params.append(birth_date)
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    param_count -= 1
                    continue
            elif field in ['identifiers', 'telecom', 'addresses', 'qualifications', 'communication', 'photo', 'fhir_resource']:
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps(value) if value else None)
            else:
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            return row_to_practitioner_response(existing)
        
        param_count += 1
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.utcnow())
        
        param_count += 1
        params.append(practitioner_id)
        
        query = f"""
        UPDATE practitioners 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING *
        """
        
        result = await conn.fetchrow(query, *params)
        return row_to_practitioner_response(result)
    except Exception as e:
        print(f"Error updating practitioner: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        await release_db_connection(conn)

@app.delete("/practitioners/{practitioner_id}")
async def delete_practitioner(practitioner_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("DELETE FROM practitioners WHERE id = $1 RETURNING id", practitioner_id)
        if not result:
            raise HTTPException(status_code=404, detail="Practitioner not found")
        return {"message": "Practitioner deleted successfully", "practitioner_id": str(practitioner_id)}
    finally:
        await release_db_connection(conn)

# Search endpoints
@app.get("/practitioners/search/name", response_model=List[PractitionerResponse])
async def search_practitioners_by_name(
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
        SELECT * FROM practitioners 
        {where_clause}
        ORDER BY family_name, given_names
        LIMIT ${param_count + 1}
        """
        
        params.append(limit)
        results = await conn.fetch(query, *params)
        
        return [row_to_practitioner_response(row) for row in results]
    finally:
        await release_db_connection(conn)

@app.get("/practitioners/search/identifier", response_model=List[PractitionerResponse])
async def search_practitioners_by_identifier(
    identifier_value: str,
    identifier_system: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100)
):
    conn = await get_db_connection()
    try:
        # Search in JSONB identifiers field
        if identifier_system:
            query = """
            SELECT * FROM practitioners 
            WHERE identifiers @> $1
            ORDER BY family_name, given_names
            LIMIT $2
            """
            search_criteria = json.dumps([{"system": identifier_system, "value": identifier_value}])
            params = [search_criteria, limit]
        else:
            query = """
            SELECT * FROM practitioners 
            WHERE identifiers::text ILIKE $1
            ORDER BY family_name, given_names
            LIMIT $2
            """
            params = [f'%{identifier_value}%', limit]
        
        results = await conn.fetch(query, *params)
        return [row_to_practitioner_response(row) for row in results]
    finally:
        await release_db_connection(conn)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
