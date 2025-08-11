"""
Enhanced Claims Service Routers with DenialPrediction Integration

This module provides additional API endpoints for the Claims service that support
integration with the DenialPrediction system, including prediction management
and denial record handling.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from models.database import get_db
from models.fhir_models import Claim, ClaimResponse, ExplanationOfBenefit, Coverage
from models.enhanced_models import Prediction, DenialRecord, RemediationAction, ModelVersion

logger = logging.getLogger(__name__)

# Create routers
predictions_router = APIRouter(prefix="/predictions", tags=["predictions"])
denial_records_router = APIRouter(prefix="/denial-records", tags=["denial-records"])
stats_router = APIRouter(prefix="/stats", tags=["statistics"])

# Prediction endpoints

@predictions_router.post("/", response_model=Dict[str, Any])
async def create_prediction(
    prediction_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create a new prediction record"""
    try:
        prediction = Prediction(
            claim_id=prediction_data["claim_id"],
            model_version=prediction_data["model_version"],
            denial_probability=prediction_data["denial_probability"],
            risk_level=prediction_data["risk_level"],
            top_risk_factors=prediction_data.get("top_risk_factors"),
            recommended_actions=prediction_data.get("recommended_actions"),
            shap_values=prediction_data.get("shap_values")
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        # Also update the claim with prediction data
        claim = db.query(Claim).filter(Claim.id == prediction_data["claim_id"]).first()
        if claim:
            claim.denial_probability = prediction_data["denial_probability"]
            claim.risk_level = prediction_data["risk_level"]
            claim.prediction_timestamp = datetime.utcnow()
            claim.model_version = prediction_data["model_version"]
            claim.top_risk_factors = prediction_data.get("top_risk_factors")
            claim.recommended_actions = prediction_data.get("recommended_actions")
            claim.shap_values = prediction_data.get("shap_values")
            db.commit()
        
        return {
            "status": "success",
            "message": "Prediction created successfully",
            "prediction_id": prediction.id,
            "claim_id": prediction.claim_id
        }
    except Exception as e:
        logger.error(f"Error creating prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@predictions_router.get("/", response_model=List[Dict[str, Any]])
async def get_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    claim_id: Optional[str] = Query(None),
    model_version: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get predictions with optional filtering"""
    try:
        query = db.query(Prediction)
        
        if claim_id:
            query = query.filter(Prediction.claim_id == claim_id)
        if model_version:
            query = query.filter(Prediction.model_version == model_version)
        
        predictions = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": p.id,
                "claim_id": p.claim_id,
                "model_version": p.model_version,
                "denial_probability": p.denial_probability,
                "risk_level": p.risk_level,
                "top_risk_factors": p.top_risk_factors,
                "recommended_actions": p.recommended_actions,
                "prediction_timestamp": p.prediction_timestamp.isoformat() if p.prediction_timestamp else None,
                "actual_outcome": p.actual_outcome,
                "feedback_received": p.feedback_received
            }
            for p in predictions
        ]
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@predictions_router.get("/{prediction_id}", response_model=Dict[str, Any])
async def get_prediction(prediction_id: str, db: Session = Depends(get_db)):
    """Get a specific prediction by ID"""
    try:
        prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        return {
            "id": prediction.id,
            "claim_id": prediction.claim_id,
            "model_version": prediction.model_version,
            "denial_probability": prediction.denial_probability,
            "risk_level": prediction.risk_level,
            "top_risk_factors": prediction.top_risk_factors,
            "recommended_actions": prediction.recommended_actions,
            "shap_values": prediction.shap_values,
            "prediction_timestamp": prediction.prediction_timestamp.isoformat() if prediction.prediction_timestamp else None,
            "actual_outcome": prediction.actual_outcome,
            "feedback_received": prediction.feedback_received
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@predictions_router.put("/{prediction_id}/feedback", response_model=Dict[str, Any])
async def update_prediction_feedback(
    prediction_id: str,
    feedback_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update prediction with feedback"""
    try:
        prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        prediction.actual_outcome = feedback_data.get("actual_outcome")
        prediction.feedback_received = True
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Prediction feedback updated successfully",
            "prediction_id": prediction.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prediction feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Denial Records endpoints

@denial_records_router.post("/", response_model=Dict[str, Any])
async def create_denial_record(
    denial_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create a new denial record"""
    try:
        denial_record = DenialRecord(
            claim_id=denial_data["claim_id"],
            denial_date=datetime.fromisoformat(denial_data["denial_date"]),
            denial_codes=denial_data.get("denial_codes"),
            denial_reason_text=denial_data.get("denial_reason_text"),
            classification_result=denial_data.get("classification_result"),
            resolution_status=denial_data.get("resolution_status", "pending"),
            workflow_id=denial_data.get("workflow_id")
        )
        
        db.add(denial_record)
        db.commit()
        db.refresh(denial_record)
        
        # Update the claim with denial information
        claim = db.query(Claim).filter(Claim.id == denial_data["claim_id"]).first()
        if claim:
            claim.is_denied = True
            claim.denial_date = denial_record.denial_date
            claim.denial_codes = denial_record.denial_codes
            claim.denial_reason = denial_record.denial_reason_text
            db.commit()
        
        return {
            "status": "success",
            "message": "Denial record created successfully",
            "denial_record_id": denial_record.id,
            "claim_id": denial_record.claim_id
        }
    except Exception as e:
        logger.error(f"Error creating denial record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@denial_records_router.get("/", response_model=List[Dict[str, Any]])
async def get_denial_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    claim_id: Optional[str] = Query(None),
    resolution_status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get denial records with optional filtering"""
    try:
        query = db.query(DenialRecord)
        
        if claim_id:
            query = query.filter(DenialRecord.claim_id == claim_id)
        if resolution_status:
            query = query.filter(DenialRecord.resolution_status == resolution_status)
        
        denial_records = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": dr.id,
                "claim_id": dr.claim_id,
                "denial_date": dr.denial_date.isoformat() if dr.denial_date else None,
                "denial_codes": dr.denial_codes,
                "denial_reason_text": dr.denial_reason_text,
                "classification_result": dr.classification_result,
                "resolution_status": dr.resolution_status,
                "workflow_id": dr.workflow_id,
                "created_at": dr.created_at.isoformat() if dr.created_at else None,
                "updated_at": dr.updated_at.isoformat() if dr.updated_at else None
            }
            for dr in denial_records
        ]
    except Exception as e:
        logger.error(f"Error getting denial records: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@denial_records_router.get("/{record_id}", response_model=Dict[str, Any])
async def get_denial_record(record_id: int, db: Session = Depends(get_db)):
    """Get a specific denial record by ID"""
    try:
        denial_record = db.query(DenialRecord).filter(DenialRecord.id == record_id).first()
        if not denial_record:
            raise HTTPException(status_code=404, detail="Denial record not found")
        
        return {
            "id": denial_record.id,
            "claim_id": denial_record.claim_id,
            "denial_date": denial_record.denial_date.isoformat() if denial_record.denial_date else None,
            "denial_codes": denial_record.denial_codes,
            "denial_reason_text": denial_record.denial_reason_text,
            "classification_result": denial_record.classification_result,
            "resolution_status": denial_record.resolution_status,
            "workflow_id": denial_record.workflow_id,
            "created_at": denial_record.created_at.isoformat() if denial_record.created_at else None,
            "updated_at": denial_record.updated_at.isoformat() if denial_record.updated_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting denial record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@denial_records_router.put("/{record_id}", response_model=Dict[str, Any])
async def update_denial_record(
    record_id: int,
    denial_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a denial record"""
    try:
        denial_record = db.query(DenialRecord).filter(DenialRecord.id == record_id).first()
        if not denial_record:
            raise HTTPException(status_code=404, detail="Denial record not found")
        
        # Update fields
        if "denial_codes" in denial_data:
            denial_record.denial_codes = denial_data["denial_codes"]
        if "denial_reason_text" in denial_data:
            denial_record.denial_reason_text = denial_data["denial_reason_text"]
        if "classification_result" in denial_data:
            denial_record.classification_result = denial_data["classification_result"]
        if "resolution_status" in denial_data:
            denial_record.resolution_status = denial_data["resolution_status"]
        if "workflow_id" in denial_data:
            denial_record.workflow_id = denial_data["workflow_id"]
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Denial record updated successfully",
            "denial_record_id": denial_record.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating denial record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoints

@stats_router.get("/claims", response_model=Dict[str, Any])
async def get_claims_stats(db: Session = Depends(get_db)):
    """Get claims statistics"""
    try:
        total_claims = db.query(Claim).count()
        active_claims = db.query(Claim).filter(Claim.status == "active").count()
        denied_claims = db.query(Claim).filter(Claim.is_denied == True).count()
        high_risk_claims = db.query(Claim).filter(Claim.risk_level == "HIGH").count()
        
        # Calculate average denial probability
        avg_denial_prob = db.query(Claim.denial_probability).filter(
            Claim.denial_probability.isnot(None)
        ).scalar()
        
        return {
            "total_claims": total_claims,
            "active_claims": active_claims,
            "denied_claims": denied_claims,
            "high_risk_claims": high_risk_claims,
            "average_denial_probability": float(avg_denial_prob) if avg_denial_prob else 0.0,
            "denial_rate": (denied_claims / total_claims * 100) if total_claims > 0 else 0.0
        }
    except Exception as e:
        logger.error(f"Error getting claims stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@stats_router.get("/predictions", response_model=Dict[str, Any])
async def get_predictions_stats(db: Session = Depends(get_db)):
    """Get predictions statistics"""
    try:
        total_predictions = db.query(Prediction).count()
        high_risk_predictions = db.query(Prediction).filter(Prediction.risk_level == "HIGH").count()
        feedback_count = db.query(Prediction).filter(Prediction.feedback_received == True).count()
        
        # Calculate average denial probability
        avg_prob = db.query(Prediction.denial_probability).scalar()
        
        # Get model versions
        model_versions = db.query(Prediction.model_version).distinct().all()
        
        return {
            "total_predictions": total_predictions,
            "high_risk_predictions": high_risk_predictions,
            "feedback_count": feedback_count,
            "average_denial_probability": float(avg_prob) if avg_prob else 0.0,
            "model_versions": [mv[0] for mv in model_versions],
            "feedback_coverage": (feedback_count / total_predictions * 100) if total_predictions > 0 else 0.0
        }
    except Exception as e:
        logger.error(f"Error getting predictions stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@stats_router.get("/denials", response_model=Dict[str, Any])
async def get_denials_stats(db: Session = Depends(get_db)):
    """Get denials statistics"""
    try:
        total_denials = db.query(DenialRecord).count()
        pending_denials = db.query(DenialRecord).filter(DenialRecord.resolution_status == "pending").count()
        resolved_denials = db.query(DenialRecord).filter(DenialRecord.resolution_status == "resolved").count()
        in_progress_denials = db.query(DenialRecord).filter(DenialRecord.resolution_status == "in_progress").count()
        
        return {
            "total_denials": total_denials,
            "pending_denials": pending_denials,
            "resolved_denials": resolved_denials,
            "in_progress_denials": in_progress_denials,
            "resolution_rate": (resolved_denials / total_denials * 100) if total_denials > 0 else 0.0
        }
    except Exception as e:
        logger.error(f"Error getting denials stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Claims endpoints

@stats_router.get("/claims/{claim_id}/predict", response_model=Dict[str, Any])
async def predict_claim_denial(claim_id: str, db: Session = Depends(get_db)):
    """Predict denial probability for a specific claim"""
    try:
        claim = db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # This would typically call the DenialPrediction service
        # For now, return a mock prediction
        import random
        
        mock_prediction = {
            "denial_probability": random.uniform(0.1, 0.8),
            "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "top_risk_factors": ["claim_amount", "provider_history", "diagnosis_codes"],
            "recommended_actions": ["Verify eligibility", "Check authorization", "Review documentation"],
            "model_version": "mock-v1.0.0"
        }
        
        # Update claim with prediction
        claim.denial_probability = mock_prediction["denial_probability"]
        claim.risk_level = mock_prediction["risk_level"]
        claim.prediction_timestamp = datetime.utcnow()
        claim.model_version = mock_prediction["model_version"]
        claim.top_risk_factors = mock_prediction["top_risk_factors"]
        claim.recommended_actions = mock_prediction["recommended_actions"]
        
        db.commit()
        
        return {
            "claim_id": claim_id,
            "prediction": mock_prediction,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting claim denial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@stats_router.get("/claims/predictions", response_model=List[Dict[str, Any]])
async def get_claim_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all claims with their predictions"""
    try:
        query = db.query(Claim).filter(Claim.denial_probability.isnot(None))
        
        if risk_level:
            query = query.filter(Claim.risk_level == risk_level)
        
        claims = query.offset(skip).limit(limit).all()
        
        return [
            {
                "claim_id": claim.id,
                "patient_id": claim.patient_id,
                "provider_id": claim.provider_id,
                "status": claim.status,
                "denial_probability": claim.denial_probability,
                "risk_level": claim.risk_level,
                "prediction_timestamp": claim.prediction_timestamp.isoformat() if claim.prediction_timestamp else None,
                "model_version": claim.model_version,
                "top_risk_factors": claim.top_risk_factors,
                "recommended_actions": claim.recommended_actions
            }
            for claim in claims
        ]
    except Exception as e:
        logger.error(f"Error getting claim predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 