"""
Agent API endpoints for InsuranceVerification AI functionality
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.schemas.agent import (
    AgentRequest, AgentResponse, ChatRequest, ChatResponse,
    InsuranceVerificationRequest, InsuranceVerificationResponse,
    InsuranceExtractionRequest, InsuranceExtractionResponse,
    EligibilityCheckRequest, EligibilityCheckResponse,
    EDIAnalysisRequest, EDIAnalysisResponse,
    ComplexVerificationRequest, ComplexVerificationResponse,
    ToolInfo, AgentHealthResponse, AgentMetricsResponse
)
from app.services.agentic_integration import agentic_insurance_verification

router = APIRouter()

# Initialize the agentic insurance verification
try:
    agentic_insurance_verification = agentic_insurance_verification
except Exception as e:
    print(f"Warning: Could not initialize agentic insurance verification: {e}")

@router.post("/tasks", response_model=AgentResponse)
async def create_agent_task(request: AgentRequest):
    """Create and execute an AI agent task"""
    try:
        if request.task_type.value == "verify_insurance":
            # Handle insurance verification
            if not request.context or "member_id" not in request.context or "provider_npi" not in request.context:
                raise HTTPException(status_code=400, detail="Missing required parameters: member_id and provider_npi")
            
            result = await agentic_insurance_verification.verify_insurance_coverage(
                member_id=request.context["member_id"],
                provider_npi=request.context["provider_npi"],
                service_type=request.context.get("service_type", "30")
            )
            
            return AgentResponse(
                success=result.get("success", False),
                message="Insurance verification completed",
                data=result.get("result", {})
            )
        
        elif request.task_type.value == "extract_insurance_info":
            # Handle insurance information extraction
            if not request.context or "file_path" not in request.context:
                raise HTTPException(status_code=400, detail="Missing required parameter: file_path")
            
            result = await agentic_insurance_verification.extract_insurance_information(
                file_path=request.context["file_path"],
                file_type=request.context.get("file_type", "image")
            )
            
            return AgentResponse(
                success=result.get("success", False),
                message="Insurance information extraction completed",
                data=result.get("result", {})
            )
        
        elif request.task_type.value == "check_eligibility":
            # Handle eligibility check
            if not request.context or "member_id" not in request.context or "service_type" not in request.context:
                raise HTTPException(status_code=400, detail="Missing required parameters: member_id and service_type")
            
            result = await agentic_insurance_verification.check_patient_eligibility(
                member_id=request.context["member_id"],
                service_type=request.context["service_type"],
                provider_npi=request.context.get("provider_npi")
            )
            
            return AgentResponse(
                success=result.get("success", False),
                message="Eligibility check completed",
                data=result.get("result", {})
            )
        
        elif request.task_type.value == "analyze_edi":
            # Handle EDI analysis
            if not request.context or "edi_content" not in request.context:
                raise HTTPException(status_code=400, detail="Missing required parameter: edi_content")
            
            result = await agentic_insurance_verification.analyze_edi_transaction(
                edi_content=request.context["edi_content"],
                transaction_type=request.context.get("transaction_type", "270")
            )
            
            return AgentResponse(
                success=result.get("success", False),
                message="EDI analysis completed",
                data=result.get("result", {})
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported task type: {request.task_type}")
    
    except Exception as e:
        return AgentResponse(
            success=False,
            message=f"Task execution failed: {str(e)}",
            data=None
        )

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI agent about insurance verification"""
    try:
        result = await agentic_insurance_verification.chat_with_insurance_data(
            message=request.message,
            user_id=request.user_id,
            context=request.context
        )
        
        return ChatResponse(
            response=result.get("response", "I'm sorry, I couldn't process your request."),
            conversation_id=result.get("conversation_id", f"conv_{request.user_id}_{datetime.now().timestamp()}")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.post("/verify-insurance", response_model=InsuranceVerificationResponse)
async def verify_insurance_ai(request: InsuranceVerificationRequest):
    """Verify insurance coverage using AI agent"""
    try:
        result = await agentic_insurance_verification.verify_insurance_coverage(
            member_id=request.member_id,
            provider_npi=request.provider_npi,
            service_type=request.service_type
        )
        
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "Verification failed"))
        
        verification_data = result.get("result", {})
        
        return InsuranceVerificationResponse(
            member_id=verification_data.get("member_id"),
            provider_npi=verification_data.get("provider_npi"),
            service_type=verification_data.get("service_type"),
            is_eligible=verification_data.get("is_eligible", False),
            coverage_details=verification_data.get("coverage_details", {}),
            benefits=verification_data.get("benefits", {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insurance verification failed: {str(e)}")

@router.post("/extract-insurance-info", response_model=InsuranceExtractionResponse)
async def extract_insurance_info_ai(request: InsuranceExtractionRequest):
    """Extract insurance information using AI agent"""
    try:
        result = await agentic_insurance_verification.extract_insurance_information(
            file_path=request.file_path,
            file_type=request.file_type
        )
        
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "Extraction failed"))
        
        extraction_data = result.get("result", {})
        
        return InsuranceExtractionResponse(
            file_path=extraction_data.get("file_path"),
            file_type=extraction_data.get("file_type"),
            extracted_info=extraction_data.get("extracted_info", {}),
            confidence_score=extraction_data.get("confidence_score", 0.0)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insurance information extraction failed: {str(e)}")

@router.post("/check-eligibility", response_model=EligibilityCheckResponse)
async def check_eligibility_ai(request: EligibilityCheckRequest):
    """Check patient eligibility using AI agent"""
    try:
        result = await agentic_insurance_verification.check_patient_eligibility(
            member_id=request.member_id,
            service_type=request.service_type,
            provider_npi=request.provider_npi
        )
        
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "Eligibility check failed"))
        
        eligibility_data = result.get("result", {})
        
        return EligibilityCheckResponse(
            member_id=eligibility_data.get("member_id"),
            service_type=eligibility_data.get("service_type"),
            provider_npi=eligibility_data.get("provider_npi"),
            is_eligible=eligibility_data.get("is_eligible", False),
            service_details=eligibility_data.get("service_details", {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eligibility check failed: {str(e)}")

@router.post("/analyze-edi", response_model=EDIAnalysisResponse)
async def analyze_edi_ai(request: EDIAnalysisRequest):
    """Analyze EDI transaction using AI agent"""
    try:
        result = await agentic_insurance_verification.analyze_edi_transaction(
            edi_content=request.edi_content,
            transaction_type=request.transaction_type
        )
        
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "EDI analysis failed"))
        
        analysis_data = result.get("result", {})
        
        return EDIAnalysisResponse(
            transaction_type=analysis_data.get("transaction_type"),
            edi_content=analysis_data.get("edi_content"),
            analysis=analysis_data.get("analysis", {}),
            validation=analysis_data.get("validation", {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EDI analysis failed: {str(e)}")

@router.post("/complex-verification", response_model=ComplexVerificationResponse)
async def complex_verification_ai(request: ComplexVerificationRequest):
    """Perform complex verification with multiple service types"""
    try:
        result = await agentic_insurance_verification.process_complex_verification({
            "member_id": request.member_id,
            "provider_npi": request.provider_npi,
            "service_types": request.service_types
        })
        
        return ComplexVerificationResponse(
            member_id=result.get("member_id"),
            provider_npi=result.get("provider_npi"),
            verification_results=result.get("verification_results", []),
            overall_eligible=result.get("overall_eligible", False)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complex verification failed: {str(e)}")

@router.get("/tools", response_model=List[ToolInfo])
async def list_available_tools():
    """List available AI agent tools"""
    try:
        tools = await agentic_insurance_verification.get_available_tools()
        return [ToolInfo(**tool) for tool in tools]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get available tools: {str(e)}")

@router.get("/health", response_model=AgentHealthResponse)
async def check_agent_health():
    """Check AI agent health"""
    try:
        tools = await agentic_insurance_verification.get_available_tools()
        tool_names = [tool["name"] for tool in tools]
        
        return AgentHealthResponse(
            status="healthy",
            model_provider="openai",
            available_tools=tool_names
        )
    
    except Exception as e:
        return AgentHealthResponse(
            status="unhealthy",
            model_provider="unknown",
            available_tools=[],
            timestamp=datetime.now()
        )

@router.get("/metrics", response_model=AgentMetricsResponse)
async def get_agent_metrics():
    """Get AI agent metrics"""
    try:
        # Mock metrics for now
        return AgentMetricsResponse(
            total_requests=100,
            successful_requests=95,
            failed_requests=5,
            average_response_time=1.2,
            most_used_tools=[
                {"name": "verify_insurance", "count": 45},
                {"name": "check_eligibility", "count": 30},
                {"name": "extract_insurance_info", "count": 15},
                {"name": "analyze_edi", "count": 10}
            ]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@router.get("/conversations/{user_id}")
async def get_user_conversations(user_id: str, limit: int = Query(10, ge=1, le=100)):
    """Get conversation history for a user"""
    try:
        # Mock conversation history
        conversations = [
            {
                "conversation_id": f"conv_{user_id}_1",
                "messages": [
                    {"role": "user", "content": "Can you verify insurance for member 123456789?", "timestamp": "2024-01-15T10:00:00Z"},
                    {"role": "assistant", "content": "I can help you verify insurance coverage. Please provide the member ID and provider NPI to get started.", "timestamp": "2024-01-15T10:00:01Z"}
                ],
                "created_at": "2024-01-15T10:00:00Z"
            }
        ]
        
        return {
            "user_id": user_id,
            "conversations": conversations[:limit],
            "total_count": len(conversations)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get conversations: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a specific conversation"""
    try:
        # Mock deletion
        return {
            "success": True,
            "message": f"Conversation {conversation_id} deleted successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")

@router.post("/batch-verification")
async def batch_verification(requests: List[InsuranceVerificationRequest]):
    """Perform batch insurance verification"""
    try:
        results = []
        
        for request in requests:
            result = await agentic_insurance_verification.verify_insurance_coverage(
                member_id=request.member_id,
                provider_npi=request.provider_npi,
                service_type=request.service_type
            )
            results.append({
                "request": request.dict(),
                "result": result
            })
        
        return {
            "total_requests": len(requests),
            "successful_requests": len([r for r in results if r["result"].get("success", False)]),
            "failed_requests": len([r for r in results if not r["result"].get("success", False)]),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch verification failed: {str(e)}") 