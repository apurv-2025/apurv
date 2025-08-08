import re
from typing import List, Optional
from pydantic import validator
from datetime import date, datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Simple phone validation - can be enhanced based on requirements
    pattern = r'^\+?[\d\s\-\(\)]+$'
    return re.match(pattern, phone) is not None


def validate_priority(priority: str) -> bool:
    """Validate task priority"""
    valid_priorities = ["none", "low", "medium", "high", "urgent"]
    return priority.lower() in valid_priorities


def validate_status(status: str) -> bool:
    """Validate task status"""
    valid_statuses = ["todo", "in_progress", "completed", "cancelled"]
    return status.lower() in valid_statuses


def validate_due_date(due_date: Optional[date]) -> bool:
    """Validate due date is not in the past"""
    if due_date is None:
        return True
    return due_date >= date.today()
