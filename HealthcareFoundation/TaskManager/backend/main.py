from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import asyncio
import logging

from app.core.config import settings
from app.core.database import engine, get_db
from app.models import models
from app.api.v1.api import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.websockets.connection_manager import ConnectionManager
from app.websockets.notifications import NotificationManager
from app.background.tasks import cleanup_old_files, generate_reports, send_due_date_reminders

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global managers
connection_manager = ConnectionManager()
notification_manager = NotificationManager(connection_manager)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Task Management System API...")
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Start background tasks
    if settings.ENVIRONMENT == "production":
        asyncio.create_task(background_task_scheduler())
    
    logger.info("Startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Task Management System API...")


async def background_task_scheduler():
    """Schedule background tasks"""
    while True:
        try:
            # Run daily at 2 AM
            await asyncio.sleep(3600)  # Check every hour
            
            from datetime import datetime
            now = datetime.now()
            
            # Daily tasks at 2 AM
            if now.hour == 2 and now.minute < 5:
                logger.info("Running daily background tasks...")
                
                # Clean up old files
                await cleanup_old_files(days_old=30)
                
                # Generate reports
                await generate_reports()
                
                # Send due date reminders
                await send_due_date_reminders()
                
                logger.info("Daily background tasks completed")
                
                # Sleep for 1 hour to avoid running multiple times
                await asyncio.sleep(3600)
                
        except Exception as e:
            logger.error(f"Background task error: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes before retrying


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Task Management System API with FastAPI",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, calls=100, period=60)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Create uploads directory
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_FOLDER), name="uploads")

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# WebSocket routes
from app.api.v1.endpoints.websockets import router as websocket_router
app.include_router(websocket_router, prefix="/ws", tags=["websockets"])

# Auth routes
from app.api.v1.endpoints.auth import router as auth_router
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])


@app.get("/")
def read_root():
    return {
        "message": "Task Management System API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.post("/notify/{user_id}")
async def send_notification(
    user_id: int,
    message: str,
    notification_type: str = "info",
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Send notification to specific user via WebSocket"""
    await notification_manager.send_task_notification(
        user_id=user_id,
        event_type="manual_notification",
        task_data={"message": message, "type": notification_type}
    )
    return {"message": "Notification sent"}


@app.post("/broadcast")
async def broadcast_message(
    message: str,
    notification_type: str = "info"
):
    """Broadcast message to all connected users"""
    await notification_manager.send_system_notification(
        message=message,
        notification_type=notification_type
    )
    return {"message": "Broadcast sent"}


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False,
        log_level="info"
    )

