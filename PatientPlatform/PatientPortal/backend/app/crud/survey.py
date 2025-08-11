"""
Survey CRUD operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..models.survey import Survey, SurveyQuestion, SurveyResponse
from ..schemas.survey import SurveyCreate, SurveyUpdate, SurveyQuestionCreate, SurveyResponseCreate


def create_survey(db: Session, survey: SurveyCreate) -> Survey:
    """Create a new survey."""
    db_survey = Survey(**survey.dict())
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


def get_survey(db: Session, survey_id: int) -> Optional[Survey]:
    """Get a survey by ID."""
    return db.query(Survey).filter(Survey.id == survey_id).first()


def get_surveys(db: Session, skip: int = 0, limit: int = 100, survey_type: Optional[str] = None) -> List[Survey]:
    """Get surveys with optional filtering."""
    query = db.query(Survey)
    if survey_type:
        query = query.filter(Survey.survey_type == survey_type)
    return query.offset(skip).limit(limit).all()


def get_active_surveys(db: Session, survey_type: Optional[str] = None) -> List[Survey]:
    """Get active surveys."""
    query = db.query(Survey).filter(Survey.is_active == True)
    if survey_type:
        query = query.filter(Survey.survey_type == survey_type)
    return query.all()


def update_survey(db: Session, survey_id: int, survey: SurveyUpdate) -> Optional[Survey]:
    """Update a survey."""
    db_survey = get_survey(db, survey_id)
    if db_survey:
        update_data = survey.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_survey, field, value)
        db.commit()
        db.refresh(db_survey)
    return db_survey


def delete_survey(db: Session, survey_id: int) -> bool:
    """Delete a survey."""
    db_survey = get_survey(db, survey_id)
    if db_survey:
        db.delete(db_survey)
        db.commit()
        return True
    return False


def create_survey_question(db: Session, question: SurveyQuestionCreate) -> SurveyQuestion:
    """Create a new survey question."""
    db_question = SurveyQuestion(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_survey_questions(db: Session, survey_id: int) -> List[SurveyQuestion]:
    """Get questions for a survey."""
    return db.query(SurveyQuestion).filter(
        SurveyQuestion.survey_id == survey_id
    ).order_by(SurveyQuestion.order_index).all()


def update_survey_question(db: Session, question_id: int, question_update: Dict[str, Any]) -> Optional[SurveyQuestion]:
    """Update a survey question."""
    db_question = db.query(SurveyQuestion).filter(SurveyQuestion.id == question_id).first()
    if db_question:
        for field, value in question_update.items():
            setattr(db_question, field, value)
        db.commit()
        db.refresh(db_question)
    return db_question


def delete_survey_question(db: Session, question_id: int) -> bool:
    """Delete a survey question."""
    db_question = db.query(SurveyQuestion).filter(SurveyQuestion.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        return True
    return False


def create_survey_response(db: Session, response: SurveyResponseCreate) -> SurveyResponse:
    """Create a new survey response."""
    db_response = SurveyResponse(**response.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_survey_responses(db: Session, survey_id: int, skip: int = 0, limit: int = 100) -> List[SurveyResponse]:
    """Get responses for a survey."""
    return db.query(SurveyResponse).filter(
        SurveyResponse.survey_id == survey_id
    ).offset(skip).limit(limit).all()


def get_user_survey_responses(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[SurveyResponse]:
    """Get survey responses for a user."""
    return db.query(SurveyResponse).filter(
        SurveyResponse.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_survey_response(db: Session, response_id: int) -> Optional[SurveyResponse]:
    """Get a specific survey response."""
    return db.query(SurveyResponse).filter(SurveyResponse.id == response_id).first()


def update_survey_response(db: Session, response_id: int, response_update: Dict[str, Any]) -> Optional[SurveyResponse]:
    """Update a survey response."""
    db_response = get_survey_response(db, response_id)
    if db_response:
        for field, value in response_update.items():
            setattr(db_response, field, value)
        db.commit()
        db.refresh(db_response)
    return db_response


def get_survey_analytics(db: Session, survey_id: int) -> Dict[str, Any]:
    """Get analytics for a survey."""
    responses = db.query(SurveyResponse).filter(SurveyResponse.survey_id == survey_id).all()
    
    if not responses:
        return {
            "survey_id": survey_id,
            "total_responses": 0,
            "average_rating": None,
            "response_rate": 0.0,
            "question_analytics": {}
        }
    
    total_responses = len(responses)
    ratings = [r.overall_rating for r in responses if r.overall_rating is not None]
    average_rating = sum(ratings) / len(ratings) if ratings else None
    
    # Calculate question analytics
    question_analytics = {}
    for response in responses:
        for question_id, answer in response.response_data.items():
            if question_id not in question_analytics:
                question_analytics[question_id] = {"answers": [], "count": 0}
            question_analytics[question_id]["answers"].append(answer)
            question_analytics[question_id]["count"] += 1
    
    return {
        "survey_id": survey_id,
        "total_responses": total_responses,
        "average_rating": average_rating,
        "response_rate": 0.0,  # Would need total potential respondents to calculate
        "question_analytics": question_analytics
    }


def check_survey_eligibility(db: Session, user_id: int, survey_type: str, 
                           appointment_id: Optional[int] = None, 
                           conversation_id: Optional[str] = None) -> bool:
    """Check if a user is eligible for a survey."""
    # Check if user has already completed a survey for this trigger
    query = db.query(SurveyResponse).filter(SurveyResponse.user_id == user_id)
    
    if survey_type == "visit" and appointment_id:
        query = query.filter(SurveyResponse.appointment_id == appointment_id)
    elif survey_type == "ai_chat" and conversation_id:
        query = query.filter(SurveyResponse.conversation_id == conversation_id)
    
    existing_response = query.first()
    return existing_response is None


def get_survey_for_trigger(db: Session, survey_type: str) -> Optional[Survey]:
    """Get the appropriate survey for a trigger."""
    return db.query(Survey).filter(
        and_(Survey.survey_type == survey_type, Survey.is_active == True)
    ).first() 