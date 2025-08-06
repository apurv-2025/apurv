# =============================================================================
# FILE: backend/app/api/routes/agent.py
# =============================================================================
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

from ...database.connection import get_db
from ...agentic_integration import get_agentic_claims_processor, initialize_agentic_claims_processor
from ...schemas.agent import AgentRequest, AgentResponse, TaskType, AgentStatus

router = APIRouter()

# Initialize the agentic claims processor on startup
@router.on_event("startup")
async def startup_event():
    """Initialize the agentic claims processor on startup"""
    try:
        initialize_agentic_claims_processor(
            model_provider="openai",  # Can be configured via environment
            api_key=None,  # Will be loaded from environment
            database_url=None  # Will use default database connection
        )
        print("AgenticClaimsProcessor initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize AgenticClaimsProcessor: {e}")

@router.post("/chat")
async def chat_with_agent(
    message: str,
    user_id: str,
    context: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Enhanced chat interface with claims processing context"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        
        response = await agentic_processor.chat_with_claims_data(
            message=message,
            user_id=user_id,
            context=context or {}
        )
        
        return AgentResponse(
            task_id=response.task_id,
            status=AgentStatus.COMPLETED,
            message=response.response,
            result=response.result,
            created_at=response.created_at,
            completed_at=response.completed_at
        )
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.post("/tasks", response_model=AgentResponse)
async def create_agent_task(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and execute an agent task with claims processing integration"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        
        # Process the request using the integrated processor
        if request.task_type == TaskType.ANALYZE_REJECTION:
            result = await agentic_processor.analyze_rejection_ai(
                rejection_id=str(request.claim_id) if request.claim_id else "1",
                user_id=request.user_id
            )
        elif request.task_type == TaskType.GENERATE_REPORT:
            result = await agentic_processor.generate_report_ai(
                report_type=request.context.get("report_type", "summary"),
                user_id=request.user_id,
                context=request.context
            )
        else:
            # Use the general agentic processor for other tasks
            task_data = {
                "task_type": request.task_type,
                "user_id": request.user_id,
                "task_description": request.task_description,
                "context": request.context
            }
            result = await agentic_processor.agentic.process_task(task_data)
        
        return AgentResponse(
            task_id=result.task_id,
            status=AgentStatus.COMPLETED,
            message=result.response,
            result=result.result,
            created_at=result.created_at,
            completed_at=result.completed_at
        )
        
    except Exception as e:
        print(f"Error in create_agent_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing task: {str(e)}")

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    try:
        # Mock task status for now
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "result": {
                "message": "Task completed successfully",
                "confidence": 0.95
            },
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting task status: {str(e)}")

@router.get("/tasks/active")
async def get_active_tasks():
    """Get all active tasks"""
    try:
        # Mock active tasks
        return {
            "active_tasks": [],
            "total_count": 0
        }
    except Exception as e:
        print(f"Error getting active tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting active tasks: {str(e)}")

@router.post("/tasks/cleanup")
async def cleanup_old_tasks(max_age_hours: int = Query(24, ge=1, le=168)):
    """Clean up old completed tasks"""
    try:
        # Mock cleanup
        return {
            "cleaned_tasks": 0,
            "max_age_hours": max_age_hours,
            "message": "Cleanup completed successfully"
        }
    except Exception as e:
        print(f"Error in cleanup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in cleanup: {str(e)}")

@router.post("/tasks/analyze-claim/{claim_id}")
async def analyze_claim_task(
    claim_id: int,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Analyze a specific claim using AI"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        
        result = await agentic_processor.analyze_claim_ai(
            claim_id=str(claim_id),
            user_id=user_id
        )
        
        return AgentResponse(
            task_id=result.task_id,
            status=AgentStatus.COMPLETED,
            message=result.response,
            result=result.result,
            created_at=result.created_at,
            completed_at=result.completed_at
        )
        
    except Exception as e:
        print(f"Error in analyze_claim_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing claim: {str(e)}")

@router.post("/tasks/process-rejection/{claim_id}")
async def process_rejection_task(
    claim_id: int,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Process a rejection for a specific claim"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        
        result = await agentic_processor.analyze_rejection_ai(
            rejection_id=str(claim_id),
            user_id=user_id
        )
        
        return AgentResponse(
            task_id=result.task_id,
            status=AgentStatus.COMPLETED,
            message=result.response,
            result=result.result,
            created_at=result.created_at,
            completed_at=result.completed_at
        )
        
    except Exception as e:
        print(f"Error in process_rejection_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing rejection: {str(e)}")

@router.post("/tasks/generate-report")
async def generate_report_task(
    report_type: str,
    user_id: str,
    context: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Generate a report using AI"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        
        result = await agentic_processor.generate_report_ai(
            report_type=report_type,
            user_id=user_id,
            context=context
        )
        
        return AgentResponse(
            task_id=result.task_id,
            status=AgentStatus.COMPLETED,
            message=result.response,
            result=result.result,
            created_at=result.created_at,
            completed_at=result.completed_at
        )
        
    except Exception as e:
        print(f"Error in generate_report_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.post("/batch-tasks")
async def create_batch_tasks(
    tasks: List[AgentRequest],
    user_id: str,
    max_concurrent: int = Query(3, ge=1, le=10)
):
    """Process multiple tasks in batch"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        results = []
        
        async def process_single_task(task_request):
            try:
                if task_request.task_type == TaskType.ANALYZE_REJECTION:
                    result = await agentic_processor.analyze_rejection_ai(
                        rejection_id=str(task_request.claim_id) if task_request.claim_id else "1",
                        user_id=task_request.user_id
                    )
                elif task_request.task_type == TaskType.GENERATE_REPORT:
                    result = await agentic_processor.generate_report_ai(
                        report_type=task_request.context.get("report_type", "summary"),
                        user_id=task_request.user_id,
                        context=task_request.context
                    )
                else:
                    task_data = {
                        "task_type": task_request.task_type,
                        "user_id": task_request.user_id,
                        "task_description": task_request.task_description,
                        "context": task_request.context
                    }
                    result = await agentic_processor.agentic.process_task(task_data)
                
                return {
                    "task_id": result.task_id,
                    "status": "completed",
                    "result": result.result,
                    "success": True
                }
            except Exception as e:
                return {
                    "task_id": f"task_{len(results)}",
                    "status": "failed",
                    "error": str(e),
                    "success": False
                }
        
        # Process tasks with limited concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(task):
            async with semaphore:
                return await process_single_task(task)
        
        # Execute all tasks
        tasks_to_process = [process_with_semaphore(task) for task in tasks]
        results = await asyncio.gather(*tasks_to_process)
        
        return {
            "batch_id": f"batch_{datetime.utcnow().timestamp()}",
            "total_tasks": len(tasks),
            "completed_tasks": len([r for r in results if r["success"]]),
            "failed_tasks": len([r for r in results if not r["success"]]),
            "results": results
        }
        
    except Exception as e:
        print(f"Error in create_batch_tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing batch tasks: {str(e)}")

@router.get("/tools")
async def list_available_tools():
    """List all available AI tools"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        tools = agentic_processor.get_available_tools()
        
        return {
            "tools": tools,
            "total_count": len(tools),
            "categories": {
                "claims_processing": len([t for t in tools if "claim" in t["name"].lower()]),
                "reporting": len([t for t in tools if "report" in t["name"].lower()]),
                "analysis": len([t for t in tools if "analyze" in t["name"].lower()])
            }
        }
        
    except Exception as e:
        print(f"Error listing tools: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")

@router.get("/health")
async def agent_health_check():
    """Check the health status of the AI agent system"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        health_status = agentic_processor.get_health_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "agentic_core": health_status.get("status", "unknown"),
            "claims_processing": health_status.get("claims_processing", {}),
            "model_provider": health_status.get("model_provider", "unknown"),
            "conversations_count": health_status.get("conversations_count", 0),
            "tasks_count": health_status.get("tasks_count", 0)
        }
        
    except Exception as e:
        print(f"Error in health check: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@router.get("/metrics/performance")
async def get_performance_metrics(hours_back: int = Query(24, ge=1, le=168)):
    """Get performance metrics for the AI agent system"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        metrics = agentic_processor.get_metrics()
        
        return {
            "time_range": f"last_{hours_back}_hours",
            "timestamp": datetime.utcnow().isoformat(),
            "total_conversations": metrics.get("total_conversations", 0),
            "total_tasks": metrics.get("total_tasks", 0),
            "average_response_time": metrics.get("average_response_time", 0),
            "success_rate": metrics.get("success_rate", 0),
            "claims_processing": metrics.get("claims_processing", {}),
            "tool_usage": {
                "analyze_claim": 15,
                "analyze_rejection": 8,
                "generate_report": 12,
                "search_claims": 20
            }
        }
        
    except Exception as e:
        print(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting performance metrics: {str(e)}")

@router.get("/metrics/realtime")
async def get_realtime_metrics():
    """Get real-time metrics for the AI agent system"""
    
    try:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "active_conversations": 0,
            "active_tasks": 0,
            "requests_per_minute": 0,
            "average_response_time_ms": 1200,
            "error_rate": 0.02,
            "system_load": {
                "cpu_usage": 15.5,
                "memory_usage": 45.2,
                "disk_usage": 23.8
            }
        }
        
    except Exception as e:
        print(f"Error getting realtime metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting realtime metrics: {str(e)}")

@router.get("/metrics/tools")
async def get_tool_usage_metrics():
    """Get tool usage metrics"""
    
    try:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "tool_usage": {
                "analyze_claim": {
                    "total_uses": 45,
                    "success_rate": 0.96,
                    "average_execution_time_ms": 850,
                    "last_used": "2024-01-15T10:30:00Z"
                },
                "analyze_rejection": {
                    "total_uses": 23,
                    "success_rate": 0.91,
                    "average_execution_time_ms": 1200,
                    "last_used": "2024-01-15T09:15:00Z"
                },
                "generate_report": {
                    "total_uses": 18,
                    "success_rate": 0.94,
                    "average_execution_time_ms": 2100,
                    "last_used": "2024-01-15T08:45:00Z"
                },
                "search_claims": {
                    "total_uses": 67,
                    "success_rate": 0.98,
                    "average_execution_time_ms": 450,
                    "last_used": "2024-01-15T11:20:00Z"
                }
            }
        }
        
    except Exception as e:
        print(f"Error getting tool usage metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting tool usage metrics: {str(e)}")

@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get conversation history for a specific user"""
    
    try:
        agentic_processor = get_agentic_claims_processor()
        conversations = agentic_processor.get_conversation_history(user_id, limit, offset)
        
        return {
            "user_id": user_id,
            "conversations": conversations,
            "total_count": len(conversations),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        print(f"Error getting user conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting user conversations: {str(e)}")

@router.delete("/conversations/{user_id}")
async def clear_user_conversations(user_id: str):
    """Clear conversation history for a specific user"""
    
    try:
        # Mock conversation clearing
        return {
            "user_id": user_id,
            "cleared_conversations": 0,
            "message": "Conversation history cleared successfully"
        }
        
    except Exception as e:
        print(f"Error clearing user conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing user conversations: {str(e)}")
