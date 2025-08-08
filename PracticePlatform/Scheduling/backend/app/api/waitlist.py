"""
Waitlist API Router
Provides endpoints for waitlist management with integration to Patient and Practitioner services
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

from app.services.patient_service import patient_service
from app.services.practitioner_service import practitioner_service
from app.utils.enums import WaitlistPriority, WaitlistStatus, ServiceType

router = APIRouter(prefix="/waitlist", tags=["waitlist"])

# Pydantic models for request/response
class WaitlistEntryCreate(BaseModel):
    patient_id: Optional[str] = None  # UUID from Patient service
    practitioner_id: Optional[str] = None  # UUID from Practitioner service
    service_type: ServiceType
    priority: WaitlistPriority = WaitlistPriority.NORMAL
    preferred_dates: Optional[List[str]] = None  # List of date strings
    preferred_times: Optional[List[str]] = None  # List of time strings
    notes: Optional[str] = None

class WaitlistEntryUpdate(BaseModel):
    practitioner_id: Optional[str] = None
    service_type: Optional[ServiceType] = None
    priority: Optional[WaitlistPriority] = None
    preferred_dates: Optional[List[str]] = None
    preferred_times: Optional[List[str]] = None
    status: Optional[WaitlistStatus] = None
    notes: Optional[str] = None

class WaitlistEntryResponse(BaseModel):
    id: int
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    practitioner_id: Optional[str] = None
    practitioner_name: Optional[str] = None
    service_type: ServiceType
    priority: WaitlistPriority
    status: WaitlistStatus
    preferred_dates: Optional[List[str]] = None
    preferred_times: Optional[List[str]] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Mock waitlist storage (in production, this would be a database)
waitlist_entries = []
entry_id_counter = 1

def get_next_id():
    global entry_id_counter
    entry_id_counter += 1
    return entry_id_counter - 1

@router.get("/", response_model=List[WaitlistEntryResponse])
async def get_waitlist_entries(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    status: Optional[WaitlistStatus] = Query(None, description="Filter by status"),
    priority: Optional[WaitlistPriority] = Query(None, description="Filter by priority"),
    service_type: Optional[ServiceType] = Query(None, description="Filter by service type")
):
    """
    Get waitlist entries with optional filtering
    """
    try:
        # Filter entries
        filtered_entries = waitlist_entries.copy()
        
        if status:
            filtered_entries = [e for e in filtered_entries if e["status"] == status]
        if priority:
            filtered_entries = [e for e in filtered_entries if e["priority"] == priority]
        if service_type:
            filtered_entries = [e for e in filtered_entries if e["service_type"] == service_type]
        
        # Apply pagination
        paginated_entries = filtered_entries[skip:skip + limit]
        
        # Enrich with patient and practitioner names
        enriched_entries = []
        for entry in paginated_entries:
            enriched_entry = entry.copy()
            
            # Get patient name if patient_id exists
            if entry.get("patient_id"):
                try:
                    patient = await patient_service.get_patient_by_id(entry["patient_id"])
                    enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
                except:
                    enriched_entry["patient_name"] = "Unknown Patient"
            
            # Get practitioner name if practitioner_id exists
            if entry.get("practitioner_id"):
                try:
                    practitioner = await practitioner_service.get_practitioner_by_id(entry["practitioner_id"])
                    enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
                except:
                    enriched_entry["practitioner_name"] = "Unknown Practitioner"
            
            enriched_entries.append(enriched_entry)
        
        return enriched_entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch waitlist entries: {str(e)}")

@router.get("/{entry_id}", response_model=WaitlistEntryResponse)
async def get_waitlist_entry(entry_id: int):
    """
    Get a specific waitlist entry by ID
    """
    try:
        entry = next((e for e in waitlist_entries if e["id"] == entry_id), None)
        if not entry:
            raise HTTPException(status_code=404, detail="Waitlist entry not found")
        
        # Enrich with patient and practitioner names
        enriched_entry = entry.copy()
        
        if entry.get("patient_id"):
            try:
                patient = await patient_service.get_patient_by_id(entry["patient_id"])
                enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
            except:
                enriched_entry["patient_name"] = "Unknown Patient"
        
        if entry.get("practitioner_id"):
            try:
                practitioner = await practitioner_service.get_practitioner_by_id(entry["practitioner_id"])
                enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
            except:
                enriched_entry["practitioner_name"] = "Unknown Practitioner"
        
        return enriched_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch waitlist entry: {str(e)}")

@router.post("/", response_model=WaitlistEntryResponse)
async def create_waitlist_entry(entry_data: WaitlistEntryCreate):
    """
    Create a new waitlist entry
    """
    try:
        # Validate patient_id if provided
        if entry_data.patient_id:
            try:
                await patient_service.get_patient_by_id(entry_data.patient_id)
            except:
                raise HTTPException(status_code=400, detail="Invalid patient ID")
        
        # Validate practitioner_id if provided
        if entry_data.practitioner_id:
            try:
                await practitioner_service.get_practitioner_by_id(entry_data.practitioner_id)
            except:
                raise HTTPException(status_code=400, detail="Invalid practitioner ID")
        
        # Create new entry
        new_entry = {
            "id": get_next_id(),
            "patient_id": entry_data.patient_id,
            "practitioner_id": entry_data.practitioner_id,
            "service_type": entry_data.service_type,
            "priority": entry_data.priority,
            "status": WaitlistStatus.ACTIVE,
            "preferred_dates": entry_data.preferred_dates or [],
            "preferred_times": entry_data.preferred_times or [],
            "notes": entry_data.notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        waitlist_entries.append(new_entry)
        
        # Enrich with names for response
        enriched_entry = new_entry.copy()
        
        if new_entry.get("patient_id"):
            try:
                patient = await patient_service.get_patient_by_id(new_entry["patient_id"])
                enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
            except:
                enriched_entry["patient_name"] = "Unknown Patient"
        
        if new_entry.get("practitioner_id"):
            try:
                practitioner = await practitioner_service.get_practitioner_by_id(new_entry["practitioner_id"])
                enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
            except:
                enriched_entry["practitioner_name"] = "Unknown Practitioner"
        
        return enriched_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create waitlist entry: {str(e)}")

@router.put("/{entry_id}", response_model=WaitlistEntryResponse)
async def update_waitlist_entry(entry_id: int, entry_data: WaitlistEntryUpdate):
    """
    Update an existing waitlist entry
    """
    try:
        entry = next((e for e in waitlist_entries if e["id"] == entry_id), None)
        if not entry:
            raise HTTPException(status_code=404, detail="Waitlist entry not found")
        
        # Validate practitioner_id if provided
        if entry_data.practitioner_id:
            try:
                await practitioner_service.get_practitioner_by_id(entry_data.practitioner_id)
            except:
                raise HTTPException(status_code=400, detail="Invalid practitioner ID")
        
        # Update fields
        update_data = entry_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            entry[field] = value
        
        entry["updated_at"] = datetime.utcnow()
        
        # Enrich with names for response
        enriched_entry = entry.copy()
        
        if entry.get("patient_id"):
            try:
                patient = await patient_service.get_patient_by_id(entry["patient_id"])
                enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
            except:
                enriched_entry["patient_name"] = "Unknown Patient"
        
        if entry.get("practitioner_id"):
            try:
                practitioner = await practitioner_service.get_practitioner_by_id(entry["practitioner_id"])
                enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
            except:
                enriched_entry["practitioner_name"] = "Unknown Practitioner"
        
        return enriched_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update waitlist entry: {str(e)}")

@router.delete("/{entry_id}")
async def delete_waitlist_entry(entry_id: int):
    """
    Delete a waitlist entry
    """
    try:
        entry = next((e for e in waitlist_entries if e["id"] == entry_id), None)
        if not entry:
            raise HTTPException(status_code=404, detail="Waitlist entry not found")
        
        waitlist_entries.remove(entry)
        return {"message": "Waitlist entry deleted successfully", "entry_id": entry_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete waitlist entry: {str(e)}")

@router.get("/search/patient/{patient_id}", response_model=List[WaitlistEntryResponse])
async def search_waitlist_by_patient(patient_id: str):
    """
    Search waitlist entries by patient ID
    """
    try:
        # Validate patient exists
        await patient_service.get_patient_by_id(patient_id)
        
        # Find entries for this patient
        patient_entries = [e for e in waitlist_entries if e.get("patient_id") == patient_id]
        
        # Enrich with names
        enriched_entries = []
        for entry in patient_entries:
            enriched_entry = entry.copy()
            
            try:
                patient = await patient_service.get_patient_by_id(entry["patient_id"])
                enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
            except:
                enriched_entry["patient_name"] = "Unknown Patient"
            
            if entry.get("practitioner_id"):
                try:
                    practitioner = await practitioner_service.get_practitioner_by_id(entry["practitioner_id"])
                    enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
                except:
                    enriched_entry["practitioner_name"] = "Unknown Practitioner"
            
            enriched_entries.append(enriched_entry)
        
        return enriched_entries
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search waitlist by patient: {str(e)}")

@router.get("/search/practitioner/{practitioner_id}", response_model=List[WaitlistEntryResponse])
async def search_waitlist_by_practitioner(practitioner_id: str):
    """
    Search waitlist entries by practitioner ID
    """
    try:
        # Validate practitioner exists
        await practitioner_service.get_practitioner_by_id(practitioner_id)
        
        # Find entries for this practitioner
        practitioner_entries = [e for e in waitlist_entries if e.get("practitioner_id") == practitioner_id]
        
        # Enrich with names
        enriched_entries = []
        for entry in practitioner_entries:
            enriched_entry = entry.copy()
            
            if entry.get("patient_id"):
                try:
                    patient = await patient_service.get_patient_by_id(entry["patient_id"])
                    enriched_entry["patient_name"] = f"{' '.join(patient.get('given_names', []))} {patient.get('family_name', '')}".strip()
                except:
                    enriched_entry["patient_name"] = "Unknown Patient"
            
            try:
                practitioner = await practitioner_service.get_practitioner_by_id(entry["practitioner_id"])
                enriched_entry["practitioner_name"] = f"{' '.join(practitioner.get('given_names', []))} {practitioner.get('family_name', '')}".strip()
            except:
                enriched_entry["practitioner_name"] = "Unknown Practitioner"
            
            enriched_entries.append(enriched_entry)
        
        return enriched_entries
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search waitlist by practitioner: {str(e)}")

@router.post("/{entry_id}/schedule")
async def schedule_from_waitlist(entry_id: int):
    """
    Mark a waitlist entry as scheduled (this would typically create an appointment)
    """
    try:
        entry = next((e for e in waitlist_entries if e["id"] == entry_id), None)
        if not entry:
            raise HTTPException(status_code=404, detail="Waitlist entry not found")
        
        if entry["status"] == WaitlistStatus.SCHEDULED:
            raise HTTPException(status_code=400, detail="Entry is already scheduled")
        
        entry["status"] = WaitlistStatus.SCHEDULED
        entry["updated_at"] = datetime.utcnow()
        
        return {
            "message": "Waitlist entry marked as scheduled",
            "entry_id": entry_id,
            "status": WaitlistStatus.SCHEDULED
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule waitlist entry: {str(e)}")

@router.get("/stats/summary")
async def get_waitlist_stats():
    """
    Get waitlist statistics
    """
    try:
        total_entries = len(waitlist_entries)
        active_entries = len([e for e in waitlist_entries if e["status"] == WaitlistStatus.ACTIVE])
        contacted_entries = len([e for e in waitlist_entries if e["status"] == WaitlistStatus.CONTACTED])
        scheduled_entries = len([e for e in waitlist_entries if e["status"] == WaitlistStatus.SCHEDULED])
        
        priority_stats = {}
        for priority in WaitlistPriority:
            priority_stats[priority.value] = len([e for e in waitlist_entries if e["priority"] == priority])
        
        service_type_stats = {}
        for service_type in ServiceType:
            service_type_stats[service_type.value] = len([e for e in waitlist_entries if e["service_type"] == service_type])
        
        return {
            "total_entries": total_entries,
            "active_entries": active_entries,
            "contacted_entries": contacted_entries,
            "scheduled_entries": scheduled_entries,
            "priority_distribution": priority_stats,
            "service_type_distribution": service_type_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get waitlist stats: {str(e)}") 