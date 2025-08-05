
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
 
from app.schemas.subscription import (
    PricingPlanResponse
)
from app.services.subscription import subscription_service

router = APIRouter()
# Pricing Plans Endpoints
@router.get("/plans", response_model=List[PricingPlanResponse])
async def get_pricing_plans(db: Session = Depends(get_db)):
    """Get all active pricing plans"""
    return subscription_service.get_pricing_plans(db)

@router.get("/plans/{plan_id}/details", response_model=PricingPlanResponse)
async def get_pricing_plan(plan_id: str, db: Session = Depends(get_db)):
    """Get specific pricing plan"""
    return subscription_service.get_pricing_plan(plan_id, db)