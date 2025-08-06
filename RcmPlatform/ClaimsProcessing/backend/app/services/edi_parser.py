# =============================================================================
# FILE: backend/app/services/edi_parser.py
# =============================================================================
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..database.models import ClaimType

class EDIParser:
    """Enhanced EDI X12 parser for 837 files"""
    
    def __init__(self):
        self.segment_terminator = '~'
        self.element_separator = '*'
        self.component_separator = '^'
    
    def parse_837_file(self, edi_content: str) -> Dict[str, Any]:
        """Parse 837 EDI file and extract claim data"""
        segments = self._split_segments(edi_content)
        
        # Determine claim type from GS segment
        claim_type = self._determine_claim_type(segments)
        
        # Parse header information
        header_info = self._parse_header(segments)
        
        # Parse claims
        claims = self._parse_claims(segments, claim_type)
        
        return {
            'claim_type': claim_type,
            'header_info': header_info,
            'claims': claims,
            'raw_edi': edi_content
        }
    
    def _split_segments(self, edi_content: str) -> List[str]:
        """Split EDI content into segments"""
        # Remove any whitespace and split by segment terminator
        clean_content = edi_content.strip().replace('\n', '').replace('\r', '')
        return [seg.strip() for seg in clean_content.split(self.segment_terminator) if seg.strip()]
    
    def _determine_claim_type(self, segments: List[str]) -> ClaimType:
        """Determine claim type from GS segment"""
        for segment in segments:
            if segment.startswith('GS'):
                elements = segment.split(self.element_separator)
                if len(elements) > 1:
                    functional_group = elements[1]
                    if functional_group == 'HC':  # Healthcare Claim
                        # Look at version to determine type
                        if len(elements) > 7:
                            version = elements[7]
                            if 'D' in version:
                                return ClaimType.DENTAL
                            elif 'P' in version:
                                return ClaimType.PROFESSIONAL
                            elif 'I' in version:
                                return ClaimType.INSTITUTIONAL
        
        return ClaimType.PROFESSIONAL  # Default
    
    def _parse_header(self, segments: List[str]) -> Dict[str, Any]:
        """Parse ISA and GS header segments"""
        header = {}
        
        for segment in segments:
            if segment.startswith('ISA'):
                elements = segment.split(self.element_separator)
                if len(elements) >= 16:
                    header['interchange_control_number'] = elements[13]
                    header['interchange_date'] = elements[9]
                    header['interchange_time'] = elements[10]
                    
            elif segment.startswith('GS'):
                elements = segment.split(self.element_separator)
                if len(elements) >= 8:
                    header['functional_group_control_number'] = elements[6]
                    header['application_sender_code'] = elements[2]
                    header['application_receiver_code'] = elements[3]
        
        return header
    
    def _parse_claims(self, segments: List[str], claim_type: ClaimType) -> List[Dict[str, Any]]:
        """Parse individual claims from segments"""
        claims = []
        current_claim = None
        current_service_lines = []
        
        i = 0
        while i < len(segments):
            segment = segments[i]
            
            if segment.startswith('CLM'):
                # Start of new claim
                if current_claim:
                    current_claim['service_lines'] = current_service_lines
                    claims.append(current_claim)
                
                current_claim = self._parse_clm_segment(segment)
                current_service_lines = []
                
                # Add claim type specific details
                if claim_type == ClaimType.DENTAL:
                    current_claim['dental_details'] = self._parse_dental_details(segments, i)
            
            elif segment.startswith('NM1') and current_claim:
                # Name segments for patient, provider, etc.
                self._parse_nm1_segment(segment, current_claim, segments, i)
            
            elif segment.startswith('SBR') and current_claim:
                # Subscriber information
                self._parse_sbr_segment(segment, current_claim)
            
            elif segment.startswith('SV1') and current_claim:
                # Professional service line
                service_line = self._parse_sv1_segment(segment)
                current_service_lines.append(service_line)
            
            elif segment.startswith('SV3') and current_claim and claim_type == ClaimType.DENTAL:
                # Dental service line
                service_line = self._parse_sv3_segment(segment)
                current_service_lines.append(service_line)
            
            elif segment.startswith('DTP') and current_claim:
                # Date/Time segments
                self._parse_dtp_segment(segment, current_claim, current_service_lines)
            
            i += 1
        
        # Add last claim
        if current_claim:
            current_claim['service_lines'] = current_service_lines
            claims.append(current_claim)
        
        return claims
    
    def _parse_clm_segment(self, segment: str) -> Dict[str, Any]:
        """Parse CLM (Claim Information) segment"""
        elements = segment.split(self.element_separator)
        
        claim = {
            'claim_number': elements[1] if len(elements) > 1 else '',
            'total_charge': float(elements[2]) if len(elements) > 2 and elements[2] else 0.0,
            'place_of_service': elements[5] if len(elements) > 5 else '',
            'claim_frequency_code': elements[6] if len(elements) > 6 else '1',
        }
        
        return claim
    
    def _parse_nm1_segment(self, segment: str, claim: Dict[str, Any], segments: List[str], index: int):
        """Parse NM1 (Name) segments"""
        elements = segment.split(self.element_separator)
        
        if len(elements) < 3:
            return
        
        entity_type = elements[1]
        entity_name_type = elements[2]
        
        if entity_type == 'QC':  # Patient
            claim['patient_last_name'] = elements[3] if len(elements) > 3 else ''
            claim['patient_first_name'] = elements[4] if len(elements) > 4 else ''
            claim['patient_id'] = elements[9] if len(elements) > 9 else ''
        
        elif entity_type == '85':  # Billing Provider
            claim['provider_name'] = elements[3] if len(elements) > 3 else ''
            claim['provider_npi'] = elements[9] if len(elements) > 9 else ''
    
    def _parse_sbr_segment(self, segment: str, claim: Dict[str, Any]):
        """Parse SBR (Subscriber Information) segment"""
        elements = segment.split(self.element_separator)
        
        claim['payer_responsibility'] = elements[1] if len(elements) > 1 else 'P'
        claim['individual_relationship_code'] = elements[2] if len(elements) > 2 else '18'
    
    def _parse_sv1_segment(self, segment: str) -> Dict[str, Any]:
        """Parse SV1 (Professional Service) segment"""
        elements = segment.split(self.element_separator)
        
        # Parse procedure code (may have modifiers)
        procedure_info = elements[1].split(self.component_separator) if len(elements) > 1 else ['']
        
        service_line = {
            'procedure_code': procedure_info[0],
            'modifier_1': procedure_info[1] if len(procedure_info) > 1 else '',
            'modifier_2': procedure_info[2] if len(procedure_info) > 2 else '',
            'charge_amount': float(elements[2]) if len(elements) > 2 and elements[2] else 0.0,
            'units': int(elements[4]) if len(elements) > 4 and elements[4] else 1,
        }
        
        return service_line
    
    def _parse_sv3_segment(self, segment: str) -> Dict[str, Any]:
        """Parse SV3 (Dental Service) segment"""
        elements = segment.split(self.element_separator)
        
        # Parse procedure code and tooth information
        procedure_info = elements[1].split(self.component_separator) if len(elements) > 1 else ['']
        
        service_line = {
            'procedure_code': procedure_info[0],
            'tooth_surface': procedure_info[1] if len(procedure_info) > 1 else '',
            'charge_amount': float(elements[2]) if len(elements) > 2 and elements[2] else 0.0,
            'units': int(elements[4]) if len(elements) > 4 and elements[4] else 1,
        }
        
        return service_line
    
    def _parse_dental_details(self, segments: List[str], start_index: int) -> Dict[str, Any]:
        """Parse dental-specific segments like DN1, DN2"""
        dental_details = {}
        
        # Look for DN1 and DN2 segments after current claim
        for i in range(start_index, min(start_index + 20, len(segments))):
            segment = segments[i]
            
            if segment.startswith('DN1'):
                # Orthodontic information
                elements = segment.split(self.element_separator)
                dental_details['months_of_treatment'] = int(elements[1]) if len(elements) > 1 and elements[1] else None
            
            elif segment.startswith('DN2'):
                # Tooth status information
                elements = segment.split(self.element_separator)
                dental_details['tooth_number'] = elements[1] if len(elements) > 1 else ''
                dental_details['tooth_status'] = elements[2] if len(elements) > 2 else ''
        
        return dental_details
    
    def _parse_dtp_segment(self, segment: str, claim: Dict[str, Any], service_lines: List[Dict[str, Any]]):
        """Parse DTP (Date/Time Period) segments"""
        elements = segment.split(self.element_separator)
        
        if len(elements) < 4:
            return
        
        date_qualifier = elements[1]
        date_format = elements[2]
        date_value = elements[3]
        
        # Convert date based on format
        if date_format == 'D8' and len(date_value) == 8:
            # CCYYMMDD format
            try:
                parsed_date = datetime.strptime(date_value, '%Y%m%d')
                
                if date_qualifier == '472':  # Service Date
                    if service_lines:
                        service_lines[-1]['service_date'] = parsed_date
                elif date_qualifier == '431':  # Onset of Illness
                    claim['illness_onset_date'] = parsed_date
                    
            except ValueError:
                pass  # Invalid date format
