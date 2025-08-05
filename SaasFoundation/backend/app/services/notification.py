# service.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from typing import Optional, List, Tuple
import math
from datetime import datetime, timedelta

from . import models, schemas

class NotificationService:
    """Service layer for notification operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self, 
        user_id: int, 
        title: str, 
        message: str, 
        type: str = "info", 
        category: str = "system"
    ) -> models.Notification:
        """Create a new notification"""
        notification = models.Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            category=category
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_user_notifications(
        self,
        user_id: int,
        filters: schemas.NotificationFilters,
        page: int = 1,
        page_size: int = 20,
        order_by: str = "created_at",
        order_direction: str = "desc"
    ) -> Tuple[List[models.Notification], int, int]:
        """Get user notifications with filtering and pagination"""
        
        # Base query
        query = self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        )
        
        # Apply filters
        query = self._apply_filters(query, filters)
        
        # Get total count
        total = query.count()
        
        # Apply ordering
        order_column = getattr(models.Notification, order_by)
        if order_direction == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
        
        # Apply pagination
        offset = (page - 1) * page_size
        notifications = query.offset(offset).limit(page_size).all()
        
        # Get unread count
        unread_count = self.get_unread_count(user_id)
        
        return notifications, total, unread_count
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for user"""
        return self.db.query(models.Notification).filter(
            and_(
                models.Notification.user_id == user_id,
                models.Notification.read == False
            )
        ).count()
    
    def mark_as_read(self, user_id: int, notification_id: int) -> bool:
        """Mark a notification as read"""
        notification = self.db.query(models.Notification).filter(
            and_(
                models.Notification.id == notification_id,
                models.Notification.user_id == user_id
            )
        ).first()
        
        if not notification:
            return False
        
        notification.read = True
        self.db.commit()
        return True
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all user notifications as read"""
        affected_count = self.db.query(models.Notification).filter(
            and_(
                models.Notification.user_id == user_id,
                models.Notification.read == False
            )
        ).update({"read": True})
        
        self.db.commit()
        return affected_count
    
    def mark_multiple_as_read(self, user_id: int, notification_ids: List[int]) -> int:
        """Mark multiple notifications as read"""
        affected_count = self.db.query(models.Notification).filter(
            and_(
                models.Notification.id.in_(notification_ids),
                models.Notification.user_id == user_id
            )
        ).update({"read": True})
        
        self.db.commit()
        return affected_count
    
    def delete_notification(self, user_id: int, notification_id: int) -> bool:
        """Delete a notification"""
        notification = self.db.query(models.Notification).filter(
            and_(
                models.Notification.id == notification_id,
                models.Notification.user_id == user_id
            )
        ).first()
        
        if not notification:
            return False
        
        self.db.delete(notification)
        self.db.commit()
        return True
    
    def delete_multiple_notifications(self, user_id: int, notification_ids: List[int]) -> int:
        """Delete multiple notifications"""
        affected_count = self.db.query(models.Notification).filter(
            and_(
                models.Notification.id.in_(notification_ids),
                models.Notification.user_id == user_id
            )
        ).delete(synchronize_session=False)
        
        self.db.commit()
        return affected_count
    
    def get_notification_stats(self, user_id: int) -> dict:
        """Get notification statistics for user"""
        base_query = self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        )
        
        stats = {
            "total": base_query.count(),
            "unread": base_query.filter(models.Notification.read == False).count(),
            "by_type": {},
            "by_category": {},
            "recent_activity": {}
        }
        
        # Stats by type
        type_stats = self.db.query(
            models.Notification.type,
            func.count(models.Notification.id).label('count')
        ).filter(
            models.Notification.user_id == user_id
        ).group_by(models.Notification.type).all()
        
        stats["by_type"] = {stat.type: stat.count for stat in type_stats}
        
        # Stats by category
        category_stats = self.db.query(
            models.Notification.category,
            func.count(models.Notification.id).label('count')
        ).filter(
            models.Notification.user_id == user_id
        ).group_by(models.Notification.category).all()
        
        stats["by_category"] = {stat.category: stat.count for stat in category_stats}
        
        # Recent activity (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_count = base_query.filter(
            models.Notification.created_at >= seven_days_ago
        ).count()
        stats["recent_activity"]["last_7_days"] = recent_count
        
        return stats
    
    def _apply_filters(self, query, filters: schemas.NotificationFilters):
        """Apply filters to notification query"""
        if filters.category:
            query = query.filter(models.Notification.category == filters.category)
        
        if filters.read is not None:
            query = query.filter(models.Notification.read == filters.read)
        
        if filters.type:
            query = query.filter(models.Notification.type == filters.type)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    models.Notification.title.ilike(search_term),
                    models.Notification.message.ilike(search_term)
                )
            )
        
        return query

class NotificationPreferenceService:
    """Service layer for notification preferences"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_preferences(self, user_id: int) -> models.NotificationPreference:
        """Get user notification preferences"""
        preferences = self.db.query(models.NotificationPreference).filter(
            models.NotificationPreference.user_id == user_id
        ).first()
        
        if not preferences:
            # Create default preferences
            preferences = self.create_default_preferences(user_id)
        
        return preferences
    
    def create_default_preferences(self, user_id: int) -> models.NotificationPreference:
        """Create default notification preferences for user"""
        preferences = models.NotificationPreference(
            user_id=user_id,
            email=True,
            push=True,
            sms=False,
            weekly_digest=True
        )
        self.db.add(preferences)
        self.db.commit()
        self.db.refresh(preferences)
        return preferences
    
    def update_preferences(
        self, 
        user_id: int, 
        preferences_update: schemas.NotificationPreferenceUpdate
    ) -> models.NotificationPreference:
        """Update user notification preferences"""
        preferences = self.get_user_preferences(user_id)
        
        # Update only provided fields
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(preferences, field, value)
        
        self.db.commit()
        self.db.refresh(preferences)
        return preferences

class NotificationTemplateService:
    """Service layer for notification templates"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_template(self, name: str) -> Optional[models.NotificationTemplate]:
        """Get notification template by name"""
        return self.db.query(models.NotificationTemplate).filter(
            and_(
                models.NotificationTemplate.name == name,
                models.NotificationTemplate.is_active == True
            )
        ).first()
    
    def create_notification_from_template(
        self, 
        user_id: int, 
        template_name: str, 
        variables: dict = None
    ) -> Optional[models.Notification]:
        """Create notification from template with variable substitution"""
        template = self.get_template(template_name)
        if not template:
            return None
        
        variables = variables or {}
        
        # Simple variable substitution
        title = template.title_template
        message = template.message_template
        
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            title = title.replace(placeholder, str(value))
            message = message.replace(placeholder, str(value))
        
        # Create notification
        notification = models.Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=template.type,
            category=template.category
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def get_all_templates(self, active_only: bool = True) -> List[models.NotificationTemplate]:
        """Get all notification templates"""
        query = self.db.query(models.NotificationTemplate)
        if active_only:
            query = query.filter(models.NotificationTemplate.is_active == True)
        return query.all()