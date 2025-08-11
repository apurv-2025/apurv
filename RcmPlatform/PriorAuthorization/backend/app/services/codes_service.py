# Codes Service for Prior Authorization System
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.dao import EnhancedCodesDAO
from app.models.models import ServiceTypeCode, ProcedureCode, DiagnosisCode


class CodesService:
    def __init__(self):
        self.dao = EnhancedCodesDAO()

    def get_service_type_codes(
        self, 
        db: Session, 
        active_only: bool = True, 
        requires_auth: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Get service type codes"""
        try:
            # Get all service type codes
            codes = self.dao.get_service_type_codes(db)
            
            # Filter by active status
            if active_only:
                codes = [code for code in codes if code.is_active]
            
            # Filter by authorization requirement
            if requires_auth is not None:
                codes = [code for code in codes if code.requires_authorization == requires_auth]
            
            return [
                {
                    "code": code.code,
                    "description": code.description,
                    "category": code.category,
                    "requires_authorization": code.requires_authorization
                }
                for code in codes
            ]
        except Exception as e:
            raise Exception(f"Failed to get service type codes: {str(e)}")

    def get_service_type_code(self, db: Session, code: str) -> Optional[Dict[str, Any]]:
        """Get specific service type code"""
        try:
            service_code = self.dao.get_service_type_code_by_code(db, code)
            if not service_code:
                return None
            
            return {
                "code": service_code.code,
                "description": service_code.description,
                "category": service_code.category,
                "requires_authorization": service_code.requires_authorization
            }
        except Exception as e:
            raise Exception(f"Failed to get service type code: {str(e)}")

    def get_procedure_codes(
        self, 
        db: Session, 
        code_type: Optional[str] = None,
        category: Optional[str] = None,
        requires_auth: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get procedure codes"""
        try:
            # Get procedure codes based on filters
            if search:
                codes = self.dao.search_procedure_codes_by_description(db, search)
            elif code_type:
                codes = self.dao.get_procedure_codes_by_type(db, code_type)
            elif category:
                codes = self.dao.get_procedure_codes_by_category(db, category)
            else:
                codes = self.dao.get_procedure_codes(db, skip=skip, limit=limit, active_only=True)
            
            # Filter by authorization requirement
            if requires_auth is not None:
                codes = [code for code in codes if code.requires_authorization == requires_auth]
            
            # Apply pagination if not already done
            if not (search or code_type or category):
                codes = codes[skip:skip + limit]
            
            return [
                {
                    "code": code.code,
                    "description": code.description,
                    "code_type": code.code_type,
                    "category": code.category,
                    "requires_authorization": code.requires_authorization
                }
                for code in codes
            ]
        except Exception as e:
            raise Exception(f"Failed to get procedure codes: {str(e)}")

    def get_procedure_code(self, db: Session, code: str) -> Optional[Dict[str, Any]]:
        """Get specific procedure code"""
        try:
            procedure_code = self.dao.get_procedure_code_by_code(db, code)
            if not procedure_code:
                return None
            
            return {
                "code": procedure_code.code,
                "description": procedure_code.description,
                "code_type": procedure_code.code_type,
                "category": procedure_code.category,
                "requires_authorization": procedure_code.requires_authorization
            }
        except Exception as e:
            raise Exception(f"Failed to get procedure code: {str(e)}")

    def get_diagnosis_codes(
        self, 
        db: Session, 
        category: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get diagnosis codes"""
        try:
            # Get diagnosis codes based on filters
            if search:
                codes = self.dao.search_diagnosis_codes_by_description(db, search)
            elif category:
                codes = self.dao.get_diagnosis_codes_by_category(db, category)
            else:
                codes = self.dao.get_diagnosis_codes(db, skip=skip, limit=limit, active_only=True)
            
            return [
                {
                    "code": code.code,
                    "description": code.description,
                    "category": code.category
                }
                for code in codes
            ]
        except Exception as e:
            raise Exception(f"Failed to get diagnosis codes: {str(e)}")

    def get_diagnosis_code(self, db: Session, code: str) -> Optional[Dict[str, Any]]:
        """Get specific diagnosis code"""
        try:
            diagnosis_code = self.dao.get_diagnosis_code_by_code(db, code)
            if not diagnosis_code:
                return None
            
            return {
                "code": diagnosis_code.code,
                "description": diagnosis_code.description,
                "category": diagnosis_code.category
            }
        except Exception as e:
            raise Exception(f"Failed to get diagnosis code: {str(e)}")

    def search_codes(
        self, 
        db: Session, 
        query: str, 
        code_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search codes by query"""
        try:
            if code_type == "procedure":
                codes = self.dao.search_procedure_codes_by_description(db, query)
                return [
                    {
                        "code": code.code,
                        "description": code.description,
                        "code_type": code.code_type,
                        "category": code.category,
                        "type": "procedure"
                    }
                    for code in codes[:limit]
                ]
            elif code_type == "diagnosis":
                codes = self.dao.search_diagnosis_codes_by_description(db, query)
                return [
                    {
                        "code": code.code,
                        "description": code.description,
                        "category": code.category,
                        "type": "diagnosis"
                    }
                    for code in codes[:limit]
                ]
            else:
                # Search both types
                procedure_codes = self.dao.search_procedure_codes_by_description(db, query)
                diagnosis_codes = self.dao.search_diagnosis_codes_by_description(db, query)
                
                results = []
                
                # Add procedure codes
                for code in procedure_codes[:limit//2]:
                    results.append({
                        "code": code.code,
                        "description": code.description,
                        "code_type": code.code_type,
                        "category": code.category,
                        "type": "procedure"
                    })
                
                # Add diagnosis codes
                for code in diagnosis_codes[:limit//2]:
                    results.append({
                        "code": code.code,
                        "description": code.description,
                        "category": code.category,
                        "type": "diagnosis"
                    })
                
                return results[:limit]
        except Exception as e:
            raise Exception(f"Failed to search codes: {str(e)}")


# Create singleton instance
codes_service = CodesService() 