"""
Survey router for PatientPortal
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..crud import survey as survey_crud
from ..schemas.survey import (
    Survey, SurveyCreate, SurveyUpdate, SurveyWithQuestions,
    SurveyQuestion, SurveyQuestionCreate, SurveyQuestionUpdate,
    SurveyResponse, SurveyResponseCreate, SurveyResponseUpdate,
    SurveyResponseWithDetails, SurveyAnalytics, SurveyTrigger
)
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/surveys", tags=["surveys"])


@router.post("/", response_model=Survey)
def create_survey(
    survey: SurveyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new survey."""
    return survey_crud.create_survey(db=db, survey=survey)


@router.get("/", response_model=List[Survey])
def get_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    survey_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get surveys with optional filtering."""
    return survey_crud.get_surveys(db=db, skip=skip, limit=limit, survey_type=survey_type)


@router.get("/active", response_model=List[Survey])
def get_active_surveys(
    survey_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active surveys."""
    return survey_crud.get_active_surveys(db=db, survey_type=survey_type)


@router.get("/{survey_id}", response_model=SurveyWithQuestions)
def get_survey(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a survey with its questions."""
    survey = survey_crud.get_survey(db=db, survey_id=survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey


@router.put("/{survey_id}", response_model=Survey)
def update_survey(
    survey_id: int,
    survey: SurveyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a survey."""
    updated_survey = survey_crud.update_survey(db=db, survey_id=survey_id, survey=survey)
    if not updated_survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return updated_survey


@router.delete("/{survey_id}")
def delete_survey(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a survey."""
    success = survey_crud.delete_survey(db=db, survey_id=survey_id)
    if not success:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"message": "Survey deleted successfully"}


@router.post("/{survey_id}/questions", response_model=SurveyQuestion)
def create_survey_question(
    survey_id: int,
    question: SurveyQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a question for a survey."""
    question.survey_id = survey_id
    return survey_crud.create_survey_question(db=db, question=question)


@router.get("/{survey_id}/questions", response_model=List[SurveyQuestion])
def get_survey_questions(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get questions for a survey."""
    return survey_crud.get_survey_questions(db=db, survey_id=survey_id)


@router.put("/questions/{question_id}", response_model=SurveyQuestion)
def update_survey_question(
    question_id: int,
    question_update: SurveyQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a survey question."""
    updated_question = survey_crud.update_survey_question(
        db=db, 
        question_id=question_id, 
        question_update=question_update.dict(exclude_unset=True)
    )
    if not updated_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated_question


@router.delete("/questions/{question_id}")
def delete_survey_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a survey question."""
    success = survey_crud.delete_survey_question(db=db, question_id=question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}


@router.post("/responses", response_model=SurveyResponse)
def create_survey_response(
    response: SurveyResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a survey response."""
    # Set the user_id from the current user
    response.user_id = current_user.id
    return survey_crud.create_survey_response(db=db, response=response)


@router.get("/responses", response_model=List[SurveyResponseWithDetails])
def get_survey_responses(
    survey_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get survey responses."""
    if survey_id:
        responses = survey_crud.get_survey_responses(db=db, survey_id=survey_id, skip=skip, limit=limit)
    else:
        responses = survey_crud.get_user_survey_responses(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return responses


@router.get("/responses/{response_id}", response_model=SurveyResponseWithDetails)
def get_survey_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific survey response."""
    response = survey_crud.get_survey_response(db=db, response_id=response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@router.put("/responses/{response_id}", response_model=SurveyResponse)
def update_survey_response(
    response_id: int,
    response_update: SurveyResponseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a survey response."""
    updated_response = survey_crud.update_survey_response(
        db=db, 
        response_id=response_id, 
        response_update=response_update.dict(exclude_unset=True)
    )
    if not updated_response:
        raise HTTPException(status_code=404, detail="Response not found")
    return updated_response


@router.get("/{survey_id}/analytics", response_model=SurveyAnalytics)
def get_survey_analytics(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics for a survey."""
    analytics = survey_crud.get_survey_analytics(db=db, survey_id=survey_id)
    return analytics


@router.post("/trigger")
def trigger_survey(
    trigger: SurveyTrigger,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger a survey for a user."""
    # Get the appropriate survey for the trigger
    survey = survey_crud.get_survey_for_trigger(db=db, survey_type=trigger.trigger_type)
    if not survey:
        raise HTTPException(status_code=404, detail="No active survey found for this trigger type")
    
    # Check if user is eligible for the survey
    is_eligible = survey_crud.check_survey_eligibility(
        db=db,
        user_id=current_user.id,
        survey_type=trigger.trigger_type,
        appointment_id=trigger.trigger_data.get("appointment_id"),
        conversation_id=trigger.trigger_data.get("conversation_id")
    )
    
    if not is_eligible:
        return {"message": "User has already completed a survey for this trigger"}
    
    # Return the survey for the frontend to display
    return {
        "survey": survey,
        "questions": survey_crud.get_survey_questions(db=db, survey_id=survey.id),
        "trigger_data": trigger.trigger_data
    }


@router.get("/eligibility/{survey_type}")
def check_survey_eligibility(
    survey_type: str,
    appointment_id: Optional[int] = Query(None),
    conversation_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if a user is eligible for a survey."""
    is_eligible = survey_crud.check_survey_eligibility(
        db=db,
        user_id=current_user.id,
        survey_type=survey_type,
        appointment_id=appointment_id,
        conversation_id=conversation_id
    )
    
    if is_eligible:
        survey = survey_crud.get_survey_for_trigger(db=db, survey_type=survey_type)
        if survey:
            return {
                "eligible": True,
                "survey": survey,
                "questions": survey_crud.get_survey_questions(db=db, survey_id=survey.id)
            }
    
    return {"eligible": False}


@router.post("/templates/visit")
def create_visit_survey_template(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a default visit survey template."""
    from ..schemas.survey import SurveyType, QuestionType
    
    # Create the survey
    survey_data = SurveyCreate(
        title="Visit Experience Survey",
        description="Please share your experience with your recent visit",
        survey_type=SurveyType.VISIT,
        is_active=True
    )
    survey = survey_crud.create_survey(db=db, survey=survey_data)
    
    # Create default questions
    questions = [
        {
            "question_text": "How would you rate your overall experience?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 1
        },
        {
            "question_text": "How satisfied were you with the doctor's care?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 2
        },
        {
            "question_text": "How satisfied were you with the wait time?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 3
        },
        {
            "question_text": "How satisfied were you with the staff?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 4
        },
        {
            "question_text": "Would you recommend this doctor to others?",
            "question_type": QuestionType.YES_NO,
            "required": True,
            "order_index": 5
        },
        {
            "question_text": "Please share any additional comments or suggestions:",
            "question_type": QuestionType.TEXT,
            "required": False,
            "order_index": 6
        }
    ]
    
    for question_data in questions:
        question_data["survey_id"] = survey.id
        survey_crud.create_survey_question(db=db, question=SurveyQuestionCreate(**question_data))
    
    return {"message": "Visit survey template created successfully", "survey_id": survey.id}


@router.post("/templates/ai-chat")
def create_ai_chat_survey_template(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a default AI chat survey template."""
    from ..schemas.survey import SurveyType, QuestionType
    
    # Create the survey
    survey_data = SurveyCreate(
        title="AI Assistant Experience Survey",
        description="Please share your experience with our AI health assistant",
        survey_type=SurveyType.AI_CHAT,
        is_active=True
    )
    survey = survey_crud.create_survey(db=db, survey=survey_data)
    
    # Create default questions
    questions = [
        {
            "question_text": "How helpful was the AI assistant?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 1
        },
        {
            "question_text": "How satisfied were you with the response time?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 2
        },
        {
            "question_text": "How accurate were the AI assistant's responses?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 3
        },
        {
            "question_text": "How easy was it to understand the AI assistant's responses?",
            "question_type": QuestionType.RATING,
            "required": True,
            "order_index": 4
        },
        {
            "question_text": "Did the AI assistant solve your problem?",
            "question_type": QuestionType.YES_NO,
            "required": True,
            "order_index": 5
        },
        {
            "question_text": "Would you use the AI assistant again?",
            "question_type": QuestionType.YES_NO,
            "required": True,
            "order_index": 6
        },
        {
            "question_text": "Please share any additional feedback:",
            "question_type": QuestionType.TEXT,
            "required": False,
            "order_index": 7
        }
    ]
    
    for question_data in questions:
        question_data["survey_id"] = survey.id
        survey_crud.create_survey_question(db=db, question=SurveyQuestionCreate(**question_data))
    
    return {"message": "AI chat survey template created successfully", "survey_id": survey.id} 