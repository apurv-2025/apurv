# services.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from app.models.models import Charge, Provider, Patient, Encounter, ChargeTemplate, ChargeValidationRule
from app.schemas import (
    ChargeCreate, ChargeUpdate, ChargeSearchParams,
    ChargeTemplateCreate, ValidationError, ChargeValidation
)

class ChargeService:
    def __init__(self, db: Session, medical_code_service=None):
        self.db = db
        self.medical_code_service = medical_code_service  # Your existing service
    
    def create_charge(self, charge_data: ChargeCreate, captured_by: uuid.UUID) -> Charge:
        """Create a new charge with validation"""
        
        # Validate the charge data
        validation_result = self.validate_charge(charge_data)
        if not validation_result.is_valid:
            raise ValueError(f"Charge validation failed: {validation_result.errors}")
        
        # Get code descriptions if not provided
        if not charge_data.cpt_description and self.medical_code_service:
            cpt_info = self.medical_code_service.get_cpt_code(charge_data.cpt_code)
            charge_data.cpt_description = cpt_info.get('description') if cpt_info else None
        
        if not charge_data.icd_description and self.medical_code_service:
            icd_info = self.medical_code_service.get_icd_code(charge_data.icd_code)
            charge_data.icd_description = icd_info.get('description') if icd_info else None
        
        # Create the charge
        charge = Charge(
            **charge_data.dict(),
            captured_by=captured_by,
            validation_errors=[error.dict() for error in validation_result.warnings],
            audit_log=[{
                "action": "created",
                "user_id": str(captured_by),
                "timestamp": datetime.utcnow().isoformat(),
                "details": "Charge created"
            }]
        )
        
        self.db.add(charge)
        self.db.commit()
        self.db.refresh(charge)
        return charge
    
    def update_charge(self, charge_id: uuid.UUID, charge_data: ChargeUpdate, updated_by: uuid.UUID) -> Optional[Charge]:
        """Update an existing charge"""
        charge = self.db.query(Charge).filter(Charge.id == charge_id).first()
        if not charge:
            return None
        
        # Store old values for audit
        old_values = {
            "cpt_code": charge.cpt_code,
            "icd_code": charge.icd_code,
            "status": charge.status
        }
        
        # Update fields
        update_data = charge_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(charge, field, value)
        
        # Update audit log
        if not charge.audit_log:
            charge.audit_log = []
        
        charge.audit_log.append({
            "action": "updated",
            "user_id": str(updated_by),
            "timestamp": datetime.utcnow().isoformat(),
            "old_values": old_values,
            "new_values": update_data
        })
        
        charge.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(charge)
        return charge
    
    def get_charge(self, charge_id: uuid.UUID) -> Optional[Charge]:
        """Get a charge by ID with related data"""
        return self.db.query(Charge)\
            .join(Patient)\
            .join(Provider)\
            .join(Encounter)\
            .filter(Charge.id == charge_id)\
            .first()
    
    def search_charges(self, params: ChargeSearchParams) -> tuple[List[Charge], int]:
        """Search charges with filtering and pagination"""
        query = self.db.query(Charge)\
            .join(Patient)\
            .join(Provider)\
            .join(Encounter)
        
        # Apply filters
        if params.patient_id:
            query = query.filter(Charge.patient_id == params.patient_id)
        if params.provider_id:
            query = query.filter(Charge.provider_id == params.provider_id)
        if params.encounter_id:
            query = query.filter(Charge.encounter_id == params.encounter_id)
        if params.status:
            query = query.filter(Charge.status == params.status)
        if params.date_from:
            query = query.filter(Charge.captured_at >= params.date_from)
        if params.date_to:
            query = query.filter(Charge.captured_at <= params.date_to)
        if params.cpt_code:
            query = query.filter(Charge.cpt_code == params.cpt_code)
        if params.specialty:
            query = query.filter(Provider.specialty == params.specialty)
        
        # Count total
        total_count = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.page_size
        charges = query.order_by(desc(Charge.captured_at))\
            .offset(offset)\
            .limit(params.page_size)\
            .all()
        
        return charges, total_count
    
    def validate_charge(self, charge_data: ChargeCreate) -> ChargeValidation:
        """Validate charge data against business rules"""
        errors = []
        warnings = []
        
        # Basic validation
        if not charge_data.cpt_code:
            errors.append(ValidationError(
                field="cpt_code",
                code="required",
                message="CPT code is required",
                severity="error"
            ))
        
        if not charge_data.icd_code:
            errors.append(ValidationError(
                field="icd_code",
                code="required",
                message="ICD code is required",
                severity="error"
            ))
        
        # Code format validation
        if charge_data.cpt_code and len(charge_data.cpt_code) != 5:
            errors.append(ValidationError(
                field="cpt_code",
                code="invalid_format",
                message="CPT code must be 5 digits",
                severity="error"
            ))
        
        # Validate against medical code service
        if self.medical_code_service and charge_data.cpt_code:
            if not self.medical_code_service.validate_cpt_code(charge_data.cpt_code):
                errors.append(ValidationError(
                    field="cpt_code",
                    code="invalid_code",
                    message="CPT code not found in code database",
                    severity="error"
                ))
        
        if self.medical_code_service and charge_data.icd_code:
            if not self.medical_code_service.validate_icd_code(charge_data.icd_code):
                errors.append(ValidationError(
                    field="icd_code",
                    code="invalid_code",
                    message="ICD code not found in code database",
                    severity="error"
                ))
        
        # Business rule validation
        validation_rules = self.db.query(ChargeValidationRule)\
            .filter(ChargeValidationRule.is_active == True)\
            .all()
        
        for rule in validation_rules:
            rule_result = self._apply_validation_rule(rule, charge_data)
            if rule_result:
                if rule_result.severity == "error":
                    errors.append(rule_result)
                else:
                    warnings.append(rule_result)
        
        return ChargeValidation(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _apply_validation_rule(self, rule: ChargeValidationRule, charge_data: ChargeCreate) -> Optional[ValidationError]:
        """Apply a specific validation rule"""
        # This is where you'd implement specific business rules
        # Example: check if certain CPT/ICD combinations are valid
        
        if rule.rule_type == "code_combination":
            # Example rule: certain CPT codes require specific ICD codes
            config = rule.rule_config
            if (charge_data.cpt_code in config.get("cpt_codes", []) and
                charge_data.icd_code not in config.get("required_icd_codes", [])):
                return ValidationError(
                    field="icd_code",
                    code="invalid_combination",
                    message=rule.error_message or "Invalid CPT/ICD combination",
                    severity="error"
                )
        
        return None
    
    def get_missed_charges(self, date_from: datetime, date_to: datetime) -> List[Dict[str, Any]]:
        """Find encounters without charges (missed charges)"""
        subquery = self.db.query(Charge.encounter_id).subquery()
        
        missed_encounters = self.db.query(Encounter)\
            .join(Patient)\
            .join(Provider)\
            .filter(
                and_(
                    Encounter.encounter_date >= date_from,
                    Encounter.encounter_date <= date_to,
                    Encounter.status == "completed",
                    ~Encounter.id.in_(subquery)
                )
            ).all()
        
        return [
            {
                "encounter_id": enc.id,
                "patient_name": f"{enc.patient.first_name} {enc.patient.last_name}",
                "provider_name": f"{enc.provider.first_name} {enc.provider.last_name}",
                "encounter_date": enc.encounter_date,
                "encounter_type": enc.encounter_type,
                "specialty": enc.provider.specialty
            }
            for enc in missed_encounters
        ]

class ChargeTemplateService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_template(self, template_data: ChargeTemplateCreate) -> ChargeTemplate:
        """Create a new charge template"""
        template = ChargeTemplate(**template_data.dict())
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
    
    def get_templates_for_provider(self, provider_id: uuid.UUID, specialty: str) -> List[ChargeTemplate]:
        """Get templates for a specific provider and specialty"""
        return self.db.query(ChargeTemplate)\
            .filter(
                or_(
                    ChargeTemplate.provider_id == provider_id,
                    and_(
                        ChargeTemplate.provider_id.is_(None),
                        ChargeTemplate.specialty == specialty
                    )
                )
            )\
            .filter(ChargeTemplate.is_active == True)\
            .order_by(ChargeTemplate.is_system_template, ChargeTemplate.name)\
            .all()
    
    def update_template(self, template_id: uuid.UUID, updates: Dict[str, Any]) -> Optional[ChargeTemplate]:
        """Update a template"""
        template = self.db.query(ChargeTemplate).filter(ChargeTemplate.id == template_id).first()
        if not template:
            return None
        
        for field, value in updates.items():
            setattr(template, field, value)
        
        template.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(template)
        return template

class ReportingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_charge_metrics(self, date_from: datetime, date_to: datetime, 
                          specialty: Optional[str] = None) -> Dict[str, Any]:
        """Get charge capture metrics"""
        
        query = self.db.query(Charge)\
            .join(Provider)\
            .filter(Charge.captured_at.between(date_from, date_to))
        
        if specialty:
            query = query.filter(Provider.specialty == specialty)
        
        charges = query.all()
        
        # Calculate metrics
        total_charges = len(charges)
        charges_by_status = {}
        charges_by_specialty = {}
        
        for charge in charges:
            # Status distribution
            status = charge.status
            charges_by_status[status] = charges_by_status.get(status, 0) + 1
            
            # Specialty distribution (if not filtering by specialty)
            if not specialty:
                provider_specialty = charge.provider.specialty
                charges_by_specialty[provider_specialty] = charges_by_specialty.get(provider_specialty, 0) + 1
        
        # Calculate average capture time
        encounter_charges = [(c.encounter.encounter_date, c.captured_at) for c in charges 
                           if c.encounter and c.encounter.encounter_date]
        
        if encounter_charges:
            capture_times = [(captured - encounter).total_seconds() / 60 
                           for encounter, captured in encounter_charges]
            avg_capture_time = sum(capture_times) / len(capture_times)
        else:
            avg_capture_time = None
        
        # Get missed charges count
        charge_service = ChargeService(self.db)
        missed_charges = charge_service.get_missed_charges(date_from, date_to)
        
        return {
            "total_charges": total_charges,
            "charges_by_status": charges_by_status,
            "charges_by_specialty": charges_by_specialty if not specialty else {},
            "avg_capture_time": avg_capture_time,
            "missed_charges_count": len(missed_charges),
            "date_range": {"from": date_from, "to": date_to}
        }
