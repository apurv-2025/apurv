from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class LabResult(Base):
    __tablename__ = "lab_results"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ordering_doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    test_name = Column(String, nullable=False)
    test_date = Column(Date, nullable=False)
    result_value = Column(String)
    reference_range = Column(String)
    status = Column(String, nullable=False)  # normal, abnormal, critical
    notes = Column(Text)
    file_path = Column(String)  # for PDF reports
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("User", back_populates="lab_results")
    ordering_doctor = relationship("Doctor", back_populates="lab_results") 