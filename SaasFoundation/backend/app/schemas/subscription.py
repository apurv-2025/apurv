from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
import uuid

class PricingPlanResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    description: Optional[str]
    price_monthly: Decimal
    price_yearly: Decimal
    features: List[str]
    limits: Dict[str, Any]
    is_active: bool
    sort_order: int
    
    class Config:
        from_attributes = True

class SubscriptionResponse(BaseModel):
    id: uuid.UUID
    plan: PricingPlanResponse
    status: str
    billing_cycle: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    plan_id: uuid.UUID
    billing_cycle: str = "monthly"
    
    @field_validator('billing_cycle')
    @classmethod
    def validate_billing_cycle(cls, v):
        if v not in ['monthly', 'yearly']:
            raise ValueError('Billing cycle must be either monthly or yearly')
        return v

class SubscriptionUpdate(BaseModel):
    plan_id: Optional[uuid.UUID] = None
    billing_cycle: Optional[str] = None
    cancel_at_period_end: Optional[bool] = None
    
    @field_validator('billing_cycle')
    @classmethod
    def validate_billing_cycle(cls, v):
        if v is not None and v not in ['monthly', 'yearly']:
            raise ValueError('Billing cycle must be either monthly or yearly')
        return v

class PaymentMethodCreate(BaseModel):
    type: str = "card"
    last_four: str
    brand: str
    exp_month: int
    exp_year: int
    is_default: bool = False
    
    @field_validator('last_four')
    @classmethod
    def validate_last_four(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError('Last four must be exactly 4 digits')
        return v
    
    @field_validator('exp_month')
    @classmethod
    def validate_exp_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError('Expiration month must be between 1 and 12')
        return v
    
    @field_validator('exp_year')
    @classmethod
    def validate_exp_year(cls, v):
        current_year = datetime.now().year
        if v < current_year or v > current_year + 20:
            raise ValueError('Expiration year must be valid')
        return v

class PaymentMethodResponse(BaseModel):
    id: uuid.UUID
    type: str
    last_four: str
    brand: str
    exp_month: int
    exp_year: int
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceResponse(BaseModel):
    id: uuid.UUID
    amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    currency: str
    status: str
    due_date: datetime
    paid_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class UsageMetricResponse(BaseModel):
    metric_name: str
    metric_value: int
    period_start: datetime
    period_end: datetime
    
    class Config:
        from_attributes = True

class SubscriptionSummary(BaseModel):
    subscription: SubscriptionResponse
    usage_metrics: List[UsageMetricResponse]
    recent_invoices: List[InvoiceResponse]
    payment_methods: List[PaymentMethodResponse]
