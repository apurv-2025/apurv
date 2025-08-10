# File: app/services/edi_278_service.py - EDI 278 Prior Authorization Service
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Any, Tuple, List
import logging

from app.core.config import settings
from app.core.exceptions import EDIException
from app.schemas.prior_authorization import (
    PriorAuthorizationRequestCreate, 
    AuthorizationDecision,
    ResponseCode
)

logger = logging.getLogger(__name__)


class EDI278Service:
    """Service for handling EDI 278 Prior Authorization transactions."""
    
    def __init__(self):
        self.submitter_id = settings.EDI_SUBMITTER_ID
        self.receiver_id = settings.EDI_RECEIVER_ID
    
    def generate_control_numbers(self) -> Tuple[str, str, str]:
        """Generate control numbers for EDI transactions."""
        interchange_control_num = str(uuid.uuid4().int)[:9]
        group_control_num = str(uuid.uuid4().int)[:9]
        transaction_control_num = str(uuid.uuid4().int)[:9]
        
        return interchange_control_num, group_control_num, transaction_control_num
    
    def generate_edi_278_request(self, request_data: PriorAuthorizationRequestCreate) -> Tuple[str, str, Dict[str, str]]:
        """Generate EDI 278 Prior Authorization Request."""
        try:
            logger.info(f"Generating EDI 278 request for patient: {request_data.patient_first_name} {request_data.patient_last_name}")
            
            # Generate control numbers
            interchange_control_num, group_control_num, transaction_control_num = self.generate_control_numbers()
            
            # Current timestamp
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M")
            
            # Format dates
            dob_formatted = request_data.patient_dob.strftime("%Y%m%d")
            service_date_from = request_data.service_date_from.strftime("%Y%m%d")
            service_date_to = (request_data.service_date_to or request_data.service_date_from).strftime("%Y%m%d")
            
            # Build EDI 278 segments
            segments = []
            
            # ISA - Interchange Control Header
            segments.append(
                f"ISA*00*          *00*          *ZZ*{self.submitter_id:<15}*ZZ*{self.receiver_id:<15}*{current_date}*{current_time}*^*00501*{interchange_control_num}*0*T*:~"
            )
            
            # GS - Functional Group Header
            segments.append(
                f"GS*HI*{self.submitter_id}*{self.receiver_id}*{current_date}*{current_time}*{group_control_num}*X*005010X217~"
            )
            
            # ST - Transaction Set Header
            segments.append(
                f"ST*278*{transaction_control_num}*005010X217~"
            )
            
            # BHT - Beginning of Hierarchical Transaction
            segments.append(
                f"BHT*0007*{request_data.request_type.value}*{transaction_control_num}*{current_date}*{current_time}~"
            )
            
            # HL - Hierarchical Level (Utilization Management Organization)
            segments.append("HL*1**20*1~")
            
            # NM1 - Utilization Management Organization Name
            segments.append(f"NM1*X3*2*{self.receiver_id}*****46*{self.receiver_id}~")
            
            # HL - Hierarchical Level (Requester)
            segments.append("HL*2*1*21*1~")
            
            # NM1 - Requester Name
            segments.append(f"NM1*1P*2*{request_data.requesting_provider_name or 'PROVIDER'}*****XX*{request_data.requesting_provider_npi}~")
            
            # HL - Hierarchical Level (Patient)
            segments.append("HL*3*2*22*1~")
            
            # NM1 - Patient Name
            segments.append(
                f"NM1*QC*1*{request_data.patient_last_name}*{request_data.patient_first_name}*****MI*{request_data.member_id}~"
            )
            
            # DMG - Patient Demographics
            segments.append(f"DMG*D8*{dob_formatted}*{request_data.patient_gender.value}~")
            
            # HL - Hierarchical Level (Service)
            segments.append("HL*4*3*23*0~")
            
            # TRN - Trace Number
            segments.append(f"TRN*1*{transaction_control_num}*{self.submitter_id}~")
            
            # UM - Utilization Management
            segments.append(f"UM*{request_data.certification_type.value}*{request_data.service_type_code or '1'}~")
            
            # DTP - Service Date(s)
            if service_date_from == service_date_to:
                segments.append(f"DTP*472*D8*{service_date_from}~")
            else:
                segments.append(f"DTP*472*RD8*{service_date_from}-{service_date_to}~")
            
            # Add diagnosis codes
            if request_data.diagnosis_codes:
                diagnosis_string = "*".join([f"ABK:{diag.code}" for diag in request_data.diagnosis_codes[:12]])  # Max 12 diagnoses
                segments.append(f"HI*{diagnosis_string}~")
            
            # Add procedure codes
            for i, procedure in enumerate(request_data.procedure_codes[:6], 1):  # Max 6 procedures
                segments.append(f"SV1*HC:{procedure.code}*{procedure.units or 1}*UN~")
            
            # PWK - Paperwork (if supporting documentation)
            if request_data.clinical_information:
                segments.append("PWK*OZ*FT~")
                segments.append(f"MSG*{request_data.medical_necessity[:264]}~")  # Max 264 chars
            
            # SE - Transaction Set Trailer
            segment_count = len(segments) + 1
            segments.append(f"SE*{segment_count}*{transaction_control_num}~")
            
            # GE - Functional Group Trailer
            segments.append(f"GE*1*{group_control_num}~")
            
            # IEA - Interchange Control Trailer
            segments.append(f"IEA*1*{interchange_control_num}~")
            
            edi_278_content = '\n'.join(segments)
            
            control_numbers = {
                'interchange_control_number': interchange_control_num,
                'group_control_number': group_control_num,
                'transaction_control_number': transaction_control_num
            }
            
            logger.info(f"EDI 278 request generated successfully with transaction ID: {transaction_control_num}")
            return edi_278_content, transaction_control_num, control_numbers
            
        except Exception as e:
            logger.error(f"Error generating EDI 278 request: {str(e)}")
            raise EDIException(f"Failed to generate EDI 278 request: {str(e)}", "278")
    
    def generate_edi_278_response(self, request_id: str, decision: AuthorizationDecision) -> str:
        """Generate EDI 278 Prior Authorization Response."""
        try:
            logger.info(f"Generating EDI 278 response for request: {request_id}")
            
            # Generate control numbers
            interchange_control_num, group_control_num, transaction_control_num = self.generate_control_numbers()
            
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M")
            
            # Build EDI 278 response segments
            segments = []
            
            # ISA - Interchange Control Header
            segments.append(
                f"ISA*00*          *00*          *ZZ*{self.receiver_id:<15}*ZZ*{self.submitter_id:<15}*{current_date}*{current_time}*^*00501*{interchange_control_num}*0*T*:~"
            )
            
            # GS - Functional Group Header
            segments.append(
                f"GS*HI*{self.receiver_id}*{self.submitter_id}*{current_date}*{current_time}*{group_control_num}*X*005010X217~"
            )
            
            # ST - Transaction Set Header
            segments.append(
                f"ST*278*{transaction_control_num}*005010X217~"
            )
            
            # BHT - Beginning of Hierarchical Transaction
            segments.append(
                f"BHT*0007*11*{request_id}*{current_date}*{current_time}~"
            )
            
            # HL - Hierarchical Level (Utilization Management Organization)
            segments.append("HL*1**20*1~")
            
            # NM1 - Utilization Management Organization Name
            segments.append(f"NM1*X3*2*{self.receiver_id}*****46*{self.receiver_id}~")
            
            # HL - Hierarchical Level (Service)
            segments.append("HL*2*1*23*0~")
            
            # TRN - Trace Number
            segments.append(f"TRN*2*{request_id}*{self.receiver_id}~")
            
            # UM - Utilization Management Response
            segments.append(f"UM*{decision.response_code.value}*1~")
            
            # REF - Authorization Number (if approved)
            if decision.authorization_number:
                segments.append(f"REF*BB*{decision.authorization_number}~")
            
            # DTP - Effective Date
            if decision.effective_date:
                effective_date = decision.effective_date.strftime("%Y%m%d")
                segments.append(f"DTP*007*D8*{effective_date}~")
            
            # DTP - Expiration Date
            if decision.expiration_date:
                expiration_date = decision.expiration_date.strftime("%Y%m%d")
                segments.append(f"DTP*036*D8*{expiration_date}~")
            
            # SV1 - Professional Service (approved units)
            if decision.units_approved:
                segments.append(f"SV1*HC:99999*{decision.units_approved}*UN~")
            
            # MSG - Decision Reason
            if decision.decision_reason:
                segments.append(f"MSG*{decision.decision_reason[:264]}~")
            
            # Additional Information Required
            if decision.additional_information_required:
                segments.append("PWK*CT*FT~")
                segments.append(f"MSG*{decision.additional_information_required[:264]}~")
            
            # SE - Transaction Set Trailer
            segment_count = len(segments) + 1
            segments.append(f"SE*{segment_count}*{transaction_control_num}~")
            
            # GE - Functional Group Trailer
            segments.append(f"GE*1*{group_control_num}~")
            
            # IEA - Interchange Control Trailer
            segments.append(f"IEA*1*{interchange_control_num}~")
            
            edi_278_response = '\n'.join(segments)
            
            logger.info(f"EDI 278 response generated successfully for request: {request_id}")
            return edi_278_response
            
        except Exception as e:
            logger.error(f"Error generating EDI 278 response: {str(e)}")
            raise EDIException(f"Failed to generate EDI 278 response: {str(e)}", "278")
    
    def validate_edi_278(self, edi_content: str) -> bool:
        """Validate EDI 278 format and required segments."""
        try:
            segments = edi_content.split('~')
            required_segments = ['ISA', 'GS', 'ST', 'BHT', 'HL', 'NM1', 'UM', 'SE', 'GE', 'IEA']
            
            found_segments = set()
            for segment in segments:
                if segment.strip():
                    segment_id = segment.split('*')[0]
                    found_segments.add(segment_id)
            
            missing_segments = set(required_segments) - found_segments
            if missing_segments:
                logger.warning(f"Missing required segments: {missing_segments}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating EDI 278: {str(e)}")
            return False
