# File: app/dao/audit_dao.py
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.dao.base_dao import BaseDAO
from app.models.models import AuthorizationAudit
from datetime import datetime


class AuthorizationAuditDAO(BaseDAO[AuthorizationAudit]):
    def __init__(self):
        super().__init__(AuthorizationAudit)

    def create_audit_entry(
        self,
        db: Session,
        *,
        request_id: str,
        action: str,
        actor: Optional[str] = None,
        notes: Optional[str] = None,
        previous_status: Optional[str] = None,
        new_status: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuthorizationAudit:
        """Create a new audit entry"""
        audit_data = {
            "request_id": request_id,
            "action": action,
            "actor": actor,
            "notes": notes,
            "previous_status": previous_status,
            "new_status": new_status,
            "metadata": metadata
        }
        return self.create(db, obj_in=audit_data)

    def get_by_request_id(
        self, 
        db: Session, 
        request_id: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuthorizationAudit]:
        """Get all audit entries for a request"""
        return db.query(AuthorizationAudit).filter(
            AuthorizationAudit.request_id == request_id
        ).order_by(desc(AuthorizationAudit.created_at)).offset(skip).limit(limit).all()

    def get_by_action(
        self, 
        db: Session, 
        action: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuthorizationAudit]:
        """Get all audit entries for a specific action"""
        return db.query(AuthorizationAudit).filter(
            AuthorizationAudit.action == action
        ).order_by(desc(AuthorizationAudit.created_at)).offset(skip).limit(limit).all()

    def get_by_actor(
        self, 
        db: Session, 
        actor: str,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuthorizationAudit]:
        """Get all audit entries for a specific actor"""
        return db.query(AuthorizationAudit).filter(
            AuthorizationAudit.actor == actor
        ).order_by(desc(AuthorizationAudit.created_at)).offset(skip).limit(limit).all()

    def get_recent_activity(
        self, 
        db: Session,
        *,
        hours: int = 24,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuthorizationAudit]:
        """Get recent audit activity within specified hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return db.query(AuthorizationAudit).filter(
            AuthorizationAudit.created_at >= cutoff_time
        ).order_by(desc(AuthorizationAudit.created_at)).offset(skip).limit(limit).all()


