from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime, date
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/telehealth", tags=["telehealth"])

# Mock telehealth data
MOCK_UPCOMING_APPOINTMENTS = [
    {
        "id": 1,
        "appointmentId": "TH-2024-001",
        "type": "video",
        "patientName": "John Smith",
        "providerName": "Dr. Sarah Johnson",
        "specialty": "Primary Care",
        "scheduledDate": "2024-02-20",
        "scheduledTime": "2:00 PM",
        "duration": 30,
        "status": "scheduled",
        "meetingUrl": "https://telehealth.clinic.com/room/th-001",
        "joinAvailable": True,
        "joinTime": "1:50 PM",
        "preVisitCompleted": True,
        "techCheckPassed": True,
        "appointmentNotes": "Follow-up for blood pressure monitoring",
        "insuranceVerified": True,
        "consentSigned": True,
        "prescriptionsReady": False,
        "documentsToReview": ["Lab Results - Feb 15", "Previous Visit Summary"]
    },
    {
        "id": 2,
        "appointmentId": "TH-2024-002",
        "type": "audio",
        "patientName": "John Smith",
        "providerName": "Dr. Michael Chen",
        "specialty": "Cardiology",
        "scheduledDate": "2024-02-25",
        "scheduledTime": "10:30 AM",
        "duration": 45,
        "status": "confirmed",
        "meetingUrl": "https://telehealth.clinic.com/room/th-002",
        "joinAvailable": False,
        "joinTime": "10:20 AM",
        "preVisitCompleted": False,
        "techCheckPassed": False,
        "appointmentNotes": "Consultation for cardiac stress test results",
        "insuranceVerified": True,
        "consentSigned": False,
        "prescriptionsReady": True,
        "documentsToReview": ["Stress Test Results", "EKG Report", "Medication History"]
    },
    {
        "id": 3,
        "appointmentId": "TH-2024-003",
        "type": "video",
        "patientName": "John Smith",
        "providerName": "Dr. Emily Rodriguez",
        "specialty": "Dermatology",
        "scheduledDate": "2024-03-05",
        "scheduledTime": "3:15 PM",
        "duration": 20,
        "status": "pending-confirmation",
        "meetingUrl": None,
        "joinAvailable": False,
        "joinTime": None,
        "preVisitCompleted": False,
        "techCheckPassed": False,
        "appointmentNotes": "Skin lesion evaluation with photo documentation",
        "insuranceVerified": False,
        "consentSigned": False,
        "prescriptionsReady": False,
        "documentsToReview": ["Previous Dermatology Photos", "Treatment History"]
    }
]

MOCK_COMPLETED_SESSIONS = [
    {
        "id": 101,
        "appointmentId": "TH-2024-050",
        "patientName": "John Smith",
        "providerName": "Dr. Sarah Johnson",
        "specialty": "Primary Care",
        "sessionDate": "2024-02-01",
        "sessionTime": "2:00 PM",
        "duration": 28,
        "actualDuration": 28,
        "type": "video",
        "status": "completed",
        "quality": "excellent",
        "issuesReported": False,
        "summary": "Routine follow-up completed successfully. Blood pressure stable.",
        "prescriptionsIssued": 2,
        "followUpScheduled": True,
        "nextAppointment": "2024-03-01",
        "patientSatisfaction": 5,
        "technicalIssues": "None",
        "recordingAvailable": True,
        "transcriptAvailable": True
    },
    {
        "id": 102,
        "appointmentId": "TH-2024-049",
        "patientName": "John Smith",
        "providerName": "Dr. Lisa Park",
        "specialty": "Mental Health",
        "sessionDate": "2024-01-28",
        "sessionTime": "11:00 AM",
        "duration": 50,
        "actualDuration": 52,
        "type": "video",
        "status": "completed",
        "quality": "good",
        "issuesReported": True,
        "summary": "Therapy session focused on anxiety management techniques.",
        "prescriptionsIssued": 0,
        "followUpScheduled": True,
        "nextAppointment": "2024-02-25",
        "patientSatisfaction": 4,
        "technicalIssues": "Minor audio delay in first 5 minutes",
        "recordingAvailable": False,
        "transcriptAvailable": False
    }
]

MOCK_SYSTEM_STATUS = {
    "serverStatus": "operational",
    "lastCheck": "2024-02-16 14:30:00",
    "uptime": "99.97%",
    "activeUsers": 1247,
    "systemLoad": "low",
    "maintenanceScheduled": False,
    "maintenanceWindow": None,
    "supportedBrowsers": ["Chrome 90+", "Firefox 88+", "Safari 14+", "Edge 90+"],
    "minimumBandwidth": "1 Mbps upload / 1 Mbps download",
    "recommendedBandwidth": "2 Mbps upload / 2 Mbps download",
    "systemRequirements": {
        "os": ["Windows 10+", "macOS 10.15+", "iOS 14+", "Android 8+"],
        "browser": ["Chrome", "Firefox", "Safari", "Edge"],
        "camera": "HD Camera (720p minimum)",
        "microphone": "Built-in or external microphone",
        "speakers": "Built-in speakers or headphones recommended"
    }
}

MOCK_DEVICE_CHECKS = {
    "camera": {"status": "working", "resolution": "1080p", "framerate": "30fps"},
    "microphone": {"status": "working", "level": 85, "quality": "good"},
    "speakers": {"status": "working", "volume": 75, "quality": "excellent"},
    "connection": {
        "status": "excellent",
        "speed": "45.2 Mbps",
        "latency": "23ms",
        "packetLoss": "0.1%",
        "jitter": "2ms"
    },
    "browser": {
        "name": "Chrome",
        "version": "121.0.6167.184",
        "supported": True,
        "webrtc": True,
        "permissions": {
            "camera": "granted",
            "microphone": "granted",
            "notifications": "granted"
        }
    },
    "lastChecked": "2024-02-16 14:25:00"
}

MOCK_SUPPORT_RESOURCES = [
    {
        "id": 1,
        "category": "Getting Started",
        "title": "First-Time Telehealth Setup Guide",
        "description": "Complete guide for setting up your device for telehealth visits",
        "type": "guide",
        "estimatedTime": "5 minutes",
        "steps": [
            "Download and install required software",
            "Test your camera and microphone",
            "Check your internet connection",
            "Complete practice session",
            "Review appointment details"
        ],
        "popular": True,
        "lastUpdated": "2024-02-10"
    },
    {
        "id": 2,
        "category": "Troubleshooting",
        "title": "Audio and Video Issues",
        "description": "Solve common audio and video problems during telehealth calls",
        "type": "troubleshooting",
        "estimatedTime": "3 minutes",
        "commonIssues": [
            "No video appearing",
            "Audio not working",
            "Poor video quality",
            "Echo or feedback",
            "Connection dropping"
        ],
        "popular": True,
        "lastUpdated": "2024-02-12"
    },
    {
        "id": 3,
        "category": "Privacy & Security",
        "title": "Telehealth Privacy and Security",
        "description": "Understanding how your privacy is protected during virtual visits",
        "type": "information",
        "estimatedTime": "4 minutes",
        "topics": [
            "HIPAA compliance",
            "End-to-end encryption",
            "Recording policies",
            "Data storage and retention",
            "Patient rights and consent"
        ],
        "popular": False,
        "lastUpdated": "2024-02-08"
    },
    {
        "id": 4,
        "category": "Device Support",
        "title": "Supported Devices and Browsers",
        "description": "Complete list of compatible devices and system requirements",
        "type": "reference",
        "estimatedTime": "2 minutes",
        "devices": [
            "Desktop computers (Windows, Mac, Linux)",
            "Smartphones (iOS, Android)",
            "Tablets (iPad, Android tablets)",
            "Smart TVs with camera (limited support)"
        ],
        "popular": False,
        "lastUpdated": "2024-02-05"
    },
    {
        "id": 5,
        "category": "Best Practices",
        "title": "Tips for a Successful Telehealth Visit",
        "description": "Best practices to ensure a smooth and productive virtual appointment",
        "type": "tips",
        "estimatedTime": "3 minutes",
        "tips": [
            "Choose a quiet, private location",
            "Test technology 15 minutes before appointment",
            "Have good lighting facing you",
            "Prepare questions and documents in advance",
            "Use headphones for better audio quality"
        ],
        "popular": True,
        "lastUpdated": "2024-02-14"
    }
]

@router.get("/appointments/upcoming")
async def get_upcoming_appointments(current_user: User = Depends(get_current_user)):
    """Get upcoming telehealth appointments for the user"""
    try:
        # Filter appointments for the current user (in real implementation)
        appointments = MOCK_UPCOMING_APPOINTMENTS.copy()
        # Sort by scheduled date and time
        appointments.sort(key=lambda x: f"{x['scheduledDate']} {x['scheduledTime']}")
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching upcoming appointments: {str(e)}")

@router.get("/appointments/completed")
async def get_completed_sessions(
    limit: Optional[int] = 10,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get completed telehealth sessions"""
    try:
        sessions = MOCK_COMPLETED_SESSIONS.copy()
        
        # Filter by date range if provided
        if date_from:
            sessions = [s for s in sessions if s["sessionDate"] >= date_from]
        if date_to:
            sessions = [s for s in sessions if s["sessionDate"] <= date_to]
        
        # Sort by session date (newest first)
        sessions.sort(key=lambda x: x["sessionDate"], reverse=True)
        
        # Apply limit
        if limit:
            sessions = sessions[:limit]
        
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching completed sessions: {str(e)}")

@router.get("/appointments/{appointment_id}")
async def get_appointment_details(appointment_id: str, current_user: User = Depends(get_current_user)):
    """Get details for a specific telehealth appointment"""
    try:
        # Search in upcoming appointments
        appointment = next((apt for apt in MOCK_UPCOMING_APPOINTMENTS if apt["appointmentId"] == appointment_id), None)
        
        if not appointment:
            # Search in completed sessions
            appointment = next((sess for sess in MOCK_COMPLETED_SESSIONS if sess["appointmentId"] == appointment_id), None)
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching appointment details: {str(e)}")

@router.post("/appointments/{appointment_id}/join")
async def join_appointment(appointment_id: str, current_user: User = Depends(get_current_user)):
    """Generate join link for telehealth appointment"""
    try:
        appointment = next((apt for apt in MOCK_UPCOMING_APPOINTMENTS if apt["appointmentId"] == appointment_id), None)
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        if not appointment["joinAvailable"]:
            raise HTTPException(status_code=400, detail="Join not available yet")
        
        # In real implementation, this would generate a secure join token
        join_token = f"token_{appointment_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "joinUrl": f"{appointment['meetingUrl']}?token={join_token}",
            "joinToken": join_token,
            "appointmentId": appointment_id,
            "provider": appointment["providerName"],
            "scheduledTime": f"{appointment['scheduledDate']} {appointment['scheduledTime']}",
            "duration": appointment["duration"],
            "type": appointment["type"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error joining appointment: {str(e)}")

@router.get("/system/status")
async def get_system_status(current_user: User = Depends(get_current_user)):
    """Get current telehealth system status"""
    try:
        return MOCK_SYSTEM_STATUS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching system status: {str(e)}")

@router.post("/system/device-check")
async def run_device_check(current_user: User = Depends(get_current_user)):
    """Run device compatibility and performance check"""
    try:
        # In real implementation, this would perform actual device checks
        device_checks = MOCK_DEVICE_CHECKS.copy()
        device_checks["lastChecked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate some variation in results
        import random
        device_checks["connection"]["speed"] = f"{random.uniform(20, 50):.1f} Mbps"
        device_checks["connection"]["latency"] = f"{random.randint(15, 35)}ms"
        
        return {
            "status": "completed",
            "results": device_checks,
            "overall": "excellent" if all(
                check.get("status") == "working" for check in [
                    device_checks["camera"],
                    device_checks["microphone"], 
                    device_checks["speakers"]
                ]
            ) else "issues-detected",
            "recommendations": [
                "Your setup looks great for telehealth appointments",
                "Consider using headphones for better audio quality",
                "Ensure good lighting for video calls"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running device check: {str(e)}")

@router.get("/support/resources")
async def get_support_resources(
    category: Optional[str] = None,
    popular_only: Optional[bool] = False,
    current_user: User = Depends(get_current_user)
):
    """Get telehealth support resources and guides"""
    try:
        resources = MOCK_SUPPORT_RESOURCES.copy()
        
        # Filter by category
        if category and category != "all":
            resources = [r for r in resources if r["category"] == category]
        
        # Filter by popularity
        if popular_only:
            resources = [r for r in resources if r["popular"]]
        
        # Sort by popularity and last updated
        resources.sort(key=lambda x: (x["popular"], x["lastUpdated"]), reverse=True)
        
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching support resources: {str(e)}")

@router.get("/support/resource/{resource_id}")
async def get_support_resource(resource_id: int, current_user: User = Depends(get_current_user)):
    """Get detailed support resource content"""
    try:
        resource = next((r for r in MOCK_SUPPORT_RESOURCES if r["id"] == resource_id), None)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Support resource not found")
        
        return resource
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching support resource: {str(e)}")

@router.post("/support/contact")
async def contact_support(
    issue_type: str,
    description: str,
    priority: str = "medium",
    current_user: User = Depends(get_current_user)
):
    """Submit a support request"""
    try:
        # In real implementation, this would create a support ticket
        ticket_id = f"TH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "ticketId": ticket_id,
            "status": "submitted",
            "issueType": issue_type,
            "priority": priority,
            "estimatedResponse": "15 minutes" if priority == "urgent" else "2 hours",
            "message": "Support request submitted successfully. You will be contacted shortly."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting support request: {str(e)}")

@router.post("/appointments/{appointment_id}/tech-check")
async def complete_tech_check(appointment_id: str, current_user: User = Depends(get_current_user)):
    """Mark technology check as completed for an appointment"""
    try:
        appointment = next((apt for apt in MOCK_UPCOMING_APPOINTMENTS if apt["appointmentId"] == appointment_id), None)
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # In real implementation, this would update the database
        appointment["techCheckPassed"] = True
        
        return {
            "appointmentId": appointment_id,
            "techCheckPassed": True,
            "message": "Technology check completed successfully",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing tech check: {str(e)}")

@router.get("/summary")
async def get_telehealth_summary(current_user: User = Depends(get_current_user)):
    """Get telehealth dashboard summary"""
    try:
        upcoming_count = len(MOCK_UPCOMING_APPOINTMENTS)
        completed_count = len(MOCK_COMPLETED_SESSIONS)
        ready_appointments = len([apt for apt in MOCK_UPCOMING_APPOINTMENTS if apt["techCheckPassed"] and apt["preVisitCompleted"]])
        
        return {
            "upcomingAppointments": upcoming_count,
            "completedSessions": completed_count,
            "readyAppointments": ready_appointments,
            "systemStatus": MOCK_SYSTEM_STATUS["serverStatus"],
            "connectionQuality": MOCK_DEVICE_CHECKS["connection"]["status"],
            "nextAppointment": MOCK_UPCOMING_APPOINTMENTS[0] if MOCK_UPCOMING_APPOINTMENTS else None,
            "averageSatisfaction": sum(s["patientSatisfaction"] for s in MOCK_COMPLETED_SESSIONS) / len(MOCK_COMPLETED_SESSIONS) if MOCK_COMPLETED_SESSIONS else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching telehealth summary: {str(e)}")