from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.models import (
    Subscription, PricingPlan, PaymentMethod, Invoice, UsageMetric
)
from app.schemas.subscription import (
    SubscriptionCreate, SubscriptionUpdate, PaymentMethodCreate
)

class SubscriptionService:
    def get_current_subscription(self, organization_id: str, db: Session):
        """Get organization's current active subscription with details"""
        subscription = db.query(Subscription).filter(
            Subscription.organization_id == organization_id,
            Subscription.status == "active"
        ).first()
        
        if not subscription:
            raise HTTPException(status_code=404, detail="No active subscription found")
        
        # Get usage metrics for current period
        usage_metrics = db.query(UsageMetric).filter(
            UsageMetric.organization_id == organization_id,
            UsageMetric.period_start >= subscription.current_period_start,
            UsageMetric.period_end <= subscription.current_period_end
        ).all()
        
        # Get recent invoices
        recent_invoices = db.query(Invoice).filter(
            Invoice.organization_id == organization_id
        ).order_by(Invoice.created_at.desc()).limit(5).all()
        
        # Get payment methods
        payment_methods = db.query(PaymentMethod).filter(
            PaymentMethod.organization_id == organization_id
        ).order_by(PaymentMethod.is_default.desc(), PaymentMethod.created_at.desc()).all()
        
        return {
            "subscription": subscription,
            "usage_metrics": usage_metrics,
            "recent_invoices": recent_invoices,
            "payment_methods": payment_methods
        }

    def create_subscription(self, organization_id: str, subscription_data: SubscriptionCreate, db: Session):
        """Create or upgrade subscription"""
        # Check if plan exists
        plan = db.query(PricingPlan).filter(PricingPlan.id == subscription_data.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Pricing plan not found")
        
        # Cancel existing subscription
        existing_subscription = db.query(Subscription).filter(
            Subscription.organization_id == organization_id,
            Subscription.status == "active"
        ).first()
        
        if existing_subscription:
            existing_subscription.status = "cancelled"
            existing_subscription.updated_at = datetime.utcnow()
        
        # Calculate period end based on billing cycle
        period_start = datetime.utcnow()
        if subscription_data.billing_cycle == "yearly":
            period_end = period_start + timedelta(days=365)
        else:
            period_end = period_start + timedelta(days=30)
        
        # Create new subscription
        new_subscription = Subscription(
            organization_id=organization_id,
            plan_id=subscription_data.plan_id,
            status="active",
            billing_cycle=subscription_data.billing_cycle,
            current_period_start=period_start,
            current_period_end=period_end
        )
        
        db.add(new_subscription)
        
        # Create invoice for paid plans
        if plan.name != "free":
            amount = plan.price_yearly if subscription_data.billing_cycle == "yearly" else plan.price_monthly
            tax_amount = amount * Decimal("0.1")  # 10% tax
            total_amount = amount + tax_amount
            
            invoice = Invoice(
                organization_id=organization_id,
                subscription_id=new_subscription.id,
                amount=amount,
                tax_amount=tax_amount,
                total_amount=total_amount,
                due_date=datetime.utcnow() + timedelta(days=7),
                status="pending"
            )
            db.add(invoice)
        
        db.commit()
        db.refresh(new_subscription)
        
        return new_subscription

    def update_subscription(self, subscription_id: str, organization_id: str, subscription_data: SubscriptionUpdate, db: Session):
        """Update subscription"""
        subscription = db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.organization_id == organization_id
        ).first()
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        # Update fields
        if subscription_data.plan_id:
            plan = db.query(PricingPlan).filter(PricingPlan.id == subscription_data.plan_id).first()
            if not plan:
                raise HTTPException(status_code=404, detail="Pricing plan not found")
            subscription.plan_id = subscription_data.plan_id
        
        if subscription_data.billing_cycle:
            subscription.billing_cycle = subscription_data.billing_cycle
        
        if subscription_data.cancel_at_period_end is not None:
            subscription.cancel_at_period_end = subscription_data.cancel_at_period_end
        
        subscription.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subscription)
        
        return subscription

    def cancel_subscription(self, subscription_id: str, organization_id: str, db: Session):
        """Cancel subscription"""
        subscription = db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.organization_id == organization_id
        ).first()
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        subscription.cancel_at_period_end = True
        subscription.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Subscription will be cancelled at the end of the current period"}

    def get_pricing_plans(self, db: Session) -> List[PricingPlan]:
        """Get all active pricing plans"""
        return db.query(PricingPlan).filter(PricingPlan.is_active == True).order_by(PricingPlan.sort_order).all()

    def get_pricing_plan(self, plan_id: str, db: Session) -> PricingPlan:
        """Get specific pricing plan"""
        plan = db.query(PricingPlan).filter(PricingPlan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Pricing plan not found")
        return plan

    def add_payment_method(self, organization_id: str, payment_data: PaymentMethodCreate, db: Session):
        """Add new payment method"""
        # If this is set as default, unset other defaults
        if payment_data.is_default:
            db.query(PaymentMethod).filter(
                PaymentMethod.organization_id == organization_id,
                PaymentMethod.is_default == True
            ).update({"is_default": False})
        
        payment_method = PaymentMethod(
            organization_id=organization_id,
            type=payment_data.type,
            last_four=payment_data.last_four,
            brand=payment_data.brand,
            exp_month=payment_data.exp_month,
            exp_year=payment_data.exp_year,
            is_default=payment_data.is_default
        )
        
        db.add(payment_method)
        db.commit()
        db.refresh(payment_method)
        
        return payment_method

    def get_payment_methods(self, organization_id: str, db: Session):
        """Get organization's payment methods"""
        return db.query(PaymentMethod).filter(
            PaymentMethod.organization_id == organization_id
        ).order_by(PaymentMethod.is_default.desc(), PaymentMethod.created_at.desc()).all()

    def delete_payment_method(self, payment_method_id: str, organization_id: str, db: Session):
        """Delete payment method"""
        payment_method = db.query(PaymentMethod).filter(
            PaymentMethod.id == payment_method_id,
            PaymentMethod.organization_id == organization_id
        ).first()
        
        if not payment_method:
            raise HTTPException(status_code=404, detail="Payment method not found")
        
        db.delete(payment_method)
        db.commit()
        
        return {"message": "Payment method deleted successfully"}

    def get_invoices(self, organization_id: str, db: Session, limit: int = 10, offset: int = 0):
        """Get organization's invoices"""
        return db.query(Invoice).filter(
            Invoice.organization_id == organization_id
        ).order_by(Invoice.created_at.desc()).offset(offset).limit(limit).all()

    def get_invoice(self, invoice_id: str, organization_id: str, db: Session):
        """Get specific invoice"""
        invoice = db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.organization_id == organization_id
        ).first()
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        return invoice

    def pay_invoice(self, invoice_id: str, organization_id: str, db: Session):
        """Simulate payment of invoice"""
        invoice = db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.organization_id == organization_id,
            Invoice.status == "pending"
        ).first()
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found or already paid")
        
        # Simulate payment processing
        invoice.status = "paid"
        invoice.paid_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Invoice paid successfully"}

    def record_usage(self, organization_id: str, metric_name: str, value: int, db: Session):
        """Record usage metric"""
        # Get current period (monthly)
        now = datetime.utcnow()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            period_end = period_start.replace(year=period_start.year + 1, month=1) - timedelta(seconds=1)
        else:
            period_end = period_start.replace(month=period_start.month + 1) - timedelta(seconds=1)
        
        # Check if metric exists for this period
        existing_metric = db.query(UsageMetric).filter(
            UsageMetric.organization_id == organization_id,
            UsageMetric.metric_name == metric_name,
            UsageMetric.period_start == period_start
        ).first()
        
        if existing_metric:
            existing_metric.metric_value += value
        else:
            new_metric = UsageMetric(
                organization_id=organization_id,
                metric_name=metric_name,
                metric_value=value,
                period_start=period_start,
                period_end=period_end
            )
            db.add(new_metric)
        
        db.commit()
        
        return {"message": f"Usage recorded: {metric_name} +{value}"}

    def get_usage_metrics(self, organization_id: str, db: Session, period_start: Optional[datetime] = None, period_end: Optional[datetime] = None):
        """Get usage metrics for organization"""
        query = db.query(UsageMetric).filter(UsageMetric.organization_id == organization_id)
        
        if period_start:
            query = query.filter(UsageMetric.period_start >= period_start)
        if period_end:
            query = query.filter(UsageMetric.period_end <= period_end)
        
        return query.order_by(UsageMetric.period_start.desc()).all()

# Singleton instance
subscription_service = SubscriptionService()
