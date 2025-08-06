# =============================================================================
# FILE: backend/app/api/routes/agent.py
# =============================================================================
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime

from ...database.connection import get_db
from ...agent.manager import get_agent_manager
from ...agent.monitoring import get_agent_metrics
from ...schemas.agent import AgentRequest, AgentResponse, TaskType, AgentStatus

router = APIRouter()

@router.post("/tasks", response_model=AgentResponse)
async def create_agent_task(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and execute an agent task"""
    
    try:
        agent_manager = get_agent_manager()
        
        # Convert Pydantic model to dict and add task ID
        request_dict = request.dict()
        task_id = f"task_{datetime.utcnow().timestamp()}"
        request_dict["task_id"] = task_id
        
        # Process the request
        result = await agent_manager.process_task(request_dict)
        
        return AgentResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing agent request: {str(e)}")

@router.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    
    agent_manager = get_agent_manager()
    status = agent_manager.get_task_status(task_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return status

@router.get("/tasks/active")
async def get_active_tasks():
    """Get all currently active tasks"""
    
    agent_manager = get_agent_manager()
    return {"active_tasks": agent_manager.get_active_tasks()}

@router.post("/tasks/cleanup")
async def cleanup_old_tasks(max_age_hours: int = Query(24, ge=1, le=168)):
    """Clean up old completed tasks"""
    
    agent_manager = get_agent_manager()
    agent_manager.cleanup_old_tasks(max_age_hours)
    
    return {"message": f"Cleaned up tasks older than {max_age_hours} hours"}

@router.post("/tasks/analyze-claim/{claim_id}")
async def analyze_claim_task(
    claim_id: int,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Quick task to analyze a specific claim"""
    
    request = AgentRequest(
        task_type=TaskType.VALIDATE_CLAIM,
        user_id=user_id,
        task_description=f"Analyze and validate claim {claim_id}",
        context={"claim_id": claim_id}
    )
    
    agent_manager = get_agent_manager()
    response = await agent_manager.process_task(request.dict())
    
    return AgentResponse(**response)

@router.post("/tasks/process-rejection/{claim_id}")
async def process_rejection_task(
    claim_id: int,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Task to analyze a rejected claim and suggest fixes"""
    
    request = AgentRequest(
        task_type=TaskType.ANALYZE_REJECTION,
        user_id=user_id,
        task_description=f"Analyze rejection for claim {claim_id} and suggest fixes",
        context={"claim_id": claim_id}
    )
    
    agent_manager = get_agent_manager()
    response = await agent_manager.process_task(request.dict())
    
    return AgentResponse(**response)

@router.post("/tasks/generate-report")
async def generate_report_task(
    report_type: str,
    user_id: str,
    context: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Generate various types of reports"""
    
    request = AgentRequest(
        task_type=TaskType.GENERATE_REPORT,
        user_id=user_id,
        task_description=f"Generate {report_type} report",
        context={"report_type": report_type, **(context or {})}
    )
    
    agent_manager = get_agent_manager()
    response = await agent_manager.process_task(request.dict())
    
    return AgentResponse(**response)

@router.post("/chat")
async def chat_with_agent(
    message: str,
    user_id: str,
    context: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Chat interface for natural language questions"""
    
    request = AgentRequest(
        task_type=TaskType.ANSWER_QUESTION,
        user_id=user_id,
        task_description=message,
        context=context or {}
    )
    
    agent_manager = get_agent_manager()
    response = await agent_manager.process_task(request.dict())
    
    return AgentResponse(**response)

@router.post("/batch-tasks")
async def create_batch_tasks(
    tasks: List[AgentRequest],
    user_id: str,
    max_concurrent: int = Query(3, ge=1, le=10)
):
    """Process multiple tasks in batch with concurrency control"""
    
    agent_manager = get_agent_manager()
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single_task(task_request):
        async with semaphore:
            try:
                request_dict = task_request.dict()
                request_dict["user_id"] = user_id
                return await agent_manager.process_task(request_dict)
            except Exception as e:
                return {"error": str(e), "task": task_request.dict()}
    
    # Process all tasks concurrently with limit
    results = await asyncio.gather(
        *[process_single_task(task) for task in tasks],
        return_exceptions=True
    )
    
    return {
        "batch_id": f"batch_{datetime.utcnow().timestamp()}",
        "total_tasks": len(tasks),
        "results": results
    }

@router.get("/tools")
async def list_available_tools():
    """List all available tools for the agent"""
    
    from ...agent.tools import ClaimsTools
    tools = ClaimsTools()
    tool_list = []
    
    for tool in tools.get_tools():
        tool_list.append({
            "name": tool.name,
            "description": tool.description,
            "type": type(tool).__name__
        })
    
    return {"tools": tool_list}

@router.get("/health")
async def agent_health_check():
    """Check agent health and status"""
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager.agent:
            await agent_manager.initialize()
        
        # Test with a simple task
        test_request = {
            "task_type": TaskType.ANSWER_QUESTION,
            "user_id": "health_check",
            "task_description": "System health check",
            "context": {}
        }
        
        start_time = datetime.utcnow()
        await agent_manager.process_task(test_request)
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "status": "healthy",
            "agent_initialized": agent_manager.agent is not None,
            "tools_count": len(agent_manager.tools.get_tools()) if agent_manager.tools else 0,
            "active_tasks": len(agent_manager.active_tasks),
            "response_time": response_time,
            "model_provider": agent_manager.settings.MODEL_PROVIDER,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/metrics/performance")
async def get_performance_metrics(hours_back: int = Query(24, ge=1, le=168)):
    """Get agent performance metrics"""
    
    metrics = get_agent_metrics()
    return metrics.get_performance_summary(hours_back)

@router.get("/metrics/realtime")
async def get_realtime_metrics():
    """Get real-time agent metrics"""
    
    metrics = get_agent_metrics()
    return metrics.get_real_time_stats()

@router.get("/metrics/tools")
async def get_tool_usage_metrics():
    """Get tool usage statistics"""
    
    metrics = get_agent_metrics()
    
    # Analyze tool performance
    from collections import defaultdict
    tool_stats = defaultdict(lambda: {"usage_count": 0, "success_count": 0, "total_duration": 0})
    
    for task in metrics.task_history:
        for tool in task.get("tools_used", []):
            tool_stats[tool]["usage_count"] += 1
            if task["success"]:
                tool_stats[tool]["success_count"] += 1
            tool_stats[tool]["total_duration"] += task["duration"]
    
    # Calculate success rates and average durations
    result = {}
    for tool, stats in tool_stats.items():
        result[tool] = {
            "usage_count": stats["usage_count"],
            "success_rate": (stats["success_count"] / stats["usage_count"] * 100) if stats["usage_count"] > 0 else 0,
            "average_duration": stats["total_duration"] / stats["usage_count"] if stats["usage_count"] > 0 else 0
        }
    
    return {"tool_metrics": result}
