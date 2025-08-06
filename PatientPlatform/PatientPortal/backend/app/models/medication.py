from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prescriber_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    refills_remaining = Column(Integer, default=0)
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("User", back_populates="medications")
    prescriber = relationship("Doctor", back_populates="medications") 