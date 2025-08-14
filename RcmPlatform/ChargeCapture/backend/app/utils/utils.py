# utils.py - Backend utilities
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from decimal import Decimal
import re
import uuid

class ValidationUtils:
    """Utility functions for data validation"""
    
    @staticmethod
    def validate_cpt_code(code: str) -> bool:
        """Validate CPT code format (5 digits)"""
        if not code:
            return False
        return bool(re.match(r'^\d{5}$', code))
    
    @staticmethod
    def validate_icd_code(code: str) -> bool:
        """Validate ICD-10 code format"""
        if not code:
            return False
        # Basic ICD-10 pattern: Letter followed by 2 digits, then optional decimal and additional characters
        return bool(re.match(r'^[A-Z]\d{2}(\.\d{1,4})?$', code))
    
    @staticmethod
    def validate_npi(npi: str) -> bool:
        """Validate NPI (National Provider Identifier) - 10 digits"""
        if not npi:
            return False
        return bool(re.match(r'^\d{10}$', npi))
    
    @staticmethod
    def validate_mrn(mrn: str) -> bool:
        """Validate Medical Record Number format"""
        if not mrn:
            return False
        # Allow alphanumeric with dashes, 3-20 characters
        return bool(re.match(r'^[A-Z0-9\-]{3,20}$', mrn))

class DateUtils:
    """Utility functions for date operations"""
    
    @staticmethod
    def get_date_range(period: str) -> tuple[datetime, datetime]:
        """Get date range for common periods"""
        now = datetime.now()
        
        if period == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'yesterday':
            yesterday = now - timedelta(days=1)
            start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif period == 'this_week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif period == 'last_week':
            start = now - timedelta(days=now.weekday() + 7)
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif period == 'this_month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Get last day of month
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            end = next_month - timedelta(microseconds=1)
        elif period == 'last_month':
            if now.month == 1:
                start = now.replace(year=now.year - 1, month=12, day=1)
            else:
                start = now.replace(month=now.month - 1, day=1)
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(day=1) - timedelta(microseconds=1)
        else:
            # Default to last 30 days
            start = now - timedelta(days=30)
            end = now
        
        return start, end
    
    @staticmethod
    def calculate_business_days(start_date: datetime, end_date: datetime) -> int:
        """Calculate business days between two dates"""
        delta = end_date - start_date
        days = delta.days
        business_days = 0
        
        for i in range(days + 1):
            current_date = start_date + timedelta(days=i)
            if current_date.weekday() < 5:  # Monday=0, Sunday=6
                business_days += 1
        
        return business_days

class ChargeUtils:
    """Utility functions for charge-related operations"""
    
    @staticmethod
    def calculate_charge_amount(cpt_code: str, units: int = 1, payer: str = None) -> Optional[Decimal]:
        """Calculate charge amount based on fee schedule"""
        # This would typically integrate with a fee schedule database
        # For now, return mock amounts based on CPT code
        
        fee_schedule = {
            '99213': Decimal('150.00'),
            '99214': Decimal('200.00'),
            '99215': Decimal('250.00'),
            '99201': Decimal('120.00'),
            '99202': Decimal('160.00'),
            '99203': Decimal('200.00'),
            '99204': Decimal('280.00'),
            '99205': Decimal('350.00'),
            '93306': Decimal('400.00'),  # Echo
            '93015': Decimal('300.00'),  # Stress test
        }
        
        base_amount = fee_schedule.get(cpt_code)
        if base_amount:
            return base_amount * units
        
        return None
    
    @staticmethod
    def format_code_description(code: str, description: str) -> str:
        """Format code and description for display"""
        if description:
            return f"{code} - {description}"
        return code
    
    @staticmethod
    def get_modifier_description(modifier: str) -> str:
        """Get description for common modifiers"""
        modifier_descriptions = {
            '25': 'Significant, separately identifiable E/M service',
            '26': 'Professional component',
            '50': 'Bilateral procedure',
            '51': 'Multiple procedures',
            '52': 'Reduced services',
            '53': 'Discontinued procedure',
            '59': 'Distinct procedural service',
            'LT': 'Left side',
            'RT': 'Right side',
            'TC': 'Technical component'
        }
        return modifier_descriptions.get(modifier, modifier)

class AuditUtils:
    """Utility functions for audit logging"""
    
    @staticmethod
    def create_audit_entry(action: str, user_id: uuid.UUID, entity_type: str, 
                          entity_id: uuid.UUID, old_values: Dict[str, Any] = None,
                          new_values: Dict[str, Any] = None, 
                          additional_details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create standardized audit log entry"""
        return {
            "action": action,
            "user_id": str(user_id),
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "timestamp": datetime.utcnow().isoformat(),
            "old_values": old_values,
            "new_values": new_values,
            "additional_details": additional_details or {}
        }
    
    @staticmethod
    def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive information in audit logs"""
        sensitive_fields = ['ssn', 'dob', 'insurance_id', 'credit_card']
        masked_data = data.copy()
        
        for field in sensitive_fields:
            if field in masked_data:
                value = str(masked_data[field])
                if len(value) > 4:
                    masked_data[field] = '*' * (len(value) - 4) + value[-4:]
                else:
                    masked_data[field] = '*' * len(value)
        
        return masked_data

class SecurityUtils:
    """Security-related utility functions"""
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_string)
        return sanitized.strip()
    
    @staticmethod
    def validate_user_permissions(user_role: str, required_permission: str) -> bool:
        """Check if user has required permission"""
        permission_hierarchy = {
            'admin': ['read', 'write', 'delete', 'approve'],
            'provider': ['read', 'write'],
            'biller': ['read', 'write', 'approve'],
            'viewer': ['read']
        }
        
        user_permissions = permission_hierarchy.get(user_role, [])
        return required_permission in user_permissions

class ExportUtils:
    """Utility functions for data export"""
    
    @staticmethod
    def prepare_charges_for_export(charges: List[Dict[str, Any]], 
                                  format_type: str = 'csv') -> List[Dict[str, Any]]:
        """Prepare charge data for export"""
        export_data = []
        
        for charge in charges:
            export_row = {
                'Charge ID': charge.get('id'),
                'Patient Name': charge.get('patient_name'),
                'MRN': charge.get('patient_mrn'),
                'Encounter Date': charge.get('encounter_date'),
                'Provider': charge.get('provider_name'),
                'CPT Code': charge.get('cpt_code'),
                'CPT Description': charge.get('cpt_description'),
                'ICD Code': charge.get('icd_code'),
                'ICD Description': charge.get('icd_description'),
                'Units': charge.get('units'),
                'Quantity': charge.get('quantity'),
                'Amount': charge.get('charge_amount'),
                'Status': charge.get('status'),
                'Captured Date': charge.get('captured_at'),
                'Notes': charge.get('notes')
            }
            export_data.append(export_row)
        
        return export_data
    
    @staticmethod
    def generate_filename(base_name: str, extension: str = 'csv') -> str:
        """Generate filename with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp}.{extension}"

# Error handling utilities
class ChargeError(Exception):
    """Base exception for charge-related errors"""
    pass

class ValidationError(ChargeError):
    """Exception for validation errors"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class BusinessRuleError(ChargeError):
    """Exception for business rule violations"""
    def __init__(self, rule_name: str, message: str):
        self.rule_name = rule_name
        self.message = message
        super().__init__(f"Business rule '{rule_name}': {message}")

class IntegrationError(ChargeError):
    """Exception for external service integration errors"""
    def __init__(self, service: str, message: str):
        self.service = service
        self.message = message
        super().__init__(f"{service} integration error: {message}")

# Configuration management
class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/charge_capture_db"
    
    # API Settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_DEBUG = True
    
    # Security
    SECRET_KEY = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # External Services
    MEDICAL_CODE_SERVICE_URL = "http://localhost:8001"
    BILLING_SERVICE_URL = "http://localhost:8002"
    
    # Validation
    MAX_CHARGE_AMOUNT = Decimal('10000.00')
    MAX_UNITS = 100
    
    # Performance
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    CACHE_TTL = 300  # 5 minutes
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        import os
        
        cls.DATABASE_URL = os.getenv('DATABASE_URL', cls.DATABASE_URL)
        cls.API_DEBUG = os.getenv('API_DEBUG', 'false').lower() == 'true'
        cls.SECRET_KEY = os.getenv('SECRET_KEY', cls.SECRET_KEY)
        
        return cls
