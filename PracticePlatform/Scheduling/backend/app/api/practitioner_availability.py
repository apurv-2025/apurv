from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, timedelta

from app.database import get_db
from app.schemas.practitioner_availability import (
    PractitionerAvailabilityCreate,
    PractitionerAvailabilityUpdate,
    PractitionerAvailabilityResponse,
    PractitionerAvailabilityBulkCreate
)
from app.services.practitioner_availability_service import practitioner_availability_service

router = APIRouter(prefix="/practitioner-availability", tags=["practitioner-availability"])

@router.post("/", response_model=PractitionerAvailabilityResponse)
async def create_practitioner_availability(
    availability: PractitionerAvailabilityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new practitioner availability entry."""
    try:
        return await practitioner_availability_service.create_availability(db, availability)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create availability: {str(e)}"
        )

@router.post("/bulk", response_model=List[PractitionerAvailabilityResponse])
async def create_bulk_practitioner_availability(
    bulk_data: PractitionerAvailabilityBulkCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create multiple availability entries for a practitioner."""
    try:
        return await practitioner_availability_service.create_bulk_availability(db, bulk_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create bulk availability: {str(e)}"
        )

@router.get("/{practitioner_id}", response_model=List[PractitionerAvailabilityResponse])
async def get_practitioner_availability(
    practitioner_id: str,
    start_date: Optional[date] = Query(None, description="Start date for availability range"),
    end_date: Optional[date] = Query(None, description="End date for availability range"),
    active_only: bool = Query(True, description="Only return active availability entries"),
    db: AsyncSession = Depends(get_db)
):
    """Get availability for a specific practitioner."""
    try:
        return await practitioner_availability_service.get_practitioner_availability(
            db, practitioner_id, start_date, end_date, active_only
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get availability: {str(e)}"
        )

@router.get("/{practitioner_id}/schedule")
async def get_practitioner_schedule(
    practitioner_id: str,
    start_date: date = Query(..., description="Start date for schedule"),
    end_date: date = Query(..., description="End date for schedule"),
    db: AsyncSession = Depends(get_db)
):
    """Get a practitioner's complete schedule including availability and appointments."""
    try:
        return await practitioner_availability_service.get_practitioner_schedule(
            db, practitioner_id, start_date, end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get schedule: {str(e)}"
        )

@router.get("/{practitioner_id}/available-slots")
async def get_available_slots(
    practitioner_id: str,
    appointment_date: date = Query(..., description="Date to check for available slots"),
    appointment_type_id: Optional[int] = Query(None, description="Appointment type ID for duration calculation"),
    duration_minutes: Optional[int] = Query(None, description="Duration in minutes (overrides appointment type)"),
    db: AsyncSession = Depends(get_db)
):
    """Get available time slots for a practitioner on a specific date."""
    try:
        slots = await practitioner_availability_service.get_available_slots(
            db, practitioner_id, appointment_date, appointment_type_id, duration_minutes
        )
        return {
            "practitioner_id": practitioner_id,
            "date": appointment_date,
            "slots": slots
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get available slots: {str(e)}"
        )

@router.put("/{availability_id}", response_model=PractitionerAvailabilityResponse)
async def update_practitioner_availability(
    availability_id: int,
    availability_update: PractitionerAvailabilityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing practitioner availability entry."""
    try:
        updated = await practitioner_availability_service.update_availability(
            db, availability_id, availability_update
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability entry not found"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update availability: {str(e)}"
        )

@router.delete("/{availability_id}")
async def delete_practitioner_availability(
    availability_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a practitioner availability entry."""
    try:
        success = await practitioner_availability_service.delete_availability(db, availability_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability entry not found"
            )
        return {"message": "Availability entry deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete availability: {str(e)}"
        )

@router.patch("/{availability_id}/deactivate", response_model=PractitionerAvailabilityResponse)
async def deactivate_practitioner_availability(
    availability_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Deactivate a practitioner availability entry (soft delete)."""
    try:
        deactivated = await practitioner_availability_service.deactivate_availability(db, availability_id)
        if not deactivated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Availability entry not found"
            )
        return deactivated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to deactivate availability: {str(e)}"
        )

@router.get("/{practitioner_id}/weekly-schedule")
async def get_weekly_schedule(
    practitioner_id: str,
    week_start: date = Query(..., description="Start of the week (Monday)"),
    db: AsyncSession = Depends(get_db)
):
    """Get a practitioner's schedule for a specific week."""
    try:
        # Calculate end of week (Sunday)
        end_date = week_start + timedelta(days=6)
        
        return await practitioner_availability_service.get_practitioner_schedule(
            db, practitioner_id, week_start, end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get weekly schedule: {str(e)}"
        ) 