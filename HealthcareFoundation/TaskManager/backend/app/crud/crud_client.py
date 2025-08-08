from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.models import Client, Task
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Client]:
        return db.query(self.model).filter(Client.email == email).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Client]:
        return db.query(self.model).filter(Client.name == name).first()

    def search(self, db: Session, *, query: str, skip: int = 0, limit: int = 100) -> List[Client]:
        search_term = f"%{query}%"
        return db.query(self.model).filter(
            Client.name.ilike(search_term) |
            Client.email.ilike(search_term) |
            Client.company.ilike(search_term)
        ).offset(skip).limit(limit).all()

    def get_with_task_count(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Client]:
        return db.query(
            self.model,
            func.count(Task.id).label("task_count")
        ).outerjoin(Task).group_by(self.model.id).offset(skip).limit(limit).all()

    def get_client_tasks(self, db: Session, *, client_id: int) -> List[Task]:
        return db.query(Task).filter(Task.client_id == client_id).all()


client = CRUDClient(Client)
