from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialty = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    medications = relationship("Medication", back_populates="prescriber")
    lab_results = relationship("LabResult", back_populates="ordering_doctor")
    messages_sent = relationship("Message", back_populates="sender") 