from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from models.database import Base
from typing import Dict, Any, Optional
import json
import hashlib
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    agent_id = Column(Integer)
    action = Column(String)  # create, update, delete, interact, view
    resource_type = Column(String)  # agent, knowledge, user, chat
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    session_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data_hash = Column(String)  # For integrity verification

class AuditService:
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: str,
        details: Dict[str, Any],
        ip_address: str = None,
        user_agent: str = None,
        agent_id: Optional[int] = None
    ):
        """Log an action for audit purposes"""
        
        # Create data hash for integrity
        data_to_hash = json.dumps({
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "timestamp": datetime.utcnow().isoformat()
        }, sort_keys=True)
        
        data_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        audit_log = AuditLog(
            user_id=user_id,
            agent_id=agent_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            data_hash=data_hash
        )
        
        self.db.add(audit_log)
        self.db.commit()
    
    def get_user_activity(self, user_id: int, limit: int = 100):
        """Get recent activity for a user"""
        return self.db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    def get_agent_interactions(self, agent_id: int, limit: int = 100):
        """Get interactions for a specific agent"""
        return self.db.query(AuditLog).filter(
            AuditLog.agent_id == agent_id,
            AuditLog.action == "interact"
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
