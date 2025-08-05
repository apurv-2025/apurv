# api.py
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from typing import Optional, List
import math

from app.models.models import User, Notification,NotificationPreference
from app.schemas.notification import (
    NotificationBase, NotificationCreate,
    NotificationFilters,NotificationListResponse,
    NotificationType,NotificationCategory,
    UnreadCountResponse,NotificationResponse,
    SuccessResponse,NotificationMarkRead,
    BulkOperationResponse,NotificationBulkRead,
    NotificationBulkDelete,NotificationPreferenceResponse,
    NotificationUpdate,NotificationPreferenceUpdate
)


from app.core.database import get_db

router = APIRouter()

# Dependency to get current user (you'll need to implement this based on your auth system)
def get_current_user(db: Session = Depends(get_db)) -> User:
    # This is a placeholder - implement based on your authentication system
    # For now, we'll assume user_id=1 for testing
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Helper function to apply filters
def apply_notification_filters(query, filters: NotificationFilters):
    if filters.category:
        query = query.filter(Notification.category == filters.category)
    
    if filters.read is not None:
        query = query.filter(Notification.read == filters.read)
    
    if filters.type:
        query = query.filter(Notification.type == filters.type)
    
    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Notification.title.ilike(search_term),
                Notification.message.ilike(search_term)
            )
        )
    
    return query

@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    category: Optional[NotificationCategory] = None,
    read: Optional[bool] = None,
    search: Optional[str] = None,
    type: Optional[NotificationType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("created_at", pattern="^(created_at|updated_at|title)$"),
    order_direction: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's notifications with filtering and pagination"""
    
    # Create filters object
    filters = NotificationFilters(
        category=category,
        read=read,
        search=search,
        type=type
    )
    
    # Base query for user's notifications
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id
    )
    
    # Apply filters
    query = apply_notification_filters(query, filters)
    
    # Get total count before pagination
    total = query.count()
    
    # Get unread count
    unread_count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.read == False
        )
    ).count()
    
    # Apply ordering
    order_column = getattr(Notification, order_by)
    if order_direction == "desc":
        query = query.order_by(desc(order_column))
    else:
        query = query.order_by(asc(order_column))
    
    # Apply pagination
    offset = (page - 1) * page_size
    notifications = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / page_size)
    
    return NotificationListResponse(
        notifications=notifications,
        total=total,
        unread_count=unread_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.read == False
        )
    ).count()
    
    return UnreadCountResponse(count=count)

@router.post("/", response_model=NotificationResponse)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification (admin/system use)"""
    
    # Check if user exists
    user = db.query(User).filter(User.id == notification.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    return db_notification

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific notification"""
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return notification

@router.patch("/{notification_id}/read", response_model=SuccessResponse)
async def mark_notification_read(
    notification_id: int = Path(..., gt=0),
    read_data: NotificationMarkRead = NotificationMarkRead(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a notification as read/unread"""
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read = read_data.read
    db.commit()
    
    return SuccessResponse(
        success=True,
        message=f"Notification marked as {'read' if read_data.read else 'unread'}"
    )

@router.patch("/read-all", response_model=BulkOperationResponse)
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all user's notifications as read"""
    affected_count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.read == False
        )
    ).update({"read": True})
    
    db.commit()
    
    return BulkOperationResponse(
        success=True,
        affected_count=affected_count,
        message=f"Marked {affected_count} notifications as read"
    )

@router.patch("/bulk/read", response_model=BulkOperationResponse)
async def mark_multiple_notifications_read(
    bulk_data: NotificationBulkRead,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark multiple notifications as read/unread"""
    affected_count = db.query(Notification).filter(
        and_(
            Notification.id.in_(bulk_data.notification_ids),
            Notification.user_id == current_user.id
        )
    ).update({"read": bulk_data.read})
    
    db.commit()
    
    return BulkOperationResponse(
        success=True,
        affected_count=affected_count,
        message=f"Marked {affected_count} notifications as {'read' if bulk_data.read else 'unread'}"
    )

@router.delete("/{notification_id}", response_model=SuccessResponse)
async def delete_notification(
    notification_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a notification"""
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return SuccessResponse(
        success=True,
        message="Notification deleted successfully"
    )

@router.delete("/bulk/delete", response_model=BulkOperationResponse)
async def delete_multiple_notifications(
    bulk_data: NotificationBulkDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete multiple notifications"""
    affected_count = db.query(Notification).filter(
        and_(
            Notification.id.in_(bulk_data.notification_ids),
            Notification.user_id == current_user.id
        )
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return BulkOperationResponse(
        success=True,
        affected_count=affected_count,
        message=f"Deleted {affected_count} notifications"
    )

@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_update: NotificationUpdate,
    notification_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a notification (admin use)"""
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Update only provided fields
    update_data = notification_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notification, field, value)
    
    db.commit()
    db.refresh(notification)
    
    return notification

# Preference endpoints
@router.get("/preferences", response_model=NotificationPreferenceResponse)
async def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's notification preferences"""
    preferences = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not preferences:
        # Create default preferences if none exist
        preferences = NotificationPreference(
            user_id=current_user.id,
            email=True,
            push=True,
            sms=False,
            weekly_digest=True
        )
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    
    return preferences

@router.put("/preferences", response_model=NotificationPreferenceResponse)
async def update_notification_preferences(
    preferences_update: NotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's notification preferences"""
    preferences = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not preferences:
        # Create new preferences if none exist
        preferences_data = preferences_update.model_dump(exclude_unset=True)
        preferences_data['user_id'] = current_user.id
        preferences = NotificationPreference(**preferences_data)
        db.add(preferences)
    else:
        # Update existing preferences
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(preferences, field, value)
    
    db.commit()
    db.refresh(preferences)
    
    return preferences

# Statistics endpoint (bonus)
@router.get("/stats")
async def get_notification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notification statistics for the user"""
    
    base_query = db.query(Notification).filter(
        Notification.user_id == current_user.id
    )
    
    stats = {
        "total": base_query.count(),
        "unread": base_query.filter(Notification.read == False).count(),
        "by_type": {},
        "by_category": {}
    }
    
    # Stats by type
    type_stats = db.query(
        Notification.type,
        func.count(Notification.id).label('count')
    ).filter(
        Notification.user_id == current_user.id
    ).group_by(Notification.type).all()
    
    stats["by_type"] = {stat.type: stat.count for stat in type_stats}
    
    # Stats by category
    category_stats = db.query(
        Notification.category,
        func.count(Notification.id).label('count')
    ).filter(
        Notification.user_id == current_user.id
    ).group_by(Notification.category).all()
    
    stats["by_category"] = {stat.category: stat.count for stat in category_stats}
    
    return stats