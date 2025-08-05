"""
Auth.Py 
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, EmailVerify, ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user import UserResponse
from app.services.auth import auth_service
from app.dependencies import get_current_user
from app.models.models import User
from pydantic import ValidationError


router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return auth_service.create_user(user_data, db)


@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        print(f"1. Input validation passed: {user_data}")
        
        result = auth_service.authenticate_user(user_data, db)
        print(f"2. Auth service result: {result}")
        
        # Test UserResponse validation separately
        user_response = UserResponse.model_validate(result["user"])
        print(f"3. User validation passed: {user_response}")
        
        # Test TokenResponse validation
        token_response = TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            user=user_response
        )
        print(f"4. Token response created: {token_response}")
        
        return token_response
        
    except ValidationError as e:
        print(f"Validation Error Details: {e}")
        return {"error": "Validation failed", "details": str(e)}
    except KeyError as e:
        print(f"Missing key in result: {e}")
        return {"error": "Missing key", "details": str(e)}


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout current user"""
    try:
        # Call the auth service logout method
        result = auth_service.logout_user(current_user, db)
        return {
            "message": "Successfully logged out",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Logout failed: {str(e)}"
        )


@router.post("/verify")
async def verify_email(emailVerify: EmailVerify, db: Session = Depends(get_db)):
    """Verify user email"""
    return auth_service.verify_email(emailVerify.token, db)

@router.post("/resend-verification")
async def resend_verification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resend email verification"""
    return auth_service.resend_verification(current_user, db)