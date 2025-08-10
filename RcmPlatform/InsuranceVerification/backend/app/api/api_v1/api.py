# File: app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.api_v1.endpoints import upload, eligibility, health

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(eligibility.router, prefix="/eligibility", tags=["eligibility"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
