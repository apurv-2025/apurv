import os
import logging
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, BackgroundTasks

from app.models.models import User, VerificationToken
from app.schemas.auth import (
    UserCreate, UserLogin, ForgotPasswordRequest, 
    ResetPasswordRequest, TokenVerificationRequest,
    SuccessResponse, TokenValidationResponse
)
from app.core.security import verify_password, get_password_hash, create_access_token
from app.services.email import email_service
from app.services.organization import organization_service
from app.utils.datetime_utils import utcnow
from app.core.database import get_db

logger = logging.getLogger(__name__)

#
# Auth Service Class Implementation
#

class AuthService:
    def create_user(self, user_data: UserCreate, db: Session) -> dict:
        """Register a new user"""
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create verification token
        verification_token = secrets.token_urlsafe(32)
        token_record = VerificationToken(
            user_id=user.id,
            token=verification_token,
            expires_at=utcnow() + timedelta(hours=24)
        )
        db.add(token_record)
        db.commit()
        
        # Create default organization and free subscription
        organization = organization_service.create_default_organization(user.id, db)
        organization_service.create_free_subscription(organization.id, db)
        
        db.commit()
        
        # Send verification email
        email_service.send_verification_email(user.email, verification_token)
        
        return {
            "message": "User registered successfully. Please check your email to verify your account.",
            "user_id": str(user.id)
        }

    def authenticate_user(self, user_data: UserLogin, db: Session) -> dict:
        """Login user"""
        user = db.query(User).filter(User.email == user_data.email).first()
        
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    def logout_user(self, current_user: User, db: Session) -> dict:
        """Logout current user"""
        try:
            # Update user's last logout timestamp if you have this field
            # current_user.last_logout = utcnow()
            # db.commit()
            
            # Log the logout event (optional)
            print("User {current_user.email} logged out at {utcnow()}")
            
            return {
                "message": "Successfully logged out",
                "status": "success",
                "timestamp": utcnow().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout failed: {str(e)}"
            )


    def verify_email(self, token: str, db: Session) -> dict:
        """Verify user email"""
        print(token)
        print(utcnow())
        
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
        
        return {"message": "Email verified successfully"}

    def resend_verification(self, current_user: User, db: Session) -> dict:
        """Resend email verification"""
        if current_user.is_verified:
            raise HTTPException(status_code=400, detail="Email is already verified")
        
        # Delete existing tokens
        db.query(VerificationToken).filter(VerificationToken.user_id == current_user.id).delete()
        
        # Create new token
        verification_token = secrets.token_urlsafe(32)
        token_record = VerificationToken(
            user_id=current_user.id,
            token=verification_token,
            expires_at=utcnow() + timedelta(hours=24)   
        )
        db.add(token_record)
        db.commit()
        
        # Send verification email
        email_service.send_verification_email(current_user.email, verification_token)
        
        return {"message": "Verification email sent successfully"}


# Singleton instance
auth_service = AuthService()
