# =============================================================================
# FILE: api/enhanced_fastapi_app.py
# =============================================================================
"""
Enhanced Claims Anomaly Detection FastAPI with Claims Service Integration

This module provides enhanced API endpoints that combine ClaimsAnomaly's ML
anomaly detection capabilities with the foundational Claims service's
FHIR-based CRUD operations.
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.enhanced_inference import EnhancedClaimsInferenceEngine

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
    fhir_claim_id: Optional[str] = None
    integration_status: Optional[str] = None
    stored_in_fhir: Optional[bool] = None

class BatchRequest(BaseModel):
    claims: List[ClaimData] = Field(..., max_items=1000, description="List of claims to score")
    use_fhir: bool = Field(True, description="Store claims in FHIR service")

class BatchResponse(BaseModel):
    results: List[ClaimScore]
    count: int
    timestamp: str
    integration_status: Optional[str] = None
    stored_in_fhir: Optional[bool] = None
    successfully_stored: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model_loaded: bool
    integration_status: Optional[str] = None

class ModelInfoResponse(BaseModel):
    is_trained: bool
    feature_columns: Optional[List[str]]
    model_type: str
    last_updated: str
    integration_enabled: bool
    claims_service_url: str
    enhanced_features: List[str]

class IntegrationHealthResponse(BaseModel):
    health_status: Dict[str, Any]
    integration: str

# Create FastAPI app
app = FastAPI(
    title="Enhanced Claims Anomaly Detection API",
    description="REST API for detecting anomalous health insurance claims using ML with FHIR integration",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global variables for configuration
CLAIMS_SERVICE_URL = os.getenv('CLAIMS_SERVICE_URL', 'http://localhost:8001')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global enhanced inference engine
enhanced_inference_engine: Optional[EnhancedClaimsInferenceEngine] = None

def load_model():
    """Load the trained model and initialize enhanced inference engine"""
    global enhanced_inference_engine
    try:
        model_path = "models/claims_anomaly_model.pkl"
        if os.path.exists(model_path):
            enhanced_inference_engine = EnhancedClaimsInferenceEngine(model_path, CLAIMS_SERVICE_URL)
            logger.info(f"Enhanced inference engine initialized with model from {model_path} and Claims Service URL: {CLAIMS_SERVICE_URL}")
            return True
        else:
            logger.error(f"Model file not found: {model_path}")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("Starting Enhanced Claims Anomaly Detection API...")
    if not load_model():
        logger.error("Failed to load model. API will not function properly.")

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check the health of the API and ML model"""
    try:
        if enhanced_inference_engine:
            health_status = await enhanced_inference_engine.health_check()
            return HealthResponse(
                status="healthy" if health_status['overall_status'] == 'healthy' else 'degraded',
                timestamp=datetime.utcnow().isoformat(),
                model_loaded=enhanced_inference_engine.inference_engine.is_model_loaded(),
                integration_status=health_status['overall_status']
            )
        else:
            return HealthResponse(
                status="unhealthy",
                timestamp=datetime.utcnow().isoformat(),
                model_loaded=False,
                integration_status="error"
            )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            timestamp=datetime.utcnow().isoformat(),
            model_loaded=False,
            integration_status="error"
        )

@app.post("/api/v1/score", response_model=ClaimScore, tags=["Scoring"])
async def score_single_claim(
    claim: ClaimData,
    use_fhir: bool = Query(True, description="Store claim in FHIR service")
):
    """Score a single claim for anomaly detection with FHIR integration"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        # Convert Pydantic model to dict
        claim_dict = claim.dict()
        
        # Score claim with integration
        result = await enhanced_inference_engine.score_single_claim(claim_dict, use_fhir)
        
        return ClaimScore(
            claim_id=result['claim_id'],
            risk_score=result['risk_score'],
            classification=result['classification'],
            top_drivers=result['top_drivers'],
            timestamp=result['timestamp'],
            fhir_claim_id=result.get('fhir_claim_id'),
            integration_status=result.get('integration_status'),
            stored_in_fhir=result.get('stored_in_fhir')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scoring single claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/score/batch", response_model=BatchResponse, tags=["Scoring"])
async def score_batch_claims(batch_request: BatchRequest):
    """Score a batch of claims for anomaly detection with FHIR integration"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        # Convert Pydantic models to dicts
        claims_list = [claim.dict() for claim in batch_request.claims]
        
        # Score batch with integration
        result = await enhanced_inference_engine.score_batch_claims(claims_list, batch_request.use_fhir)
        
        return BatchResponse(
            results=result['results'],
            count=result['count'],
            timestamp=result['timestamp'],
            integration_status=result.get('integration_status'),
            stored_in_fhir=result.get('stored_in_fhir'),
            successfully_stored=result.get('successfully_stored')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scoring batch claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def get_model_info():
    """Get information about the loaded ML model and integration"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        model_info = enhanced_inference_engine.get_model_info()
        
        return ModelInfoResponse(
            is_trained=model_info.get('is_trained', False),
            feature_columns=model_info.get('feature_columns'),
            model_type=model_info.get('model_type', 'Unknown'),
            last_updated=model_info.get('last_updated', datetime.utcnow().isoformat()),
            integration_enabled=model_info.get('integration_enabled', True),
            claims_service_url=model_info.get('claims_service_url', 'http://localhost:8001'),
            enhanced_features=model_info.get('enhanced_features', [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/claims/from-service", response_model=Dict[str, Any], tags=["Claims"])
async def get_claims_from_service(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of claims to retrieve"),
    use_fhir: bool = Query(True, description="Get claims from FHIR service")
):
    """Get claims from Claims service for scoring"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        claims_data = await enhanced_inference_engine.get_claims_for_scoring(limit, use_fhir)
        
        return {
            "claims": claims_data['claims'],
            "total": claims_data['total'],
            "source": claims_data['source'],
            "error": claims_data.get('error')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting claims from service: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/score/from-service", response_model=Dict[str, Any], tags=["Scoring"])
async def score_claims_from_service(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of claims to retrieve and score"),
    use_fhir: bool = Query(True, description="Get claims from FHIR service")
):
    """Get claims from Claims service and score them for anomalies"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        result = await enhanced_inference_engine.score_claims_from_service(limit, use_fhir)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scoring claims from service: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stats/anomaly", response_model=Dict[str, Any], tags=["Statistics"])
async def get_anomaly_statistics(
    use_fhir: bool = Query(True, description="Include FHIR statistics")
):
    """Get anomaly detection statistics from both local and FHIR sources"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        stats = await enhanced_inference_engine.get_anomaly_statistics(use_fhir)
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting anomaly statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health/integration", response_model=IntegrationHealthResponse, tags=["Health"])
async def health_check_integration():
    """Check health of both local ML system and Claims service integration"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        health_status = await enhanced_inference_engine.health_check()
        
        return IntegrationHealthResponse(
            health_status=health_status,
            integration="enhanced_claims_anomaly"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking integration health: {e}")
        return IntegrationHealthResponse(
            health_status={
                'local': {'status': 'error', 'error': str(e)},
                'fhir': {'status': 'unknown'},
                'overall_status': 'error'
            },
            integration="enhanced_claims_anomaly"
        )

@app.post("/api/v1/validate/claim", response_model=Dict[str, Any], tags=["Validation"])
async def validate_claim_data(claim: ClaimData):
    """Validate claim data for both ML scoring and FHIR storage"""
    try:
        if not enhanced_inference_engine:
            raise HTTPException(status_code=503, detail="ML model not loaded")
        
        claim_dict = claim.dict()
        validation_result = await enhanced_inference_engine.validate_claim_data(claim_dict)
        
        return validation_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating claim data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/example", tags=["Examples"])
async def get_example_claim():
    """Get an example claim for testing"""
    example_claim = {
        "claim_id": "EXAMPLE-001",
        "submission_date": "2024-01-15",
        "provider_id": "PROVIDER-123",
        "provider_specialty": "Cardiology",
        "patient_age": 45,
        "patient_gender": "M",
        "cpt_code": "99213",
        "icd_code": "I10",
        "units_of_service": 1,
        "billed_amount": 150.00,
        "paid_amount": 120.00,
        "place_of_service": "11",
        "prior_authorization": "N",
        "modifier": "",
        "is_anomaly": 0
    }
    
    return {
        "example_claim": example_claim,
        "description": "Example claim data for testing anomaly detection",
        "note": "This is sample data for demonstration purposes"
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Enhanced Claims Anomaly Detection API with FHIR Integration",
        "version": "2.0.0",
        "features": [
            "ML-powered anomaly detection",
            "FHIR Claims service integration",
            "Real-time scoring",
            "Batch processing",
            "Health monitoring",
            "Data validation",
            "Statistics and analytics"
        ],
        "endpoints": {
            "health": "/health",
            "integration_health": "/api/v1/health/integration",
            "single_scoring": "/api/v1/score",
            "batch_scoring": "/api/v1/score/batch",
            "service_scoring": "/api/v1/score/from-service",
            "model_info": "/api/v1/model/info",
            "statistics": "/api/v1/stats/anomaly",
            "validation": "/api/v1/validate/claim",
            "example": "/api/v1/example"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True) 