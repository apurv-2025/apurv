# AI Assistant API Endpoints for Prior Authorization System

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agentic_integration import create_agentic_prior_authorization
from pydantic import BaseModel
import uuid
import os

router = APIRouter()

# Initialize agentic integration
agentic_service = create_agentic_prior_authorization(
    model_provider=os.getenv("AI_MODEL_PROVIDER", "openai"),
    api_key=os.getenv("AI_API_KEY"),
    database_url=os.getenv("DATABASE_URL")
)


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    user_id: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    conversation_id: Optional[str] = None
    timestamp: str
    error: Optional[str] = None


class PriorAuthRequest(BaseModel):
    patient_id: str
    provider_npi: str
    procedure_codes: Optional[List[Dict[str, str]]] = []
    diagnosis_codes: Optional[List[Dict[str, str]]] = []
    service_date: Optional[str] = None
    medical_necessity: Optional[str] = None


class AuthorizationStatusRequest(BaseModel):
    request_id: str


class EDIGenerationRequest(BaseModel):
    edi_type: str  # "278" or "275"
    patient_id: str
    request_id: Optional[str] = None
    provider_npi: Optional[str] = None
    service_date: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None


class PatientLookupRequest(BaseModel):
    patient_id: Optional[str] = None
    member_id: Optional[str] = None


class CodeLookupRequest(BaseModel):
    code_type: str  # "procedure", "diagnosis", "service_type"
    search_term: Optional[str] = None
    code: Optional[str] = None


class ComplexWorkflowRequest(BaseModel):
    workflow: List[Dict[str, Any]]


class ToolInfo(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


# Chat endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI assistant about prior authorization"""
    try:
        result = await agentic_service.chat_with_prior_auth_data(
            message=request.message,
            user_id=request.user_id,
            context=request.context
        )
        
        return ChatResponse(
            success=result.get("success", False),
            response=result.get("response", "I'm sorry, I couldn't process your request."),
            conversation_id=result.get("conversation_id"),
            timestamp=result.get("timestamp", ""),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/conversations/{user_id}")
async def get_conversation_history(
    user_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get conversation history for a user"""
    try:
        # This would typically query the database for conversation history
        # For now, return mock data
        conversations = [
            {
                "conversation_id": f"conv_{uuid.uuid4().hex[:8]}",
                "user_id": user_id,
                "messages": [
                    {
                        "role": "user",
                        "content": "How do I create a prior authorization request?",
                        "timestamp": "2024-01-15T10:30:00Z"
                    },
                    {
                        "role": "assistant",
                        "content": "To create a prior authorization request, you need to provide patient information, provider details, procedure codes, and diagnosis codes. Would you like me to help you with the specific steps?",
                        "timestamp": "2024-01-15T10:30:05Z"
                    }
                ],
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:05Z"
            }
        ]
        
        return {
            "success": True,
            "conversations": conversations[:limit],
            "total": len(conversations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    try:
        # This would typically delete the conversation from the database
        return {
            "success": True,
            "message": f"Conversation {conversation_id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")


# Tool endpoints
@router.post("/create-prior-auth")
async def create_prior_authorization_ai(
    request: PriorAuthRequest,
    db: Session = Depends(get_db)
):
    """Create a prior authorization request using AI assistance"""
    try:
        result = await agentic_service.create_prior_authorization(
            auth_data=request.model_dump()
        )
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Prior authorization request created successfully",
                "data": result.get("result")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to create prior authorization"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating prior authorization: {str(e)}")


@router.post("/check-status")
async def check_authorization_status_ai(
    request: AuthorizationStatusRequest,
    db: Session = Depends(get_db)
):
    """Check authorization status using AI assistance"""
    try:
        result = await agentic_service.check_authorization_status(
            request_id=request.request_id
        )
        
        if result.get("success"):
            return {
                "success": True,
                "data": result.get("result")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to check status"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking authorization status: {str(e)}")


@router.post("/generate-edi")
async def generate_edi_ai(
    request: EDIGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate EDI document using AI assistance"""
    try:
        result = await agentic_service.generate_edi_document(
            edi_type=request.edi_type,
            data=request.model_dump(exclude={"edi_type"})
        )
        
        if result.get("success"):
            return {
                "success": True,
                "message": f"EDI {request.edi_type} generated successfully",
                "data": result.get("result")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to generate EDI"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating EDI: {str(e)}")


@router.post("/lookup-patient")
async def lookup_patient_ai(
    request: PatientLookupRequest,
    db: Session = Depends(get_db)
):
    """Lookup patient information using AI assistance"""
    try:
        result = await agentic_service.lookup_patient(
            patient_id=request.patient_id,
            member_id=request.member_id
        )
        
        if result.get("success"):
            return {
                "success": True,
                "data": result.get("result")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to lookup patient"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error looking up patient: {str(e)}")


@router.post("/lookup-codes")
async def lookup_codes_ai(
    request: CodeLookupRequest,
    db: Session = Depends(get_db)
):
    """Lookup healthcare codes using AI assistance"""
    try:
        result = await agentic_service.lookup_codes(
            code_type=request.code_type,
            search_term=request.search_term,
            code=request.code
        )
        
        if result.get("success"):
            return {
                "success": True,
                "data": result.get("result")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to lookup codes"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error looking up codes: {str(e)}")


@router.post("/complex-workflow")
async def process_complex_workflow(
    request: ComplexWorkflowRequest,
    db: Session = Depends(get_db)
):
    """Process complex prior authorization workflow using AI"""
    try:
        result = await agentic_service.process_complex_request(
            request=request.model_dump()
        )
        
        if result.get("success"):
            return {
                "success": True,
                "message": "Complex workflow processed successfully",
                "data": result.get("workflow_results")
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to process workflow"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing workflow: {str(e)}")


# Management endpoints
@router.get("/tools")
async def get_available_tools(
    db: Session = Depends(get_db)
):
    """Get list of available AI tools"""
    try:
        tools = await agentic_service.get_available_tools()
        
        # Add custom tool descriptions
        custom_tools = [
            {
                "name": "create_prior_authorization",
                "description": "Create a new prior authorization request",
                "parameters": {
                    "patient_id": "string (required)",
                    "provider_npi": "string (required)",
                    "procedure_codes": "array (optional)",
                    "diagnosis_codes": "array (optional)",
                    "service_date": "string (optional)",
                    "medical_necessity": "string (optional)"
                }
            },
            {
                "name": "check_authorization_status",
                "description": "Check the status of a prior authorization request",
                "parameters": {
                    "request_id": "string (required)"
                }
            },
            {
                "name": "generate_edi",
                "description": "Generate EDI 278 (authorization request) or EDI 275 (patient information)",
                "parameters": {
                    "edi_type": "string (required) - '278' or '275'",
                    "patient_id": "string (required)",
                    "request_id": "string (optional)",
                    "provider_npi": "string (optional)",
                    "service_date": "string (optional)",
                    "birth_date": "string (optional)",
                    "gender": "string (optional)"
                }
            },
            {
                "name": "lookup_patient",
                "description": "Lookup patient information by ID or member ID",
                "parameters": {
                    "patient_id": "string (optional)",
                    "member_id": "string (optional)"
                }
            },
            {
                "name": "lookup_codes",
                "description": "Lookup procedure codes, diagnosis codes, or service type codes",
                "parameters": {
                    "code_type": "string (required) - 'procedure', 'diagnosis', or 'service_type'",
                    "search_term": "string (optional)",
                    "code": "string (optional)"
                }
            }
        ]
        
        return {
            "success": True,
            "tools": custom_tools,
            "agentic_core_available": len(tools) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tools: {str(e)}")


@router.get("/health")
async def ai_health_check(
    db: Session = Depends(get_db)
):
    """Check AI assistant health"""
    try:
        # Test basic functionality
        test_result = await agentic_service.chat_with_prior_auth_data(
            message="Hello",
            user_id="health_check"
        )
        
        return {
            "success": True,
            "status": "healthy" if test_result.get("success") else "degraded",
            "agentic_core_available": test_result.get("success", False),
            "timestamp": test_result.get("timestamp", "")
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "agentic_core_available": False
        }


@router.get("/examples")
async def get_ai_examples(
    db: Session = Depends(get_db)
):
    """Get example AI assistant interactions"""
    examples = [
        {
            "category": "Prior Authorization Creation",
            "examples": [
                {
                    "user": "I need to create a prior authorization for patient John Doe",
                    "assistant": "I'll help you create a prior authorization request. I'll need the patient ID, provider NPI, procedure codes, and diagnosis codes. Let me look up the patient information first."
                },
                {
                    "user": "What information do I need for a prior authorization?",
                    "assistant": "For a prior authorization request, you typically need: 1) Patient information (ID, member ID), 2) Provider NPI, 3) Procedure codes (CPT), 4) Diagnosis codes (ICD-10), 5) Service date, and 6) Medical necessity statement."
                }
            ]
        },
        {
            "category": "Code Lookup",
            "examples": [
                {
                    "user": "What's the CPT code for an office visit?",
                    "assistant": "Let me look up the CPT codes for office visits. Common codes include: 99213 (20-29 minutes), 99214 (30-39 minutes), and 99215 (40-54 minutes) for established patients."
                },
                {
                    "user": "Find diagnosis codes for diabetes",
                    "assistant": "I'll search for diabetes-related diagnosis codes. Common ICD-10 codes include E11.9 (Type 2 diabetes without complications), E10.9 (Type 1 diabetes without complications), and E11.65 (Type 2 diabetes with hyperglycemia)."
                }
            ]
        },
        {
            "category": "EDI Generation",
            "examples": [
                {
                    "user": "Generate an EDI 278 for my authorization request",
                    "assistant": "I'll generate an EDI 278 authorization request. I'll need the patient ID, provider NPI, and request details to create the proper EDI format."
                },
                {
                    "user": "Create an EDI 275 for patient information",
                    "assistant": "I'll generate an EDI 275 patient information document. This will include the patient's demographic and insurance information in the proper EDI format."
                }
            ]
        },
        {
            "category": "Status Checking",
            "examples": [
                {
                    "user": "What's the status of authorization request AUTH12345?",
                    "assistant": "Let me check the status of authorization request AUTH12345 for you. I'll look up the current status, decision date, and any additional details."
                },
                {
                    "user": "Has my prior authorization been approved?",
                    "assistant": "I'll check the status of your prior authorization request. I'll need the request ID to look up the current status and decision information."
                }
            ]
        }
    ]
    
    return {
        "success": True,
        "examples": examples
    } 