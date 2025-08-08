# =============================================================================
# FILE: backend/app/api/agent.py
# =============================================================================
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

from ..agent.manager import AgentManager
from ..agent.state import TaskType, AgentStatus

router = APIRouter(prefix="/agent", tags=["Agent"])

# Initialize agent manager
agent_manager = AgentManager()

# Pydantic models for request/response
class AgentRequest(BaseModel):
    task_description: str
    user_id: str
    task_type: Optional[str] = "general_query"
    context: Optional[Dict[str, Any]] = {}

class AgentResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    message: str
    error: Optional[str] = None
    suggestions: List[str] = []
    next_actions: List[str] = []
    confidence_score: float = 0.0
    processing_time: float = 0.0
    completed_at: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    processing_time: Optional[float] = None
    created_at: str
    updated_at: Optional[str] = None

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """Chat with the scheduling agent"""
    try:
        # Prepare request for agent
        agent_request = {
            "user_id": request.user_id,
            "task_description": request.task_description,
            "task_type": request.task_type,
            "context": request.context or {}
        }
        
        # Process through agent
        response = await agent_manager.process_request(agent_request)
        
        return AgentResponse(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    try:
        task = agent_manager.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskStatusResponse(
            task_id=task["task_id"],
            status=task["status"],
            result=task.get("result"),
            message=task.get("message"),
            processing_time=task.get("processing_time"),
            created_at=task["start_time"].isoformat(),
            updated_at=task.get("end_time", task["start_time"]).isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: str):
    """Cancel an active task"""
    try:
        success = agent_manager.cancel_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found or already completed")
        
        return {"message": "Task cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling task: {str(e)}")

@router.get("/tasks", response_model=List[TaskStatusResponse])
async def get_active_tasks():
    """Get all currently active tasks"""
    try:
        active_tasks = agent_manager.get_active_tasks()
        
        return [
            TaskStatusResponse(
                task_id=task["task_id"],
                status=task["status"],
                result=task.get("result"),
                message=task.get("message"),
                processing_time=task.get("processing_time"),
                created_at=task["start_time"].isoformat(),
                updated_at=task.get("end_time", task["start_time"]).isoformat()
            )
            for task in active_tasks
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving active tasks: {str(e)}")

@router.get("/history", response_model=List[TaskStatusResponse])
async def get_task_history(limit: int = 50):
    """Get recent task history"""
    try:
        history = agent_manager.get_task_history(limit=limit)
        
        return [
            TaskStatusResponse(
                task_id=task["task_id"],
                status=task["status"],
                result=task.get("result"),
                message=task.get("message"),
                processing_time=task.get("processing_time"),
                created_at=task["start_time"].isoformat(),
                updated_at=task.get("end_time", task["start_time"]).isoformat()
            )
            for task in history
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task history: {str(e)}")

@router.get("/status")
async def get_agent_status():
    """Get overall agent status and statistics"""
    try:
        return agent_manager.get_agent_status()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent status: {str(e)}")

@router.get("/statistics")
async def get_task_statistics():
    """Get statistics by task type"""
    try:
        return agent_manager.get_task_type_statistics()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task statistics: {str(e)}")

@router.get("/monitoring/health")
async def get_agent_health():
    """Get detailed agent health information"""
    try:
        return agent_manager.monitoring.get_health_status()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent health: {str(e)}")

@router.get("/monitoring/performance")
async def get_performance_metrics(window_minutes: int = 60):
    """Get performance metrics for the specified time window"""
    try:
        return agent_manager.monitoring.get_performance_metrics(window_minutes=window_minutes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving performance metrics: {str(e)}")

@router.get("/monitoring/errors")
async def get_error_summary(hours: int = 24):
    """Get error summary for the specified time period"""
    try:
        return agent_manager.monitoring.get_error_summary(hours=hours)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving error summary: {str(e)}")

@router.get("/monitoring/uptime")
async def get_agent_uptime():
    """Get agent uptime information"""
    try:
        return agent_manager.monitoring.get_uptime()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving uptime: {str(e)}")

@router.post("/tools/execute")
async def execute_tool(tool_name: str, args: Dict[str, Any]):
    """Execute a specific agent tool directly"""
    try:
        # Find the tool
        tool = None
        for t in agent_manager.tools.get_tools():
            if t.name == tool_name:
                tool = t
                break
        
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        # Execute the tool
        result = tool._run(**args)
        
        return {
            "tool_name": tool_name,
            "result": result,
            "executed_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")

@router.get("/tools")
async def list_available_tools():
    """List all available agent tools"""
    try:
        tools = agent_manager.tools.get_tools()
        
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "args_schema": getattr(tool, 'args_schema', {})
            }
            for tool in tools
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")

@router.delete("/history")
async def clear_task_history(older_than_days: int = 30):
    """Clear old task history"""
    try:
        cleared_count = agent_manager.clear_history(older_than_days=older_than_days)
        
        return {
            "message": f"Cleared {cleared_count} old task records",
            "cleared_count": cleared_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@router.get("/export/history")
async def export_task_history(format: str = "json"):
    """Export task history in specified format"""
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'json' or 'csv'")
        
        exported_data = agent_manager.export_task_history(format=format)
        
        return {
            "format": format,
            "data": exported_data,
            "exported_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting history: {str(e)}")

@router.get("/export/metrics")
async def export_monitoring_metrics(format: str = "json"):
    """Export monitoring metrics in specified format"""
    try:
        if format not in ["json"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'json'")
        
        exported_data = agent_manager.monitoring.export_metrics(format=format)
        
        return {
            "format": format,
            "data": exported_data,
            "exported_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting metrics: {str(e)}")

@router.post("/reset")
async def reset_agent_metrics():
    """Reset all agent metrics and monitoring data"""
    try:
        agent_manager.monitoring.reset_metrics()
        agent_manager.task_history = []
        agent_manager.active_tasks = {}
        
        return {"message": "Agent metrics reset successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting metrics: {str(e)}")

# Health check endpoint
@router.get("/health")
async def agent_health_check():
    """Health check for the agent service"""
    try:
        health_status = agent_manager.monitoring.get_health_status()
        
        return {
            "status": "healthy" if health_status["status"] == "healthy" else "degraded",
            "agent_status": health_status["status"],
            "health_score": health_status["health_score"],
            "uptime_seconds": health_status["uptime"]["uptime_seconds"],
            "last_activity_seconds": health_status["last_activity"]["seconds_since_last"]
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        } 