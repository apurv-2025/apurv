# Patient Service for Prior Authorization System
# Now uses Patient microservice client instead of local database

from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.patient_client import (
    patient_client, 
    PatientCreate, 
    PatientUpdate, 
    PatientResponse,
    PatientIdentifier,
    PatientTelecom,
    PatientAddress
)
from app.schemas.patient_information import (
    PatientInformationCreate,
    PatientInformationUpdate,
    PatientInformation,
    PatientSummary,
    PatientSearchRequest,
    PatientEDI275Response
)
from app.services.edi_275_service import EDI275Service
import uuid


class PatientService:
    def __init__(self):
        self.edi_service = EDI275Service()

    def _convert_to_patient_create(self, patient_data: PatientInformationCreate) -> PatientCreate:
        """Convert Prior Authorization patient data to Patient microservice format"""
        # Convert identifiers
        identifiers = []
        if patient_data.member_id_primary:
            identifiers.append(PatientIdentifier(
                system="member-id",
                value=patient_data.member_id_primary,
                use="official"
            ))
        
        # Convert telecom
        telecom = []
        if patient_data.phone_mobile:
            telecom.append(PatientTelecom(
                system="phone",
                value=patient_data.phone_mobile,
                use="mobile"
            ))
        if patient_data.phone_home:
            telecom.append(PatientTelecom(
                system="phone",
                value=patient_data.phone_home,
                use="home"
            ))
        if patient_data.email:
            telecom.append(PatientTelecom(
                system="email",
                value=patient_data.email,
                use="home"
            ))
        
        # Convert addresses
        addresses = []
        if patient_data.address_line1 or patient_data.city or patient_data.state:
            addresses.append(PatientAddress(
                use="home",
                type="postal",
                line=[patient_data.address_line1] if patient_data.address_line1 else None,
                city=patient_data.city,
                state=patient_data.state,
                postal_code=patient_data.zip_code,
                country="US"
            ))
        
        return PatientCreate(
            fhir_id=f"PAT{uuid.uuid4().hex[:8].upper()}",
            family_name=patient_data.last_name,
            given_names=[patient_data.first_name] if patient_data.first_name else None,
            identifiers=identifiers,
            telecom=telecom,
            addresses=addresses,
            gender=patient_data.gender.lower() if patient_data.gender else None,
            birth_date=patient_data.date_of_birth,
            active=True
        )

    def _convert_to_patient_update(self, patient_update: PatientInformationUpdate) -> PatientUpdate:
        """Convert Prior Authorization patient update to Patient microservice format"""
        update_data = {}
        
        if patient_update.first_name is not None or patient_update.last_name is not None:
            given_names = [patient_update.first_name] if patient_update.first_name else None
            update_data["given_names"] = given_names
            update_data["family_name"] = patient_update.last_name
        
        # Convert telecom updates
        telecom = []
        if patient_update.phone_mobile:
            telecom.append(PatientTelecom(
                system="phone",
                value=patient_update.phone_mobile,
                use="mobile"
            ))
        if patient_update.phone_home:
            telecom.append(PatientTelecom(
                system="phone",
                value=patient_update.phone_home,
                use="home"
            ))
        if patient_update.email:
            telecom.append(PatientTelecom(
                system="email",
                value=patient_update.email,
                use="home"
            ))
        
        if telecom:
            update_data["telecom"] = telecom
        
        # Convert address updates
        if any([patient_update.address_line1, patient_update.city, patient_update.state]):
            addresses = [PatientAddress(
                use="home",
                type="postal",
                line=[patient_update.address_line1] if patient_update.address_line1 else None,
                city=patient_update.city,
                state=patient_update.state,
                postal_code=patient_update.zip_code,
                country="US"
            )]
            update_data["addresses"] = addresses
        
        return PatientUpdate(**update_data)

    def _convert_from_patient_response(self, patient: PatientResponse) -> PatientInformation:
        """Convert Patient microservice response to Prior Authorization format"""
        # Extract member ID from identifiers
        member_id = None
        if patient.identifiers:
            for identifier in patient.identifiers:
                if identifier.get('system') == 'member-id':
                    member_id = identifier.get('value')
                    break
        
        # Extract contact information from telecom
        phone_mobile = None
        phone_home = None
        email = None
        if patient.telecom:
            for contact in patient.telecom:
                if contact.get('system') == 'phone':
                    if contact.get('use') == 'mobile':
                        phone_mobile = contact.get('value')
                    elif contact.get('use') == 'home':
                        phone_home = contact.get('value')
                elif contact.get('system') == 'email':
                    email = contact.get('value')
        
        # Extract address information
        address_line1 = None
        city = None
        state = None
        zip_code = None
        if patient.addresses:
            for address in patient.addresses:
                if address.get('use') == 'home':
                    lines = address.get('line', [])
                    address_line1 = lines[0] if lines else None
                    city = address.get('city')
                    state = address.get('state')
                    zip_code = address.get('postal_code')
                    break
        
        return PatientInformation(
            id=patient.id,
            patient_id=patient.fhir_id,
            first_name=patient.given_names[0] if patient.given_names else None,
            last_name=patient.family_name,
            date_of_birth=patient.birth_date,
            gender=patient.gender.upper() if patient.gender else None,
            address_line1=address_line1,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_mobile=phone_mobile,
            phone_home=phone_home,
            email=email,
            member_id_primary=member_id,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )

    def create_patient(self, db: Session, patient_data: PatientInformationCreate) -> PatientInformation:
        """Create a new patient via Patient microservice"""
        try:
            # Convert to Patient microservice format
            patient_create = self._convert_to_patient_create(patient_data)
            
            # Create patient in Patient microservice
            patient_response = patient_client.create_patient(patient_create)
            
            # Convert back to Prior Authorization format
            return self._convert_from_patient_response(patient_response)
        except Exception as e:
            raise Exception(f"Failed to create patient: {str(e)}")

    def get_patient(self, db: Session, patient_id: str) -> Optional[PatientInformation]:
        """Get patient by ID from Patient microservice"""
        try:
            patient_response = patient_client.get_patient(patient_id)
            if patient_response:
                return self._convert_from_patient_response(patient_response)
            return None
        except Exception as e:
            raise Exception(f"Failed to get patient: {str(e)}")

    def update_patient(self, db: Session, patient_id: str, patient_update: PatientInformationUpdate) -> Optional[PatientInformation]:
        """Update patient information via Patient microservice"""
        try:
            # Convert to Patient microservice format
            update_data = self._convert_to_patient_update(patient_update)
            
            # Update patient in Patient microservice
            patient_response = patient_client.update_patient(patient_id, update_data)
            if patient_response:
                return self._convert_from_patient_response(patient_response)
            return None
        except Exception as e:
            raise Exception(f"Failed to update patient: {str(e)}")

    def get_patient_by_member_id(self, db: Session, member_id: str) -> Optional[PatientInformation]:
        """Get patient by member ID from Patient microservice"""
        try:
            patient_response = patient_client.get_patient_by_identifier(member_id, "member-id")
            if patient_response:
                return self._convert_from_patient_response(patient_response)
            return None
        except Exception as e:
            raise Exception(f"Failed to get patient by member ID: {str(e)}")

    def search_patients(
        self, 
        db: Session, 
        search_request: PatientSearchRequest
    ) -> List[PatientSummary]:
        """Search patients via Patient microservice"""
        try:
            # Convert search request to Patient microservice format
            if search_request.first_name or search_request.last_name:
                patients = patient_client.search_patients_by_name(
                    family_name=search_request.last_name,
                    given_name=search_request.first_name,
                    limit=search_request.limit
                )
            else:
                patients = patient_client.search_patients(
                    skip=search_request.offset,
                    limit=search_request.limit
                )
            
            # Convert to Prior Authorization format
            return [
                PatientSummary(
                    id=patient.id,
                    patient_id=patient.fhir_id,
                    first_name=patient.given_names[0] if patient.given_names else None,
                    last_name=patient.family_name,
                    date_of_birth=patient.birth_date,
                    gender=patient.gender.upper() if patient.gender else None,
                    member_id_primary=None,  # Would need to extract from identifiers
                    city=None,  # Would need to extract from addresses
                    state=None,  # Would need to extract from addresses
                    created_at=patient.created_at
                )
                for patient in patients
            ]
        except Exception as e:
            raise Exception(f"Failed to search patients: {str(e)}")

    def generate_edi_275(self, db: Session, patient_id: str) -> PatientEDI275Response:
        """Generate EDI 275 for patient from Patient microservice"""
        try:
            patient = self.get_patient(db, patient_id)
            if not patient:
                raise ValueError(f"Patient {patient_id} not found")
            
            edi_content = self.edi_service.generate_edi_275(patient)
            
            return PatientEDI275Response(
                patient_id=patient_id,
                edi_275=edi_content,
                message="EDI 275 generated successfully",
                generated_at=patient.created_at
            )
        except Exception as e:
            raise Exception(f"Failed to generate EDI 275: {str(e)}")


# Create singleton instance
patient_service = PatientService() 