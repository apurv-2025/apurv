# File: app/dao/enhanced_codes_dao.py
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from app.dao.base_dao import BaseDAO
from app.models.models import ServiceTypeCode, ProcedureCode, DiagnosisCode
from app.schemas.codes import CodeSearchRequest
from datetime import datetime


class EnhancedCodesDAO:
    def __init__(self):
        self.service_type_dao = BaseDAO(ServiceTypeCode)
        self.procedure_dao = BaseDAO(ProcedureCode)
        self.diagnosis_dao = BaseDAO(DiagnosisCode)

    def search_all_codes(
        self, 
        db: Session, 
        search_request: CodeSearchRequest,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Search across all code types"""
        results = {
            'service_types': [],
            'procedures': [],
            'diagnoses': []
        }
        
        if search_request.search_term:
            # Service types
            service_query = db.query(ServiceTypeCode).filter(
                and_(
                    ServiceTypeCode.description.ilike(f"%{search_request.search_term}%"),
                    ServiceTypeCode.is_active == search_request.active_only
                )
            )
            if search_request.category:
                service_query = service_query.filter(ServiceTypeCode.category == search_request.category)
            
            service_codes = service_query.limit(limit // 3).all()
            results['service_types'] = [
                {
                    'code': sc.code,
                    'description': sc.description,
                    'category': sc.category,
                    'type': 'service_type'
                }
                for sc in service_codes
            ]
            
            # Procedure codes
            proc_query = db.query(ProcedureCode).filter(
                and_(
                    ProcedureCode.description.ilike(f"%{search_request.search_term}%"),
                    ProcedureCode.is_active == search_request.active_only
                )
            )
            if search_request.category:
                proc_query = proc_query.filter(ProcedureCode.category == search_request.category)
            
            proc_codes = proc_query.limit(limit // 3).all()
            results['procedures'] = [
                {
                    'code': pc.code,
                    'description': pc.description,
                    'category': pc.category,
                    'code_type': pc.code_type,
                    'type': 'procedure'
                }
                for pc in proc_codes
            ]
            
            # Diagnosis codes
            diag_query = db.query(DiagnosisCode).filter(
                and_(
                    DiagnosisCode.description.ilike(f"%{search_request.search_term}%"),
                    DiagnosisCode.is_active == search_request.active_only
                )
            )
            if search_request.category:
                diag_query = diag_query.filter(DiagnosisCode.category == search_request.category)
            
            diag_codes = diag_query.limit(limit // 3).all()
            results['diagnoses'] = [
                {
                    'code': dc.code,
                    'description': dc.description,
                    'category': dc.category,
                    'type': 'diagnosis'
                }
                for dc in diag_codes
            ]
        
        return results

    def get_code_usage_statistics(self, db: Session) -> Dict[str, Any]:
        """Get code usage statistics from authorization requests"""
        from sqlalchemy import text
        
        # Most used procedure codes
        procedure_usage_query = text("""
            SELECT 
                jsonb_array_elements(procedure_codes)->>'code' as code,
                COUNT(*) as usage_count
            FROM prior_authorization_requests 
            WHERE procedure_codes IS NOT NULL
            GROUP BY jsonb_array_elements(procedure_codes)->>'code'
            ORDER BY usage_count DESC
            LIMIT 20
        """)
        
        procedure_usage = db.execute(procedure_usage_query).fetchall()
        
        # Most used diagnosis codes
        diagnosis_usage_query = text("""
            SELECT 
                jsonb_array_elements(diagnosis_codes)->>'code' as code,
                COUNT(*) as usage_count
            FROM prior_authorization_requests 
            WHERE diagnosis_codes IS NOT NULL
            GROUP BY jsonb_array_elements(diagnosis_codes)->>'code'
            ORDER BY usage_count DESC
            LIMIT 20
        """)
        
        diagnosis_usage = db.execute(diagnosis_usage_query).fetchall()
        
        return {
            'most_used_procedures': [
                {'code': code, 'usage_count': count}
                for code, count in procedure_usage
            ],
            'most_used_diagnoses': [
                {'code': code, 'usage_count': count}
                for code, count in diagnosis_usage
            ],
            'generated_at': datetime.utcnow()
        }

    def validate_code_combinations(
        self, 
        db: Session, 
        procedure_codes: List[str], 
        diagnosis_codes: List[str]
    ) -> Dict[str, Any]:
        """Validate procedure and diagnosis code combinations"""
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'suggestions': []
        }
        
        # Check if codes exist
        existing_procedures = db.query(ProcedureCode.code).filter(
            and_(
                ProcedureCode.code.in_(procedure_codes),
                ProcedureCode.is_active == True
            )
        ).all()
        existing_proc_codes = {p.code for p in existing_procedures}
        
        existing_diagnoses = db.query(DiagnosisCode.code).filter(
            and_(
                DiagnosisCode.code.in_(diagnosis_codes),
                DiagnosisCode.is_active == True
            )
        ).all()
        existing_diag_codes = {d.code for d in existing_diagnoses}
        
        # Check for missing codes
        missing_procedures = set(procedure_codes) - existing_proc_codes
        missing_diagnoses = set(diagnosis_codes) - existing_diag_codes
        
        if missing_procedures:
            validation_results['errors'].append(
                f"Invalid procedure codes: {', '.join(missing_procedures)}"
            )
            validation_results['valid'] = False
        
        if missing_diagnoses:
            validation_results['errors'].append(
                f"Invalid diagnosis codes: {', '.join(missing_diagnoses)}"
            )
            validation_results['valid'] = False
        
        # Check authorization requirements
        auth_required_procedures = db.query(ProcedureCode).filter(
            and_(
                ProcedureCode.code.in_(procedure_codes),
                ProcedureCode.requires_authorization == True
            )
        ).all()
        
        if auth_required_procedures:
            auth_codes = [p.code for p in auth_required_procedures]
            validation_results['warnings'].append(
                f"These procedures require prior authorization: {', '.join(auth_codes)}"
            )
        
        return validation_results

