""" 
Subscription.py 
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.subscription import (
    SubscriptionResponse, 
    SubscriptionCreate, 
    SubscriptionUpdate, 
    SubscriptionSummary, 
    UsageMetricResponse
)
from app.services.subscription import subscription_service
from app.services.organization import organization_service

router = APIRouter()


# Subscription Management Endpoints
@router.get("/current", response_model=SubscriptionSummary)
async def get_current_subscription(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get current user's subscription with full details"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    summary_data = subscription_service.get_current_subscription(organization.id, db)
    
    return SubscriptionSummary(
        subscription=summary_data["subscription"],
        usage_metrics=summary_data["usage_metrics"],
        recent_invoices=summary_data["recent_invoices"],
        payment_methods=summary_data["payment_methods"]
    )

@router.post("", response_model=SubscriptionResponse)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or upgrade subscription"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    # Only owners can manage subscriptions
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only organization owners can manage subscriptions")
    
    return subscription_service.create_subscription(organization.id, subscription_data, db)

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: str,
    subscription_data: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update subscription"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role != "owner":
        raise HTTPException(status_code=403, detail="Only organization owners can manage subscriptions")
    
    return subscription_service.update_subscription(subscription_id, organization.id, subscription_data, db)

@router.delete("/{subscription_id}")
async def cancel_subscription(
    subscription_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel subscription"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role != "owner":
        raise HTTPException(status_code=403, detail="Only organization owners can manage subscriptions")
    
    return subscription_service.cancel_subscription(subscription_id, organization.id, db)


# Usage Metrics Endpoints
@router.get("/usage", response_model=List[UsageMetricResponse])
async def get_usage_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    period_start: Optional[datetime] = Query(None),
    period_end: Optional[datetime] = Query(None)
):
    """Get usage metrics for user"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    return subscription_service.get_usage_metrics(organization.id, db, period_start, period_end)

@router.post("/usage/{metric_name}")
async def record_usage(
    metric_name: str,
    value: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record usage metric"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    return subscription_service.record_usage(organization.id, metric_name, value, db)
