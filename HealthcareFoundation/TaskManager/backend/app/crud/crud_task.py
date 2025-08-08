from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, case
from datetime import date, datetime

from app.crud.base import CRUDBase
from app.models.models import Task, Client
from app.schemas.task import TaskCreate, TaskUpdate, TaskStats


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_by_status(self, db: Session, *, status: str) -> List[Task]:
        return db.query(self.model).filter(Task.status == status).all()

    def get_by_priority(self, db: Session, *, priority: str) -> List[Task]:
        return db.query(self.model).filter(Task.priority == priority).all()

    def get_by_client(self, db: Session, *, client_id: int) -> List[Task]:
        return db.query(self.model).filter(Task.client_id == client_id).all()

    def get_overdue(self, db: Session) -> List[Task]:
        today = date.today()
        return db.query(self.model).filter(
            and_(
                Task.due_date.isnot(None),
                Task.due_date < today,
                Task.status != "completed"
            )
        ).all()

    def get_due_today(self, db: Session) -> List[Task]:
        today = date.today()
        return db.query(self.model).filter(
            and_(
                Task.due_date == today,
                Task.status != "completed"
            )
        ).all()

    def search(self, db: Session, *, query: str, skip: int = 0, limit: int = 100) -> List[Task]:
        search_term = f"%{query}%"
        return db.query(self.model).filter(
            or_(
                Task.name.ilike(search_term),
                Task.description.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()

    def get_filtered(
        self,
        db: Session,
        *,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        client_id: Optional[int] = None,
        overdue: Optional[bool] = None,
        due_date: Optional[date] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        query = db.query(self.model)

        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if client_id:
            query = query.filter(Task.client_id == client_id)
        
        if overdue:
            today = date.today()
            query = query.filter(
                and_(
                    Task.due_date.isnot(None),
                    Task.due_date < today,
                    Task.status != "completed"
                )
            )
        
        if due_date:
            query = query.filter(Task.due_date == due_date)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Task.name.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_stats(self, db: Session) -> TaskStats:
        total_tasks = db.query(func.count(Task.id)).scalar()
        completed_tasks = db.query(func.count(Task.id)).filter(Task.status == "completed").scalar()
        
        today = date.today()
        overdue_tasks = db.query(func.count(Task.id)).filter(
            and_(
                Task.due_date.isnot(None),
                Task.due_date < today,
                Task.status != "completed"
            )
        ).scalar()
        
        due_today = db.query(func.count(Task.id)).filter(
            and_(
                Task.due_date == today,
                Task.status != "completed"
            )
        ).scalar()

        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return TaskStats(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            pending_tasks=pending_tasks,
            overdue_tasks=overdue_tasks,
            due_today=due_today,
            completion_rate=round(completion_rate, 2)
        )

    def create_with_attachments(
        self, db: Session, *, obj_in: TaskCreate, attachment_ids: List[int] = None
    ) -> Task:
        db_obj = self.create(db=db, obj_in=obj_in)
        
        if attachment_ids:
            from app.crud.crud_attachment import attachment
            for attachment_id in attachment_ids:
                att = attachment.get(db=db, id=attachment_id)
                if att:
                    att.task_id = db_obj.id
            db.commit()
            db.refresh(db_obj)
        
        return db_obj


task = CRUDTask(Task)
