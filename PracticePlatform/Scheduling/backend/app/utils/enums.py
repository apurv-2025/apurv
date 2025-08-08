"""
Scheduling2.0 - Enums
Merged enums from both MBH-Scheduling and Scheduling projects
"""

from enum import Enum

# Service Types (merged from both projects)
class ServiceType(str, Enum):
    THERAPY = "THERAPY"
    CONSULTATION = "CONSULTATION"
    ASSESSMENT = "ASSESSMENT"
    MEDICAL = "MEDICAL"
    MENTAL_HEALTH = "MENTAL_HEALTH"
    FOLLOW_UP = "FOLLOW_UP"
    EMERGENCY = "EMERGENCY"

# Appointment Status (merged from both projects)
class AppointmentStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    COMPLETED = "COMPLETED"

# Appointment Types (merged from both projects)
class AppointmentType(str, Enum):
    APPOINTMENT = "APPOINTMENT"
    CONSULTATION = "CONSULTATION"
    FOLLOW_UP = "FOLLOW_UP"
    INITIAL = "INITIAL"
    EMERGENCY = "EMERGENCY"

# Session Types (from MBH-Scheduling)
class SessionType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    COUPLE = "COUPLE"
    FAMILY = "FAMILY"
    GROUP = "GROUP"
    TELEHEALTH = "TELEHEALTH"
    IN_PERSON = "IN_PERSON"

# Billing Types (from MBH-Scheduling)
class BillingType(str, Enum):
    SELF_PAY = "SELF_PAY"
    INSURANCE = "INSURANCE"
    SLIDING_SCALE = "SLIDING_SCALE"
    MEDICARE = "MEDICARE"
    MEDICAID = "MEDICAID"

# Waitlist Priority (from MBH-Scheduling)
class WaitlistPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

# Waitlist Status (from MBH-Scheduling)
class WaitlistStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CONTACTED = "CONTACTED"
    SCHEDULED = "SCHEDULED"
    REMOVED = "REMOVED"

# User Roles (from Scheduling project)
class UserRole(str, Enum):
    ADMIN = "admin"
    PRACTITIONER = "practitioner"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    THERAPIST = "therapist"
    PSYCHIATRIST = "psychiatrist" 