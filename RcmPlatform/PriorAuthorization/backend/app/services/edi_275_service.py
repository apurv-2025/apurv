# File: app/services/edi_275_service.py - EDI 275 Patient Information Service
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple
import logging

from app.core.config import settings
from app.core.exceptions import EDIException
from app.schemas.patient_information import PatientInformationCreate

logger = logging.getLogger(__name__)


class EDI275Service:
    """Service for handling EDI 275 Patient Information transactions."""
    
    def __init__(self):
        self.submitter_id = settings.EDI_SUBMITTER_ID
        self.receiver_id = settings.EDI_RECEIVER_ID
    
    def generate_control_numbers(self) -> Tuple[str, str, str]:
        """Generate control numbers for EDI transactions."""
        interchange_control_num = str(uuid.uuid4().int)[:9]
        group_control_num = str(uuid.uuid4().int)[:9]
        transaction_control_num = str(uuid.uuid4().int)[:9]
        
        return interchange_control_num, group_control_num, transaction_control_num
    
    def generate_edi_275(self, patient_data: PatientInformationCreate) -> Tuple[str, str]:
        """Generate EDI 275 Patient Information transaction."""
        try:
            logger.info(f"Generating EDI 275 for patient: {patient_data.first_name} {patient_data.last_name}")
            
            # Generate control numbers
            interchange_control_num, group_control_num, transaction_control_num = self.generate_control_numbers()
            
            # Current timestamp
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M")
            
            # Format date of birth
            dob_formatted = patient_data.date_of_birth.strftime("%Y%m%d")
            
            # Build EDI 275 segments
            segments = []
            
            # ISA - Interchange Control Header
            segments.append(
                f"ISA*00*          *00*          *ZZ*{self.submitter_id:<15}*ZZ*{self.receiver_id:<15}*{current_date}*{current_time}*^*00501*{interchange_control_num}*0*T*:~"
            )
            
            # GS - Functional Group Header
            segments.append(
                f"GS*HR*{self.submitter_id}*{self.receiver_id}*{current_date}*{current_time}*{group_control_num}*X*005010X212~"
            )
            
            # ST - Transaction Set Header
            segments.append(
                f"ST*275*{transaction_control_num}*005010X212~"
            )
            
            # BHT - Beginning of Hierarchical Transaction
            segments.append(
                f"BHT*0010*00*{transaction_control_num}*{current_date}*{current_time}~"
            )
            
            # HL - Hierarchical Level (Information Source)
            segments.append("HL*1**20*1~")
            
            # NM1 - Information Source Name
            segments.append(f"NM1*PR*2*{self.submitter_id}*****PI*{self.submitter_id}~")
            
            # HL - Hierarchical Level (Information Receiver)
            segments.append("HL*2*1*21*1~")
            
            # NM1 - Information Receiver Name
            segments.append(f"NM1*41*2*{self.receiver_id}*****46*{self.receiver_id}~")
            
            # HL - Hierarchical Level (Patient)
            segments.append("HL*3*2*22*0~")
            
            # NM1 - Patient Name
            middle_initial = patient_data.middle_name[0] if patient_data.middle_name else ""
            segments.append(
                f"NM1*QC*1*{patient_data.last_name}*{patient_data.first_name}*{middle_initial}***MI*{patient_data.member_id_primary or 'UNKNOWN'}~"
            )
            
            # N3 - Patient Address
            if patient_data.address_line1:
                if patient_data.address_line2:
                    segments.append(f"N3*{patient_data.address_line1}*{patient_data.address_line2}~")
                else:
                    segments.append(f"N3*{patient_data.address_line1}~")
            
            # N4 - Patient Geographic Location
            if patient_data.city and patient_data.state:
                segments.append(f"N4*{patient_data.city}*{patient_data.state}*{patient_data.zip_code or ''}~")
            
            # DMG - Patient Demographics
            segments.append(f"DMG*D8*{dob_formatted}*{patient_data.gender.value}~")
            
            # PER - Patient Contact Information
            contact_info = []
            if patient_data.phone_home:
                contact_info.extend(["HP", patient_data.phone_home])
            if patient_data.phone_work:
                contact_info.extend(["WP", patient_data.phone_work])
            if patient_data.email:
                contact_info.extend(["EM", patient_data.email])
            
            if contact_info:
                contact_string = "*".join(contact_info)
                segments.append(f"PER*IC**{contact_string}~")
            
            # INS - Patient Insurance Information
            if patient_data.primary_insurance:
                segments.append("INS*Y*18*001*25*A~")
                
                # NM1 - Insurance Carrier Name
                segments.append(f"NM1*IN*2*{patient_data.primary_insurance.carrier_name}~")
                
                # REF - Policy Number
                segments.append(f"REF*1L*{patient_data.primary_insurance.policy_number}~")
                
                # Group Number
                if patient_data.primary_insurance.group_number:
                    segments.append(f"REF*1M*{patient_data.primary_insurance.group_number}~")
            
            # Secondary Insurance
            if patient_data.secondary_insurance:
                segments.append("INS*N*18*002*25*A~")
                segments.append(f"NM1*IN*2*{patient_data.secondary_insurance.carrier_name}~")
                segments.append(f"REF*1L*{patient_data.secondary_insurance.policy_number}~")
            
            # Emergency Contact Information
            if patient_data.emergency_contact:
                segments.append(f"NM1*E1*1*{patient_data.emergency_contact.name}~")
                segments.append(f"PER*IC**HP*{patient_data.emergency_contact.phone}~")
                segments.append(f"REL*{patient_data.emergency_contact.relationship}~")
            
            # Medical Conditions
            if patient_data.medical_conditions:
                condition_codes = []
                for condition in patient_data.medical_conditions[:12]:  # Max 12 conditions
                    if condition.icd_code:
                        condition_codes.append(f"ABK:{condition.icd_code}")
                
                if condition_codes:
                    condition_string = "*".join(condition_codes)
                    segments.append(f"HI*{condition_string}~")
            
            # Allergies (using PWK segment for additional patient information)
            if patient_data.allergies:
                allergy_info = "; ".join([f"{allergy.allergen}" for allergy in patient_data.allergies])
                segments.append("PWK*AL*FT~")
                segments.append(f"MSG*ALLERGIES: {allergy_info[:264]}~")
            
            # Current Medications
            if patient_data.medications:
                med_info = "; ".join([f"{med.name} {med.dosage or ''}" for med in patient_data.medications])
                segments.append("PWK*RX*FT~")
                segments.append(f"MSG*MEDICATIONS: {med_info[:264]}~")
            
            # HIPAA Authorization
            if patient_data.hipaa_authorization:
                consent_date = patient_data.consent_date.strftime("%Y%m%d") if patient_data.consent_date else current_date
                segments.append(f"DTP*090*D8*{consent_date}~")
            
            # SE - Transaction Set Trailer
            segment_count = len(segments) + 1
            segments.append(f"SE*{segment_count}*{transaction_control_num}~")
            
            # GE - Functional Group Trailer
            segments.append(f"GE*1*{group_control_num}~")
            
            # IEA - Interchange Control Trailer
            segments.append(f"IEA*1*{interchange_control_num}~")
            
            edi_275_content = '\n'.join(segments)
            
            logger.info(f"EDI 275 generated successfully with transaction ID: {transaction_control_num}")
            return edi_275_content, transaction_control_num
            
        except Exception as e:
            logger.error(f"Error generating EDI 275: {str(e)}")
            raise EDIException(f"Failed to generate EDI 275: {str(e)}", "275")
    
    def parse_edi_275_response(self, edi_content: str) -> Dict[str, Any]:
        """Parse EDI 275 response to extract patient information."""
        try:
            segments = edi_content.split('~')
            patient_info = {}
            
            for segment in segments:
                if segment.startswith('NM1*QC'):
                    # Patient name segment
                    parts = segment.split('*')
                    if len(parts) >= 6:
                        patient_info['last_name'] = parts[3]
                        patient_info['first_name'] = parts[4]
                        patient_info['middle_name'] = parts[5] if parts[5] else None
                
                elif segment.startswith('DMG'):
                    # Demographics segment
                    parts = segment.split('*')
                    if len(parts) >= 4:
                        patient_info['date_of_birth'] = parts[2]
                        patient_info['gender'] = parts[3]
                
                elif segment.startswith('N3'):
                    # Address segment
                    parts = segment.split('*')
                    patient_info['address_line1'] = parts[1] if len(parts) > 1 else None
                    patient_info['address_line2'] = parts[2] if len(parts) > 2 else None
                
                elif segment.startswith('N4'):
                    # Geographic location segment
                    parts = segment.split('*')
                    if len(parts) >= 4:
                        patient_info['city'] = parts[1]
                        patient_info['state'] = parts[2]
                        patient_info['zip_code'] = parts[3]
            
            return patient_info
            
        except Exception as e:
            logger.error(f"Error parsing EDI 275 response: {str(e)}")
            raise EDIException(f"Failed to parse EDI 275 response: {str(e)}", "275")
