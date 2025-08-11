# File: app/api/api_v1/api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import prior_authorization, patient, codes, agent

api_router = APIRouter()

api_router.include_router(prior_authorization.router, prefix="/prior-auth", tags=["prior-authorization"])
api_router.include_router(patient.router, prefix="/patients", tags=["patients"])
api_router.include_router(codes.router, prefix="/codes", tags=["codes"])
api_router.include_router(agent.router, prefix="/agent", tags=["ai-assistant"])
