#!/usr/bin/env python3
"""
Claims Anomaly Detection FastAPI

This module provides a FastAPI for the claims anomaly detection system.
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.inference import ClaimsInferenceEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class ClaimData(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier")
    submission_date: str = Field(..., description="Claim submission date (YYYY-MM-DD)")
    provider_id: str = Field(..., description="Provider identifier")
    provider_specialty: str = Field(..., description="Provider specialty")
    patient_age: int = Field(..., ge=0, le=120, description="Patient age")
    patient_gender: str = Field(..., pattern="^[MF]$", description="Patient gender (M/F)")
    cpt_code: str = Field(..., description="CPT procedure code")
    icd_code: str = Field(..., description="ICD diagnosis code")
    units_of_service: int = Field(..., ge=1, description="Units of service")
    billed_amount: float = Field(..., gt=0, description="Billed amount")
    paid_amount: float = Field(..., ge=0, description="Paid amount")
    place_of_service: str = Field(..., description="Place of service code")
    prior_authorization: str = Field(..., pattern="^[YN]$", description="Prior authorization (Y/N)")
    modifier: Optional[str] = Field("", description="Procedure modifier")
    is_anomaly: Optional[int] = Field(0, ge=0, le=1, description="Anomaly flag (0/1)")

class ClaimScore(BaseModel):
    claim_id: str
    risk_score: float
    classification: str
    top_drivers: List[str]
    timestamp: str

class BatchRequest(BaseModel):
    claims: List[ClaimData] = Field(..., max_items=1000, description="List of claims to score")

class BatchResponse(BaseModel):
    results: List[ClaimScore]
    count: int
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model_loaded: bool

class ModelInfoResponse(BaseModel):
    is_trained: bool
    feature_columns: Optional[List[str]]
    model_type: str
    last_updated: str

# Create FastAPI app
app = FastAPI(
    title="Claims Anomaly Detection API",
    description="REST API for detecting anomalous health insurance claims using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global inference engine
inference_engine: Optional[ClaimsInferenceEngine] = None

def load_model():
    """Load the trained model"""
    global inference_engine
    try:
        model_path = "models/claims_anomaly_model.pkl"
        if os.path.exists(model_path):
            inference_engine = ClaimsInferenceEngine(model_path)
            logger.info(f"Model loaded from {model_path}")
            return True
        else:
            logger.error(f"Model file not found: {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    if not load_model():
        logger.error("Failed to load model during startup")
        raise RuntimeError("Model loading failed")

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=inference_engine is not None and inference_engine.model.is_trained
    )

@app.post("/api/v1/score", response_model=ClaimScore, tags=["Scoring"])
async def score_single_claim(claim: ClaimData):
    """Score a single claim"""
    try:
        if inference_engine is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Convert Pydantic model to dict
        claim_dict = claim.dict()
        
        # Score the claim
        result = inference_engine.score_single_claim(claim_dict)
        
        return ClaimScore(
            claim_id=result['claim_id'],
            risk_score=result['risk_score'],
            classification=result['classification'],
            top_drivers=result['top_drivers'],
            timestamp=result['timestamp']
        )
        
    except Exception as e:
        logger.error(f"Error scoring claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/score/batch", response_model=BatchResponse, tags=["Scoring"])
async def score_batch_claims(batch_request: BatchRequest):
    """Score multiple claims"""
    try:
        if inference_engine is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Convert Pydantic models to list of dicts
        claims_list = [claim.dict() for claim in batch_request.claims]
        
        # Score the claims
        import pandas as pd
        claims_df = pd.DataFrame(claims_list)
        results = inference_engine.score_claims_batch(claims_df)
        
        # Convert to response format
        results_list = []
        for _, row in results.iterrows():
            results_list.append(ClaimScore(
                claim_id=row['claim_id'],
                risk_score=row['risk_score'],
                classification=row['classification'],
                top_drivers=row['top_drivers'],
                timestamp=row['timestamp']
            ))
        
        return BatchResponse(
            results=results_list,
            count=len(results_list),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error scoring batch claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def get_model_info():
    """Get model information"""
    try:
        if inference_engine is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        info = inference_engine.get_model_info()
        return ModelInfoResponse(
            is_trained=info['is_trained'],
            feature_columns=info['feature_columns'],
            model_type=info['model_type'],
            last_updated=info['last_updated']
        )
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/example", tags=["Examples"])
async def get_example_claim():
    """Get an example claim structure"""
    example_claim = {
        'claim_id': 'CLM_EXAMPLE_001',
        'submission_date': '2025-08-01',
        'provider_id': 'PROV_00001',
        'provider_specialty': 'Internal Medicine',
        'patient_age': 45,
        'patient_gender': 'M',
        'cpt_code': '99214',
        'icd_code': 'I10',
        'units_of_service': 1,
        'billed_amount': 200.0,
        'paid_amount': 180.0,
        'place_of_service': '11',
        'prior_authorization': 'N',
        'modifier': '',
        'is_anomaly': 0
    }
    
    return {
        'example_claim': example_claim,
        'description': 'This is an example of the required claim structure for scoring'
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Claims Anomaly Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 