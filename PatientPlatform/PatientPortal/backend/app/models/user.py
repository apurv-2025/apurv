from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(Date)
    insurance_provider = Column(String)
    insurance_id = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")
    lab_results = relationship("LabResult", back_populates="patient")
    messages_received = relationship("Message", back_populates="recipient") 