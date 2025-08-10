from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from app.dao.base import BaseDAO
from app.models.health_insurance import PatientInformation
from app.schemas.patient_information import (
    PatientSummary,
    PatientSearchRequest,
    PatientStatistics
)
from datetime import date, datetime
import uuid


class EnhancedPatientDAO(BaseDAO[PatientInformation]):
    def __init__(self):
        super().__init__(PatientInformation)

    def create_patient_with_id(self, db: Session, patient_data: Dict[str, Any]) -> PatientInformation:
        """Create patient with auto-generated patient_id"""
        if 'patient_id' not in patient_data:
            patient_data['patient_id'] = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        return self.create(db, obj_in=patient_data)

    def get_patient_summary(self, db: Session, patient_id: str) -> Optional[PatientSummary]:
        """Get patient summary information"""
        patient = self.get_by_field(db, 'patient_id', patient_id)
        if patient:
            return PatientSummary.model_validate(patient)
        return None

    def advanced_search(
        self, 
        db: Session, 
        search_request: PatientSearchRequest,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[PatientSummary], int]:
        """Advanced patient search with count"""
        query = db.query(PatientInformation)
        
        # Build filters
        if search_request.first_name:
            query = query.filter(
                PatientInformation.first_name.ilike(f"%{search_request.first_name}%")
            )
        
        if search_request.last_name:
            query = query.filter(
                PatientInformation.last_name.ilike(f"%{search_request.last_name}%")
            )
        
        if search_request.date_of_birth:
            query = query.filter(PatientInformation.date_of_birth == search_request.date_of_birth)
        
        if search_request.member_id:
            query = query.filter(
                or_(
                    PatientInformation.member_id_primary == search_request.member_id,
                    PatientInformation.member_id_secondary == search_request.member_id
                )
            )
        
        if search_request.phone:
            phone_filter = or_(
                PatientInformation.phone_home.ilike(f"%{search_request.phone}%"),
                PatientInformation.phone_work.ilike(f"%{search_request.phone}%"),
                PatientInformation.phone_mobile.ilike(f"%{search_request.phone}%")
            )
            query = query.filter(phone_filter)
        
        if search_request.email:
            query = query.filter(PatientInformation.email.ilike(f"%{search_request.email}%"))
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        patients = query.offset(skip).limit(limit).all()
        summaries = [PatientSummary.model_validate(p) for p in patients]
        
        return summaries, total

    def get_patients_by_insurance_carrier(
        self, 
        db: Session, 
        carrier_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PatientInformation]:
        """Get patients by insurance carrier"""
        query = db.query(PatientInformation).filter(
            or_(
                PatientInformation.primary_insurance['carrier_name'].astext == carrier_name,
                PatientInformation.secondary_insurance['carrier_name'].astext == carrier_name
            )
        )
        return query.offset(skip).limit(limit).all()

    def get_patients_with_conditions(
        self, 
        db: Session, 
        condition_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PatientInformation]:
        """Get patients with specific medical condition"""
        # Using PostgreSQL JSON operations
        query = db.query(PatientInformation).filter(
            PatientInformation.medical_conditions.op('?|')(text(f"'{condition_name}'"))
        )
        return query.offset(skip).limit(limit).all()

    def get_patients_by_age_range(
        self, 
        db: Session, 
        min_age: int, 
        max_age: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[PatientInformation]:
        """Get patients within age range"""
        today = date.today()
        max_birth_date = date(today.year - min_age, today.month, today.day)
        min_birth_date = date(today.year - max_age, today.month, today.day)
        
        query = db.query(PatientInformation).filter(
            and_(
                PatientInformation.date_of_birth >= min_birth_date,
                PatientInformation.date_of_birth <= max_birth_date
            )
        )
        return query.offset(skip).limit(limit).all()

    def get_patient_statistics(self, db: Session) -> PatientStatistics:
        """Get patient statistics"""
        total_patients = db.query(func.count(PatientInformation.id)).scalar()
        
        # Get authorization counts
        auth_query = text("""
            SELECT COUNT(DISTINCT patient_id) 
            FROM prior_authorization_requests
        """)
        patients_with_auth = db.execute(auth_query).scalar()
        
        # Gender distribution
        gender_stats = db.query(
            PatientInformation.gender,
            func.count(PatientInformation.id)
        ).group_by(PatientInformation.gender).all()
        
        by_gender = {gender: count for gender, count in gender_stats}
        
        # Age group distribution
        age_groups_query = text("""
            SELECT 
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 18 THEN 'Under 18'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 18 AND 30 THEN '18-30'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 31 AND 50 THEN '31-50'
                    WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) BETWEEN 51 AND 65 THEN '51-65'
                    ELSE 'Over 65'
                END as age_group,
                COUNT(*)
            FROM patient_information
            GROUP BY age_group
        """)
        age_groups = db.execute(age_groups_query).fetchall()
        by_age_group = {group: count for group, count in age_groups}
        
        # Insurance type distribution
        insurance_query = text("""
            SELECT 
                primary_insurance->>'carrier_name' as carrier,
                COUNT(*)
            FROM patient_information
            WHERE primary_insurance IS NOT NULL
            GROUP BY primary_insurance->>'carrier_name'
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        insurance_stats = db.execute(insurance_query).fetchall()
        by_insurance_type = {carrier: count for carrier, count in insurance_stats}
        
        avg_auth = patients_with_auth / total_patients if total_patients > 0 else 0
        
        return PatientStatistics(
            total_patients=total_patients,
            patients_with_authorizations=patients_with_auth,
            average_authorizations_per_patient=avg_auth,
            by_gender=by_gender,
            by_age_group=by_age_group,
            by_insurance_type=by_insurance_type,
            generated_at=datetime.utcnow()
        )

    def bulk_update_insurance(
        self, 
        db: Session, 
        updates: List[Dict[str, Any]]
    ) -> List[PatientInformation]:
        """Bulk update patient insurance information"""
        updated_patients = []
        
        for update_data in updates:
            patient_id = update_data.get('patient_id')
            if not patient_id:
                continue
                
            patient = self.get_by_field(db, 'patient_id', patient_id)
            if patient:
                insurance_updates = {
                    k: v for k, v in update_data.items() 
                    if k in ['primary_insurance', 'secondary_insurance', 'member_id_primary', 'member_id_secondary']
                }
                if insurance_updates:
                    updated_patient = self.update(db, db_obj=patient, obj_in=insurance_updates)
                    updated_patients.append(updated_patient)
        
        return updated_patients

