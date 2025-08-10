# File: app/api/api.py
from fastapi import APIRouter
from app.api.endpoints import patient, prior_authorization, codes

api_router = APIRouter()

api_router.include_router(
    patient.router, 
    prefix="/patients", 
    tags=["patients"]
)

api_router.include_router(
    prior_authorization.router, 
    prefix="/prior-auth", 
    tags=["prior-authorization"]
)

api_router.include_router(
    codes.router, 
    prefix="/codes", 
    tags=["codes"]
)
