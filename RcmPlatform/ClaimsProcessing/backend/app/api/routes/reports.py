# =============================================================================
# FILE: backend/app/api/routes/reports.py
# =============================================================================
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ...database.connection import get_db
from ...database.models import Claim, ClaimStatus, ClaimType

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    # Total claims by status
    status_counts = db.query(
        Claim.status, 
        func.count(Claim.id).label('count')
    ).group_by(Claim.status).all()
    
    # Claims by type
    type_counts = db.query(
        Claim.claim_type,
        func.count(Claim.id).label('count')
    ).group_by(Claim.claim_type).all()
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_claims = db.query(func.count(Claim.id)).filter(
        Claim.created_at >= thirty_days_ago
    ).scalar()
    
    # Financial summary
    financial_summary = db.query(
        func.sum(Claim.total_charge).label('total_charged'),
        func.sum(Claim.allowed_amount).label('total_allowed'),
        func.sum(Claim.paid_amount).label('total_paid')
    ).first()
    
    return {
        "status_distribution": [{"status": s.status, "count": s.count} for s in status_counts],
        "type_distribution": [{"type": t.claim_type, "count": t.count} for t in type_counts],
        "recent_claims_30_days": recent_claims,
        "financial_summary": {
            "total_charged": float(financial_summary.total_charged or 0),
            "total_allowed": float(financial_summary.total_allowed or 0),
            "total_paid": float(financial_summary.total_paid or 0)
        }
    }

@router.get("/rejection-analysis")
def get_rejection_analysis(db: Session = Depends(get_db)):
    """Get rejection analysis report"""
    
    rejected_claims = db.query(Claim).filter(
        Claim.status == ClaimStatus.REJECTED
    ).all()
    
    error_categories = {}
    for claim in rejected_claims:
        if claim.validation_errors:
            for error in claim.validation_errors.get('errors', []):
                category = error.split(':')[0] if ':' in error else 'Other'
                error_categories[category] = error_categories.get(category, 0) + 1
    
    return {
        "total_rejected": len(rejected_claims),
        "error_categories": error_categories,
        "rejection_rate": len(rejected_claims) / max(db.query(func.count(Claim.id)).scalar(), 1) * 100
    }

@router.get("/reconciliation")
def get_reconciliation_report(db: Session = Depends(get_db)):
    """Get financial reconciliation report"""
    
    # Claims with payments
    paid_claims = db.query(Claim).filter(
        Claim.status.in_([ClaimStatus.PAID, ClaimStatus.ADJUSTED])
    ).all()
    
    reconciliation_data = []
    for claim in paid_claims:
        reconciliation_data.append({
            "claim_number": claim.claim_number,
            "claim_type": claim.claim_type,
            "total_charge": float(claim.total_charge),
            "allowed_amount": float(claim.allowed_amount or 0),
            "paid_amount": float(claim.paid_amount or 0),
            "patient_responsibility": float(claim.patient_responsibility or 0),
            "adjustment_amount": float(claim.total_charge - (claim.paid_amount or 0) - (claim.patient_responsibility or 0))
        })
    
    return {
        "reconciliation_data": reconciliation_data,
        "summary": {
            "total_claims": len(paid_claims),
            "total_charged": sum(float(c.total_charge) for c in paid_claims),
            "total_paid": sum(float(c.paid_amount or 0) for c in paid_claims),
            "total_adjustments": sum(
                float(c.total_charge - (c.paid_amount or 0) - (c.patient_responsibility or 0)) 
                for c in paid_claims
            )
        }
    }
