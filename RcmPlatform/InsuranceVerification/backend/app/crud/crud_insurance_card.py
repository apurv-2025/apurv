# File: app/crud/crud_insurance_card.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.models import InsuranceCard
from app.schemas.insurance_card import InsuranceCardCreate, InsuranceCardUpdate


class CRUDInsuranceCard(CRUDBase[InsuranceCard, InsuranceCardCreate, InsuranceCardUpdate]):
    """CRUD operations for InsuranceCard."""
    
    def get_by_member_id(self, db: Session, *, member_id: str) -> Optional[InsuranceCard]:
        """Get insurance card by member ID."""
        return db.query(InsuranceCard).filter(InsuranceCard.member_id == member_id).first()
    
    def get_recent(self, db: Session, *, limit: int = 10) -> List[InsuranceCard]:
        """Get most recently created insurance cards."""
        return (
            db.query(InsuranceCard)
            .order_by(desc(InsuranceCard.created_at))
            .limit(limit)
            .all()
        )
    
    def search_by_name(self, db: Session, *, name: str) -> List[InsuranceCard]:
        """Search insurance cards by patient name."""
        return (
            db.query(InsuranceCard)
            .filter(InsuranceCard.patient_name.ilike(f"%{name}%"))
            .all()
        )


insurance_card = CRUDInsuranceCard(InsuranceCard)
