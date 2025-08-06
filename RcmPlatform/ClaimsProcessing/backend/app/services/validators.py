# =============================================================================
# FILE: backend/app/services/validators.py
# =============================================================================
from typing import Dict, List, Any
from datetime import datetime, timedelta
import re

from ..database.models import Claim, ClaimType

class ClaimValidator:
    """Enhanced claim validation service with dental-specific rules"""
    
    def __init__(self):
        self.cdt_codes = self._load_cdt_codes()
        self.cpt_codes = self._load_cpt_codes()
        self.frequency_rules = self._load_frequency_rules()
    
    def validate_claim(self, claim: Claim) -> Dict[str, Any]:
        """Main validation method"""
        
        errors = []
        warnings = []
        
        # Basic validation
        errors.extend(self._validate_required_fields(claim))
        errors.extend(self._validate_npi(claim.provider_npi))
        errors.extend(self._validate_patient_info(claim))
        
        # Service line validation
        for service_line in claim.service_lines:
            line_errors = self._validate_service_line(service_line, claim.claim_type)
            errors.extend(line_errors)
        
        # Claim type specific validation
        if claim.claim_type == ClaimType.DENTAL:
            errors.extend(self._validate_dental_claim(claim))
        elif claim.claim_type == ClaimType.PROFESSIONAL:
            errors.extend(self._validate_professional_claim(claim))
        elif claim.claim_type == ClaimType.INSTITUTIONAL:
            errors.extend(self._validate_institutional_claim(claim))
        
        # Frequency validation
        warnings.extend(self._validate_frequencies(claim))
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_required_fields(self, claim: Claim) -> List[str]:
        """Validate required claim fields"""
        errors = []
        
        if not claim.patient_first_name:
            errors.append("Patient first name is required")
        
        if not claim.patient_last_name:
            errors.append("Patient last name is required")
        
        if not claim.provider_npi:
            errors.append("Provider NPI is required")
        
        if not claim.provider_name:
            errors.append("Provider name is required")
        
        if claim.total_charge <= 0:
            errors.append("Total charge must be greater than 0")
        
        if not claim.service_lines:
            errors.append("At least one service line is required")
        
        return errors
    
    def _validate_npi(self, npi: str) -> List[str]:
        """Validate NPI format and check digit"""
        errors = []
        
        if not npi:
            return ["NPI is required"]
        
        # Remove any non-digits
        npi_digits = re.sub(r'\D', '', npi)
        
        if len(npi_digits) != 10:
            errors.append("NPI must be 10 digits")
            return errors
        
        # Luhn algorithm check
        if not self._luhn_check(npi_digits):
            errors.append("Invalid NPI check digit")
        
        return errors
    
    def _validate_patient_info(self, claim: Claim) -> List[str]:
        """Validate patient information"""
        errors = []
        
        if claim.patient_dob:
            # Check if patient is not from the future
            if claim.patient_dob > datetime.now():
                errors.append("Patient date of birth cannot be in the future")
            
            # Check reasonable age limits
            age = (datetime.now() - claim.patient_dob).days / 365.25
            if age > 120:
                errors.append("Patient age seems unrealistic (over 120 years)")
        
        return errors
    
    def _validate_service_line(self, service_line, claim_type: ClaimType) -> List[str]:
        """Validate individual service line"""
        errors = []
        
        # Procedure code validation
        if claim_type == ClaimType.DENTAL:
            if not self._is_valid_cdt_code(service_line.procedure_code):
                errors.append(f"Invalid CDT code: {service_line.procedure_code}")
        else:
            if not self._is_valid_cpt_code(service_line.procedure_code):
                errors.append(f"Invalid CPT code: {service_line.procedure_code}")
        
        # Charge amount validation
        if service_line.charge_amount <= 0:
            errors.append(f"Service line {service_line.line_number}: charge amount must be greater than 0")
        
        # Units validation
        if service_line.units <= 0:
            errors.append(f"Service line {service_line.line_number}: units must be greater than 0")
        
        # Date validation
        if service_line.service_date_from:
            if service_line.service_date_from > datetime.now():
                errors.append(f"Service line {service_line.line_number}: service date cannot be in the future")
        
        return errors
    
    def _validate_dental_claim(self, claim: Claim) -> List[str]:
        """Dental-specific validation"""
        errors = []
        
        if claim.dental_details:
            dental = claim.dental_details
            
            # Tooth number validation
            if dental.tooth_number:
                if not self._is_valid_tooth_number(dental.tooth_number):
                    errors.append(f"Invalid tooth number: {dental.tooth_number}")
            
            # Tooth surface validation
            if dental.tooth_surface:
                if not self._is_valid_tooth_surface(dental.tooth_surface):
                    errors.append(f"Invalid tooth surface: {dental.tooth_surface}")
        
        return errors
    
    def _validate_professional_claim(self, claim: Claim) -> List[str]:
        """Professional claim specific validation"""
        errors = []
        
        # Check for required diagnosis codes
        has_diagnosis = any(
            line.diagnosis_code_1 for line in claim.service_lines
        )
        
        if not has_diagnosis:
            errors.append("At least one service line must have a diagnosis code")
        
        return errors
    
    def _validate_institutional_claim(self, claim: Claim) -> List[str]:
        """Institutional claim specific validation"""
        errors = []
        
        # Institutional claims typically require revenue codes
        # This would be more complex in a real implementation
        
        return errors
    
    def _validate_frequencies(self, claim: Claim) -> List[str]:
        """Validate procedure frequency limits"""
        warnings = []
        
        for service_line in claim.service_lines:
            procedure_code = service_line.procedure_code
            
            if procedure_code in self.frequency_rules:
                rule = self.frequency_rules[procedure_code]
                # This would check against historical claims for this patient
                # For now, just add a warning for demonstration
                warnings.append(f"Frequency check needed for {procedure_code}: {rule['description']}")
        
        return warnings
    
    def _is_valid_cdt_code(self, code: str) -> bool:
        """Validate CDT (dental) procedure code"""
        if not code:
            return False
        
        # CDT codes are D followed by 4 digits
        if not re.match(r'^D\d{4}$', code):
            return False
        
        # Check against loaded CDT codes (simplified)
        return code in self.cdt_codes
    
    def _is_valid_cpt_code(self, code: str) -> bool:
        """Validate CPT (medical) procedure code"""
        if not code:
            return False
        
        # CPT codes are 5 digits
        if not re.match(r'^\d{5}$', code):
            return False
        
        return code in self.cpt_codes
    
    def _is_valid_tooth_number(self, tooth_number: str) -> bool:
        """Validate tooth number using Universal Numbering System"""
        if not tooth_number:
            return True  # Optional field
        
        # Adult teeth: 1-32
        # Primary teeth: A-T
        if tooth_number.isdigit():
            return 1 <= int(tooth_number) <= 32
        elif tooth_number.isalpha() and len(tooth_number) == 1:
            return tooth_number.upper() in 'ABCDEFGHIJKLMNOPQRST'
        
        return False
    
    def _is_valid_tooth_surface(self, surface: str) -> bool:
        """Validate tooth surface codes"""
        if not surface:
            return True  # Optional field
        
        valid_surfaces = {'M', 'O', 'D', 'L', 'B', 'I', 'F'}
        return all(s.upper() in valid_surfaces for s in surface)
    
    def _luhn_check(self, number: str) -> bool:
        """Luhn algorithm for NPI validation"""
    def _luhn_check(self, number: str) -> bool:
        """Luhn algorithm for NPI validation"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0
    
    def _load_cdt_codes(self) -> set:
        """Load CDT code database (simplified)"""
        # In real implementation, this would load from a database or file
        return {
            'D0120', 'D0140', 'D0150', 'D0160', 'D0170', 'D0180',  # Diagnostic
            'D1110', 'D1120', 'D1206', 'D1208',  # Preventive
            'D2140', 'D2150', 'D2160', 'D2161', 'D2330', 'D2331', 'D2332', 'D2335',  # Restorative
            'D2740', 'D2750', 'D2751', 'D2752',  # Crowns
            'D3220', 'D3240', 'D3310', 'D3320',  # Endodontics
            'D4210', 'D4211', 'D4240', 'D4241',  # Periodontics
            'D7140', 'D7210', 'D7220', 'D7230',  # Oral Surgery
            'D8210', 'D8220', 'D8230', 'D8240',  # Orthodontics
        }
    
    def _load_cpt_codes(self) -> set:
        """Load CPT code database (simplified)"""
        # In real implementation, this would load from a database or file
        return {
            '99201', '99202', '99203', '99204', '99205',  # Office visits
            '99211', '99212', '99213', '99214', '99215',  # Established patient
            '99221', '99222', '99223',  # Hospital visits
            '36415', '85025', '80053', '80061',  # Lab procedures
            '73030', '73060', '73070', '73080',  # Radiology
        }
    
    def _load_frequency_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load procedure frequency rules"""
        return {
            'D1110': {  # Adult prophylaxis
                'frequency': '2 per year',
                'description': 'Routine cleaning - typically 2 per year'
            },
            'D1120': {  # Child prophylaxis
                'frequency': '2 per year',
                'description': 'Child cleaning - typically 2 per year'
            },
            'D0274': {  # Bitewing X-rays
                'frequency': '1 per year',
                'description': 'Bitewing X-rays - typically once per year'
            },
            'D0210': {  # Full mouth X-rays
                'frequency': '1 per 3-5 years',
                'description': 'Full mouth X-rays - typically every 3-5 years'
            }
        }
