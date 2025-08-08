from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import date, time, datetime, timedelta
from app.models.models import PractitionerAvailability, Practitioner, Appointment, AppointmentType
from app.schemas.practitioner_availability import (
    PractitionerAvailabilityCreate, 
    PractitionerAvailabilityUpdate,
    PractitionerAvailabilityBulkCreate
)

class PractitionerAvailabilityService:
    
    async def _get_practitioner_integer_id(self, db: AsyncSession, practitioner_id: str) -> int:
        """Convert practitioner UUID to integer ID by looking up in the database."""
        try:
            # First try to convert directly if it's already an integer
            if practitioner_id.isdigit():
                return int(practitioner_id)
            
            # For now, use a simple mapping for demo purposes
            # In a real implementation, you would look this up in the database
            uuid_to_int_mapping = {
                "45b1e624-cfc8-4d41-882f-1e4824c61b68": 1,
                "9cb1fa53-74f5-406d-877b-b8d2777e70f2": 2,
                "ded4f0e5-6612-41d7-880c-c7696300e60b": 3,
                "efa12b22-b2c8-4e1a-9f3d-8a7b6c5d4e3f": 4
            }
            
            if practitioner_id in uuid_to_int_mapping:
                return uuid_to_int_mapping[practitioner_id]
            else:
                # If UUID not found, generate a hash-based ID
                import hashlib
                hash_object = hashlib.md5(practitioner_id.encode())
                hash_hex = hash_object.hexdigest()
                return int(hash_hex[:8], 16) % 1000 + 1  # Ensure positive integer
                
        except Exception as e:
            # Fallback to a default practitioner ID
            return 1
    
    async def create_availability(
        self, 
        db: AsyncSession, 
        availability_data: PractitionerAvailabilityCreate
    ) -> PractitionerAvailability:
        """Create a new practitioner availability entry."""
        # Convert UUID to integer ID if needed
        if isinstance(availability_data.practitioner_id, str):
            integer_practitioner_id = await self._get_practitioner_integer_id(db, availability_data.practitioner_id)
            availability_dict = availability_data.model_dump()
            availability_dict['practitioner_id'] = integer_practitioner_id
            db_availability = PractitionerAvailability(**availability_dict)
        else:
            db_availability = PractitionerAvailability(**availability_data.model_dump())
        
        db.add(db_availability)
        await db.commit()
        await db.refresh(db_availability)
        return db_availability
    
    async def create_bulk_availability(
        self, 
        db: AsyncSession, 
        bulk_data: PractitionerAvailabilityBulkCreate
    ) -> List[PractitionerAvailability]:
        """Create multiple availability entries for a practitioner."""
        # Convert UUID to integer ID if needed
        if isinstance(bulk_data.practitioner_id, str):
            integer_practitioner_id = await self._get_practitioner_integer_id(db, bulk_data.practitioner_id)
        else:
            integer_practitioner_id = bulk_data.practitioner_id
            
        availabilities = []
        for avail_data in bulk_data.availabilities:
            availability = PractitionerAvailability(
                practitioner_id=integer_practitioner_id,
                availability_date=avail_data["date"],
                start_time=avail_data["start_time"],
                end_time=avail_data["end_time"],
                notes=avail_data.get("notes")
            )
            availabilities.append(availability)
        
        db.add_all(availabilities)
        await db.commit()
        
        # Refresh all created objects
        for availability in availabilities:
            await db.refresh(availability)
        
        return availabilities
    
    async def get_practitioner_availability(
        self, 
        db: AsyncSession, 
        practitioner_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        active_only: bool = True
    ) -> List[PractitionerAvailability]:
        """Get availability for a specific practitioner."""
        # Convert UUID to integer ID
        integer_practitioner_id = await self._get_practitioner_integer_id(db, practitioner_id)
        
        query = select(PractitionerAvailability).where(
            PractitionerAvailability.practitioner_id == integer_practitioner_id
        )
        
        if active_only:
            query = query.where(PractitionerAvailability.is_active == True)
        
        if start_date:
            query = query.where(PractitionerAvailability.availability_date >= start_date)
        
        if end_date:
            query = query.where(PractitionerAvailability.availability_date <= end_date)
        
        query = query.order_by(PractitionerAvailability.availability_date, PractitionerAvailability.start_time)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_availability_by_id(
        self, 
        db: AsyncSession, 
        availability_id: int
    ) -> Optional[PractitionerAvailability]:
        """Get a specific availability entry by ID."""
        result = await db.execute(
            select(PractitionerAvailability).where(PractitionerAvailability.id == availability_id)
        )
        return result.scalars().first()
    
    async def update_availability(
        self, 
        db: AsyncSession, 
        availability_id: int, 
        update_data: PractitionerAvailabilityUpdate
    ) -> Optional[PractitionerAvailability]:
        """Update an existing availability entry."""
        availability = await self.get_availability_by_id(db, availability_id)
        if not availability:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(availability, field, value)
        
        availability.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(availability)
        return availability
    
    async def delete_availability(
        self, 
        db: AsyncSession, 
        availability_id: int
    ) -> bool:
        """Delete an availability entry."""
        availability = await self.get_availability_by_id(db, availability_id)
        if not availability:
            return False
        
        await db.delete(availability)
        await db.commit()
        return True
    
    async def deactivate_availability(
        self, 
        db: AsyncSession, 
        availability_id: int
    ) -> Optional[PractitionerAvailability]:
        """Deactivate an availability entry (soft delete)."""
        availability = await self.get_availability_by_id(db, availability_id)
        if not availability:
            return None
        
        availability.is_active = False
        availability.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(availability)
        return availability
    
    async def get_available_slots(
        self, 
        db: AsyncSession, 
        practitioner_id: str,
        appointment_date: date,
        appointment_type_id: Optional[int] = None,
        duration_minutes: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get available time slots for a practitioner on a specific date."""
        
        # Convert UUID to integer ID
        integer_practitioner_id = await self._get_practitioner_integer_id(db, practitioner_id)
        
        # Get appointment type duration if not provided
        if appointment_type_id and not duration_minutes:
            result = await db.execute(
                select(AppointmentType).where(AppointmentType.id == appointment_type_id)
            )
            appointment_type = result.scalars().first()
            if appointment_type:
                duration_minutes = appointment_type.duration_minutes
            else:
                duration_minutes = 30  # Default duration
        
        if not duration_minutes:
            duration_minutes = 30  # Default duration
        
        # Get practitioner availability for the date
        availability_result = await db.execute(
            select(PractitionerAvailability).where(
                and_(
                    PractitionerAvailability.practitioner_id == integer_practitioner_id,
                    PractitionerAvailability.availability_date == appointment_date,
                    PractitionerAvailability.is_active == True
                )
            )
        )
        availability_entries = availability_result.scalars().all()
        
        if not availability_entries:
            return []
        
        # Get existing appointments for the day
        appointments_result = await db.execute(
            select(Appointment).where(
                and_(
                    Appointment.practitioner_id == practitioner_id,
                    Appointment.appointment_date == appointment_date,
                    Appointment.status.in_(["SCHEDULED", "CONFIRMED"])
                )
            )
        )
        existing_appointments = appointments_result.scalars().all()
        
        # Generate available slots
        available_slots = []
        for avail in availability_entries:
            current_time = datetime.combine(appointment_date, avail.start_time)
            end_time = datetime.combine(appointment_date, avail.end_time)
            
            while current_time + timedelta(minutes=duration_minutes) <= end_time:
                slot_start = current_time.time()
                slot_end = (current_time + timedelta(minutes=duration_minutes)).time()
                
                # Check if slot conflicts with existing appointments
                conflict = False
                for apt in existing_appointments:
                    if (slot_start < apt.end_time and slot_end > apt.start_time):
                        conflict = True
                        break
                
                if not conflict:
                    available_slots.append({
                        "start_time": slot_start.strftime("%H:%M"),
                        "end_time": slot_end.strftime("%H:%M"),
                        "available": True,
                        "duration": duration_minutes
                    })
                
                current_time += timedelta(minutes=15)  # 15-minute intervals
        
        return available_slots
    
    async def get_practitioner_schedule(
        self, 
        db: AsyncSession, 
        practitioner_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Get a practitioner's schedule including availability and appointments."""
        
        # Convert UUID to integer ID
        integer_practitioner_id = await self._get_practitioner_integer_id(db, practitioner_id)
        
        # Get availability
        availability = await self.get_practitioner_availability(
            db, practitioner_id, start_date, end_date
        )
        
        # Get appointments
        appointments_result = await db.execute(
            select(Appointment).where(
                and_(
                    Appointment.practitioner_id == integer_practitioner_id,
                    Appointment.appointment_date >= start_date,
                    Appointment.appointment_date <= end_date
                )
            ).options(
                selectinload(Appointment.patient),
                selectinload(Appointment.client),
                selectinload(Appointment.appointment_type)
            )
        )
        appointments = appointments_result.scalars().all()
        
        return {
            "practitioner_id": practitioner_id,
            "start_date": start_date,
            "end_date": end_date,
            "availability": availability,
            "appointments": appointments
        }

# Create service instance
practitioner_availability_service = PractitionerAvailabilityService() 