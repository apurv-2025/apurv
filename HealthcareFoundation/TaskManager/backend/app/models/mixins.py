from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin:
    """Mixin for adding timestamp fields to models"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
