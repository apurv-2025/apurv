# app/api/v1/api.py (Updated to include new endpoints)
from fastapi import APIRouter
from app.api.v1.endpoints import tasks, clients, attachments, auth, websockets

api_router = APIRouter()

# Include all routers
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Add monitoring endpoint
@api_router.get("/status")
def api_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/tasks",
            "clients": "/clients",
            "attachments": "/attachments",
            "auth": "/auth",
            "websockets": "/ws"
        }
    }

