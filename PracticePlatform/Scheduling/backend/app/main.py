"""
Scheduling2.0 - Main Application Entry Point
Merged FastAPI application combining features from both MBH-Scheduling and Scheduling projects
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional

from app.database import engine, Base, get_db
from app.models.models import *
from app.utils.enums import UserRole

# Import routers
from app.api import patients, practitioners, waitlist, agent, practitioner_availability, notifications

# Create all database tables
async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Initialize the FastAPI app
app = FastAPI(
    title="Scheduling2.0 API",
    version="2.0.0",
    description="Unified scheduling system for medical and mental health practices",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React app URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Login endpoint for authentication."""
    # For now, return a mock token for demo purposes
    # In production, you would validate credentials against the database
    if form_data.username == "admin@clinic.com" and form_data.password == "password123":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/users/me")
async def read_users_me():
    """Get current user information."""
    # For demo purposes, return mock user data
    return {
        "id": 1,
        "email": "admin@clinic.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "phone": "555-0100",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }

# Calendar and Appointment endpoints
# Mock appointments data store
appointments_store = [
    {
        "id": 1,
        "title": "Dr. John Smith - John Doe",
        "start": "2024-08-05T09:00:00",
        "end": "2024-08-05T10:00:00",
        "practitioner_id": "efa12b22-b2a8-4de5-b1fe-b06925cd4922",
        "practitioner_name": "John Robert Smith",
        "patient_id": 1,
        "patient_name": "John Doe",
        "client_id": None,
        "appointment_type": "Emergency",
        "status": "CONFIRMED",
        "location": "Main Clinic",
        "notes": "Updated to emergency appointment",
        "color": "#f39c12"
    },
    {
        "id": 2,
        "title": "Dr. Sarah Johnson - Sarah Johnson",
        "start": "2024-08-05T14:00:00",
        "end": "2024-08-05T15:00:00",
        "practitioner_id": "ded4f0e5-6612-41d7-880c-c7696300e60b",
        "practitioner_name": "Sarah Marie Johnson",
        "patient_id": None,
        "patient_name": None,
        "client_id": 1,
        "client_name": "Sarah Johnson",
        "appointment_type": "THERAPY",
        "status": "SCHEDULED",
        "location": "Telehealth",
        "notes": "Therapy session",
        "color": "#e74c3c"
    },
    {
        "id": 3,
        "title": "Dr. John Smith - Follow-up",
        "start": "2024-08-06T11:00:00",
        "end": "2024-08-06T11:30:00",
        "practitioner_id": "efa12b22-b2a8-4de5-b1fe-b06925cd4922",
        "practitioner_name": "John Robert Smith",
        "patient_id": 2,
        "patient_name": "Jane Smith",
        "client_id": None,
        "appointment_type": "FOLLOW_UP",
        "status": "SCHEDULED",
        "location": "Main Clinic",
        "notes": "Follow-up appointment",
        "color": "#2ecc71"
    },
    {
        "id": 4,
        "title": "Dr. Robert Williams - Consultation",
        "start": "2024-08-07T10:00:00",
        "end": "2024-08-07T11:00:00",
        "practitioner_id": "9cb1fa53-74f5-406d-877b-b8d2777e70f2",
        "practitioner_name": "Robert James Williams",
        "patient_id": 3,
        "patient_name": "Michael Brown",
        "client_id": None,
        "appointment_type": "CONSULTATION",
        "status": "SCHEDULED",
        "location": "Downtown Office",
        "notes": "Initial consultation",
        "color": "#3498db"
    },
    {
        "id": 5,
        "title": "Dr. Emily Davis - Assessment",
        "start": "2024-08-07T15:00:00",
        "end": "2024-08-07T16:00:00",
        "practitioner_id": "45b1e624-cfc8-4d41-882f-1e4824c61b68",
        "practitioner_name": "Emily Claire Davis",
        "patient_id": 4,
        "patient_name": "Lisa Wilson",
        "client_id": None,
        "appointment_type": "ASSESSMENT",
        "status": "SCHEDULED",
        "location": "West Clinic",
        "notes": "Psychological assessment",
        "color": "#9b59b6"
    }
]

@app.get("/appointments/")
async def get_appointments(
    start_date: str = None,
    end_date: str = None,
    practitioner_id: int = None,
    patient_id: int = None,
    client_id: int = None
):
    """Get appointments for calendar view."""
    # Filter appointments based on parameters
    filtered_appointments = appointments_store.copy()
    
    if start_date and end_date:
        # Filter appointments by date range
        filtered_appointments = [
            apt for apt in filtered_appointments 
            if start_date <= apt["start"][:10] <= end_date
        ]
    
    if practitioner_id:
        filtered_appointments = [apt for apt in filtered_appointments if apt["practitioner_id"] == practitioner_id]
    
    if patient_id:
        filtered_appointments = [apt for apt in filtered_appointments if apt["patient_id"] == patient_id]
    
    if client_id:
        filtered_appointments = [apt for apt in filtered_appointments if apt["client_id"] == client_id]
    
    return filtered_appointments

@app.post("/appointments/")
async def create_appointment(appointment_data: dict):
    """Create a new appointment."""
    try:
        # Generate new ID
        new_id = max([apt["id"] for apt in appointments_store]) + 1 if appointments_store else 1
        
        # Get appointment type and assign color
        appointment_type = appointment_data.get("appointment_type", "CONSULTATION")
        
        # Color mapping based on appointment type
        color_mapping = {
            "CONSULTATION": "#3498db",     # Blue
            "INITIAL CONSULTATION": "#3498db",  # Blue
            "THERAPY": "#e74c3c",          # Red  
            "THERAPY SESSION": "#e74c3c",  # Red
            "FOLLOW_UP": "#2ecc71",        # Green
            "FOLLOW-UP": "#2ecc71",        # Green
            "EMERGENCY": "#f39c12",        # Orange
            "ASSESSMENT": "#9b59b6",       # Purple
            "MEDICAL": "#1abc9c",          # Teal
            "MENTAL_HEALTH": "#e67e22"     # Dark Orange
        }
        
        # Get color for appointment type, default to blue
        appointment_color = color_mapping.get(appointment_type.upper(), "#3498db")
        
        # Create new appointment
        new_appointment = {
            "id": new_id,
            "title": appointment_data.get("title", "New Appointment"),
            "start": appointment_data.get("start"),
            "end": appointment_data.get("end"),
            "practitioner_id": appointment_data.get("practitioner_id"),
            "practitioner_name": appointment_data.get("practitioner_name", ""),
            "patient_id": appointment_data.get("patient_id"),
            "patient_name": appointment_data.get("patient_name", ""),
            "client_id": appointment_data.get("client_id"),
            "client_name": appointment_data.get("client_name", ""),
            "appointment_type": appointment_type,
            "status": appointment_data.get("status", "SCHEDULED"),
            "location": appointment_data.get("location", ""),
            "notes": appointment_data.get("notes", ""),
            "color": appointment_color
        }
        
        # Add to store
        appointments_store.append(new_appointment)
        
        return new_appointment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create appointment: {str(e)}")

@app.put("/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, appointment_data: dict):
    """Update an existing appointment."""
    try:
        # Find appointment
        appointment = next((apt for apt in appointments_store if apt["id"] == appointment_id), None)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Color mapping based on appointment type
        color_mapping = {
            "CONSULTATION": "#3498db",     # Blue
            "INITIAL CONSULTATION": "#3498db",  # Blue
            "THERAPY": "#e74c3c",          # Red  
            "THERAPY SESSION": "#e74c3c",  # Red
            "FOLLOW_UP": "#2ecc71",        # Green
            "FOLLOW-UP": "#2ecc71",        # Green
            "EMERGENCY": "#f39c12",        # Orange
            "ASSESSMENT": "#9b59b6",       # Purple
            "MEDICAL": "#1abc9c",          # Teal
            "MENTAL_HEALTH": "#e67e22"     # Dark Orange
        }
        
        # Update appointment
        for key, value in appointment_data.items():
            if key in appointment:
                appointment[key] = value
        
        # Update color if appointment type changed
        if "appointment_type" in appointment_data:
            appointment_type = appointment_data["appointment_type"]
            appointment["color"] = color_mapping.get(appointment_type.upper(), "#3498db")
        
        return appointment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update appointment: {str(e)}")

@app.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    """Delete an appointment."""
    try:
        # Find and remove appointment
        global appointments_store
        appointment = next((apt for apt in appointments_store if apt["id"] == appointment_id), None)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        appointments_store = [apt for apt in appointments_store if apt["id"] != appointment_id]
        
        return {"message": "Appointment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete appointment: {str(e)}")

@app.get("/practitioners/")
async def get_practitioners(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get all practitioners for calendar from integrated service."""
    try:
        from app.services.practitioner_service import practitioner_service
        practitioners = await practitioner_service.get_practitioners(skip=skip, limit=limit, active=active)
        
        # Transform to calendar format
        calendar_practitioners = []
        colors = ["#3498db", "#e74c3c", "#f39c12", "#2ecc71", "#9b59b6", "#1abc9c"]
        
        for i, practitioner in enumerate(practitioners):
            # Extract name from FHIR format
            family_name = practitioner.get("family_name", "")
            given_names = practitioner.get("given_names", [])
            given_name = " ".join(given_names) if given_names else ""
            full_name = f"{given_name} {family_name}".strip()
            
            if not full_name:
                full_name = f"Practitioner {practitioner.get('fhir_id', 'Unknown')}"
            
            calendar_practitioners.append({
                "id": practitioner.get("id"),
                "name": full_name,
                "specialty": "General Practice",  # Default specialty
                "color": colors[i % len(colors)],
                "fhir_id": practitioner.get("fhir_id"),
                "active": practitioner.get("active", True)
            })
        
        # Apply pagination
        start_index = skip
        end_index = skip + limit
        paginated_practitioners = calendar_practitioners[start_index:end_index]
        
        return paginated_practitioners
    except Exception as e:
        # Fallback to mock data if service is unavailable
        mock_data = [
            {
                "id": 1,
                "name": "Dr. John Smith",
                "specialty": "General Medicine",
                "color": "#3498db",
                "fhir_id": "mock-001",
                "active": True
            },
            {
                "id": 2,
                "name": "Dr. Sarah Wilson",
                "specialty": "Psychology",
                "color": "#e74c3c",
                "fhir_id": "mock-002",
                "active": True
            },
            {
                "id": 3,
                "name": "Dr. Michael Brown",
                "specialty": "Psychiatry",
                "color": "#f39c12",
                "fhir_id": "mock-003",
                "active": True
            }
        ]
        
        # Apply pagination to mock data
        start_index = skip
        end_index = skip + limit
        return mock_data[start_index:end_index]

@app.get("/practitioners/count")
async def get_practitioners_count(
    active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get total count of practitioners."""
    try:
        from app.services.practitioner_service import practitioner_service
        # Get all practitioners to count them
        practitioners = await practitioner_service.get_practitioners(limit=1000, active=active)
        return {"total": len(practitioners)}
    except Exception as e:
        # Fallback to mock count
        return {"total": 9}  # Current number of practitioners in the system

@app.get("/appointment-types/")
async def get_appointment_types():
    """Get appointment types for calendar."""
    return [
        {
            "id": 1,
            "name": "Initial Consultation",
            "duration_minutes": 60,
            "color": "#3498db"
        },
        {
            "id": 2,
            "name": "Therapy Session",
            "duration_minutes": 50,
            "color": "#e74c3c"
        },
        {
            "id": 3,
            "name": "Follow-up",
            "duration_minutes": 30,
            "color": "#2ecc71"
        },
        {
            "id": 4,
            "name": "Emergency",
            "duration_minutes": 45,
            "color": "#f39c12"
        }
    ]



# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0",
        "service": "Scheduling2.0 API"
    }



# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Scheduling2.0 API",
        "version": "2.0.0",
        "description": "Unified scheduling system for medical and mental health practices",
        "docs": "/docs",
        "health": "/health"
    }

# Mock practitioner availability endpoints for demo
@app.get("/practitioner-availability/{practitioner_id}")
async def get_practitioner_availability_mock(practitioner_id: str):
    """Mock endpoint for practitioner availability."""
    return []

@app.post("/practitioner-availability/")
async def create_practitioner_availability_mock(availability_data: dict):
    """Mock endpoint for creating practitioner availability."""
    return {
        "id": 1,
        "practitioner_id": availability_data.get("practitioner_id"),
        "availability_date": availability_data.get("availability_date"),
        "start_time": availability_data.get("start_time"),
        "end_time": availability_data.get("end_time"),
        "notes": availability_data.get("notes"),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@app.get("/practitioner-availability/{practitioner_id}/available-slots")
async def get_available_slots_mock(
    practitioner_id: str,
    appointment_date: str,
    appointment_type_id: int = None,
    duration_minutes: int = None
):
    """Mock endpoint for available slots."""
    # Generate mock available slots
    slots = []
    for i in range(8):  # 8 hours of availability
        hour = 9 + i
        if hour < 17:  # 9 AM to 5 PM
            time_slot = f"{hour:02d}:00"
            slots.append({
                "start_time": time_slot,
                "end_time": f"{hour:02d}:30",
                "available": True,
                "duration": duration_minutes or 30
            })
    
    return {
        "practitioner_id": practitioner_id,
        "date": appointment_date,
        "slots": slots
    }

# Include routers
app.include_router(patients.router)
app.include_router(practitioners.router)
app.include_router(waitlist.router)
app.include_router(agent.router)
app.include_router(notifications.router)
# app.include_router(practitioner_availability.router)  # Commented out to use mock endpoints

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    await create_tables()
    print("Scheduling2.0 API started successfully!")

# Run the server (for development use only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 