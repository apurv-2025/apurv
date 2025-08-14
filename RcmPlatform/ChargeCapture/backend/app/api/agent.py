"""
AI Agent API endpoints for ChargeCapture
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from app.agent_schemas.agent import (
    AgentRequest, AgentResponse, ChatRequest, ChatResponse,
    ChargeCaptureRequest, ChargeCaptureResponse,
    ChargeValidationRequest, ChargeValidationResponse,
    ChargeTemplateRequest, ChargeTemplateResponse,
    ChargeAnalysisRequest, ChargeAnalysisResponse,
    ToolInfo, AgentHealthResponse, AgentMetricsResponse,
    ConversationHistory
)
from app.services.agentic_integration import agentic_charge_capture

router = APIRouter(prefix="/api/v1/agent", tags=["AI Agent"])

# In-memory storage for conversation history (in production, use database)
conversation_history: Dict[str, List[Dict[str, Any]]] = {}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI assistant"""
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Chat with the agent
        result = await agentic_charge_capture.chat(
            message=request.message,
            conversation_id=conversation_id
        )
        
        # Store conversation history
        if conversation_id not in conversation_history:
            conversation_history[conversation_id] = []
        
        conversation_history[conversation_id].append({
            "user_message": request.message,
            "assistant_response": result.get("response", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "tools_used": result.get("tools_used", [])
        })
        
        return ChatResponse(
            success=result.get("success", False),
            response=result.get("response", "Sorry, I couldn't process your request."),
            conversation_id=conversation_id,
            tools_used=result.get("tools_used", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/capture-charge", response_model=ChargeCaptureResponse)
async def capture_charge_with_ai(request: ChargeCaptureRequest):
    """Capture a charge with AI assistance"""
    try:
        result = await agentic_charge_capture.capture_charge(request.dict())
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Charge capture failed"))
        
        charge_data = result.get("result", {})
        
        return ChargeCaptureResponse(
            success=True,
            charge_id=charge_data.get("charge_id"),
            encounter_id=charge_data.get("encounter_id"),
            patient_id=charge_data.get("patient_id"),
            provider_id=charge_data.get("provider_id"),
            cpt_code=charge_data.get("cpt_code"),
            icd_code=charge_data.get("icd_code"),
            status=charge_data.get("status"),
            capture_method=charge_data.get("capture_method"),
            captured_at=datetime.fromisoformat(charge_data.get("captured_at")),
            validation_errors=charge_data.get("validation_errors", []),
            suggestions=charge_data.get("suggestions", []),
            message="Charge captured successfully with AI assistance"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Charge capture error: {str(e)}")


@router.post("/validate-charge", response_model=ChargeValidationResponse)
async def validate_charge_with_ai(request: ChargeValidationRequest):
    """Validate a charge with AI assistance"""
    try:
        result = await agentic_charge_capture.validate_charge(request.dict())
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Charge validation failed"))
        
        validation_data = result.get("result", {})
        
        return ChargeValidationResponse(
            success=True,
            cpt_code=validation_data.get("cpt_code"),
            icd_code=validation_data.get("icd_code"),
            modifiers=validation_data.get("modifiers", []),
            charge_amount=validation_data.get("charge_amount"),
            is_valid=validation_data.get("is_valid", False),
            validation_errors=validation_data.get("validation_errors", []),
            warnings=validation_data.get("warnings", []),
            recommendations=validation_data.get("recommendations", []),
            compliance_score=validation_data.get("compliance_score", 0),
            validation_date=datetime.fromisoformat(validation_data.get("validation_date")),
            message="Charge validation completed"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Charge validation error: {str(e)}")


@router.post("/get-templates", response_model=ChargeTemplateResponse)
async def get_charge_templates_with_ai(request: ChargeTemplateRequest):
    """Get charge templates with AI assistance"""
    try:
        result = await agentic_charge_capture.get_charge_template(request.dict())
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Template retrieval failed"))
        
        template_data = result.get("result", {})
        
        return ChargeTemplateResponse(
            success=True,
            specialty=template_data.get("specialty"),
            procedure_type=template_data.get("procedure_type"),
            templates=template_data.get("templates", []),
            suggestions=template_data.get("suggestions", []),
            message="Templates retrieved successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template retrieval error: {str(e)}")


@router.post("/analyze-charges", response_model=ChargeAnalysisResponse)
async def analyze_charges_with_ai(request: ChargeAnalysisRequest):
    """Analyze charges with AI assistance"""
    try:
        result = await agentic_charge_capture.analyze_charges(request.dict())
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Charge analysis failed"))
        
        analysis_data = result.get("result", {})
        
        return ChargeAnalysisResponse(
            success=True,
            provider_id=analysis_data.get("provider_id"),
            date_range=analysis_data.get("date_range"),
            total_charges=analysis_data.get("total_charges", 0),
            total_amount=analysis_data.get("total_amount", 0.0),
            average_charge=analysis_data.get("average_charge", 0.0),
            top_cpt_codes=analysis_data.get("top_cpt_codes", []),
            top_icd_codes=analysis_data.get("top_icd_codes", []),
            rejection_rate=analysis_data.get("rejection_rate", 0.0),
            common_rejection_reasons=analysis_data.get("common_rejection_reasons", []),
            recommendations=analysis_data.get("recommendations", []),
            analysis_date=datetime.fromisoformat(analysis_data.get("analysis_date")),
            message="Charge analysis completed"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Charge analysis error: {str(e)}")


@router.get("/conversations/{conversation_id}", response_model=List[Dict[str, Any]])
async def get_conversation_history(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversation_history:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation_history[conversation_id]


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in conversation_history:
        del conversation_history[conversation_id]
        return {"message": "Conversation deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Conversation not found")


@router.get("/tools", response_model=List[ToolInfo])
async def get_available_tools():
    """Get available AI tools"""
    tools = [
        ToolInfo(
            name="capture_charge",
            description="Capture a new charge with validation and auto-population",
            parameters=["encounter_id", "patient_id", "provider_id", "cpt_code", "icd_code"],
            examples=[
                "Capture a charge for encounter 123 with CPT 99213 and ICD Z00.00",
                "Create a new charge for patient 456 with auto-populated codes"
            ]
        ),
        ToolInfo(
            name="validate_charge",
            description="Validate a charge for compliance and accuracy",
            parameters=["cpt_code", "icd_code", "modifiers", "charge_amount"],
            examples=[
                "Validate CPT 99213 with ICD Z00.00",
                "Check if modifier 25 is appropriate for this charge"
            ]
        ),
        ToolInfo(
            name="get_charge_template",
            description="Get charge templates for specific specialties or procedures",
            parameters=["specialty", "procedure_type"],
            examples=[
                "Get templates for cardiology procedures",
                "Find office visit templates for primary care"
            ]
        ),
        ToolInfo(
            name="analyze_charges",
            description="Analyze charge patterns and provide insights",
            parameters=["provider_id", "date_range", "specialty"],
            examples=[
                "Analyze charges for provider 789 in the last 30 days",
                "Get charge analysis for cardiology specialty"
            ]
        )
    ]
    
    return tools


@router.get("/health", response_model=AgentHealthResponse)
async def get_agent_health():
    """Get AI agent health status"""
    from app.services.agentic_integration import AGENTIC_CORE_AVAILABLE
    
    return AgentHealthResponse(
        status="healthy" if AGENTIC_CORE_AVAILABLE else "degraded",
        agentic_core_available=AGENTIC_CORE_AVAILABLE,
        tools_available=["capture_charge", "validate_charge", "get_charge_template", "analyze_charges"],
        last_updated=datetime.utcnow()
    )


@router.get("/metrics", response_model=AgentMetricsResponse)
async def get_agent_metrics():
    """Get AI agent metrics"""
    # Mock metrics (in production, these would come from database)
    return AgentMetricsResponse(
        total_conversations=len(conversation_history),
        total_charges_captured=25,
        total_validations=150,
        average_response_time=1.2,
        success_rate=0.95,
        most_used_tools=[
            {"name": "validate_charge", "usage_count": 75},
            {"name": "capture_charge", "usage_count": 25},
            {"name": "get_charge_template", "usage_count": 30},
            {"name": "analyze_charges", "usage_count": 20}
        ],
        last_updated=datetime.utcnow()
    ) 