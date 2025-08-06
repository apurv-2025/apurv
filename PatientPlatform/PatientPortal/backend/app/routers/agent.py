"""
Agent router for PatientPortal AI functionality
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

from ..database import get_db
from ..agentic_integration import get_agentic_patient_portal, initialize_agentic_patient_portal
from ..schemas.agent import (
    AgentRequest, AgentResponse, TaskType, AgentStatus, ChatRequest, ChatResponse,
    AppointmentSchedulingRequest, MedicationCheckRequest, LabResultsRequest,
    HealthSummaryRequest, MedicationReminderRequest, DoctorSearchRequest
)

router = APIRouter()

# Initialize agentic patient portal on startup
try:
    initialize_agentic_patient_portal()
except Exception as e:
    print(f"Warning: Could not initialize agentic patient portal: {e}")

@router.post("/tasks", response_model=AgentResponse)
async def create_agent_task(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and execute an agent task"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        # Convert Pydantic model to dict and add task ID
        request_dict = request.dict()
        task_id = f"task_{datetime.utcnow().timestamp()}"
        request_dict["task_id"] = task_id
        
        # Process the request
        result = await agentic_portal.agentic.process_task(request_dict)
        
        return AgentResponse(**result.dict())
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent request: {str(e)}")

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        # Mock status check
        status = {
            "task_id": task_id,
            "status": "completed",
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": datetime.utcnow().isoformat()
        }
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks/active")
async def get_active_tasks():
    """Get all currently active tasks"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        # Mock active tasks
        return {"active_tasks": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with the AI agent"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.chat_with_patient_data(
            message=request.message,
            user_id=request.user_id,
            context=request.context
        )
        
        return ChatResponse(
            response=response.response,
            conversation_id=request.conversation_id,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.post("/schedule-appointment")
async def schedule_appointment_ai(
    request: AppointmentSchedulingRequest,
    db: Session = Depends(get_db)
):
    """Schedule an appointment using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.schedule_appointment_ai(
            patient_id=request.patient_id,
            appointment_type=request.appointment_type,
            preferred_date=request.preferred_date
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.SCHEDULE_APPOINTMENT,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling appointment: {str(e)}")

@router.post("/check-medications")
async def check_medications_ai(
    request: MedicationCheckRequest,
    db: Session = Depends(get_db)
):
    """Check medications using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.check_medications_ai(
            patient_id=request.patient_id
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.CHECK_MEDICATIONS,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking medications: {str(e)}")

@router.post("/analyze-lab-results")
async def analyze_lab_results_ai(
    request: LabResultsRequest,
    db: Session = Depends(get_db)
):
    """Analyze lab results using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.analyze_lab_results_ai(
            patient_id=request.patient_id,
            lab_result_id=request.lab_result_id
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.VIEW_LAB_RESULTS,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing lab results: {str(e)}")

@router.post("/generate-health-summary")
async def generate_health_summary_ai(
    request: HealthSummaryRequest,
    db: Session = Depends(get_db)
):
    """Generate health summary using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.generate_health_summary_ai(
            patient_id=request.patient_id,
            report_type=request.report_type
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.GENERATE_HEALTH_SUMMARY,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating health summary: {str(e)}")

@router.post("/setup-medication-reminder")
async def setup_medication_reminder_ai(
    request: MedicationReminderRequest,
    db: Session = Depends(get_db)
):
    """Set up medication reminder using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.setup_medication_reminder_ai(
            patient_id=request.patient_id,
            medication_id=request.medication_id,
            reminder_time=request.reminder_time
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.SETUP_MEDICATION_REMINDER,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting up medication reminder: {str(e)}")

@router.post("/find-doctors")
async def find_doctors_ai(
    request: DoctorSearchRequest,
    db: Session = Depends(get_db)
):
    """Find doctors using AI"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        response = await agentic_portal.find_doctors_ai(
            specialty=request.specialty,
            location=request.location
        )
        
        return AgentResponse(
            task_id=response.task_id,
            task_type=TaskType.FIND_DOCTOR,
            status=AgentStatus.COMPLETED,
            response=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding doctors: {str(e)}")

@router.get("/conversation-history/{user_id}")
async def get_conversation_history(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get conversation history for a user"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        conversations = agentic_portal.get_conversation_history(user_id, limit, offset)
        return {"conversations": conversations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting conversation history: {str(e)}")

@router.get("/tools")
async def list_available_tools():
    """List available AI tools"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        tools = agentic_portal.get_available_tools()
        return {"tools": tools}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")

@router.get("/health")
async def agent_health_check():
    """Check the health status of the AI agent"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        health_status = agentic_portal.get_health_status()
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/metrics")
async def get_agent_metrics():
    """Get performance metrics for the AI agent"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        metrics = agentic_portal.get_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")

@router.post("/batch-tasks")
async def create_batch_tasks(
    tasks: List[AgentRequest],
    user_id: str,
    max_concurrent: int = Query(3, ge=1, le=10)
):
    """Create and execute multiple tasks in batch"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        
        async def process_single_task(task_request):
            try:
                result = await agentic_portal.agentic.process_task(task_request.dict())
                return {"task_id": task_request.task_id, "status": "completed", "result": result.dict()}
            except Exception as e:
                return {"task_id": task_request.task_id, "status": "failed", "error": str(e)}
        
        # Process tasks concurrently
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(task):
            async with semaphore:
                return await process_single_task(task)
        
        results = await asyncio.gather(*[process_with_semaphore(task) for task in tasks])
        
        return {
            "batch_id": f"batch_{datetime.utcnow().timestamp()}",
            "total_tasks": len(tasks),
            "results": results,
            "created_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch tasks: {str(e)}")

@router.delete("/conversations/{user_id}")
async def clear_conversation_history(user_id: str):
    """Clear conversation history for a user"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        success = agentic_portal.agentic.clear_conversation_history(user_id)
        
        if success:
            return {"message": f"Conversation history cleared for user {user_id}"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation history: {str(e)}")

@router.get("/tools/{tool_name}/info")
async def get_tool_info(tool_name: str):
    """Get detailed information about a specific tool"""
    
    try:
        agentic_portal = get_agentic_patient_portal()
        tools = agentic_portal.get_available_tools()
        
        tool_info = next((tool for tool in tools if tool["name"] == tool_name), None)
        
        if tool_info:
            return tool_info
        else:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tool info: {str(e)}") 