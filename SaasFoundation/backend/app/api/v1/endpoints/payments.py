from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.subscription import (
    PaymentMethodCreate, 
    PaymentMethodResponse
)
from app.services.subscription import subscription_service
from app.services.organization import organization_service

router = APIRouter()

# Payment Methods Endpoints
@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
async def get_payment_methods(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get user's payment methods"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    return subscription_service.get_payment_methods(organization.id, db)

@router.post("/payment-methods", response_model=PaymentMethodResponse)
async def add_payment_method(
    payment_data: PaymentMethodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add new payment method"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions to manage payment methods")
    
    return subscription_service.add_payment_method(organization.id, payment_data, db)

@router.delete("/payment-methods/{payment_method_id}")
async def delete_payment_method(
    payment_method_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete payment method"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions to manage payment methods")
    
    return subscription_service.delete_payment_method(payment_method_id, organization.id, db)