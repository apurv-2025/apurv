from typing import List, Optional
from sqlalchemy.orm import Session
import os

from app.crud.base import CRUDBase
from app.models.models import TaskAttachment
from app.schemas.attachment import AttachmentCreate


class CRUDAttachment(CRUDBase[TaskAttachment, AttachmentCreate, dict]):
    def get_by_task(self, db: Session, *, task_id: int) -> List[TaskAttachment]:
        return db.query(self.model).filter(TaskAttachment.task_id == task_id).all()

    def get_by_filename(self, db: Session, *, filename: str) -> Optional[TaskAttachment]:
        return db.query(self.model).filter(TaskAttachment.file_name == filename).first()

    def remove_with_file(self, db: Session, *, id: int) -> TaskAttachment:
        obj = db.query(self.model).get(id)
        if obj:
            # Delete physical file
            if os.path.exists(obj.file_path):
                os.remove(obj.file_path)
            
            # Delete database record
            db.delete(obj)
            db.commit()
        return obj

    def update_task_id(self, db: Session, *, attachment_id: int, task_id: int) -> Optional[TaskAttachment]:
        obj = db.query(self.model).get(attachment_id)
        if obj:
            obj.task_id = task_id
            db.commit()
            db.refresh(obj)
        return obj

    def get_orphaned(self, db: Session) -> List[TaskAttachment]:
        """Get attachments not associated with any task"""
        return db.query(self.model).filter(TaskAttachment.task_id.is_(None)).all()


attachment = CRUDAttachment(TaskAttachment)
