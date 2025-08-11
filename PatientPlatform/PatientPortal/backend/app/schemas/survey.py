"""
Survey schemas for PatientPortal
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class SurveyType(str, Enum):
    """Survey types."""
    VISIT = "visit"
    AI_CHAT = "ai_chat"
    GENERAL = "general"


class QuestionType(str, Enum):
    """Question types."""
    RATING = "rating"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"
    YES_NO = "yes_no"


class SurveyBase(BaseModel):
    """Base survey model."""
    title: str = Field(..., description="Survey title")
    description: Optional[str] = Field(None, description="Survey description")
    survey_type: SurveyType = Field(..., description="Type of survey")
    is_active: bool = Field(default=True, description="Whether survey is active")


class SurveyCreate(SurveyBase):
    """Create survey request model."""
    pass


class SurveyUpdate(BaseModel):
    """Update survey request model."""
    title: Optional[str] = None
    description: Optional[str] = None
    survey_type: Optional[SurveyType] = None
    is_active: Optional[bool] = None


class Survey(SurveyBase):
    """Survey response model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SurveyQuestionBase(BaseModel):
    """Base survey question model."""
    question_text: str = Field(..., description="Question text")
    question_type: QuestionType = Field(..., description="Type of question")
    options: Optional[List[str]] = Field(None, description="Options for multiple choice questions")
    required: bool = Field(default=True, description="Whether question is required")
    order_index: int = Field(default=0, description="Question order")


class SurveyQuestionCreate(SurveyQuestionBase):
    """Create survey question request model."""
    survey_id: int = Field(..., description="Survey ID")


class SurveyQuestionUpdate(BaseModel):
    """Update survey question request model."""
    question_text: Optional[str] = None
    question_type: Optional[QuestionType] = None
    options: Optional[List[str]] = None
    required: Optional[bool] = None
    order_index: Optional[int] = None


class SurveyQuestion(SurveyQuestionBase):
    """Survey question response model."""
    id: int
    survey_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SurveyResponseBase(BaseModel):
    """Base survey response model."""
    survey_id: int = Field(..., description="Survey ID")
    response_data: Dict[str, Any] = Field(..., description="Response data")
    overall_rating: Optional[float] = Field(None, ge=1, le=5, description="Overall rating (1-5)")
    feedback_text: Optional[str] = Field(None, description="Additional feedback")


class SurveyResponseCreate(SurveyResponseBase):
    """Create survey response request model."""
    user_id: int = Field(..., description="User ID")
    appointment_id: Optional[int] = Field(None, description="Appointment ID")
    conversation_id: Optional[str] = Field(None, description="AI conversation ID")


class SurveyResponseUpdate(BaseModel):
    """Update survey response request model."""
    response_data: Optional[Dict[str, Any]] = None
    overall_rating: Optional[float] = None
    feedback_text: Optional[str] = None


class SurveyResponse(SurveyResponseBase):
    """Survey response model."""
    id: int
    user_id: int
    appointment_id: Optional[int] = None
    conversation_id: Optional[str] = None
    completed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class SurveyWithQuestions(Survey):
    """Survey with questions included."""
    questions: List[SurveyQuestion] = []


class SurveyResponseWithDetails(SurveyResponse):
    """Survey response with survey details."""
    survey: Survey


class SurveyAnalytics(BaseModel):
    """Survey analytics model."""
    survey_id: int
    total_responses: int
    average_rating: Optional[float] = None
    response_rate: float
    question_analytics: Dict[str, Any] = {}
    created_at: datetime


class SurveyTrigger(BaseModel):
    """Survey trigger model for automatic survey generation."""
    trigger_type: str = Field(..., description="Type of trigger")
    trigger_data: Dict[str, Any] = Field(..., description="Trigger data")
    survey_template_id: Optional[int] = Field(None, description="Survey template to use")
    delay_minutes: int = Field(default=0, description="Delay before sending survey") 