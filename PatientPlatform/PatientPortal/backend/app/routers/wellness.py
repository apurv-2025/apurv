from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from ..database import get_db
from ..dependencies import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/wellness", tags=["wellness"])

@router.get("/data")
def get_wellness_data(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive wellness data"""
    try:
        # Mock data for wellness metrics
        mock_data = {
            "mentalHealth": {
                "moodScore": 7.5,
                "stressLevel": 3,
                "meditationMinutes": 15,
                "sleepQuality": 8.2
            },
            "physicalWellness": {
                "hydrationLevel": 85,
                "nutritionScore": 7.8,
                "recoveryScore": 8.5,
                "energyLevel": 8
            },
            "habits": [
                {
                    "id": 1,
                    "name": "Morning Meditation",
                    "streak": 12,
                    "target": 365,
                    "category": "mental_health",
                    "frequency": "daily",
                    "iconType": "brain",
                    "color": "purple"
                },
                {
                    "id": 2,
                    "name": "Hydration Goal",
                    "streak": 5,
                    "target": 30,
                    "category": "physical",
                    "frequency": "daily",
                    "iconType": "droplets",
                    "color": "blue"
                },
                {
                    "id": 3,
                    "name": "Sleep Schedule",
                    "streak": 8,
                    "target": 30,
                    "category": "physical",
                    "frequency": "daily",
                    "iconType": "moon",
                    "color": "indigo"
                }
            ],
            "apps": [
                {
                    "id": 1,
                    "name": "Headspace",
                    "type": "Meditation",
                    "status": "connected",
                    "sessions": 45,
                    "lastSync": datetime.now() - timedelta(hours=1),
                    "iconType": "brain"
                },
                {
                    "id": 2,
                    "name": "MyFitnessPal",
                    "type": "Nutrition",
                    "status": "connected",
                    "entries": 28,
                    "lastSync": datetime.now() - timedelta(minutes=30),
                    "iconType": "leaf"
                }
            ],
            "weeklyProgress": [
                {"day": "Mon", "mood": 7, "stress": 4, "energy": 8},
                {"day": "Tue", "mood": 8, "stress": 3, "energy": 9},
                {"day": "Wed", "mood": 6, "stress": 5, "energy": 7},
                {"day": "Thu", "mood": 7, "stress": 3, "energy": 8},
                {"day": "Fri", "mood": 9, "stress": 2, "energy": 9},
                {"day": "Sat", "mood": 8, "stress": 2, "energy": 8},
                {"day": "Sun", "mood": 7, "stress": 3, "energy": 8}
            ]
        }
        
        return mock_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wellness data"
        )

@router.get("/habits")
def get_habits(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wellness habits"""
    try:
        # Mock habits data
        habits = [
            {
                "id": 1,
                "name": "Morning Meditation",
                "description": "10 minutes of mindfulness meditation",
                "category": "mental_health",
                "streak": 12,
                "longestStreak": 25,
                "target": 365,
                "frequency": "daily",
                "reminderTime": "07:00",
                "isActive": True
            },
            {
                "id": 2,
                "name": "Hydration Goal",
                "description": "Drink 8 glasses of water daily",
                "category": "physical",
                "streak": 5,
                "longestStreak": 15,
                "target": 30,
                "frequency": "daily",
                "reminderTime": "09:00",
                "isActive": True
            }
        ]
        
        return {"habits": habits, "total": len(habits)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve habits"
        )

@router.put("/habits/{habit_id}")
def update_habit(
    habit_id: int,
    data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a wellness habit"""
    try:
        # In production, this would update the database
        return {
            "message": f"Habit {habit_id} updated successfully",
            "habitId": habit_id,
            "updatedFields": list(data.keys()),
            "updatedAt": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update habit"
        )

@router.get("/apps")
def get_connected_apps(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get connected wellness apps"""
    try:
        apps = [
            {
                "id": 1,
                "name": "Headspace",
                "type": "Meditation",
                "category": "mental_health",
                "status": "connected",
                "apiVersion": "2.1",
                "permissions": ["read_sessions", "read_progress"],
                "lastSync": datetime.now() - timedelta(hours=1),
                "dataTypes": ["meditation_sessions", "mood_tracking"]
            },
            {
                "id": 2,
                "name": "MyFitnessPal",
                "type": "Nutrition",
                "category": "physical",
                "status": "connected",
                "apiVersion": "1.5",
                "permissions": ["read_nutrition", "read_weight"],
                "lastSync": datetime.now() - timedelta(minutes=30),
                "dataTypes": ["nutrition_intake", "calorie_tracking"]
            },
            {
                "id": 3,
                "name": "Sleep Cycle",
                "type": "Sleep",
                "category": "physical",
                "status": "disconnected",
                "apiVersion": "3.0",
                "permissions": [],
                "lastSync": None,
                "dataTypes": ["sleep_patterns", "sleep_quality"]
            }
        ]
        
        return {"apps": apps, "total": len(apps)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve connected apps"
        )

@router.post("/apps/connect")
def connect_wellness_app(
    app_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect a new wellness app"""
    try:
        # In production, this would handle OAuth flow and store credentials
        return {
            "message": f"Successfully connected to {app_data.get('name', 'app')}",
            "appId": app_data.get("id"),
            "status": "connected",
            "connectedAt": datetime.now(),
            "permissions": app_data.get("permissions", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect wellness app"
        )

@router.post("/mood/log")
def log_mood(
    mood_data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log daily mood and wellness metrics"""
    try:
        # In production, this would save to database
        return {
            "message": "Mood logged successfully",
            "timestamp": datetime.now(),
            "moodScore": mood_data.get("mood"),
            "notes": mood_data.get("notes", ""),
            "stressLevel": mood_data.get("stress"),
            "energyLevel": mood_data.get("energy")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log mood data"
        )

@router.get("/health")
def wellness_health_check():
    """Health check for wellness integration"""
    return {
        "status": "healthy",
        "integrations": {
            "headspace": True,
            "myfitnesspal": True,
            "sleep_cycle": False,
            "calm": True
        },
        "last_sync": datetime.now(),
        "active_users": 875,
        "total_sessions": 12450
    }