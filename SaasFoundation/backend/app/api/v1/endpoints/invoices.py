from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.subscription import (
    InvoiceResponse
)
from app.services.subscription import subscription_service
from app.services.organization import organization_service

router = APIRouter()

# Invoice Endpoints
@router.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get user's invoices"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    return subscription_service.get_invoices(organization.id, db, limit, offset)

@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific invoice"""
    organization, _ = organization_service.get_user_organization(current_user.id, db)
    
    if not organization:
        raise HTTPException(status_code=404, detail="No organization found")
    
    return subscription_service.get_invoice(invoice_id, organization.id, db)

@router.post("/invoices/{invoice_id}/pay")
async def pay_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simulate payment of invoice"""
    organization, role = organization_service.get_user_organization(current_user.id, db)
    
    if not organization or role not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions to pay invoices")
    
    return subscription_service.pay_invoice(invoice_id, organization.id, db)