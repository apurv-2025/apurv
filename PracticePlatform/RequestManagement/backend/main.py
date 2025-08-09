from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Practice Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "practice_management"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

# Pydantic models
class PractitionerBase(BaseModel):
    name: str
    specialization: str
    email: str

class Practitioner(PractitionerBase):
    id: int
    created_at: datetime

class ClientBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class Client(ClientBase):
    id: int
    created_at: datetime

class AppointmentRequestCreate(BaseModel):
    client_id: int
    practitioner_id: int
    requested_datetime: datetime
    source: str = "website"  # website, client_portal, ai_agent
    notes: Optional[str] = None

class AppointmentRequestUpdate(BaseModel):
    status: str  # 'approved' or 'denied'

class AppointmentRequest(BaseModel):
    id: int
    client_id: int
    client_name: str
    practitioner_id: int
    practitioner_name: str
    requested_datetime: datetime
    status: str
    source: str
    notes: Optional[str]
    created_at: datetime

# API Routes

@app.get("/practitioners", response_model=List[Practitioner])
async def get_practitioners():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM practitioners ORDER BY name")
            practitioners = cursor.fetchall()
            return practitioners
    finally:
        conn.close()

@app.get("/clients", response_model=List[Client])
async def get_clients():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM clients ORDER BY name")
            clients = cursor.fetchall()
            return clients
    finally:
        conn.close()

@app.post("/appointment-requests", response_model=dict)
async def create_appointment_request(request: AppointmentRequestCreate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO appointment_requests (client_id, practitioner_id, requested_datetime, source, notes)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
                """,
                (request.client_id, request.practitioner_id, request.requested_datetime, request.source, request.notes)
            )
            request_id = cursor.fetchone()[0]
            conn.commit()
            return {"id": request_id, "message": "Appointment request created successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/appointment-requests", response_model=List[AppointmentRequest])
async def get_appointment_requests():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    ar.id, ar.client_id, c.name as client_name,
                    ar.practitioner_id, p.name as practitioner_name,
                    ar.requested_datetime, ar.status, ar.source, ar.notes, ar.created_at
                FROM appointment_requests ar
                JOIN clients c ON ar.client_id = c.id
                JOIN practitioners p ON ar.practitioner_id = p.id
                ORDER BY ar.created_at DESC
                """
            )
            requests = cursor.fetchall()
            return requests
    finally:
        conn.close()

@app.get("/appointment-requests/client/{client_id}", response_model=List[AppointmentRequest])
async def get_client_appointment_requests(client_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    ar.id, ar.client_id, c.name as client_name,
                    ar.practitioner_id, p.name as practitioner_name,
                    ar.requested_datetime, ar.status, ar.source, ar.notes, ar.created_at
                FROM appointment_requests ar
                JOIN clients c ON ar.client_id = c.id
                JOIN practitioners p ON ar.practitioner_id = p.id
                WHERE ar.client_id = %s
                ORDER BY ar.created_at DESC
                """,
                (client_id,)
            )
            requests = cursor.fetchall()
            return requests
    finally:
        conn.close()

@app.put("/appointment-requests/{request_id}", response_model=dict)
async def update_appointment_request(request_id: int, update: AppointmentRequestUpdate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE appointment_requests 
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (update.status, request_id)
            )
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Appointment request not found")
            
            # If approved, create an appointment
            if update.status == 'approved':
                cursor.execute(
                    """
                    INSERT INTO appointments (client_id, practitioner_id, scheduled_datetime, notes)
                    SELECT client_id, practitioner_id, requested_datetime, notes
                    FROM appointment_requests WHERE id = %s
                    """,
                    (request_id,)
                )
            
            conn.commit()
            return {"message": f"Appointment request {update.status} successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/appointment-requests/pending", response_model=List[AppointmentRequest])
async def get_pending_requests():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    ar.id, ar.client_id, c.name as client_name,
                    ar.practitioner_id, p.name as practitioner_name,
                    ar.requested_datetime, ar.status, ar.source, ar.notes, ar.created_at
                FROM appointment_requests ar
                JOIN clients c ON ar.client_id = c.id
                JOIN practitioners p ON ar.practitioner_id = p.id
                WHERE ar.status = 'pending'
                ORDER BY ar.created_at ASC
                """
            )
            requests = cursor.fetchall()
            return requests
    finally:
        conn.close()

@app.get("/appointment-requests/source/{source}", response_model=List[AppointmentRequest])
async def get_requests_by_source(source: str):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT 
                    ar.id, ar.client_id, c.name as client_name,
                    ar.practitioner_id, p.name as practitioner_name,
                    ar.requested_datetime, ar.status, ar.source, ar.notes, ar.created_at
                FROM appointment_requests ar
                JOIN clients c ON ar.client_id = c.id
                JOIN practitioners p ON ar.practitioner_id = p.id
                WHERE ar.source = %s
                ORDER BY ar.created_at DESC
                """,
                (source,)
            )
            requests = cursor.fetchall()
            return requests
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
