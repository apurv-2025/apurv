from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.user import UserResponse
from app.services.user import user_service
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(
    forgotPasswordRequest: ForgotPasswordRequest, 
    db: Session = Depends(get_db)
    ):
    """Forgot Password"""
    return user_service.forgot_password(forgotPasswordRequest, db)

@router.post("/reset-password")
async def reset_password(
    resetPasswordRequest: ResetPasswordRequest, 
    db: Session = Depends(get_db)):
    """Reset Password"""
    return user_service.reset_password(resetPasswordRequest, db)

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    updated_user = user_service.update_profile(current_user, profile_data, db)
    
    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        is_verified=updated_user.is_verified,
        created_at=updated_user.created_at
    )

@router.put("/change-password")
async def change_password(
    password_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    return user_service.change_password(current_user, password_data, db)

@router.get("/preferences")
async def get_preferences(current_user: User = Depends(get_current_user)):
    """Get user preferences"""
    return user_service.get_preferences(current_user)

@router.put("/preferences")
async def update_preferences(
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update user preferences"""
    return user_service.update_preferences(current_user, preferences)

@router.get("/export")
async def export_user_data(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Export user data"""
    export_data = user_service.export_user_data(current_user, db)
    
    return JSONResponse(
        content=export_data,
        headers={"Content-Disposition": "attachment; filename=user_data.json"}
    )

@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account and all associated data"""
    return user_service.delete_account(current_user, db)
