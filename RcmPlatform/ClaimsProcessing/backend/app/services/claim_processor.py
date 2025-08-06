# =============================================================================
# FILE: backend/app/services/claim_processor.py
# =============================================================================
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from ..database.models import Claim, ServiceLine, DentalDetail, ClaimStatus, ClaimType
from ..schemas.claims import ClaimCreate
from .edi_parser import EDIParser
from .validators import ClaimValidator

class ClaimProcessor:
    """Enhanced claim processing service with AI agent integration"""
    
    def __init__(self, db: Session):
        self.db = db
        self.edi_parser = EDIParser()
        self.validator = ClaimValidator()
    
    def create_claim_from_edi(self, edi_content: str, payer_id: int) -> Claim:
        """Create claim from EDI file content"""
        
        # Parse EDI content
        parsed_data = self.edi_parser.parse_837_file(edi_content)
        
        if not parsed_data['claims']:
            raise ValueError("No claims found in EDI file")
        
        # Process first claim (in real implementation, handle multiple claims)
        edi_claim = parsed_data['claims'][0]
        
        # Create claim object
        claim_data = self._map_edi_to_claim(edi_claim, parsed_data['claim_type'], payer_id)
        
        # Generate unique claim number
        claim_number = self._generate_claim_number()
        
        # Create database record
        db_claim = Claim(
            claim_number=claim_number,
            claim_type=parsed_data['claim_type'],
            patient_first_name=claim_data.get('patient_first_name', ''),
            patient_last_name=claim_data.get('patient_last_name', ''),
            patient_dob=claim_data.get('patient_dob'),
            patient_id=claim_data.get('patient_id', ''),
            provider_name=claim_data.get('provider_name', ''),
            provider_npi=claim_data.get('provider_npi', ''),
            provider_taxonomy=claim_data.get('provider_taxonomy'),
            payer_id=payer_id,
            total_charge=Decimal(str(claim_data.get('total_charge', 0))),
            raw_edi_data=edi_content,
            parsed_data=parsed_data,
            status=ClaimStatus.QUEUED
        )
        
        self.db.add(db_claim)
        self.db.flush()  # Get the ID
        
        # Add service lines
        for line_data in claim_data.get('service_lines', []):
            service_line = ServiceLine(
                claim_id=db_claim.id,
                line_number=line_data.get('line_number', 1),
                procedure_code=line_data.get('procedure_code', ''),
                procedure_description=line_data.get('procedure_description'),
                service_date_from=line_data.get('service_date'),
                charge_amount=Decimal(str(line_data.get('charge_amount', 0))),
                units=line_data.get('units', 1),
                diagnosis_code_1=line_data.get('diagnosis_code_1'),
                modifier_1=line_data.get('modifier_1'),
                modifier_2=line_data.get('modifier_2')
            )
            self.db.add(service_line)
        
        # Add dental details if dental claim
        if parsed_data['claim_type'] == ClaimType.DENTAL and 'dental_details' in claim_data:
            dental_data = claim_data['dental_details']
            dental_detail = DentalDetail(
                claim_id=db_claim.id,
                tooth_number=dental_data.get('tooth_number'),
                tooth_surface=dental_data.get('tooth_surface'),
                oral_cavity_area=dental_data.get('oral_cavity_area'),
                treatment_plan_sequence=dental_data.get('treatment_plan_sequence'),
                months_of_treatment=dental_data.get('months_of_treatment'),
                prosthetic_replacement=dental_data.get('prosthetic_replacement', False),
                initial_placement_date=dental_data.get('initial_placement_date')
            )
            self.db.add(dental_detail)
        
        self.db.commit()
        self.db.refresh(db_claim)
        
        return db_claim
    
    def validate_claim(self, claim_id: int) -> Dict[str, Any]:
        """Validate a claim and update its status"""
        
        claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise ValueError(f"Claim {claim_id} not found")
        
        # Update status to validating
        claim.status = ClaimStatus.VALIDATING
        self.db.commit()
        
        # Run validation
        validation_result = self.validator.validate_claim(claim)
        
        # Update claim with validation results
        claim.validation_errors = validation_result['errors']
        
        if validation_result['is_valid']:
            claim.status = ClaimStatus.VALIDATED
        else:
            claim.status = ClaimStatus.REJECTED
        
        self.db.commit()
        
        return validation_result
    
    def submit_claim(self, claim_id: int) -> bool:
        """Submit validated claim to payer"""
        
        claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise ValueError(f"Claim {claim_id} not found")
        
        if claim.status != ClaimStatus.VALIDATED:
            raise ValueError(f"Claim {claim_id} must be validated before submission")
        
        # Generate outbound EDI (simplified)
        edi_content = self._generate_outbound_edi(claim)
        
        # Submit via configured transmission method
        # This would integrate with actual transmission services
        success = self._transmit_to_payer(claim, edi_content)
        
        if success:
            claim.status = ClaimStatus.SENT
            claim.submitted_at = datetime.utcnow()
            self.db.commit()
        
        return success
    
    def process_835_remittance(self, edi_content: str) -> List[int]:
        """Process 835 remittance advice and update claims"""
        
        # Parse 835 EDI content (simplified)
        remittance_data = self._parse_835_content(edi_content)
        
        updated_claims = []
        
        for payment in remittance_data.get('payments', []):
            claim_number = payment.get('claim_number')
            claim = self.db.query(Claim).filter(Claim.claim_number == claim_number).first()
            
            if claim:
                claim.status = ClaimStatus.PAID if payment.get('paid_amount', 0) > 0 else ClaimStatus.DENIED
                claim.allowed_amount = Decimal(str(payment.get('allowed_amount', 0)))
                claim.paid_amount = Decimal(str(payment.get('paid_amount', 0)))
                claim.patient_responsibility = Decimal(str(payment.get('patient_responsibility', 0)))
                claim.processed_at = datetime.utcnow()
                
                updated_claims.append(claim.id)
        
        self.db.commit()
        return updated_claims
    
    def _map_edi_to_claim(self, edi_claim: Dict[str, Any], claim_type: ClaimType, payer_id: int) -> Dict[str, Any]:
        """Map parsed EDI claim to our claim structure"""
        
        claim_data = {
            'patient_first_name': edi_claim.get('patient_first_name', ''),
            'patient_last_name': edi_claim.get('patient_last_name', ''),
            'patient_id': edi_claim.get('patient_id', ''),
            'provider_name': edi_claim.get('provider_name', ''),
            'provider_npi': edi_claim.get('provider_npi', ''),
            'total_charge': edi_claim.get('total_charge', 0),
            'service_lines': []
        }
        
        # Convert service lines
        for i, line in enumerate(edi_claim.get('service_lines', []), 1):
            service_line = {
                'line_number': i,
                'procedure_code': line.get('procedure_code', ''),
                'charge_amount': line.get('charge_amount', 0),
                'units': line.get('units', 1),
                'service_date': datetime.now(),  # Should parse from DTP segments
                'modifier_1': line.get('modifier_1'),
                'modifier_2': line.get('modifier_2')
            }
            
            # Add tooth information for dental claims
            if claim_type == ClaimType.DENTAL:
                service_line['tooth_surface'] = line.get('tooth_surface')
            
            claim_data['service_lines'].append(service_line)
        
        # Add dental details if present
        if claim_type == ClaimType.DENTAL and 'dental_details' in edi_claim:
            claim_data['dental_details'] = edi_claim['dental_details']
        
        return claim_data
    
    def _generate_claim_number(self) -> str:
        """Generate unique claim number"""
        import uuid
        return f"CLM{str(uuid.uuid4())[:8].upper()}"
    
    def _generate_outbound_edi(self, claim: Claim) -> str:
        """Generate outbound EDI content for claim submission"""
        # This is a simplified version - real implementation would be much more complex
        return f"ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*^*00501*000000001*0*P*:~"
    
    def _transmit_to_payer(self, claim: Claim, edi_content: str) -> bool:
        """Transmit claim to payer via configured method"""
        # This would implement actual transmission logic (FTP, AS2, API)
        # For now, just simulate success
        return True
    
    def _parse_835_content(self, edi_content: str) -> Dict[str, Any]:
        """Parse 835 remittance advice EDI content"""
        # Simplified 835 parsing - real implementation would be much more complex
        return {
            'payments': [
                {
                    'claim_number': 'CLM12345678',
                    'allowed_amount': 100.00,
                    'paid_amount': 80.00,
                    'patient_responsibility': 20.00
                }
            ]
        }
