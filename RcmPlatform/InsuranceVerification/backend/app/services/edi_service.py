# File: app/services/edi_service.py
import uuid
from datetime import datetime
from typing import Dict, Any, Tuple
import logging

from app.core.config import settings
from app.core.exceptions import EDIException
from app.schemas.eligibility import EligibilityRequestCreate

logger = logging.getLogger(__name__)


class EDIService:
    """Service for handling EDI 270/271 transactions."""
    
    def __init__(self):
        self.submitter_id = settings.EDI_SUBMITTER_ID
        self.receiver_id = settings.EDI_RECEIVER_ID
    
    def generate_control_numbers(self) -> Tuple[str, str, str]:
        """Generate control numbers for EDI transactions."""
        interchange_control_num = str(uuid.uuid4().int)[:9]
        group_control_num = str(uuid.uuid4().int)[:9]
        transaction_control_num = str(uuid.uuid4().int)[:9]
        
        return interchange_control_num, group_control_num, transaction_control_num
    
    def generate_edi_270(self, request_data: EligibilityRequestCreate) -> Tuple[str, str, Dict[str, str]]:
        """Generate EDI 270 (Eligibility Inquiry) transaction."""
        try:
            logger.info(f"Generating EDI 270 for member: {request_data.member_id}")
            
            # Generate control numbers
            interchange_control_num, group_control_num, transaction_control_num = self.generate_control_numbers()
            
            # Current timestamp
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M")
            
            # Format date of birth
            dob_formatted = request_data.subscriber_dob.strftime("%Y%m%d")
            
            # Build EDI 270 segments
            segments = []
            
            # ISA - Interchange Control Header
            segments.append(
                f"ISA*00*          *00*          *ZZ*{self.submitter_id:<15}*ZZ*{self.receiver_id:<15}*{current_date}*{current_time}*^*00501*{interchange_control_num}*0*T*:~"
            )
            
            # GS - Functional Group Header
            segments.append(
                f"GS*HS*{self.submitter_id}*{self.receiver_id}*{current_date}*{current_time}*{group_control_num}*X*005010X279A1~"
            )
            
            # ST - Transaction Set Header
            segments.append(
                f"ST*270*{transaction_control_num}*005010X279A1~"
            )
            
            # BHT - Beginning of Hierarchical Transaction
            segments.append(
                f"BHT*0022*13*{transaction_control_num}*{current_date}*{current_time}~"
            )
            
            # HL - Information Source Level
            segments.append("HL*1**20*1~")
            
            # PRV - Provider Information (if needed)
            segments.append("PRV*BI*PXC*207Q00000X~")
            
            # NM1 - Information Source Name
            segments.append(f"NM1*PR*2*{request_data.provider_npi}*****PI*{request_data.provider_npi}~")
            
            # HL - Information Receiver Level
            segments.append("HL*2*1*21*1~")
            
            # NM1 - Information Receiver Name (Subscriber)
            segments.append(
                f"NM1*1P*1*{request_data.subscriber_last_name}*{request_data.subscriber_first_name}*****MI*{request_data.member_id}~"
            )
            
            # DMG - Demographic Information
            segments.append(f"DMG*D8*{dob_formatted}~")
            
            # HL - Subscriber Level
            segments.append("HL*3*2*22*0~")
            
            # TRN - Trace Number
            segments.append(f"TRN*1*{transaction_control_num}~")
            
            # EQ - Eligibility or Benefit Inquiry
            segments.append(f"EQ*{request_data.service_type}~")
            
            # SE - Transaction Set Trailer
            segment_count = len(segments) + 1  # +1 for SE segment itself
            segments.append(f"SE*{segment_count}*{transaction_control_num}~")
            
            # GE - Functional Group Trailer
            segments.append(f"GE*1*{group_control_num}~")
            
            # IEA - Interchange Control Trailer
            segments.append(f"IEA*1*{interchange_control_num}~")
            
            edi_270_content = '\n'.join(segments)
            
            control_numbers = {
                'interchange_control_number': interchange_control_num,
                'group_control_number': group_control_num,
                'transaction_control_number': transaction_control_num
            }
            
            logger.info(f"EDI 270 generated successfully with transaction ID: {transaction_control_num}")
            return edi_270_content, transaction_control_num, control_numbers
            
        except Exception as e:
            logger.error(f"Error generating EDI 270: {str(e)}")
            raise EDIException(f"Failed to generate EDI 270: {str(e)}", "270")
    
    def generate_edi_271(self, request_id: str, eligibility_data: Dict[str, Any]) -> str:
        """Generate EDI 271 (Eligibility Response) transaction."""
        try:
            logger.info(f"Generating EDI 271 for request: {request_id}")
            
            # Generate control numbers
            interchange_control_num, group_control_num, transaction_control_num = self.generate_control_numbers()
            
            current_date = datetime.now().strftime("%Y%m%d")
            current_time = datetime.now().strftime("%H%M")
            
            # Determine eligibility status
            eligible_code = "Y" if eligibility_data.get("is_eligible", False) else "N"
            
            # Build EDI 271 segments
            segments = []
            
            # ISA - Interchange Control Header
            segments.append(
                f"ISA*00*          *00*          *ZZ*{self.receiver_id:<15}*ZZ*{self.submitter_id:<15}*{current_date}*{current_time}*^*00501*{interchange_control_num}*0*T*:~"
            )
            
            # GS - Functional Group Header
            segments.append(
                f"GS*HB*{self.receiver_id}*{self.submitter_id}*{current_date}*{current_time}*{group_control_num}*X*005010X279A1~"
            )
            
            # ST - Transaction Set Header
            segments.append(
                f"ST*271*{transaction_control_num}*005010X279A1~"
            )
            
            # BHT - Beginning of Hierarchical Transaction
            segments.append(
                f"BHT*0022*11*{request_id}*{current_date}*{current_time}~"
            )
            
            # HL - Information Source Level
            segments.append("HL*1**20*1~")
            
            # PRV - Provider Information
            segments.append("PRV*BI*PXC*207Q00000X~")
            
            # NM1 - Information Source Name
            segments.append("NM1*PR*2*INSURANCE COMPANY*****PI*12345~")
            
            # HL - Information Receiver Level
            segments.append("HL*2*1*21*1~")
            
            # NM1 - Information Receiver Name
            member_id = eligibility_data.get('member_id', 'UNKNOWN')
            segments.append(f"NM1*1P*1*DOE*JOHN*****MI*{member_id}~")
            
            # N3 - Address Information
            segments.append("N3*123 MAIN ST~")
            
            # N4 - Geographic Location
            segments.append("N4*ANYTOWN*ST*12345~")
            
            # DMG - Demographic Information
            segments.append("DMG*D8*19800101~")
            
            # HL - Subscriber Level
            segments.append("HL*3*2*22*0~")
            
            # TRN - Trace Number
            segments.append(f"TRN*2*{request_id}~")
            
            # EB - Eligibility or Benefit Information
            service_type = eligibility_data.get('service_type', '30')
            segments.append(f"EB*{eligible_code}*{service_type}~")
            
            # MSG - Message Text
            if eligibility_data.get("is_eligible"):
                segments.append("MSG*COVERAGE IS ACTIVE~")
            else:
                segments.append("MSG*COVERAGE NOT FOUND~")
            
            # Add benefit details if available
            if eligibility_data.get("benefits"):
                benefits = eligibility_data["benefits"]
                
                # Add deductible information
                if benefits.get("medical", {}).get("deductible"):
                    segments.append(f"EB*A*30**27*{benefits['medical']['deductible'].replace('$', '')}~")
                
                # Add copay information
                if benefits.get("medical", {}).get("copay"):
                    segments.append(f"EB*B*30**23*{benefits['medical']['copay'].replace('$', '')}~")
            
            # SE - Transaction Set Trailer
            segment_count = len(segments) + 1  # +1 for SE segment itself
            segments.append(f"SE*{segment_count}*{transaction_control_num}~")
            
            # GE - Functional Group Trailer
            segments.append(f"GE*1*{group_control_num}~")
            
            # IEA - Interchange Control Trailer
            segments.append(f"IEA*1*{interchange_control_num}~")
            
            edi_271_content = '\n'.join(segments)
            
            logger.info(f"EDI 271 generated successfully for request: {request_id}")
            return edi_271_content
            
        except Exception as e:
            logger.error(f"Error generating EDI 271: {str(e)}")
            raise EDIException(f"Failed to generate EDI 271: {str(e)}", "271")
    
    def validate_edi_270(self, edi_content: str) -> bool:
        """Validate EDI 270 format and required segments."""
        try:
            segments = edi_content.split('~')
            required_segments = ['ISA', 'GS', 'ST', 'BHT', 'HL', 'NM1', 'EQ', 'SE', 'GE', 'IEA']
            
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
            logger.error(f"Error validating EDI 270: {str(e)}")
            return False
