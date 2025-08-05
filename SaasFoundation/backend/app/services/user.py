import os
import secrets
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from typing import Dict, Any

from app.models.models import User, Organization, OrganizationMember, Subscription, Invoice, UsageMetric, VerificationToken
from app.core.security import get_password_hash, verify_password
from app.services.organization import organization_service
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, SuccessResponse
from app.utils.database_utils import get_user_by_email, hash_password
from app.services.email import email_service
from app.utils.datetime_utils import utcnow
from datetime import timedelta

logger = logging.getLogger(__name__)

class UserService:
   # Forgot Password
    def forgot_password(
        self,
        request: ForgotPasswordRequest,
        db: Session
    ):
        """Handle forgot password request"""
        try:
            email = request.email.lower()
            logger.info(f"Password reset requested for email: {email}")
            
            # Find user by email
            user = get_user_by_email(db, email)
            
            # Always return success to prevent email enumeration attacks
            if user and user.is_active:
                # Generate reset token
                verification_token = secrets.token_urlsafe(32)
                token_record = VerificationToken(
                    user_id=user.id,
                    token=verification_token,
                    expires_at=utcnow() + timedelta(hours=24)
                )
                db.add(token_record)
                db.commit()
                logger.info(f"Reset token generated for user {user.id}")
                
                # Send reset email in background
                reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={verification_token}"
                
                # Send verification email
                email_service.send_password_reset_email(email, reset_url)

                logger.info(f"Password Reset email send for user {user.email}")
                
            else:
                logger.info(f"Password reset requested for non-existent email: {email}")
            
            return SuccessResponse(
                message="If an account with that email exists, a reset link has been sent."
            )
            
        except Exception as e:
            logger.error(f"Forgot password error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request"
            )

    # Reset Password
    def reset_password(
        self,
        request: ResetPasswordRequest,
        db: Session
    ):
        """Handle password reset with token"""
        try:
            logger.info("Password reset attempt with token")
            
            # Find user with valid token

            token_record = db.query(VerificationToken).filter(
                VerificationToken.token == request.token,
                VerificationToken.expires_at > utcnow()
            ).first()
        
            print(token_record)

            if not token_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )
        
            user = db.query(User).filter(User.id == token_record.user_id).first()

            if not user:
                logger.warning("Invalid or expired reset token used")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset token"
                )
            
            # Update password
            user.password_hash = hash_password(request.password)
            user.updated_at = utcnow()

            db.delete(token_record)
            db.commit()

            logger.info(f"Password reset successful for user {user.id}")
            
            return SuccessResponse(message="Password reset successful")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Reset password error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while resetting your password"
            )

    def get_profile(self, user: User) -> Dict[str, Any]:
        """Get user profile"""
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }

    def update_profile(self, user: User, profile_data: Dict[str, Any], db: Session) -> User:
        """Update user profile"""
        if 'first_name' in profile_data:
            user.first_name = profile_data['first_name']
        if 'last_name' in profile_data:
            user.last_name = profile_data['last_name']
        if 'email' in profile_data and profile_data['email'] != user.email:
            # Check if email is already taken
            existing_user = db.query(User).filter(
                User.email == profile_data['email'],
                User.id != user.id
            ).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = profile_data['email']
            user.is_verified = False  # Re-verify new email
        
        user.updated_at = utcnow()
        db.commit()
        db.refresh(user)
        
        return user

    def change_password(self, user: User, password_data: Dict[str, Any], db: Session):
        """Change user password"""
        current_password = password_data.get('currentPassword')
        new_password = password_data.get('newPassword')
        
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Validate new password
        if len(new_password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        user.password_hash = get_password_hash(new_password)
        user.updated_at = utcnow()
        db.commit()
        
        return {"message": "Password changed successfully"}

    def get_preferences(self, user: User) -> Dict[str, Any]:
        """Get user preferences"""
        # In a real app, these would be stored in the database
        return {
            "email_notifications": True,
            "marketing_emails": False,
            "security_alerts": True,
            "product_updates": True,
            "billing_notifications": True,
            "theme": "light",
            "language": "en",
            "timezone": "UTC"
        }

    def update_preferences(self, user: User, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user preferences"""
        # In a real app, save these to the database
        return {"message": "Preferences updated successfully"}

    def export_user_data(self, user: User, db: Session) -> Dict[str, Any]:
        """Export user data"""
        organization, _ = organization_service.get_user_organization(user.id, db)
        
        # Get user subscriptions
        subscriptions = []
        invoices = []
        usage_metrics = []
        
        if organization:
            subscriptions = db.query(Subscription).filter(Subscription.organization_id == organization.id).all()
            invoices = db.query(Invoice).filter(Invoice.organization_id == organization.id).all()
            usage_metrics = db.query(UsageMetric).filter(UsageMetric.organization_id == organization.id).all()
        
        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
            },
            "organization": {
                "id": str(organization.id) if organization else None,
                "name": organization.name if organization else None,
                "slug": organization.slug if organization else None,
            } if organization else None,
            "subscriptions": [
                {
                    "id": str(sub.id),
                    "status": sub.status,
                    "billing_cycle": sub.billing_cycle,
                    "created_at": sub.created_at.isoformat(),
                } for sub in subscriptions
            ],
            "invoices": [
                {
                    "id": str(inv.id),
                    "amount": float(inv.amount),
                    "status": inv.status,
                    "created_at": inv.created_at.isoformat(),
                } for inv in invoices
            ],
            "usage_metrics": [
                {
                    "metric_name": metric.metric_name,
                    "metric_value": metric.metric_value,
                    "period_start": metric.period_start.isoformat(),
                    "period_end": metric.period_end.isoformat(),
                } for metric in usage_metrics
            ]
        }

    def delete_account(self, user: User, db: Session):
        """Delete user account and all associated data"""
        organization, role = organization_service.get_user_organization(user.id, db)
        
        if organization and role == "owner":
            # If user is the only owner, cancel active subscriptions before deletion
            active_subscriptions = db.query(Subscription).filter(
                Subscription.organization_id == organization.id,
                Subscription.status == "active"
            ).all()
            
            for subscription in active_subscriptions:
                subscription.status = "cancelled"
                subscription.updated_at = utcnow()
            
            # Check if there are other owners
            other_owners = db.query(OrganizationMember).filter(
                OrganizationMember.organization_id == organization.id,
                OrganizationMember.role == "owner",
                OrganizationMember.user_id != user.id,
                OrganizationMember.status == "active"
            ).count()
            
            if other_owners == 0:
                # User is the sole owner, delete the organization
                db.delete(organization)
        
        # Delete user (cascade will handle related records)
        db.delete(user)
        db.commit()
        
        return {"message": "Account deleted successfully"}
    

    def verify_reset_token(self, token: str,db: Session):
        """Verify Token"""
        token_record = db.query(VerificationToken).filter(
            VerificationToken.token == token,
            VerificationToken.expires_at > utcnow()
        ).first()
        
        print(token_record)

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        user = db.query(User).filter(User.id == token_record.user_id).first()
        user.is_verified = True
        
        db.delete(token_record)
        db.commit()

        return {"message": "Token verified successfully"}

# Singleton instance
user_service = UserService()
