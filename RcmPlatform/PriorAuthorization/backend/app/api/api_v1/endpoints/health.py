 File: app/api/api_v1/endpoints/health.py - Health Check Endpoint
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check(*, db: Session = Depends(get_db)):
    """Health check endpoint for EDI 278/275 system."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        database_status = "healthy"
    except Exception:
        database_status = "unhealthy"
    
    return {
        "status": "healthy" if database_status == "healthy" else "degraded",
        "service": "edi-278-275-prior-authorization-system",
        "version": settings.VERSION,
        "database_status": database_status,
        "supported_transactions": ["278", "275"],
        "timestamp": datetime.utcnow()
    }
