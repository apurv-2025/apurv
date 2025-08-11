"""
Healthcare Denial Prediction API
Main FastAPI application for claim denial prediction and automation
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import redis
import json
import mlflow
import mlflow.xgboost
import joblib
from datetime import datetime
import logging
import time
import uuid
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Import our modules
from models.database import SessionLocal, Claim, Prediction, DenialRecord, RemediationAction
from models.denial_predictor import DenialPredictor
from features.feature_engineering import FeatureEngineer
from workflows.denial_classifier import DenialClassifier
from workflows.remediation_engine import AutoRemediationEngine
from api.models import (
    ClaimData, 
    PredictionResponse, 
    BatchPredictionRequest, 
    BatchPredictionResponse,
    DenialInput,
    ClassificationResponse,
    RemediationRequest,
    RemediationResponse,
    DenialStatusResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Denial Prediction API",
    description="API for predicting healthcare claim denials and automating remediation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Prometheus metrics
PREDICTION_COUNTER = Counter('denial_predictions_total', 'Total predictions made')
PREDICTION_LATENCY = Histogram('denial_prediction_duration_seconds', 'Prediction latency')
HIGH_RISK_COUNTER = Counter('high_risk_predictions_total', 'High risk predictions')

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Global model and scaler
model = None
scaler = None
feature_engineer = None

# ============================================================================
# STARTUP AND LIFECYCLE
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model and initialize components on startup"""
    global model, scaler, feature_engineer
    
    # Always initialize feature engineer
    feature_engineer = FeatureEngineer()
    
    try:
        # Load latest model from MLflow
        model_name = "denial_predictor_v1"
        model_version = "latest"
        
        model_uri = f"models:/{model_name}/{model_version}"
        model = mlflow.xgboost.load_model(model_uri)
        
        # Load scaler
        scaler = joblib.load(f"{model_name}_scaler.joblib")
        
        logger.info("Model loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        # For demo purposes, we'll continue without the model
        logger.warning("Continuing without pre-trained model")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token - simplified for demo"""
    token = credentials.credentials
    if token != "demo_token_123":  # In production, use proper JWT validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": model is not None,
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=PredictionResponse)
async def predict_single_claim(
    claim_data: ClaimData,
    token: str = Depends(verify_token)
):
    """Predict denial probability for a single claim"""
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"prediction:{claim_data.claim_id}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            result = json.loads(cached_result)
            PREDICTION_COUNTER.inc()
            return PredictionResponse(**result)
        
        # Create claim record for feature engineering
        claim_dict = claim_data.dict()
        claim_dict['submission_date'] = datetime.utcnow().isoformat()
        claim_dict['service_date'] = datetime.fromisoformat(claim_data.service_date)
        
        # Store temporarily in database for feature engineering
        db = SessionLocal()
        try:
            claim = Claim(**claim_dict)
            db.merge(claim)
            db.commit()
        finally:
            db.close()
        
        # Generate features
        features = feature_engineer.create_features(claim_data.claim_id)
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        feature_df = feature_df.fillna(0)
        
        # Ensure all required features are present
        if model is not None:
            required_features = model.get_booster().feature_names
            for feature in required_features:
                if feature not in feature_df.columns:
                    feature_df[feature] = 0.0
            
            feature_df = feature_df[required_features]
            
            # Scale features
            features_scaled = scaler.transform(feature_df)
            
            # Make prediction
            denial_probability = model.predict_proba(features_scaled)[0][1]
        else:
            # Demo mode - generate random prediction
            denial_probability = np.random.beta(2, 8)
        
        # Generate explanations
        if model is not None:
            predictor = DenialPredictor()
            predictor.model = model
            predictor.scaler = scaler
            predictor.feature_names = required_features
            
            _, explanations = predictor.predict_with_explanation(feature_df)
        else:
            explanations = {'error': 'Model not loaded'}
        
        # Determine risk level
        if denial_probability >= 0.7:
            risk_level = "HIGH"
            HIGH_RISK_COUNTER.inc()
        elif denial_probability >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate risk factors and recommendations
        top_risk_factors = _generate_risk_factors(features, explanations, denial_probability)
        recommended_actions = _generate_recommendations(claim_data, denial_probability, top_risk_factors)
        
        # Create response
        response = PredictionResponse(
            claim_id=claim_data.claim_id,
            denial_probability=round(denial_probability, 4),
            risk_level=risk_level,
            top_risk_factors=top_risk_factors,
            recommended_actions=recommended_actions,
            model_version="v1.0",
            prediction_timestamp=datetime.utcnow().isoformat()
        )
        
        # Cache result for 1 hour
        redis_client.setex(cache_key, 3600, response.json())
        
        # Store prediction in database
        _store_prediction(claim_data.claim_id, response)
        
        # Update metrics
        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(time.time() - start_time)
        
        return response
        
    except Exception as e:
        logger.error(f"Error predicting claim {claim_data.claim_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_claims(
    request: BatchPredictionRequest,
    token: str = Depends(verify_token)
):
    """Predict denial probability for multiple claims"""
    start_time = time.time()
    
    try:
        predictions = []
        high_risk_count = 0
        total_risk_score = 0.0
        
        for claim_data in request.claims:
            try:
                # Reuse single prediction logic
                prediction = await predict_single_claim(claim_data)
                predictions.append(prediction)
                
                if prediction.risk_level == "HIGH":
                    high_risk_count += 1
                
                total_risk_score += prediction.denial_probability
                
            except Exception as e:
                logger.warning(f"Failed to predict claim {claim_data.claim_id}: {e}")
                continue
        
        # Calculate summary statistics
        avg_risk_score = total_risk_score / len(predictions) if predictions else 0.0
        
        summary = {
            "total_claims": len(request.claims),
            "successful_predictions": len(predictions),
            "high_risk_claims": high_risk_count,
            "average_risk_score": round(avg_risk_score, 4),
            "processing_time_seconds": round(time.time() - start_time, 2)
        }
        
        return BatchPredictionResponse(
            predictions=predictions,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )

@app.post("/feedback")
async def submit_feedback(
    claim_id: str,
    actual_outcome: bool,
    feedback_notes: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Submit feedback on prediction accuracy"""
    try:
        db = SessionLocal()
        try:
            # Update prediction record
            prediction = db.query(Prediction).filter(
                Prediction.claim_id == claim_id
            ).first()
            
            if prediction:
                prediction.actual_outcome = actual_outcome
                prediction.feedback_received = True
                db.commit()
                
                # Invalidate cache
                redis_client.delete(f"prediction:{claim_id}")
                
                return {
                    "status": "success",
                    "message": "Feedback recorded successfully"
                }
            else:
                raise HTTPException(status_code=404, detail="Prediction not found")
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@app.get("/model/performance")
async def get_model_performance(token: str = Depends(verify_token)):
    """Get current model performance metrics"""
    try:
        db = SessionLocal()
        try:
            # Calculate metrics from recent predictions with feedback
            query = """
            SELECT 
                COUNT(*) as total_predictions,
                AVG(CASE WHEN actual_outcome = true THEN 1.0 ELSE 0.0 END) as actual_denial_rate,
                AVG(denial_probability) as avg_predicted_probability,
                COUNT(CASE WHEN feedback_received THEN 1 END) as feedback_count
            FROM predictions 
            WHERE prediction_timestamp >= NOW() - INTERVAL '30 days'
            """
            
            result = db.execute(query).fetchone()
            
            return {
                "period_days": 30,
                "total_predictions": result.total_predictions,
                "actual_denial_rate": result.actual_denial_rate,
                "avg_predicted_probability": result.avg_predicted_probability,
                "feedback_coverage": result.feedback_count / result.total_predictions if result.total_predictions > 0 else 0,
                "model_version": "v1.0",
                "last_updated": datetime.utcnow().isoformat()
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error getting model performance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_risk_factors(features: Dict[str, Any], explanations: Dict[str, Any], probability: float) -> List[Dict[str, Any]]:
    """Generate top risk factors based on SHAP values"""
    risk_factors = []
    
    try:
        if 'shap_values' in explanations and explanations['shap_values']:
            shap_values = explanations['shap_values'][0]  # First prediction
            feature_names = explanations['feature_names']
            
            # Get top contributing features
            feature_contributions = list(zip(feature_names, shap_values))
            feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
            
            for i, (feature, contribution) in enumerate(feature_contributions[:5]):
                risk_factors.append({
                    "factor": _humanize_feature_name(feature),
                    "impact": "increases" if contribution > 0 else "decreases",
                    "magnitude": abs(contribution),
                    "rank": i + 1
                })
    except Exception as e:
        logger.warning(f"Error generating risk factors: {e}")
        # Fallback to simple rule-based factors
        if probability > 0.5:
            risk_factors = [
                {"factor": "High claim amount", "impact": "increases", "magnitude": 0.1, "rank": 1},
                {"factor": "Provider history", "impact": "increases", "magnitude": 0.08, "rank": 2}
            ]
    
    return risk_factors

def _generate_recommendations(claim_data: ClaimData, probability: float, risk_factors: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on risk factors"""
    recommendations = []
    
    if probability >= 0.7:
        recommendations.append("HIGH RISK: Review claim carefully before submission")
        
        if not claim_data.authorization_number:
            recommendations.append("Verify prior authorization requirements")
        
        recommendations.append("Double-check CPT and ICD code accuracy")
        recommendations.append("Confirm patient eligibility and coverage")
        
        if claim_data.claim_amount > 10000:
            recommendations.append("Consider breaking down high-value claim into components")
            
    elif probability >= 0.4:
        recommendations.append("MEDIUM RISK: Standard review recommended")
        recommendations.append("Verify coding accuracy")
        
    else:
        recommendations.append("LOW RISK: Proceed with standard processing")
    
    # Add specific recommendations based on risk factors
    for factor in risk_factors:
        if "authorization" in factor["factor"].lower():
            recommendations.append("Request prior authorization if not obtained")
        elif "coding" in factor["factor"].lower():
            recommendations.append("Review CPT/ICD code selection with clinical team")
    
    return list(set(recommendations))  # Remove duplicates

def _humanize_feature_name(feature_name: str) -> str:
    """Convert technical feature names to human-readable descriptions"""
    name_mapping = {
        "provider_historical_denial_rate": "Provider denial history",
        "payer_denial_rate": "Payer denial rate",
        "claim_amount_log": "Claim amount",
        "patient_age": "Patient age",
        "has_authorization": "Prior authorization status",
        "number_of_cpt_codes": "Number of procedures",
        "high_dollar_claim": "High-value claim flag",
        "weekend_service": "Weekend service date",
        "payer_type_medicare": "Medicare payer",
        "provider_specialty_denial_rate": "Specialty-specific denial rate"
    }
    
    return name_mapping.get(feature_name, feature_name.replace("_", " ").title())

def _store_prediction(claim_id: str, response: PredictionResponse):
    """Store prediction in database"""
    try:
        db = SessionLocal()
        try:
            prediction = Prediction(
                claim_id=claim_id,
                model_version=response.model_version,
                denial_probability=response.denial_probability,
                predicted_causes=[factor["factor"] for factor in response.top_risk_factors],
                shap_values={}  # Would store actual SHAP values in production
            )
            db.add(prediction)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"Failed to store prediction: {e}")

# ============================================================================
# PHASE 2: DENIAL CLASSIFICATION AND REMEDIATION ENDPOINTS
# ============================================================================

@app.post("/denial/classify", response_model=ClassificationResponse)
async def classify_denial(
    denial_input: DenialInput,
    token: str = Depends(verify_token)
):
    """Classify a denial and determine appropriate remediation workflow"""
    try:
        # Initialize classifier
        classifier = DenialClassifier()
        
        # Classify the denial
        classification = classifier.classify_denial(denial_input)
        
        # Determine if automated actions are available
        automated_actions = classification.resolution_workflow.value not in [
            "manual_review", "medical_review", "appeal_filing"
        ]
        
        return ClassificationResponse(
            claim_id=denial_input.claim_id,
            cause_category=classification.cause_category.value,
            confidence=classification.confidence,
            subcategory=classification.subcategory,
            resolution_workflow=classification.resolution_workflow.value,
            appeal_success_probability=classification.appeal_success_probability,
            recommended_actions=classification.recommended_actions,
            priority_score=classification.priority_score,
            estimated_resolution_time=classification.estimated_resolution_time,
            automated_actions_available=automated_actions
        )
        
    except Exception as e:
        logger.error(f"Error classifying denial: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error classifying denial: {str(e)}"
        )

@app.post("/denial/remediate", response_model=RemediationResponse)
async def remediate_denial(
    request: RemediationRequest,
    token: str = Depends(verify_token)
):
    """Execute automated remediation workflow for a denial"""
    try:
        db = SessionLocal()
        
        # Get denial record
        denial_record = db.query(DenialRecord).filter(
            DenialRecord.id == request.denial_record_id
        ).first()
        
        if not denial_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Denial record not found"
            )
        
        # Initialize remediation engine
        remediation_engine = AutoRemediationEngine(db, redis_client)
        
        # Create denial input from record
        denial_input = DenialInput(
            claim_id=denial_record.claim_id,
            denial_codes=json.loads(denial_record.denial_codes),
            denial_reason_text=denial_record.denial_reason_text,
            claim_data={}  # Would be populated from original claim data
        )
        
        # Process the denial
        result = await remediation_engine.process_denial(denial_input)
        
        if result.get("status") == "failed":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Remediation failed: {result.get('error')}"
            )
        
        workflow_result = result.get("workflow_result", {})
        
        return RemediationResponse(
            denial_record_id=request.denial_record_id,
            status=result.get("status", "completed"),
            workflow_type=workflow_result.get("workflow_type", "manual_review"),
            actions_taken=workflow_result.get("actions_taken", []),
            estimated_completion=workflow_result.get("estimated_completion"),
            success_probability=workflow_result.get("success_probability", 0.5)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error remediating denial: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error remediating denial: {str(e)}"
        )
    finally:
        db.close()

@app.get("/denial/{denial_record_id}/status", response_model=DenialStatusResponse)
async def get_denial_status(
    denial_record_id: int,
    token: str = Depends(verify_token)
):
    """Get current status of a denial remediation workflow"""
    try:
        db = SessionLocal()
        
        # Get denial record
        denial_record = db.query(DenialRecord).filter(
            DenialRecord.id == denial_record_id
        ).first()
        
        if not denial_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Denial record not found"
            )
        
        # Get recent actions
        actions = db.query(RemediationAction).filter(
            RemediationAction.denial_record_id == denial_record_id
        ).order_by(RemediationAction.executed_at.desc()).limit(10).all()
        
        # Calculate workflow progress
        total_actions = len(actions)
        completed_actions = len([a for a in actions if a.status == "completed"])
        progress = (completed_actions / max(total_actions, 1)) * 100
        
        # Get last action
        last_action = "No actions taken" if not actions else actions[0].action_type
        
        # Determine next action based on current status
        next_action = None
        if denial_record.resolution_status == "processing":
            next_action = "Continue automated workflow"
        elif denial_record.resolution_status == "manual_review":
            next_action = "Manual review required"
        
        actions_log = []
        for action in actions:
            actions_log.append({
                "action_type": action.action_type,
                "status": action.status,
                "executed_at": action.executed_at.isoformat(),
                "data": json.loads(action.action_data) if action.action_data else {}
            })
        
        return DenialStatusResponse(
            denial_record_id=denial_record_id,
            status=denial_record.resolution_status,
            workflow_progress=progress,
            last_action=last_action,
            next_action=next_action,
            estimated_completion=None,  # Would be calculated based on workflow
            actions_log=actions_log
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting denial status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting denial status: {str(e)}"
        )
    finally:
        db.close()

@app.post("/denial/process", response_model=Dict[str, Any])
async def process_denial_end_to_end(
    denial_input: DenialInput,
    token: str = Depends(verify_token)
):
    """Process a denial end-to-end: classify and remediate"""
    try:
        db = SessionLocal()
        
        # Step 1: Classify the denial
        classifier = DenialClassifier()
        classification = classifier.classify_denial(denial_input)
        
        # Step 2: Initialize remediation engine
        remediation_engine = AutoRemediationEngine(db, redis_client)
        
        # Step 3: Process through remediation
        result = await remediation_engine.process_denial(denial_input)
        
        return {
            "classification": {
                "cause_category": classification.cause_category.value,
                "confidence": classification.confidence,
                "resolution_workflow": classification.resolution_workflow.value,
                "priority_score": classification.priority_score
            },
            "remediation": result,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error in end-to-end denial processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing denial: {str(e)}"
        )
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 