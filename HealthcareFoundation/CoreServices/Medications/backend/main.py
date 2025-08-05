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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fhir_medication_db")

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
    title="FHIR Medication Microservice",
    description="CRUD operations for FHIR Medication and MedicationRequest resources",
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
class MedicationStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    entered_in_error = "entered-in-error"

class MedicationRequestStatusEnum(str, Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"
    entered_in_error = "entered-in-error"
    stopped = "stopped"
    draft = "draft"
    unknown = "unknown"

class MedicationRequestIntentEnum(str, Enum):
    proposal = "proposal"
    plan = "plan"
    order = "order"
    original_order = "original-order"
    reflex_order = "reflex-order"
    filler_order = "filler-order"
    instance_order = "instance-order"
    option = "option"

class PriorityEnum(str, Enum):
    routine = "routine"
    urgent = "urgent"
    asap = "asap"
    stat = "stat"

# Pydantic models for Medication
class CodeableConcept(BaseModel):
    coding: Optional[List[Dict[str, Any]]] = None
    text: Optional[str] = None

class Ratio(BaseModel):
    numerator: Optional[Dict[str, Any]] = None
    denominator: Optional[Dict[str, Any]] = None

class Ingredient(BaseModel):
    item_codeable_concept: Optional[CodeableConcept] = None
    item_reference: Optional[str] = None
    is_active: Optional[bool] = None
    strength: Optional[Ratio] = None

class Batch(BaseModel):
    lot_number: Optional[str] = None
    expiration_date: Optional[date] = None

class MedicationCreate(BaseModel):
    fhir_id: str
    code: Optional[CodeableConcept] = None
    status: Optional[MedicationStatusEnum] = None
    manufacturer: Optional[UUID] = None
    form: Optional[CodeableConcept] = None
    amount: Optional[Ratio] = None
    ingredients: Optional[List[Ingredient]] = None
    batch: Optional[Batch] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class MedicationUpdate(BaseModel):
    code: Optional[CodeableConcept] = None
    status: Optional[MedicationStatusEnum] = None
    manufacturer: Optional[UUID] = None
    form: Optional[CodeableConcept] = None
    amount: Optional[Ratio] = None
    ingredients: Optional[List[Ingredient]] = None
    batch: Optional[Batch] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class MedicationResponse(BaseModel):
    id: UUID
    fhir_id: str
    code: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    manufacturer: Optional[UUID] = None
    form: Optional[Dict[str, Any]] = None
    amount: Optional[Dict[str, Any]] = None
    ingredients: Optional[List[Dict[str, Any]]] = None
    batch: Optional[Dict[str, Any]] = None
    fhir_resource: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

# Pydantic models for MedicationRequest
class MedicationRequestCreate(BaseModel):
    fhir_id: str
    status: MedicationRequestStatusEnum
    intent: MedicationRequestIntentEnum
    category: Optional[List[Dict[str, Any]]] = None  # Changed from CodeableConcept to Dict
    priority: Optional[PriorityEnum] = None
    do_not_perform: Optional[bool] = False
    reported_boolean: Optional[bool] = None
    reported_reference: Optional[str] = None  # Changed from UUID to str
    medication_id: Optional[str] = None  # Changed from UUID to str
    medication_codeable_concept: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    subject_patient_id: str  # Keep as str, convert to UUID in backend if needed
    encounter_id: Optional[str] = None  # Changed from UUID to str
    supporting_information: Optional[List[Dict[str, Any]]] = None
    authored_on: Optional[str] = None  # Changed from datetime to str
    requester: Optional[str] = None  # Changed from UUID to str
    performer: Optional[str] = None  # Changed from UUID to str
    performer_type: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    recorder: Optional[str] = None  # Changed from UUID to str
    reason_codes: Optional[List[Dict[str, Any]]] = None  # Changed from CodeableConcept to Dict
    reason_references: Optional[List[Dict[str, Any]]] = None
    instantiates_canonical: Optional[List[str]] = None
    instantiates_uri: Optional[List[str]] = None
    based_on: Optional[List[Dict[str, Any]]] = None
    group_identifier: Optional[Dict[str, Any]] = None
    course_of_therapy_type: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    insurance: Optional[List[Dict[str, Any]]] = None
    notes: Optional[List[Dict[str, Any]]] = None
    dosage_instructions: Optional[List[Dict[str, Any]]] = None
    dispense_request: Optional[Dict[str, Any]] = None
    substitution: Optional[Dict[str, Any]] = None
    prior_prescription: Optional[str] = None  # Changed from UUID to str
    detection_issue: Optional[List[Dict[str, Any]]] = None
    event_history: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class MedicationRequestUpdate(BaseModel):
    status: Optional[MedicationRequestStatusEnum] = None
    intent: Optional[MedicationRequestIntentEnum] = None
    category: Optional[List[Dict[str, Any]]] = None  # Changed from CodeableConcept to Dict
    priority: Optional[PriorityEnum] = None
    do_not_perform: Optional[bool] = None
    reported_boolean: Optional[bool] = None
    reported_reference: Optional[str] = None  # Changed from UUID to str
    medication_id: Optional[str] = None  # Changed from UUID to str
    medication_codeable_concept: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    subject_patient_id: Optional[str] = None  # Changed from UUID to str
    encounter_id: Optional[str] = None  # Changed from UUID to str
    supporting_information: Optional[List[Dict[str, Any]]] = None
    authored_on: Optional[str] = None  # Changed from datetime to str
    requester: Optional[str] = None  # Changed from UUID to str
    performer: Optional[str] = None  # Changed from UUID to str
    performer_type: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    recorder: Optional[str] = None  # Changed from UUID to str
    reason_codes: Optional[List[Dict[str, Any]]] = None  # Changed from CodeableConcept to Dict
    reason_references: Optional[List[Dict[str, Any]]] = None
    instantiates_canonical: Optional[List[str]] = None
    instantiates_uri: Optional[List[str]] = None
    based_on: Optional[List[Dict[str, Any]]] = None
    group_identifier: Optional[Dict[str, Any]] = None
    course_of_therapy_type: Optional[Dict[str, Any]] = None  # Changed from CodeableConcept to Dict
    insurance: Optional[List[Dict[str, Any]]] = None
    notes: Optional[List[Dict[str, Any]]] = None
    dosage_instructions: Optional[List[Dict[str, Any]]] = None
    dispense_request: Optional[Dict[str, Any]] = None
    substitution: Optional[Dict[str, Any]] = None
    prior_prescription: Optional[str] = None  # Changed from UUID to str
    detection_issue: Optional[List[Dict[str, Any]]] = None
    event_history: Optional[List[Dict[str, Any]]] = None
    fhir_resource: Optional[Dict[str, Any]] = None

class MedicationRequestResponse(BaseModel):
    id: UUID
    fhir_id: str
    status: str
    intent: str
    category: Optional[List[Dict[str, Any]]] = None
    priority: Optional[str] = None
    do_not_perform: Optional[bool] = None
    reported_boolean: Optional[bool] = None
    reported_reference: Optional[UUID] = None
    medication_id: Optional[UUID] = None
    medication_codeable_concept: Optional[Dict[str, Any]] = None
    subject_patient_id: UUID
    encounter_id: Optional[UUID] = None
    supporting_information: Optional[List[Dict[str, Any]]] = None
    authored_on: Optional[datetime] = None
    requester: Optional[UUID] = None
    performer: Optional[UUID] = None
    performer_type: Optional[Dict[str, Any]] = None
    recorder: Optional[UUID] = None
    reason_codes: Optional[List[Dict[str, Any]]] = None
    reason_references: Optional[List[Dict[str, Any]]] = None
    instantiates_canonical: Optional[List[str]] = None
    instantiates_uri: Optional[List[str]] = None
    based_on: Optional[List[Dict[str, Any]]] = None
    group_identifier: Optional[Dict[str, Any]] = None
    course_of_therapy_type: Optional[Dict[str, Any]] = None
    insurance: Optional[List[Dict[str, Any]]] = None
    notes: Optional[List[Dict[str, Any]]] = None
    dosage_instructions: Optional[List[Dict[str, Any]]] = None
    dispense_request: Optional[Dict[str, Any]] = None
    substitution: Optional[Dict[str, Any]] = None
    prior_prescription: Optional[UUID] = None
    detection_issue: Optional[List[Dict[str, Any]]] = None
    event_history: Optional[List[Dict[str, Any]]] = None
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
def parse_json_field(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return None
    return value

# Helper functions to convert database rows
def row_to_medication_response(row):
    row_dict = dict(row)
    json_fields = ['code', 'form', 'amount', 'ingredients', 'batch', 'fhir_resource']
    for field in json_fields:
        if field in row_dict:
            row_dict[field] = parse_json_field(row_dict[field])
    return MedicationResponse(**row_dict)

def row_to_medication_request_response(row):
    row_dict = dict(row)
    json_fields = ['category', 'medication_codeable_concept', 'supporting_information', 
                   'performer_type', 'reason_codes', 'reason_references', 'based_on',
                   'group_identifier', 'course_of_therapy_type', 'insurance', 'notes',
                   'dosage_instructions', 'dispense_request', 'substitution', 
                   'detection_issue', 'event_history', 'fhir_resource']
    for field in json_fields:
        if field in row_dict:
            row_dict[field] = parse_json_field(row_dict[field])
    return MedicationRequestResponse(**row_dict)

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
# Medication CRUD Operations
# ============================================================================

@app.post("/medications", response_model=MedicationResponse)
async def create_medication(medication: MedicationCreate):
    conn = await get_db_connection()
    try:
        query = """
        INSERT INTO medications (
            fhir_id, code, status, manufacturer, form, amount, ingredients, batch, fhir_resource
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING *
        """
        
        result = await conn.fetchrow(
            query,
            medication.fhir_id,
            json.dumps(serialize_for_json(medication.code)) if medication.code else None,
            medication.status,
            medication.manufacturer,
            json.dumps(serialize_for_json(medication.form)) if medication.form else None,
            json.dumps(serialize_for_json(medication.amount)) if medication.amount else None,
            json.dumps([serialize_for_json(ing) for ing in medication.ingredients]) if medication.ingredients else None,
            json.dumps(serialize_for_json(medication.batch)) if medication.batch else None,
            json.dumps(medication.fhir_resource) if medication.fhir_resource else None
        )
        
        return row_to_medication_response(result)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Medication with this FHIR ID already exists")
    finally:
        await release_db_connection(conn)

@app.get("/medications", response_model=List[MedicationResponse])
async def get_medications(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[MedicationStatusEnum] = None
):
    conn = await get_db_connection()
    try:
        where_conditions = []
        params = []
        param_count = 0
        
        if status is not None:
            param_count += 1
            where_conditions.append(f"status = ${param_count}")
            params.append(status)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        query = f"""
        SELECT * FROM medications 
        {where_clause}
        ORDER BY created_at DESC 
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, skip])
        results = await conn.fetch(query, *params)
        
        return [row_to_medication_response(row) for row in results]
    finally:
        await release_db_connection(conn)

@app.get("/medications/{medication_id}", response_model=MedicationResponse)
async def get_medication(medication_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM medications WHERE id = $1", medication_id)
        if not result:
            raise HTTPException(status_code=404, detail="Medication not found")
        return row_to_medication_response(result)
    finally:
        await release_db_connection(conn)

@app.put("/medications/{medication_id}", response_model=MedicationResponse)
async def update_medication(medication_id: UUID, medication_update: MedicationUpdate):
    conn = await get_db_connection()
    try:
        existing = await conn.fetchrow("SELECT * FROM medications WHERE id = $1", medication_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Medication not found")
        
        update_fields = []
        params = []
        param_count = 0
        
        update_data = medication_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            param_count += 1
            if field in ['code', 'form', 'amount', 'batch', 'fhir_resource']:
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps(serialize_for_json(value)) if value else None)
            elif field == 'ingredients':
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps([serialize_for_json(ing) for ing in value]) if value else None)
            else:
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            return row_to_medication_response(existing)
        
        param_count += 1
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.utcnow())
        
        param_count += 1
        params.append(medication_id)
        
        query = f"""
        UPDATE medications 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING *
        """
        
        result = await conn.fetchrow(query, *params)
        return row_to_medication_response(result)
    finally:
        await release_db_connection(conn)

@app.delete("/medications/{medication_id}")
async def delete_medication(medication_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("DELETE FROM medications WHERE id = $1 RETURNING id", medication_id)
        if not result:
            raise HTTPException(status_code=404, detail="Medication not found")
        return {"message": "Medication deleted successfully", "medication_id": str(medication_id)}
    finally:
        await release_db_connection(conn)

# ============================================================================
# MedicationRequest CRUD Operations
# ============================================================================

@app.post("/medication-requests", response_model=MedicationRequestResponse)
async def create_medication_request(medication_request: MedicationRequestCreate):
    conn = await get_db_connection()
    try:
        # Debug logging
        print(f"Received medication_request: {medication_request}")
        
        # Convert string patient ID to UUID if needed
        try:
            if medication_request.subject_patient_id:
                # Try to parse as UUID, if it fails, create a UUID from the string
                if not medication_request.subject_patient_id.count('-') == 4:
                    # Convert simple string to UUID format
                    patient_str = medication_request.subject_patient_id.replace('-', '')[:32]
                    patient_str = patient_str.ljust(32, '0')
                    subject_uuid = f"{patient_str[:8]}-{patient_str[8:12]}-{patient_str[12:16]}-{patient_str[16:20]}-{patient_str[20:32]}"
                else:
                    subject_uuid = medication_request.subject_patient_id
                # Validate UUID format
                UUID(subject_uuid)
            else:
                raise ValueError("subject_patient_id is required")
        except Exception as e:
            print(f"UUID conversion error: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid patient ID format: {medication_request.subject_patient_id}")
        
        # Convert other UUID fields
        medication_uuid = None
        if medication_request.medication_id:
            try:
                medication_uuid = UUID(medication_request.medication_id) if medication_request.medication_id.count('-') == 4 else None
            except:
                medication_uuid = None
        
        # Parse authored_on date
        authored_on = None
        if medication_request.authored_on:
            try:
                from dateutil import parser
                authored_on = parser.parse(medication_request.authored_on)
            except:
                authored_on = None
        
        query = """
        INSERT INTO medication_requests (
            fhir_id, status, intent, category, priority, do_not_perform, reported_boolean,
            reported_reference, medication_id, medication_codeable_concept, subject_patient_id,
            encounter_id, supporting_information, authored_on, requester, performer,
            performer_type, recorder, reason_codes, reason_references, instantiates_canonical,
            instantiates_uri, based_on, group_identifier, course_of_therapy_type, insurance,
            notes, dosage_instructions, dispense_request, substitution, prior_prescription,
            detection_issue, event_history, fhir_resource
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34)
        RETURNING *
        """
        
        result = await conn.fetchrow(
            query,
            medication_request.fhir_id,
            medication_request.status,
            medication_request.intent,
            json.dumps(medication_request.category) if medication_request.category else None,
            medication_request.priority,
            medication_request.do_not_perform,
            medication_request.reported_boolean,
            None,  # reported_reference as UUID - skip for now
            medication_uuid,
            json.dumps(medication_request.medication_codeable_concept) if medication_request.medication_codeable_concept else None,
            UUID(subject_uuid),
            None,  # encounter_id as UUID - skip for now
            json.dumps(medication_request.supporting_information) if medication_request.supporting_information else None,
            authored_on,
            None,  # requester as UUID - skip for now
            None,  # performer as UUID - skip for now
            json.dumps(medication_request.performer_type) if medication_request.performer_type else None,
            None,  # recorder as UUID - skip for now
            json.dumps(medication_request.reason_codes) if medication_request.reason_codes else None,
            json.dumps(medication_request.reason_references) if medication_request.reason_references else None,
            medication_request.instantiates_canonical,
            medication_request.instantiates_uri,
            json.dumps(medication_request.based_on) if medication_request.based_on else None,
            json.dumps(medication_request.group_identifier) if medication_request.group_identifier else None,
            json.dumps(medication_request.course_of_therapy_type) if medication_request.course_of_therapy_type else None,
            json.dumps(medication_request.insurance) if medication_request.insurance else None,
            json.dumps(medication_request.notes) if medication_request.notes else None,
            json.dumps(medication_request.dosage_instructions) if medication_request.dosage_instructions else None,
            json.dumps(medication_request.dispense_request) if medication_request.dispense_request else None,
            json.dumps(medication_request.substitution) if medication_request.substitution else None,
            None,  # prior_prescription as UUID - skip for now
            json.dumps(medication_request.detection_issue) if medication_request.detection_issue else None,
            json.dumps(medication_request.event_history) if medication_request.event_history else None,
            json.dumps(medication_request.fhir_resource) if medication_request.fhir_resource else None
        )
        
        return row_to_medication_request_response(result)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="MedicationRequest with this FHIR ID already exists")
    except Exception as e:
        print(f"Error creating medication request: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        await release_db_connection(conn)

@app.get("/medication-requests", response_model=List[MedicationRequestResponse])
async def get_medication_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[MedicationRequestStatusEnum] = None,
    intent: Optional[MedicationRequestIntentEnum] = None,
    subject_patient_id: Optional[UUID] = None
):
    conn = await get_db_connection()
    try:
        where_conditions = []
        params = []
        param_count = 0
        
        if status is not None:
            param_count += 1
            where_conditions.append(f"status = ${param_count}")
            params.append(status)
            
        if intent is not None:
            param_count += 1
            where_conditions.append(f"intent = ${param_count}")
            params.append(intent)
            
        if subject_patient_id is not None:
            param_count += 1
            where_conditions.append(f"subject_patient_id = ${param_count}")
            params.append(subject_patient_id)
        
        where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        query = f"""
        SELECT * FROM medication_requests 
        {where_clause}
        ORDER BY created_at DESC 
        LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, skip])
        results = await conn.fetch(query, *params)
        
        return [row_to_medication_request_response(row) for row in results]
    finally:
        await release_db_connection(conn)

@app.get("/medication-requests/{request_id}", response_model=MedicationRequestResponse)
async def get_medication_request(request_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM medication_requests WHERE id = $1", request_id)
        if not result:
            raise HTTPException(status_code=404, detail="MedicationRequest not found")
        return row_to_medication_request_response(result)
    finally:
        await release_db_connection(conn)

@app.put("/medication-requests/{request_id}", response_model=MedicationRequestResponse)
async def update_medication_request(request_id: UUID, medication_request_update: MedicationRequestUpdate):
    conn = await get_db_connection()
    try:
        # Debug logging
        print(f"Updating medication request {request_id} with: {medication_request_update}")
        
        existing = await conn.fetchrow("SELECT * FROM medication_requests WHERE id = $1", request_id)
        if not existing:
            raise HTTPException(status_code=404, detail="MedicationRequest not found")
        
        update_fields = []
        params = []
        param_count = 0
        
        update_data = medication_request_update.dict(exclude_unset=True)
        print(f"Update data: {update_data}")
        
        for field, value in update_data.items():
            param_count += 1
            
            # Handle UUID fields that come as strings
            if field in ['subject_patient_id', 'medication_id', 'encounter_id', 'requester', 'performer', 'recorder', 'reported_reference', 'prior_prescription']:
                if value:
                    try:
                        # Convert string to UUID format if needed
                        if not str(value).count('-') == 4:
                            # Convert simple string to UUID format
                            value_str = str(value).replace('-', '')[:32]
                            value_str = value_str.ljust(32, '0')
                            uuid_value = f"{value_str[:8]}-{value_str[8:12]}-{value_str[12:16]}-{value_str[16:20]}-{value_str[20:32]}"
                        else:
                            uuid_value = str(value)
                        # Validate UUID format
                        UUID(uuid_value)
                        update_fields.append(f"{field} = ${param_count}")
                        params.append(UUID(uuid_value))
                    except Exception as e:
                        print(f"UUID conversion error for {field}: {e}")
                        # Skip invalid UUIDs
                        param_count -= 1
                        continue
                else:
                    update_fields.append(f"{field} = ${param_count}")
                    params.append(None)
            
            # Handle datetime fields
            elif field == 'authored_on':
                if value:
                    try:
                        from dateutil import parser
                        authored_on = parser.parse(str(value))
                        update_fields.append(f"{field} = ${param_count}")
                        params.append(authored_on)
                    except Exception as e:
                        print(f"Date parsing error: {e}")
                        param_count -= 1
                        continue
                else:
                    update_fields.append(f"{field} = ${param_count}")
                    params.append(None)
            
            # Handle JSON fields
            elif field in ['medication_codeable_concept', 'performer_type', 'group_identifier', 'course_of_therapy_type', 'dispense_request', 'substitution', 'fhir_resource']:
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps(value) if value else None)
            
            # Handle JSON array fields
            elif field in ['category', 'reason_codes', 'supporting_information', 'reason_references', 'based_on', 'insurance', 'notes', 'dosage_instructions', 'detection_issue', 'event_history']:
                update_fields.append(f"{field} = ${param_count}")
                params.append(json.dumps(value) if value else None)
            
            # Handle simple fields
            else:
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            return row_to_medication_request_response(existing)
        
        param_count += 1
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.utcnow())
        
        param_count += 1
        params.append(request_id)
        
        query = f"""
        UPDATE medication_requests 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING *
        """
        
        print(f"Update query: {query}")
        print(f"Parameters: {params}")
        
        result = await conn.fetchrow(query, *params)
        return row_to_medication_request_response(result)
    except Exception as e:
        print(f"Error updating medication request: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        await release_db_connection(conn)

@app.delete("/medication-requests/{request_id}")
async def delete_medication_request(request_id: UUID):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("DELETE FROM medication_requests WHERE id = $1 RETURNING id", request_id)
        if not result:
            raise HTTPException(status_code=404, detail="MedicationRequest not found")
        return {"message": "MedicationRequest deleted successfully", "request_id": str(request_id)}
    finally:
        await release_db_connection(conn)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
