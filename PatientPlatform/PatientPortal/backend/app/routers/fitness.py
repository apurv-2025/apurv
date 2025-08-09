from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from ..database import get_db
from ..dependencies import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/fitness", tags=["fitness"])

@router.get("/data")
def get_fitness_data(
    period: str = "week",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get fitness data for the specified period"""
    try:
        # Mock data for now - in production, this would pull from connected devices
        mock_data = {
            "summary": {
                "steps": 8425,
                "calories": 342,
                "activeMinutes": 45,
                "heartRate": 72,
                "distance": 5.2
            },
            "devices": [
                {
                    "id": 1,
                    "name": "Apple Watch Series 8",
                    "type": "watch",
                    "status": "connected",
                    "lastSync": "2 minutes ago",
                    "iconType": "watch"
                },
                {
                    "id": 2,
                    "name": "iPhone Health App",
                    "type": "phone",
                    "status": "connected",
                    "lastSync": "5 minutes ago",
                    "iconType": "phone"
                },
                {
                    "id": 3,
                    "name": "Fitbit Charge 5",
                    "type": "tracker",
                    "status": "disconnected",
                    "lastSync": "2 hours ago",
                    "iconType": "activity"
                }
            ],
            "goals": [
                {"title": "Daily Steps", "current": 8425, "target": 10000, "unit": "steps"},
                {"title": "Active Minutes", "current": 45, "target": 60, "unit": "min"},
                {"title": "Calories Burned", "current": 342, "target": 500, "unit": "cal"}
            ],
            "weeklyTrend": [
                {"day": "Mon", "steps": 7200, "calories": 280},
                {"day": "Tue", "steps": 9100, "calories": 365},
                {"day": "Wed", "steps": 8800, "calories": 340},
                {"day": "Thu", "steps": 7600, "calories": 295},
                {"day": "Fri", "steps": 10200, "calories": 425},
                {"day": "Sat", "steps": 6800, "calories": 310},
                {"day": "Sun", "steps": 8425, "calories": 342}
            ]
        }
        
        return mock_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fitness data"
        )

@router.get("/devices")
def get_fitness_devices(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of connected fitness devices"""
    try:
        # Mock device data
        devices = [
            {
                "id": 1,
                "name": "Apple Watch Series 8",
                "type": "watch",
                "brand": "Apple",
                "status": "connected",
                "lastSync": datetime.now() - timedelta(minutes=2),
                "batteryLevel": 85,
                "syncFrequency": "real-time"
            },
            {
                "id": 2,
                "name": "iPhone Health App",
                "type": "phone",
                "brand": "Apple",
                "status": "connected",
                "lastSync": datetime.now() - timedelta(minutes=5),
                "batteryLevel": 92,
                "syncFrequency": "hourly"
            }
        ]
        
        return {"devices": devices, "total": len(devices)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fitness devices"
        )

@router.post("/devices/{device_id}/sync")
def sync_fitness_device(
    device_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually sync a fitness device"""
    try:
        # In production, this would trigger actual device sync
        return {
            "message": f"Device {device_id} sync initiated",
            "syncStatus": "in_progress",
            "estimatedCompletion": datetime.now() + timedelta(minutes=2)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync fitness device"
        )

@router.put("/goals")
def update_fitness_goals(
    goals: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's fitness goals"""
    try:
        # In production, this would save to database
        return {
            "message": "Fitness goals updated successfully",
            "goals": goals,
            "updatedAt": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update fitness goals"
        )

@router.get("/health")
def fitness_health_check():
    """Health check for fitness integration"""
    return {
        "status": "healthy",
        "integrations": {
            "apple_health": True,
            "fitbit": True,
            "google_fit": False
        },
        "last_sync": datetime.now(),
        "active_users": 1250
    }