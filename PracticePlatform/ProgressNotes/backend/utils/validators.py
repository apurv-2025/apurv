# backend/utils/validators.py
import re
from typing import Optional
from datetime import datetime, date

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's 10 or 11 digits (with or without country code)
    return len(digits_only) in [10, 11]

def validate_medical_record_number(mrn: str) -> bool:
    """Validate medical record number format."""
    # MRN should be alphanumeric and at least 6 characters
    pattern = r'^[A-Za-z0-9]{6,}$'
    return re.match(pattern, mrn) is not None

def validate_date_of_birth(dob: date) -> bool:
    """Validate date of birth (must be in the past and reasonable)."""
    today = date.today()
    if dob >= today:
        return False

    # Check if age is reasonable (between 0 and 150 years)
    age = today.year - dob.year
    if age < 0 or age > 150:
        return False

    return True

def validate_session_date(session_date: datetime) -> bool:
    """Validate session date (should not be too far in the future)."""
    now = datetime.now()
    # Allow sessions up to 1 week in the future
    max_future = now.replace(day=now.day + 7) if now.day <= 24 else now.replace(month=now.month + 1, day=now.day - 24)
    return session_date <= max_future
