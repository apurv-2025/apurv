# =============================================================================
# FILE: backend/app/main.py
# =============================================================================
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import asyncio
import logging

from .database.connection import get_db, engine
from .database import models
from .schemas import claims as claim_schemas
from .services.edi_parser import EDIParser
from .services.claim_processor import ClaimProcessor
from .api.routes import claims, payers, reports, agent
from .agent.manager import get_agent_manager
from .config import settings, agent_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EDI Claims Processing API with AI Agent", 
    version="3.0.0",
    description="Enhanced healthcare claims processing system with intelligent AI agent capabilities and comprehensive dental claims support"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(claims.router, prefix="/api/claims", tags=["claims"])
app.include_router(payers.router, prefix="/api/payers", tags=["payers"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])

@app.get("/")
async def root():
    return {
        "message": "EDI Claims Processing API with AI Agent",
        "version": "3.0.0",
        "features": [
            "EDI X12 transaction processing (837P, 837D, 837I)",
            "AI-powered claim analysis and validation",
            "Natural language chat interface",
            "Automated validation and insights",
            "Financial reporting and metrics",
            "Dental claims specialization",
            "835 remittance processing",
            "Enhanced claim submission workflow"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "agent": "available" if get_agent_manager().agent else "initializing",
        "version": "3.0.0"
    }

@app.on_event("startup")
async def initialize_agent():
    """Initialize the agent on application startup"""
    try:
        logger.info("Initializing AI agent...")
        agent_manager = get_agent_manager()
        await agent_manager.initialize()
        logger.info("AI agent initialized successfully")
        
    except Exception as e:
        logger.error(f"Warning: Could not initialize agent: {e}")
        logger.info("Application will continue without agent functionality")

@app.on_event("shutdown")
async def cleanup():
    """Cleanup on application shutdown"""
    try:
        agent_manager = get_agent_manager()
        agent_manager.cleanup_old_tasks(max_age_hours=1)  # Clean up recent tasks
        logger.info("Application cleanup completed")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
