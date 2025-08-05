import hashlib
import secrets
import re
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

class SecurityService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY")
        
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password meets security requirements"""
        issues = []
        
        if len(password) < 12:
            issues.append("Password must be at least 12 characters long")
        
        if not re.search(r"[a-z]", password):
            issues.append("Password must contain lowercase letters")
        
        if not re.search(r"[A-Z]", password):
            issues.append("Password must contain uppercase letters")
        
        if not re.search(r"\d", password):
            issues.append("Password must contain numbers")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            issues.append("Password must contain special characters")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "strength": "strong" if len(issues) == 0 else "weak"
        }
    
    def sanitize_input(self, text: str) -> str:
        """Basic input sanitization"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()
    
    def detect_pii(self, text: str) -> Dict[str, Any]:
        """Detect potential PII/PHI in text"""
        patterns = {
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "date_of_birth": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            "medical_record": r'\bMRN?\s*:?\s*\d+\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        detected = {}
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected[pii_type] = len(matches)
        
        return {
            "has_pii": len(detected) > 0,
            "types": detected,
            "risk_level": "high" if len(detected) > 2 else "medium" if len(detected) > 0 else "low"
        }
    
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt
