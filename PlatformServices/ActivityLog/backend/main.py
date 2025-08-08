# ========================
# main.py
# ========================
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import get_db, engine
import models
import schemas
import crud
from services import activity_service

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Activity Log API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# Dependency to get current user (simplified for demo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, validate JWT token here
    # For demo, return a mock user ID
    return "mock-user-id"


def get_client_ip(request: Request) -> str:
    return request.client.host


# ========================
# API Routes
# ========================

@app.get("/api/activity-events", response_model=List[schemas.ActivityEventResponse])
async def get_activity_events(
    event_type: str = None,
    date_range: str = "all",
    search: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get activity events for the current user"""
    filters = schemas.ActivityEventFilters(
        event_type=event_type,
        date_range=date_range,
        search=search
    )
    
    events = crud.activity_crud.get_events(db, current_user, filters, skip, limit)
    return activity_service.format_events_for_frontend(events)


@app.post("/api/activity-events", response_model=schemas.ActivityEventResponse)
async def create_activity_event(
    event: schemas.ActivityEventCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new activity event"""
    # Add IP address from request
    if not event.ip_address:
        event.ip_address = get_client_ip(request)
    
    db_event = crud.activity_crud.create_event(db, event, current_user)
    formatted_events = activity_service.format_events_for_frontend([db_event])
    return formatted_events[0]


@app.get("/api/activity-events/{event_id}", response_model=schemas.ActivityEventResponse)
async def get_activity_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get a specific activity event"""
    event = crud.activity_crud.get_event(db, event_id, current_user)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    formatted_events = activity_service.format_events_for_frontend([event])
    return formatted_events[0]


@app.post("/api/events/sign-in")
async def log_sign_in_event(
    success: bool,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Log a sign-in event"""
    ip_address = get_client_ip(request)
    location = "Westford, United States"  # In production, use IP geolocation service
    user_agent = request.headers.get("user-agent", "")
    
    event = activity_service.log_sign_in_event(
        db, current_user, success, ip_address, location, user_agent
    )
    formatted_events = activity_service.format_events_for_frontend([event])
    return formatted_events[0]


@app.post("/api/events/hipaa-audit")
async def log_hipaa_audit_event(
    action: str,
    resource: str,
    client_id: str = None,
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Log a HIPAA audit event"""
    ip_address = get_client_ip(request) if request else None
    location = "Westford, United States"
    
    event = activity_service.log_hipaa_audit_event(
        db, current_user, action, resource, client_id, ip_address, location
    )
    formatted_events = activity_service.format_events_for_frontend([event])
    return formatted_events[0]


@app.post("/api/events/history")
async def log_history_event(
    action: str,
    resource: str,
    resource_id: str = None,
    client_id: str = None,
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Log a history event"""
    ip_address = get_client_ip(request) if request else None
    location = "Westford, United States"
    
    event = activity_service.log_history_event(
        db, current_user, action, resource, resource_id, client_id, ip_address, location
    )
    formatted_events = activity_service.format_events_for_frontend([event])
    return formatted_events[0]


@app.get("/api/clients", response_model=List[schemas.ClientInDB])
async def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get clients for the current user"""
    return crud.client_crud.get_clients(db, current_user, skip, limit)


@app.post("/api/clients", response_model=schemas.ClientInDB)
async def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Create a new client"""
    return crud.client_crud.create_client(db, client, current_user)


@app.get("/")
async def root():
    return {"message": "Activity Log API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
