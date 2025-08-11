"""
Survey model for PatientPortal
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Survey(Base):
    """Survey model for collecting patient feedback."""
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    survey_type = Column(String(50), nullable=False)  # 'visit', 'ai_chat', 'general'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SurveyQuestion(Base):
    """Survey question model."""
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # 'rating', 'multiple_choice', 'text', 'yes_no'
    options = Column(JSON)  # For multiple choice questions
    required = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    survey = relationship("Survey", back_populates="questions")


class SurveyResponse(Base):
    """Survey response model."""
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    conversation_id = Column(String(255), nullable=True)  # For AI chat surveys
    response_data = Column(JSON, nullable=False)  # Store all responses
    overall_rating = Column(Float, nullable=True)
    feedback_text = Column(Text)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    survey = relationship("Survey")
    user = relationship("User")
    appointment = relationship("Appointment")


# Add relationships to Survey model
Survey.questions = relationship("SurveyQuestion", back_populates="survey", order_by="SurveyQuestion.order_index")
Survey.responses = relationship("SurveyResponse", back_populates="survey") 