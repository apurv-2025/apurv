# File: app/crud/crud_patient_information.py - Patient Information CRUD
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import PatientInformation
from app.schemas.patient_information import PatientInformationCreate, PatientInformationUpdate


class CRUDPatientInformation(CRUDBase[PatientInformation, PatientInformationCreate, PatientInformationUpdate]):
    """CRUD operations for Patient Information."""
    
    def get_by_patient_id(self, db: Session, *, patient_id: str) -> Optional[PatientInformation]:
        """Get patient information by patient ID."""
        return db.query(PatientInformation).filter(
            PatientInformation.patient_id == patient_id
        ).first()
    
    def get_by_member_id(self, db: Session, *, member_id: str) -> Optional[PatientInformation]:
        """Get patient information by member ID."""
        return db.query(PatientInformation).filter(
            PatientInformation.member_id_primary == member_id
        ).first()
    
    def search_by_name(self, db: Session, *, first_name: str = None, last_name: str = None) -> List[PatientInformation]:
        """Search patients by name."""
        query = db.query(PatientInformation)
        
        if first_name:
            query = query.filter(PatientInformation.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(PatientInformation.last_name.ilike(f"%{last_name}%"))
        
        return query.all()
    
    def get_by_ssn(self, db: Session, *, ssn: str) -> Optional[PatientInformation]:
        """Get patient by SSN (encrypted)."""
        return db.query(PatientInformation).filter(
            PatientInformation.ssn == ssn
        ).first()


patient_information = CRUDPatientInformation(PatientInformation)
