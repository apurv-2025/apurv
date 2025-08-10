# File: app/models/models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class InsuranceCard(Base, TimestampMixin):
    __tablename__ = "insurance_cards"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), index=True)
    member_id = Column(String(100), nullable=False, index=True)
    group_number = Column(String(100))
    plan_name = Column(String(255))
    insurance_company = Column(String(255))
    effective_date = Column(String(20))
    phone_number = Column(String(20))
    raw_text = Column(Text)
    file_path = Column(String(500))
    file_type = Column(String(50))


class EligibilityRequest(Base, TimestampMixin):
    __tablename__ = "eligibility_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, nullable=False, index=True)
    member_id = Column(String(100), nullable=False, index=True)
    provider_npi = Column(String(20), nullable=False, index=True)
    service_type = Column(String(10), default="30")
    subscriber_first_name = Column(String(100))
    subscriber_last_name = Column(String(100))
    subscriber_dob = Column(Date)
    edi_270_content = Column(Text, nullable=False)
    status = Column(String(20), default="pending", index=True)


class EligibilityResponse(Base, TimestampMixin):
    __tablename__ = "eligibility_responses"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), ForeignKey("eligibility_requests.request_id"), nullable=False)
    edi_271_content = Column(Text, nullable=False)
    is_eligible = Column(Boolean, nullable=False, default=False)
    benefits_info = Column(Text)  # JSON as text for simplicity
