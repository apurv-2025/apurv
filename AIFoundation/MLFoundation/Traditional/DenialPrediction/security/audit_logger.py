"""
Audit Logger for Healthcare Compliance
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import redis
from sqlalchemy import create_engine, Column, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Database model for audit logs
Base = declarative_base()

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    ip_address = Column(String)
    user_agent = Column(String)
    request_data = Column(Text)
    response_status = Column(String)
    session_id = Column(String)
    risk_score = Column(String)
    phi_accessed = Column(Boolean, default=False)

@dataclass
class SecurityContext:
    """Security context for requests"""
    user_id: str
    roles: List[str]
    permissions: List[str]
    access_level: str
    session_id: str
    ip_address: str
    user_agent: str
    timestamp: datetime

class AuditLogger:
    """Comprehensive audit logging system"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Initialize database connection
        self.engine = create_engine("postgresql://user:password@localhost/healthcare_denials")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create audit log table
        Base.metadata.create_all(bind=self.engine)
    
    async def log_access(self, security_context: SecurityContext, 
                        action: str, resource: str, 
                        request_data: Dict = None,
                        response_status: str = "success",
                        phi_accessed: bool = False):
        """Log access to resources"""
        try:
            # Calculate risk score
            risk_score = self._calculate_risk_score(security_context, action, resource, phi_accessed)
            
            # Create audit entry
            audit_entry = {
                'id': f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                'timestamp': security_context.timestamp.isoformat(),
                'user_id': security_context.user_id,
                'action': action,
                'resource': resource,
                'ip_address': security_context.ip_address,
                'user_agent': security_context.user_agent,
                'request_data': json.dumps(request_data) if request_data else None,
                'response_status': response_status,
                'session_id': security_context.session_id,
                'risk_score': risk_score,
                'phi_accessed': phi_accessed,
                'roles': ','.join(security_context.roles),
                'permissions': ','.join(security_context.permissions)
            }
            
            # Store in database
            await self._store_in_database(audit_entry)
            
            # Store in Redis for real-time monitoring
            await self._store_in_redis(audit_entry)
            
            # Log high-risk activities
            if risk_score in ['high', 'critical']:
                logger.warning(f"High-risk activity detected: {action} on {resource} by {security_context.user_id}")
            
            # Log PHI access
            if phi_accessed:
                logger.info(f"PHI accessed: {action} on {resource} by {security_context.user_id}")
            
        except Exception as e:
            logger.error(f"Error logging audit entry: {e}")
    
    def _calculate_risk_score(self, security_context: SecurityContext,
                            action: str, resource: str, phi_accessed: bool) -> str:
        """Calculate risk score for the activity"""
        risk_score = 0
        
        # Base risk factors
        if phi_accessed:
            risk_score += 50
        
        if action in ['delete', 'export', 'download']:
            risk_score += 30
        
        if resource.startswith('patient') or 'phi' in resource.lower():
            risk_score += 20
        
        # Time-based risk (off-hours access)
        hour = security_context.timestamp.hour
        if hour < 6 or hour > 22:
            risk_score += 15
        
        # IP-based risk
        if self._is_suspicious_ip(security_context.ip_address):
            risk_score += 25
        
        # User role risk
        if 'admin' in security_context.roles:
            risk_score += 10
        elif 'readonly' in security_context.roles:
            risk_score -= 10
        
        # Determine risk level
        if risk_score >= 80:
            return 'critical'
        elif risk_score >= 60:
            return 'high'
        elif risk_score >= 40:
            return 'medium'
        else:
            return 'low'
    
    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP address is suspicious"""
        # Simplified check - in production, would use threat intelligence
        suspicious_patterns = ['192.168.', '10.0.', '172.16.']
        return any(pattern in ip_address for pattern in suspicious_patterns)
    
    async def _store_in_database(self, audit_entry: Dict):
        """Store audit entry in database"""
        try:
            db = self.SessionLocal()
            try:
                log_entry = AuditLog(**audit_entry)
                db.add(log_entry)
                db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error storing audit entry in database: {e}")
    
    async def _store_in_redis(self, audit_entry: Dict):
        """Store audit entry in Redis for real-time monitoring"""
        try:
            # Store recent audit entries
            audit_key = f"audit:recent:{datetime.now().strftime('%Y%m%d:%H')}"
            self.redis_client.lpush(audit_key, json.dumps(audit_entry))
            self.redis_client.expire(audit_key, 86400)  # 24 hours
            
            # Store user activity
            user_key = f"audit:user:{audit_entry['user_id']}:{datetime.now().strftime('%Y%m%d')}"
            self.redis_client.lpush(user_key, json.dumps(audit_entry))
            self.redis_client.expire(user_key, 604800)  # 7 days
            
            # Store high-risk activities
            if audit_entry['risk_score'] in ['high', 'critical']:
                risk_key = f"audit:risk:{datetime.now().strftime('%Y%m%d')}"
                self.redis_client.lpush(risk_key, json.dumps(audit_entry))
                self.redis_client.expire(risk_key, 2592000)  # 30 days
                
        except Exception as e:
            logger.error(f"Error storing audit entry in Redis: {e}")
    
    async def get_user_activity(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get user activity for the specified number of days"""
        try:
            activities = []
            
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                user_key = f"audit:user:{user_id}:{date.strftime('%Y%m%d')}"
                
                data = self.redis_client.lrange(user_key, 0, -1)
                for entry in data:
                    activities.append(json.loads(entry))
            
            return activities
            
        except Exception as e:
            logger.error(f"Error retrieving user activity: {e}")
            return []
    
    async def get_high_risk_activities(self, days: int = 1) -> List[Dict]:
        """Get high-risk activities for the specified number of days"""
        try:
            activities = []
            
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                risk_key = f"audit:risk:{date.strftime('%Y%m%d')}"
                
                data = self.redis_client.lrange(risk_key, 0, -1)
                for entry in data:
                    activities.append(json.loads(entry))
            
            return activities
            
        except Exception as e:
            logger.error(f"Error retrieving high-risk activities: {e}")
            return []
    
    async def get_phi_access_logs(self, days: int = 7) -> List[Dict]:
        """Get PHI access logs from database"""
        try:
            db = self.SessionLocal()
            try:
                cutoff_date = datetime.now() - timedelta(days=days)
                
                logs = db.query(AuditLog).filter(
                    AuditLog.phi_accessed == True,
                    AuditLog.timestamp >= cutoff_date
                ).order_by(AuditLog.timestamp.desc()).all()
                
                return [
                    {
                        'id': log.id,
                        'timestamp': log.timestamp.isoformat(),
                        'user_id': log.user_id,
                        'action': log.action,
                        'resource': log.resource,
                        'ip_address': log.ip_address,
                        'risk_score': log.risk_score
                    }
                    for log in logs
                ]
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error retrieving PHI access logs: {e}")
            return []
    
    async def generate_audit_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        try:
            db = self.SessionLocal()
            try:
                logs = db.query(AuditLog).filter(
                    AuditLog.timestamp >= start_date,
                    AuditLog.timestamp <= end_date
                ).all()
                
                # Calculate statistics
                total_activities = len(logs)
                unique_users = len(set(log.user_id for log in logs))
                phi_access_count = len([log for log in logs if log.phi_accessed])
                high_risk_count = len([log for log in logs if log.risk_score in ['high', 'critical']])
                
                # Activity breakdown
                actions = {}
                for log in logs:
                    actions[log.action] = actions.get(log.action, 0) + 1
                
                # Risk distribution
                risk_distribution = {}
                for log in logs:
                    risk_distribution[log.risk_score] = risk_distribution.get(log.risk_score, 0) + 1
                
                return {
                    'period': {
                        'start': start_date.isoformat(),
                        'end': end_date.isoformat()
                    },
                    'summary': {
                        'total_activities': total_activities,
                        'unique_users': unique_users,
                        'phi_access_count': phi_access_count,
                        'high_risk_count': high_risk_count
                    },
                    'activity_breakdown': actions,
                    'risk_distribution': risk_distribution,
                    'recent_activities': [
                        {
                            'timestamp': log.timestamp.isoformat(),
                            'user_id': log.user_id,
                            'action': log.action,
                            'resource': log.resource,
                            'risk_score': log.risk_score
                        }
                        for log in logs[-10:]  # Last 10 activities
                    ]
                }
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error generating audit report: {e}")
            return {} 