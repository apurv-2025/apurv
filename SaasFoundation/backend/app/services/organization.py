import re
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import Organization, OrganizationMember, PricingPlan, Subscription, User

class OrganizationService:
    def create_default_organization(self, user_id: str, db: Session) -> Organization:
        """Create a default organization for new users"""
        # Create organization slug from user email
        user = db.query(User).filter(User.id == user_id).first()
        base_slug = re.sub(r'[^a-zA-Z0-9-]', '-', user.email.split('@')[0].lower())
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while db.query(Organization).filter(Organization.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        organization = Organization(
            name=f"{user.first_name}'s Organization",
            slug=slug,
            owner_id=user_id
        )
        db.add(organization)
        db.commit()
        db.refresh(organization)
        
        # Add user as owner member
        member = OrganizationMember(
            organization_id=organization.id,
            user_id=user_id,
            role="owner",
            status="active"
        )
        db.add(member)
        db.commit()
        
        return organization

    def create_free_subscription(self, organization_id: str, db: Session) -> Subscription:
        """Create a free subscription for new organizations"""
        free_plan = db.query(PricingPlan).filter(PricingPlan.name == "free").first()
        if free_plan:
            subscription = Subscription(
                organization_id=organization_id,
                plan_id=free_plan.id,
                status="active",
                billing_cycle="monthly",
                current_period_start=datetime.utcnow(),
                current_period_end=datetime.utcnow() + timedelta(days=30)
            )
            db.add(subscription)
            db.commit()
            return subscription
        return None

    def get_user_organization(self, user_id: str, db: Session) -> tuple:
        """Get user's current organization and role"""
        membership = db.query(OrganizationMember).filter(
            OrganizationMember.user_id == user_id,
            OrganizationMember.status == "active"
        ).first()
        
        if membership:
            return membership.organization, membership.role
        return None, None

# Singleton instance
organization_service = OrganizationService()
