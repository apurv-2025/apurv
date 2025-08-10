# File: app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class with common database operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID."""
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by ID {id}: {str(e)}")
            return None
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting multiple {self.model.__name__}: {str(e)}")
            return []
    
    def get_count(self, db: Session) -> int:
        """Get total count of records."""
        try:
            return db.query(self.model).count()
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__}: {str(e)}")
            return 0
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> Optional[ModelType]:
        """Create a new record."""
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Created new {self.model.__name__} with ID: {db_obj.id}")
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating {self.model.__name__}: {str(e)}")
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            return None
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """Update an existing record."""
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Updated {self.model.__name__} with ID: {db_obj.id}")
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error updating {self.model.__name__}: {str(e)}")
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            return None
    
    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Delete a record."""
        try:
            obj = db.query(self.model).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                logger.info(f"Deleted {self.model.__name__} with ID: {id}")
                return obj
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            return None

