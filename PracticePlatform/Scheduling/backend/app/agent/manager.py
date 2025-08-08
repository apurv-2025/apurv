# =============================================================================
# FILE: backend/app/agent/manager.py
# =============================================================================
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
import json
import uuid

from .graph import SchedulingAgentGraph
from .tools import SchedulingTools
from .state import AgentStatus, TaskType
from .monitoring import AgentMonitoring

class AgentManager:
    """Manages the scheduling agent lifecycle and operations"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.tools = SchedulingTools()
        self.graph = SchedulingAgentGraph(llm, self.tools)
        self.monitoring = AgentMonitoring()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_history: List[Dict[str, Any]] = []
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request through the agent"""
        
        task_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        # Initialize task tracking
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "user_id": request.get("user_id", "unknown"),
            "task_type": request.get("task_type", "general_query"),
            "description": request.get("task_description", ""),
            "status": AgentStatus.PROCESSING,
            "start_time": start_time,
            "context": request.get("context", {})
        }
        
        try:
            # Process through the graph
            response = await self.graph.process_request(request)
            
            # Update task status
            self.active_tasks[task_id]["status"] = response.get("status", AgentStatus.COMPLETED)
            self.active_tasks[task_id]["end_time"] = datetime.now()
            self.active_tasks[task_id]["processing_time"] = response.get("processing_time", 0)
            self.active_tasks[task_id]["result"] = response.get("result", {})
            
            # Add to history
            self.task_history.append(self.active_tasks[task_id].copy())
            
            # Update monitoring
            self.monitoring.record_task_completion(
                task_id=task_id,
                task_type=request.get("task_type", "general_query"),
                status=response.get("status", AgentStatus.COMPLETED),
                processing_time=response.get("processing_time", 0),
                success=response.get("status") == AgentStatus.COMPLETED
            )
            
            # Clean up active task
            del self.active_tasks[task_id]
            
            return response
            
        except Exception as e:
            # Handle errors
            error_response = {
                "task_id": task_id,
                "status": AgentStatus.FAILED,
                "error": str(e),
                "message": f"An error occurred while processing your request: {str(e)}",
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "completed_at": datetime.now().isoformat()
            }
            
            # Update task status
            self.active_tasks[task_id]["status"] = AgentStatus.FAILED
            self.active_tasks[task_id]["end_time"] = datetime.now()
            self.active_tasks[task_id]["error"] = str(e)
            
            # Add to history
            self.task_history.append(self.active_tasks[task_id].copy())
            
            # Update monitoring
            self.monitoring.record_task_completion(
                task_id=task_id,
                task_type=request.get("task_type", "general_query"),
                status=AgentStatus.FAILED,
                processing_time=(datetime.now() - start_time).total_seconds(),
                success=False
            )
            
            # Clean up active task
            del self.active_tasks[task_id]
            
            return error_response
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all currently active tasks"""
        return list(self.active_tasks.values())
    
    def get_task_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent task history"""
        return self.task_history[-limit:] if self.task_history else []
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        # Check active tasks first
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        
        # Check history
        for task in self.task_history:
            if task["task_id"] == task_id:
                return task
        
        return None
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel an active task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = AgentStatus.CANCELLED
            self.active_tasks[task_id]["end_time"] = datetime.now()
            
            # Add to history
            self.task_history.append(self.active_tasks[task_id].copy())
            
            # Clean up
            del self.active_tasks[task_id]
            
            return True
        
        return False
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get overall agent status and statistics"""
        active_count = len(self.active_tasks)
        total_completed = len([t for t in self.task_history if t["status"] == AgentStatus.COMPLETED])
        total_failed = len([t for t in self.task_history if t["status"] == AgentStatus.FAILED])
        total_cancelled = len([t for t in self.task_history if t["status"] == AgentStatus.CANCELLED])
        
        # Calculate success rate
        total_processed = total_completed + total_failed + total_cancelled
        success_rate = (total_completed / total_processed * 100) if total_processed > 0 else 0
        
        # Get average processing time
        completed_tasks = [t for t in self.task_history if t["status"] == AgentStatus.COMPLETED and "processing_time" in t]
        avg_processing_time = sum(t["processing_time"] for t in completed_tasks) / len(completed_tasks) if completed_tasks else 0
        
        return {
            "status": "healthy" if active_count < 10 else "busy",
            "active_tasks": active_count,
            "total_completed": total_completed,
            "total_failed": total_failed,
            "total_cancelled": total_cancelled,
            "success_rate": round(success_rate, 2),
            "avg_processing_time": round(avg_processing_time, 2),
            "uptime": self.monitoring.get_uptime(),
            "last_activity": self.monitoring.get_last_activity()
        }
    
    def get_task_type_statistics(self) -> Dict[str, Any]:
        """Get statistics by task type"""
        stats = {}
        
        for task in self.task_history:
            task_type = task.get("task_type", "unknown")
            if task_type not in stats:
                stats[task_type] = {
                    "total": 0,
                    "completed": 0,
                    "failed": 0,
                    "cancelled": 0,
                    "avg_processing_time": 0
                }
            
            stats[task_type]["total"] += 1
            
            if task["status"] == AgentStatus.COMPLETED:
                stats[task_type]["completed"] += 1
            elif task["status"] == AgentStatus.FAILED:
                stats[task_type]["failed"] += 1
            elif task["status"] == AgentStatus.CANCELLED:
                stats[task_type]["cancelled"] += 1
        
        # Calculate success rates and average processing times
        for task_type, data in stats.items():
            if data["total"] > 0:
                data["success_rate"] = round((data["completed"] / data["total"]) * 100, 2)
                
                # Calculate average processing time for completed tasks
                completed_tasks = [
                    t for t in self.task_history 
                    if t.get("task_type") == task_type 
                    and t["status"] == AgentStatus.COMPLETED 
                    and "processing_time" in t
                ]
                
                if completed_tasks:
                    data["avg_processing_time"] = round(
                        sum(t["processing_time"] for t in completed_tasks) / len(completed_tasks), 2
                    )
        
        return stats
    
    def clear_history(self, older_than_days: int = 30) -> int:
        """Clear old task history"""
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        original_count = len(self.task_history)
        
        self.task_history = [
            task for task in self.task_history
            if task.get("start_time", datetime.now()) > cutoff_date
        ]
        
        cleared_count = original_count - len(self.task_history)
        return cleared_count
    
    def export_task_history(self, format: str = "json") -> str:
        """Export task history in specified format"""
        if format.lower() == "json":
            return json.dumps(self.task_history, indent=2, default=str)
        elif format.lower() == "csv":
            # Simple CSV export
            if not self.task_history:
                return ""
            
            headers = list(self.task_history[0].keys())
            csv_lines = [",".join(headers)]
            
            for task in self.task_history:
                row = []
                for header in headers:
                    value = task.get(header, "")
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    row.append(str(value))
                csv_lines.append(",".join(row))
            
            return "\n".join(csv_lines)
        else:
            raise ValueError(f"Unsupported format: {format}") 