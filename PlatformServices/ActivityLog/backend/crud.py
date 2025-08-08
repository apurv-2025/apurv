# ========================
# crud.py
# ========================
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta
import models
import schemas


class ActivityEventCRUD:
    def create_event(self, db: Session, event: schemas.ActivityEventCreate, user_id: str) -> models.ActivityEvent:
        db_event = models.ActivityEvent(
            user_id=user_id,
            **event.dict()
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    def get_events(
        self, 
        db: Session, 
        user_id: str,
        filters: schemas.ActivityEventFilters,
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.ActivityEvent]:
        query = db.query(models.ActivityEvent).options(
            joinedload(models.ActivityEvent.user),
            joinedload(models.ActivityEvent.client)
        ).filter(models.ActivityEvent.user_id == user_id)
        
        # Apply filters
        if filters.event_type:
            query = query.filter(models.ActivityEvent.event_type == filters.event_type)
        
        if filters.client_id:
            query = query.filter(models.ActivityEvent.client_id == filters.client_id)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    models.ActivityEvent.event_description.ilike(search_term),
                    models.ActivityEvent.location.ilike(search_term)
                )
            )
        
        # Date range filtering
        if filters.date_range and filters.date_range != "all":
            now = datetime.utcnow()
            if filters.date_range == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                query = query.filter(models.ActivityEvent.timestamp >= start_date)
            elif filters.date_range == "week":
                start_date = now - timedelta(weeks=1)
                query = query.filter(models.ActivityEvent.timestamp >= start_date)
            elif filters.date_range == "month":
                start_date = now - timedelta(days=30)
                query = query.filter(models.ActivityEvent.timestamp >= start_date)
        
        if filters.start_date:
            query = query.filter(models.ActivityEvent.timestamp >= filters.start_date)
        
        if filters.end_date:
            query = query.filter(models.ActivityEvent.timestamp <= filters.end_date)
        
        return query.order_by(models.ActivityEvent.timestamp.desc()).offset(skip).limit(limit).all()

    def get_event(self, db: Session, event_id: str, user_id: str) -> Optional[models.ActivityEvent]:
        return db.query(models.ActivityEvent).filter(
            and_(
                models.ActivityEvent.id == event_id,
                models.ActivityEvent.user_id == user_id
            )
        ).first()


class UserCRUD:
    def get_user_by_email(self, db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()
    
    def create_user(self, db: Session, user: schemas.UserCreate) -> models.User:
        # In production, hash the password properly
        hashed_password = f"hashed_{user.password}"  # Use proper hashing like bcrypt
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class ClientCRUD:
    def get_clients(self, db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Client]:
        return db.query(models.Client).filter(
            models.Client.created_by == user_id
        ).offset(skip).limit(limit).all()
    
    def create_client(self, db: Session, client: schemas.ClientCreate, user_id: str) -> models.Client:
        db_client = models.Client(
            **client.dict(),
            created_by=user_id
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client


# Initialize CRUD instances
activity_crud = ActivityEventCRUD()
user_crud = UserCRUD()
client_crud = ClientCRUD()
