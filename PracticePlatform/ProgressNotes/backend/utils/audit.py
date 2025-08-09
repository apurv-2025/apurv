# backend/utils/audit.py
from typing import Dict, Any, Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from models import AuditLog

class AuditLogger:
    """Enhanced audit logging utility."""

    @staticmethod
    def log_user_action(
        db: Session,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """Log a user action with detailed context."""

        # Sanitize sensitive data
        if old_values:
            old_values = AuditLogger._sanitize_data(old_values)
        if new_values:
            new_values = AuditLogger._sanitize_data(new_values)

        # Add additional context if provided
        if additional_context:
            if new_values:
                new_values.update(additional_context)
            else:
                new_values = additional_context

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )

        db.add(audit_log)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            # Log the error but don't fail the main operation
            print(f"Failed to log audit entry: {e}")

    @staticmethod
    def _sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive fields from audit data."""
        sensitive_fields = [
            'password', 'password_hash', 'secret_key', 'token',
            'access_token', 'refresh_token', 'api_key'
        ]

        sanitized = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = AuditLogger._sanitize_data(value)
            else:
                sanitized[key] = value

        return sanitized

