# =============================================================================
# FILE: backend/app/agent/tools.py
# =============================================================================
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import json
from datetime import datetime, timedelta

from ..database import SessionLocal
from ..models.models import Appointment, Patient, Practitioner, WaitlistEntry
from ..services.patient_service import PatientService
from ..services.practitioner_service import PractitionerService

class SchedulingTools:
    """Collection of tools for the scheduling agent"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.patient_service = PatientService()
        self.practitioner_service = PractitionerService()
    
    def get_tools(self) -> List[BaseTool]:
        return [
            GetAppointmentTool(db=self.db),
            ScheduleAppointmentTool(db=self.db),
            RescheduleAppointmentTool(db=self.db),
            CancelAppointmentTool(db=self.db),
            FindAvailabilityTool(db=self.db),
            GetPatientInfoTool(db=self.db),
            GetPractitionerInfoTool(db=self.db),
            SearchAppointmentsTool(db=self.db),
            GetWaitlistTool(db=self.db),
            GenerateScheduleReportTool(db=self.db),
            AnalyzeScheduleTool(db=self.db),
            OptimizeScheduleTool(db=self.db)
        ]

class GetAppointmentTool(BaseTool):
    name = "get_appointment"
    description = "Retrieve detailed information about a specific appointment by ID"
    db: Session
    
    def _run(
        self, 
        appointment_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if not appointment:
                return f"Appointment with ID {appointment_id} not found"
            
            appointment_data = {
                "id": appointment.id,
                "title": appointment.title,
                "start": appointment.start.isoformat(),
                "end": appointment.end.isoformat(),
                "practitioner_id": appointment.practitioner_id,
                "patient_id": appointment.patient_id,
                "appointment_type": appointment.appointment_type,
                "status": appointment.status,
                "location": appointment.location,
                "notes": appointment.notes,
                "created_at": appointment.created_at.isoformat()
            }
            
            return json.dumps(appointment_data, indent=2)
        except Exception as e:
            return f"Error retrieving appointment: {str(e)}"

class ScheduleAppointmentTool(BaseTool):
    name = "schedule_appointment"
    description = "Schedule a new appointment with specified details"
    db: Session
    
    def _run(
        self, 
        patient_id: int,
        practitioner_id: int,
        start_time: str,
        end_time: str,
        appointment_type: str = "CONSULTATION",
        location: str = "Main Clinic",
        notes: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            # Validate patient exists
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                return f"Patient with ID {patient_id} not found"
            
            # Validate practitioner exists
            practitioner = self.db.query(Practitioner).filter(Practitioner.id == practitioner_id).first()
            if not practitioner:
                return f"Practitioner with ID {practitioner_id} not found"
            
            # Create appointment
            appointment = Appointment(
                title=f"{patient.first_name} {patient.last_name} - {appointment_type}",
                start=datetime.fromisoformat(start_time),
                end=datetime.fromisoformat(end_time),
                practitioner_id=practitioner_id,
                patient_id=patient_id,
                appointment_type=appointment_type,
                status="SCHEDULED",
                location=location,
                notes=notes
            )
            
            self.db.add(appointment)
            self.db.commit()
            self.db.refresh(appointment)
            
            result = {
                "success": True,
                "appointment_id": appointment.id,
                "message": f"Appointment scheduled successfully for {patient.first_name} {patient.last_name} with {practitioner.family_name}",
                "appointment": {
                    "id": appointment.id,
                    "title": appointment.title,
                    "start": appointment.start.isoformat(),
                    "end": appointment.end.isoformat(),
                    "location": appointment.location
                }
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error scheduling appointment: {str(e)}"

class RescheduleAppointmentTool(BaseTool):
    name = "reschedule_appointment"
    description = "Reschedule an existing appointment to a new time"
    db: Session
    
    def _run(
        self, 
        appointment_id: int,
        new_start_time: str,
        new_end_time: str,
        reason: str = "Rescheduled by agent",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if not appointment:
                return f"Appointment with ID {appointment_id} not found"
            
            old_start = appointment.start
            old_end = appointment.end
            
            appointment.start = datetime.fromisoformat(new_start_time)
            appointment.end = datetime.fromisoformat(new_end_time)
            appointment.notes = f"{appointment.notes}\n\nRescheduled: {reason}"
            
            self.db.commit()
            
            result = {
                "success": True,
                "appointment_id": appointment_id,
                "message": f"Appointment rescheduled from {old_start} to {appointment.start}",
                "old_time": {
                    "start": old_start.isoformat(),
                    "end": old_end.isoformat()
                },
                "new_time": {
                    "start": appointment.start.isoformat(),
                    "end": appointment.end.isoformat()
                }
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error rescheduling appointment: {str(e)}"

class CancelAppointmentTool(BaseTool):
    name = "cancel_appointment"
    description = "Cancel an existing appointment"
    db: Session
    
    def _run(
        self, 
        appointment_id: int,
        reason: str = "Cancelled by agent",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
            if not appointment:
                return f"Appointment with ID {appointment_id} not found"
            
            appointment.status = "CANCELLED"
            appointment.notes = f"{appointment.notes}\n\nCancelled: {reason}"
            
            self.db.commit()
            
            result = {
                "success": True,
                "appointment_id": appointment_id,
                "message": f"Appointment cancelled successfully",
                "cancelled_at": datetime.now().isoformat(),
                "reason": reason
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error cancelling appointment: {str(e)}"

class FindAvailabilityTool(BaseTool):
    name = "find_availability"
    description = "Find available time slots for a practitioner on a specific date"
    db: Session
    
    def _run(
        self, 
        practitioner_id: int,
        date: str,
        duration_minutes: int = 60,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            target_date = datetime.fromisoformat(date).date()
            
            # Get all appointments for the practitioner on that date
            appointments = self.db.query(Appointment).filter(
                Appointment.practitioner_id == practitioner_id,
                Appointment.start >= target_date,
                Appointment.start < target_date + timedelta(days=1)
            ).order_by(Appointment.start).all()
            
            # Define business hours (8 AM to 6 PM)
            business_start = datetime.combine(target_date, datetime.min.time().replace(hour=8))
            business_end = datetime.combine(target_date, datetime.min.time().replace(hour=18))
            
            # Generate available slots
            available_slots = []
            current_time = business_start
            
            while current_time + timedelta(minutes=duration_minutes) <= business_end:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                
                # Check if slot conflicts with existing appointments
                conflict = False
                for appointment in appointments:
                    if (current_time < appointment.end and slot_end > appointment.start):
                        conflict = True
                        break
                
                if not conflict:
                    available_slots.append({
                        "start": current_time.isoformat(),
                        "end": slot_end.isoformat(),
                        "duration_minutes": duration_minutes
                    })
                
                current_time += timedelta(minutes=30)  # 30-minute intervals
            
            result = {
                "practitioner_id": practitioner_id,
                "date": date,
                "available_slots": available_slots,
                "total_slots": len(available_slots)
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error finding availability: {str(e)}"

class GetPatientInfoTool(BaseTool):
    name = "get_patient_info"
    description = "Get detailed information about a patient"
    db: Session
    
    def _run(
        self, 
        patient_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                return f"Patient with ID {patient_id} not found"
            
            # Get patient's appointments
            appointments = self.db.query(Appointment).filter(
                Appointment.patient_id == patient_id
            ).order_by(Appointment.start.desc()).limit(5).all()
            
            patient_data = {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "email": patient.email,
                "phone": patient.phone,
                "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                "gender": patient.gender,
                "address": patient.address,
                "recent_appointments": [
                    {
                        "id": apt.id,
                        "title": apt.title,
                        "start": apt.start.isoformat(),
                        "status": apt.status,
                        "practitioner_id": apt.practitioner_id
                    } for apt in appointments
                ]
            }
            
            return json.dumps(patient_data, indent=2)
        except Exception as e:
            return f"Error retrieving patient info: {str(e)}"

class GetPractitionerInfoTool(BaseTool):
    name = "get_practitioner_info"
    description = "Get detailed information about a practitioner"
    db: Session
    
    def _run(
        self, 
        practitioner_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            practitioner = self.db.query(Practitioner).filter(Practitioner.id == practitioner_id).first()
            if not practitioner:
                return f"Practitioner with ID {practitioner_id} not found"
            
            # Get practitioner's appointments for today
            today = datetime.now().date()
            today_appointments = self.db.query(Appointment).filter(
                Appointment.practitioner_id == practitioner_id,
                Appointment.start >= today,
                Appointment.start < today + timedelta(days=1)
            ).order_by(Appointment.start).all()
            
            practitioner_data = {
                "id": practitioner.id,
                "family_name": practitioner.family_name,
                "given_names": practitioner.given_names,
                "specialty": practitioner.specialty,
                "active": practitioner.active,
                "today_appointments": [
                    {
                        "id": apt.id,
                        "title": apt.title,
                        "start": apt.start.isoformat(),
                        "end": apt.end.isoformat(),
                        "status": apt.status,
                        "patient_id": apt.patient_id
                    } for apt in today_appointments
                ],
                "appointments_count": len(today_appointments)
            }
            
            return json.dumps(practitioner_data, indent=2)
        except Exception as e:
            return f"Error retrieving practitioner info: {str(e)}"

class SearchAppointmentsTool(BaseTool):
    name = "search_appointments"
    description = "Search for appointments based on various criteria"
    db: Session
    
    def _run(
        self, 
        patient_id: Optional[int] = None,
        practitioner_id: Optional[int] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            query = self.db.query(Appointment)
            
            if patient_id:
                query = query.filter(Appointment.patient_id == patient_id)
            if practitioner_id:
                query = query.filter(Appointment.practitioner_id == practitioner_id)
            if status:
                query = query.filter(Appointment.status == status)
            if date_from:
                query = query.filter(Appointment.start >= datetime.fromisoformat(date_from))
            if date_to:
                query = query.filter(Appointment.start <= datetime.fromisoformat(date_to))
            
            appointments = query.order_by(Appointment.start.desc()).limit(limit).all()
            
            results = []
            for apt in appointments:
                results.append({
                    "id": apt.id,
                    "title": apt.title,
                    "start": apt.start.isoformat(),
                    "end": apt.end.isoformat(),
                    "practitioner_id": apt.practitioner_id,
                    "patient_id": apt.patient_id,
                    "status": apt.status,
                    "appointment_type": apt.appointment_type,
                    "location": apt.location
                })
            
            return json.dumps({
                "appointments": results,
                "total_found": len(results)
            }, indent=2)
        except Exception as e:
            return f"Error searching appointments: {str(e)}"

class GetWaitlistTool(BaseTool):
    name = "get_waitlist"
    description = "Get waitlist entries and manage waitlist"
    db: Session
    
    def _run(
        self, 
        status: Optional[str] = None,
        limit: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            query = self.db.query(WaitlistEntry)
            
            if status:
                query = query.filter(WaitlistEntry.status == status)
            
            entries = query.order_by(WaitlistEntry.created_at.desc()).limit(limit).all()
            
            results = []
            for entry in entries:
                results.append({
                    "id": entry.id,
                    "patient_id": entry.patient_id,
                    "practitioner_id": entry.practitioner_id,
                    "service_type": entry.service_type,
                    "priority": entry.priority,
                    "status": entry.status,
                    "notes": entry.notes,
                    "created_at": entry.created_at.isoformat()
                })
            
            return json.dumps({
                "waitlist_entries": results,
                "total_entries": len(results)
            }, indent=2)
        except Exception as e:
            return f"Error retrieving waitlist: {str(e)}"

class GenerateScheduleReportTool(BaseTool):
    name = "generate_schedule_report"
    description = "Generate various types of scheduling reports"
    db: Session
    
    def _run(
        self, 
        report_type: str = "daily",
        date: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            if not date:
                date = datetime.now().date().isoformat()
            
            target_date = datetime.fromisoformat(date).date()
            
            if report_type == "daily":
                # Daily schedule report
                appointments = self.db.query(Appointment).filter(
                    Appointment.start >= target_date,
                    Appointment.start < target_date + timedelta(days=1)
                ).order_by(Appointment.start).all()
                
                report = {
                    "report_type": "daily",
                    "date": date,
                    "total_appointments": len(appointments),
                    "appointments_by_status": {},
                    "appointments_by_practitioner": {},
                    "appointments_by_type": {}
                }
                
                for apt in appointments:
                    # Count by status
                    status = apt.status
                    report["appointments_by_status"][status] = report["appointments_by_status"].get(status, 0) + 1
                    
                    # Count by practitioner
                    practitioner_id = apt.practitioner_id
                    report["appointments_by_practitioner"][practitioner_id] = report["appointments_by_practitioner"].get(practitioner_id, 0) + 1
                    
                    # Count by type
                    apt_type = apt.appointment_type
                    report["appointments_by_type"][apt_type] = report["appointments_by_type"].get(apt_type, 0) + 1
                
                return json.dumps(report, indent=2)
            
            elif report_type == "weekly":
                # Weekly summary
                week_start = target_date - timedelta(days=target_date.weekday())
                week_end = week_start + timedelta(days=7)
                
                appointments = self.db.query(Appointment).filter(
                    Appointment.start >= week_start,
                    Appointment.start < week_end
                ).all()
                
                report = {
                    "report_type": "weekly",
                    "week_start": week_start.isoformat(),
                    "week_end": week_end.isoformat(),
                    "total_appointments": len(appointments),
                    "daily_breakdown": {}
                }
                
                for i in range(7):
                    day = week_start + timedelta(days=i)
                    day_appointments = [apt for apt in appointments if apt.start.date() == day]
                    report["daily_breakdown"][day.isoformat()] = len(day_appointments)
                
                return json.dumps(report, indent=2)
            
            else:
                return f"Unsupported report type: {report_type}"
                
        except Exception as e:
            return f"Error generating report: {str(e)}"

class AnalyzeScheduleTool(BaseTool):
    name = "analyze_schedule"
    description = "Analyze schedule patterns and provide insights"
    db: Session
    
    def _run(
        self, 
        practitioner_id: Optional[int] = None,
        days: int = 7,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            query = self.db.query(Appointment).filter(
                Appointment.start >= start_date,
                Appointment.start <= end_date
            )
            
            if practitioner_id:
                query = query.filter(Appointment.practitioner_id == practitioner_id)
            
            appointments = query.all()
            
            analysis = {
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "days": days
                },
                "total_appointments": len(appointments),
                "appointments_by_status": {},
                "appointments_by_type": {},
                "busiest_days": {},
                "utilization_rate": 0.0,
                "insights": []
            }
            
            # Analyze appointments
            for apt in appointments:
                # Count by status
                status = apt.status
                analysis["appointments_by_status"][status] = analysis["appointments_by_status"].get(status, 0) + 1
                
                # Count by type
                apt_type = apt.appointment_type
                analysis["appointments_by_type"][apt_type] = analysis["appointments_by_type"].get(apt_type, 0) + 1
                
                # Count by day
                day = apt.start.date().isoformat()
                analysis["busiest_days"][day] = analysis["busiest_days"].get(day, 0) + 1
            
            # Calculate utilization rate (assuming 8-hour workday)
            total_hours = days * 8
            total_appointment_hours = sum([
                (apt.end - apt.start).total_seconds() / 3600 for apt in appointments
            ])
            analysis["utilization_rate"] = (total_appointment_hours / total_hours) * 100
            
            # Generate insights
            if analysis["utilization_rate"] < 50:
                analysis["insights"].append("Low schedule utilization - consider marketing or outreach")
            elif analysis["utilization_rate"] > 90:
                analysis["insights"].append("High schedule utilization - consider adding more availability")
            
            if analysis["appointments_by_status"].get("CANCELLED", 0) > len(appointments) * 0.1:
                analysis["insights"].append("High cancellation rate - review scheduling policies")
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing schedule: {str(e)}"

class OptimizeScheduleTool(BaseTool):
    name = "optimize_schedule"
    description = "Provide schedule optimization suggestions"
    db: Session
    
    def _run(
        self, 
        practitioner_id: Optional[int] = None,
        optimization_type: str = "general",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            # Get recent schedule data
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
            
            query = self.db.query(Appointment).filter(
                Appointment.start >= start_date,
                Appointment.start <= end_date
            )
            
            if practitioner_id:
                query = query.filter(Appointment.practitioner_id == practitioner_id)
            
            appointments = query.all()
            
            optimization = {
                "optimization_type": optimization_type,
                "analysis_period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "total_appointments": len(appointments),
                "suggestions": [],
                "recommendations": []
            }
            
            # Analyze patterns and generate suggestions
            if optimization_type == "general":
                # General optimization suggestions
                if len(appointments) < 50:
                    optimization["suggestions"].append("Consider increasing appointment availability")
                
                cancellations = len([apt for apt in appointments if apt.status == "CANCELLED"])
                if cancellations > len(appointments) * 0.15:
                    optimization["suggestions"].append("Implement reminder system to reduce cancellations")
                
                # Check for gaps in schedule
                optimization["recommendations"].append("Review appointment duration settings")
                optimization["recommendations"].append("Consider block scheduling for similar appointment types")
            
            elif optimization_type == "capacity":
                # Capacity optimization
                daily_counts = {}
                for apt in appointments:
                    day = apt.start.date().isoformat()
                    daily_counts[day] = daily_counts.get(day, 0) + 1
                
                avg_daily = sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0
                max_daily = max(daily_counts.values()) if daily_counts else 0
                
                if max_daily > avg_daily * 1.5:
                    optimization["suggestions"].append("Uneven daily distribution - consider redistributing appointments")
                
                optimization["recommendations"].append(f"Average daily appointments: {avg_daily:.1f}")
                optimization["recommendations"].append(f"Peak daily appointments: {max_daily}")
            
            return json.dumps(optimization, indent=2)
        except Exception as e:
            return f"Error optimizing schedule: {str(e)}" 