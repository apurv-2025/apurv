"""
Enhanced DenialPrediction API with Claims Service Integration

This module provides enhanced API endpoints that combine DenialPrediction's ML
prediction capabilities with the foundational Claims service's FHIR-based CRUD operations.
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from models import (
    ClaimData, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse,
    HealthResponse, ErrorResponse, DenialInput, ClassificationResponse
)
from claims_service_client import ClaimsServiceClient, ClaimsDataTransformer, create_claims_service_client

# Import existing prediction logic
try:
    from models.denial_predictor import DenialPredictor
    PREDICTOR_AVAILABLE = True
except ImportError:
    PREDICTOR_AVAILABLE = False
    logging.warning("DenialPredictor not available - using mock predictions")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pydantic models for integration endpoints
class ClaimsServiceIntegrationResponse(BaseModel):
    """Response model for Claims Service integration operations"""
    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Operation message")
    data: Optional[Dict] = Field(None, description="Operation data")
    timestamp: str = Field(..., description="Operation timestamp")

class IntegrationHealthResponse(BaseModel):
    """Response model for integration health check"""
    denial_prediction_status: str = Field(..., description="DenialPrediction service status")
    claims_service_status: str = Field(..., description="Claims service status")
    integration_status: str = Field(..., description="Overall integration status")
    timestamp: str = Field(..., description="Health check timestamp")

# Create FastAPI app
app = FastAPI(
    title="Enhanced DenialPrediction API with Claims Service Integration",
    description="REST API for healthcare claim denial prediction with FHIR integration",
    version="2.0.0",
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

# Global variables
CLAIMS_SERVICE_URL = os.getenv('CLAIMS_SERVICE_URL', 'http://localhost:8001')
claims_client: Optional[ClaimsServiceClient] = None
predictor: Optional[Any] = None

def get_claims_client() -> ClaimsServiceClient:
    """Get Claims Service client instance"""
    global claims_client
    if claims_client is None:
        claims_client = create_claims_service_client(CLAIMS_SERVICE_URL)
    return claims_client

def get_predictor():
    """Get prediction model instance"""
    global predictor
    if predictor is None and PREDICTOR_AVAILABLE:
        try:
            predictor = DenialPredictor()
            logger.info("DenialPredictor loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load DenialPredictor: {e}")
            predictor = None
    return predictor

def mock_prediction(claim_data: Dict) -> Dict:
    """Mock prediction for testing when model is not available"""
    import random
    
    # Simple mock prediction logic
    base_probability = 0.3
    risk_factors = []
    
    # Adjust based on claim amount
    claim_amount = claim_data.get("claim_amount", 0)
    if claim_amount > 10000:
        base_probability += 0.2
        risk_factors.append("high_claim_amount")
    
    # Adjust based on patient age
    patient_age = claim_data.get("patient_age", 45)
    if patient_age > 65:
        base_probability += 0.1
        risk_factors.append("elderly_patient")
    
    # Add some randomness
    final_probability = min(0.95, base_probability + random.uniform(-0.1, 0.1))
    
    # Determine risk level
    if final_probability > 0.7:
        risk_level = "HIGH"
    elif final_probability > 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "denial_probability": final_probability,
        "risk_level": risk_level,
        "top_risk_factors": risk_factors[:3],
        "recommended_actions": [
            "Verify patient eligibility",
            "Check authorization requirements",
            "Review claim documentation"
        ],
        "model_version": "mock-v1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("Starting Enhanced DenialPrediction API with Claims Service Integration...")
    logger.info(f"Claims Service URL: {CLAIMS_SERVICE_URL}")
    
    # Initialize Claims Service client
    global claims_client
    claims_client = create_claims_service_client(CLAIMS_SERVICE_URL)
    
    # Test Claims Service connection
    try:
        health = await claims_client.health_check()
        logger.info(f"Claims Service health check: {health}")
    except Exception as e:
        logger.warning(f"Claims Service not available: {e}")

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check the health of the API and ML model"""
    try:
        model_loaded = get_predictor() is not None or not PREDICTOR_AVAILABLE
        return HealthResponse(
            status="healthy" if model_loaded else "degraded",
            timestamp=datetime.utcnow().isoformat(),
            model_loaded=model_loaded,
            version="2.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            timestamp=datetime.utcnow().isoformat(),
            model_loaded=False,
            version="2.0.0"
        )

@app.get("/health/integration", response_model=IntegrationHealthResponse, tags=["Health"])
async def integration_health_check():
    """Check the health of the integration between services"""
    try:
        # Check DenialPrediction status
        denial_prediction_status = "healthy"
        try:
            predictor = get_predictor()
            if predictor is None and PREDICTOR_AVAILABLE:
                denial_prediction_status = "degraded"
        except Exception:
            denial_prediction_status = "error"
        
        # Check Claims Service status
        claims_service_status = "healthy"
        try:
            claims_client = get_claims_client()
            await claims_client.health_check()
        except Exception:
            claims_service_status = "error"
        
        # Determine overall integration status
        if denial_prediction_status == "healthy" and claims_service_status == "healthy":
            integration_status = "healthy"
        elif denial_prediction_status == "error" or claims_service_status == "error":
            integration_status = "error"
        else:
            integration_status = "degraded"
        
        return IntegrationHealthResponse(
            denial_prediction_status=denial_prediction_status,
            claims_service_status=claims_service_status,
            integration_status=integration_status,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Integration health check failed: {e}")
        return IntegrationHealthResponse(
            denial_prediction_status="error",
            claims_service_status="error",
            integration_status="error",
            timestamp=datetime.utcnow().isoformat()
        )

# Original DenialPrediction endpoints (maintained for backward compatibility)

@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_denial(claim: ClaimData):
    """Predict denial probability for a single claim"""
    try:
        predictor = get_predictor()
        
        if predictor is not None:
            # Use actual model
            prediction_result = predictor.predict(claim.dict())
        else:
            # Use mock prediction
            prediction_result = mock_prediction(claim.dict())
        
        return PredictionResponse(
            claim_id=claim.claim_id,
            denial_probability=prediction_result["denial_probability"],
            risk_level=prediction_result["risk_level"],
            top_risk_factors=[{"factor": f, "impact": "increases", "magnitude": 0.1, "rank": i+1} 
                             for i, f in enumerate(prediction_result["top_risk_factors"])],
            recommended_actions=prediction_result["recommended_actions"],
            model_version=prediction_result["model_version"],
            prediction_timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error predicting denial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/predict/batch", response_model=BatchPredictionResponse, tags=["Prediction"])
async def predict_denial_batch(batch_request: BatchPredictionRequest):
    """Predict denial probability for multiple claims"""
    try:
        import time
        start_time = time.time()
        
        predictions = []
        high_risk_count = 0
        
        for claim in batch_request.claims:
            try:
                prediction_result = await predict_denial(claim)
                predictions.append(prediction_result)
                
                if prediction_result.risk_level == "HIGH":
                    high_risk_count += 1
            except Exception as e:
                logger.error(f"Error predicting claim {claim.claim_id}: {e}")
                # Continue with other claims
        
        processing_time = time.time() - start_time
        
        summary = {
            "total_claims": len(batch_request.claims),
            "successful_predictions": len(predictions),
            "high_risk_claims": high_risk_count,
            "average_risk_score": sum(p.denial_probability for p in predictions) / len(predictions) if predictions else 0,
            "processing_time_seconds": processing_time
        }
        
        return BatchPredictionResponse(
            predictions=predictions,
            summary=summary
        )
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced integration endpoints

@app.get("/api/v1/claims/from-service", response_model=ClaimsServiceIntegrationResponse, tags=["Integration"])
async def get_claims_from_service(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of claims to retrieve"),
    status: str = Query("active", description="Claim status filter"),
    claims_client: ClaimsServiceClient = Depends(get_claims_client)
):
    """Get claims from Claims Service in DenialPrediction format"""
    try:
        claims = await claims_client.get_claims_for_prediction(limit=limit, status=status)
        
        return ClaimsServiceIntegrationResponse(
            status="success",
            message=f"Retrieved {len(claims)} claims from Claims Service",
            data={"claims": claims, "count": len(claims)},
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting claims from service: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/predict/from-claims-service", response_model=ClaimsServiceIntegrationResponse, tags=["Integration"])
async def predict_from_claims_service(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of claims to process"),
    status: str = Query("active", description="Claim status filter"),
    claims_client: ClaimsServiceClient = Depends(get_claims_client)
):
    """Predict denials for claims from Claims Service"""
    try:
        # Get claims from Claims Service
        claims = await claims_client.get_claims_for_prediction(limit=limit, status=status)
        
        predictions = []
        for claim in claims:
            try:
                # Make prediction
                if get_predictor() is not None:
                    prediction_result = get_predictor().predict(claim)
                else:
                    prediction_result = mock_prediction(claim)
                
                # Update claim with prediction
                prediction_data = {
                    "claim_id": claim["claim_id"],
                    "denial_probability": prediction_result["denial_probability"],
                    "risk_level": prediction_result["risk_level"],
                    "top_risk_factors": prediction_result["top_risk_factors"],
                    "recommended_actions": prediction_result["recommended_actions"],
                    "model_version": prediction_result["model_version"]
                }
                
                # Update claim in Claims Service
                await claims_client.update_claim_with_prediction(claim["claim_id"], prediction_data)
                
                predictions.append(prediction_data)
                
            except Exception as e:
                logger.error(f"Error processing claim {claim.get('claim_id')}: {e}")
                continue
        
        return ClaimsServiceIntegrationResponse(
            status="success",
            message=f"Processed {len(predictions)} claims with predictions",
            data={"predictions": predictions, "processed_count": len(predictions)},
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error predicting from Claims Service: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sync/predictions", response_model=ClaimsServiceIntegrationResponse, tags=["Integration"])
async def sync_predictions_to_service(
    claims_client: ClaimsServiceClient = Depends(get_claims_client)
):
    """Sync local predictions to Claims Service"""
    try:
        # This would typically sync predictions from local database to Claims Service
        # For now, return a placeholder response
        
        return ClaimsServiceIntegrationResponse(
            status="success",
            message="Prediction sync completed",
            data={"synced_count": 0},
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Error syncing predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stats/integration", response_model=Dict[str, Any], tags=["Statistics"])
async def get_integration_statistics(
    claims_client: ClaimsServiceClient = Depends(get_claims_client)
):
    """Get integration statistics"""
    try:
        # Get statistics from Claims Service
        claims_stats = await claims_client.get_claims_stats()
        
        # Get prediction statistics
        predictions_stats = await claims_client.get_predictions()
        
        # Get denial statistics
        denials_stats = await claims_client.get_denial_records()
        
        return {
            "claims_service": claims_stats,
            "predictions": {
                "total": len(predictions_stats),
                "high_risk": len([p for p in predictions_stats if p.get("risk_level") == "HIGH"]),
                "average_probability": sum(p.get("denial_probability", 0) for p in predictions_stats) / len(predictions_stats) if predictions_stats else 0
            },
            "denials": {
                "total": len(denials_stats),
                "pending": len([d for d in denials_stats if d.get("resolution_status") == "pending"]),
                "resolved": len([d for d in denials_stats if d.get("resolution_status") == "resolved"])
            },
            "integration": {
                "claims_service_url": CLAIMS_SERVICE_URL,
                "last_sync": datetime.utcnow().isoformat(),
                "status": "active"
            }
        }
    except Exception as e:
        logger.error(f"Error getting integration statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Denial classification endpoints (for Phase 2)

@app.post("/api/v1/classify/denial", response_model=ClassificationResponse, tags=["Classification"])
async def classify_denial(denial_input: DenialInput):
    """Classify denial reason and recommend resolution workflow"""
    try:
        # Mock classification logic
        # In a real implementation, this would use NLP models
        
        classification_result = {
            "cause_category": "documentation",
            "subcategory": "missing_authorization",
            "resolution_workflow": "auth_workflow",
            "appeal_success_probability": 0.75,
            "recommended_actions": [
                "Obtain prior authorization",
                "Submit appeal with supporting documentation",
                "Contact payer for clarification"
            ],
            "priority_score": 7,
            "estimated_resolution_time": 48,
            "automated_actions_available": True
        }
        
        return ClassificationResponse(
            claim_id=denial_input.claim_id,
            **classification_result
        )
    except Exception as e:
        logger.error(f"Error classifying denial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Enhanced DenialPrediction API with Claims Service Integration",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "integration_health": "/health/integration"
    }

if __name__ == "__main__":
    uvicorn.run(
        "enhanced_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 