from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import User
from app.core.security import pwd_context

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email address"""
    return db.query(User).filter(User.email == email.lower()).first()


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

