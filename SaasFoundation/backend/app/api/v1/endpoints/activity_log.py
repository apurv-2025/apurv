"""
Activity Log API endpoints for SaaSFoundation
Provides access to logged activities from the ActivityLog service
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.activity_log import activity_logger
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/activities", response_model=List[Dict[str, Any]])
async def get_activity_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    event_category: Optional[str] = Query(None, description="Filter by event category"),
    date_range: str = Query("all", description="Date range filter"),
    search: Optional[str] = Query(None, description="Search in event descriptions"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get activity events for the current user"""
    try:
        user_id = current_user.get("id", "anonymous")
        
        events = await activity_logger.get_activity_events(
            user_id=user_id,
            event_type=event_type,
            date_range=date_range,
            search=search,
            skip=skip,
            limit=limit
        )
        
        if events is None:
            raise HTTPException(status_code=503, detail="ActivityLog service unavailable")
        
        return events
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activity events: {str(e)}")

@router.get("/activities/summary", response_model=Dict[str, Any])
async def get_activity_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get activity summary for the current user"""
    try:
        user_id = current_user.get("id", "anonymous")
        
        # Get recent activities
        recent_events = await activity_logger.get_activity_events(
            user_id=user_id,
            limit=50
        )
        
        if recent_events is None:
            raise HTTPException(status_code=503, detail="ActivityLog service unavailable")
        
        # Calculate summary statistics
        total_events = len(recent_events)
        event_types = {}
        event_categories = {}
        
        for event in recent_events:
            event_type = event.get("eventType", "unknown")
            event_category = event.get("event", "unknown")
            
            event_types[event_type] = event_types.get(event_type, 0) + 1
            event_categories[event_category] = event_categories.get(event_category, 0) + 1
        
        # Get most recent activity
        latest_activity = recent_events[0] if recent_events else None
        
        summary = {
            "total_events": total_events,
            "event_types": event_types,
            "event_categories": event_categories,
            "latest_activity": latest_activity,
            "user_id": user_id
        }
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activity summary: {str(e)}")

@router.get("/activities/health", response_model=Dict[str, Any])
async def check_activity_log_health():
    """Check ActivityLog service health"""
    try:
        is_healthy = await activity_logger.health_check()
        
        return {
            "service": "ActivityLog",
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "endpoint": activity_logger.activity_log_url
        }
        
    except Exception as e:
        return {
            "service": "ActivityLog",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "endpoint": activity_logger.activity_log_url
        }

@router.post("/activities/log", response_model=Dict[str, Any])
async def log_custom_activity(
    event_type: str,
    event_category: str,
    event_description: str,
    event_metadata: Optional[Dict[str, Any]] = None,
    request: Request = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Log a custom activity event"""
    try:
        user_id = current_user.get("id", "anonymous")
        
        result = await activity_logger.log_activity(
            event_type=event_type,
            event_category=event_category,
            event_description=event_description,
            user_id=user_id,
            request=request,
            event_metadata=event_metadata
        )
        
        if result is None:
            raise HTTPException(status_code=503, detail="Failed to log activity")
        
        return {
            "message": "Activity logged successfully",
            "event_id": result.get("id"),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log activity: {str(e)}")

@router.get("/activities/export", response_model=Dict[str, Any])
async def export_activity_events(
    format: str = Query("json", description="Export format (json, csv)"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    date_range: str = Query("all", description="Date range filter"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Export activity events"""
    try:
        user_id = current_user.get("id", "anonymous")
        
        events = await activity_logger.get_activity_events(
            user_id=user_id,
            event_type=event_type,
            date_range=date_range,
            limit=1000  # Export more records
        )
        
        if events is None:
            raise HTTPException(status_code=503, detail="ActivityLog service unavailable")
        
        if format.lower() == "csv":
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            if events:
                writer.writerow(events[0].keys())
            
            # Write data
            for event in events:
                writer.writerow(event.values())
            
            csv_content = output.getvalue()
            output.close()
            
            return {
                "format": "csv",
                "content": csv_content,
                "record_count": len(events),
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Return JSON format
            return {
                "format": "json",
                "events": events,
                "record_count": len(events),
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export activity events: {str(e)}")

@router.get("/activities/stats", response_model=Dict[str, Any])
async def get_activity_statistics(
    period: str = Query("7d", description="Statistics period (1d, 7d, 30d, 90d)"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get activity statistics"""
    try:
        user_id = current_user.get("id", "anonymous")
        
        # Get activities for the period
        events = await activity_logger.get_activity_events(
            user_id=user_id,
            date_range=period,
            limit=1000
        )
        
        if events is None:
            raise HTTPException(status_code=503, detail="ActivityLog service unavailable")
        
        # Calculate statistics
        total_events = len(events)
        event_types = {}
        event_categories = {}
        daily_activity = {}
        
        for event in events:
            event_type = event.get("eventType", "unknown")
            event_category = event.get("event", "unknown")
            event_date = event.get("date", "unknown")
            
            event_types[event_type] = event_types.get(event_type, 0) + 1
            event_categories[event_category] = event_categories.get(event_category, 0) + 1
            daily_activity[event_date] = daily_activity.get(event_date, 0) + 1
        
        # Calculate averages
        avg_daily_events = total_events / max(len(daily_activity), 1)
        
        stats = {
            "period": period,
            "total_events": total_events,
            "avg_daily_events": round(avg_daily_events, 2),
            "unique_days": len(daily_activity),
            "event_types": event_types,
            "event_categories": event_categories,
            "daily_activity": daily_activity,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve activity statistics: {str(e)}") 