# File: app/crud/crud_provider.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import Provider
from app.schemas.provider import ProviderCreate, ProviderUpdate


class CRUDProvider(CRUDBase[Provider, ProviderCreate, ProviderUpdate]):
    """CRUD operations for Provider."""
    
    def get_by_npi(self, db: Session, *, npi: str) -> Optional[Provider]:
        """Get provider by NPI."""
        return db.query(Provider).filter(Provider.npi == npi).first()
    
    def get_active(self, db: Session) -> List[Provider]:
        """Get all active providers."""
        return db.query(Provider).filter(Provider.is_active == True).all()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Provider]:
        """Search providers by name."""
        return (
            db.query(Provider)
            .filter(Provider.name.ilike(f"%{name}%"))
            .filter(Provider.is_active == True)
            .all()
        )


provider = CRUDProvider(Provider)
