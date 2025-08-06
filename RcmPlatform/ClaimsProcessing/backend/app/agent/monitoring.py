# =============================================================================
# FILE: backend/app/agent/monitoring.py
# =============================================================================
import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio

logger = logging.getLogger(__name__)

class AgentMetrics:
    """Collect and manage agent performance metrics"""
    
    def __init__(self, max_history_size: int = 1000):
        self.max_history_size = max_history_size
        self.task_history = deque(maxlen=max_history_size)
        self.error_history = deque(maxlen=max_history_size)
        self.performance_metrics = defaultdict(list)
        
    def record_task_completion(self, 
                             task_type: str, 
                             duration: float, 
                             success: bool,
                             tools_used: List[str],
                             confidence_score: float = None):
        """Record task completion metrics"""
        
        timestamp = datetime.utcnow()
        
        record = {
            "timestamp": timestamp,
            "task_type": task_type,
            "duration": duration,
            "success": success,
            "tools_used": tools_used,
            "confidence_score": confidence_score
        }
        
        self.task_history.append(record)
        
        # Update performance metrics
        self.performance_metrics[f"{task_type}_duration"].append(duration)
        self.performance_metrics[f"{task_type}_success_rate"].append(1 if success else 0)
        
        if confidence_score is not None:
            self.performance_metrics[f"{task_type}_confidence"].append(confidence_score)
    
    def record_error(self, task_type: str, error_message: str, error_type: str = "unknown"):
        """Record error information"""
        
        error_record = {
            "timestamp": datetime.utcnow(),
            "task_type": task_type,
            "error_message": error_message,
            "error_type": error_type
        }
        
        self.error_history.append(error_record)
    
    def get_performance_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """Get performance summary for the last N hours"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        recent_tasks = [
            task for task in self.task_history 
            if task["timestamp"] >= cutoff_time
        ]
        
        recent_errors = [
            error for error in self.error_history 
            if error["timestamp"] >= cutoff_time
        ]
        
        if not recent_tasks:
            return {"message": "No tasks in the specified time period"}
        
        # Calculate metrics
        total_tasks = len(recent_tasks)
        successful_tasks = sum(1 for task in recent_tasks if task["success"])
        success_rate = (successful_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        avg_duration = sum(task["duration"] for task in recent_tasks) / total_tasks
        
        # Task type breakdown
        task_type_counts = defaultdict(int)
        for task in recent_tasks:
            task_type_counts[task["task_type"]] += 1
        
        # Error analysis
        error_type_counts = defaultdict(int)
        for error in recent_errors:
            error_type_counts[error["error_type"]] += 1
        
        # Tool usage
        tool_usage = defaultdict(int)
        for task in recent_tasks:
            for tool in task.get("tools_used", []):
                tool_usage[tool] += 1
        
        # Confidence scores
        confidence_scores = [
            task["confidence_score"] for task in recent_tasks 
            if task.get("confidence_score") is not None
        ]
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else None
        
        return {
            "time_period": f"Last {hours_back} hours",
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": round(success_rate, 2),
            "average_duration": round(avg_duration, 2),
            "average_confidence": round(avg_confidence, 2) if avg_confidence else None,
            "task_type_breakdown": dict(task_type_counts),
            "error_breakdown": dict(error_type_counts),
            "tool_usage": dict(tool_usage),
            "total_errors": len(recent_errors)
        }
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Get real-time statistics"""
        
        last_hour = datetime.utcnow() - timedelta(hours=1)
        last_10_minutes = datetime.utcnow() - timedelta(minutes=10)
        
        recent_tasks_hour = [
            task for task in self.task_history 
            if task["timestamp"] >= last_hour
        ]
        
        recent_tasks_10min = [
            task for task in self.task_history 
            if task["timestamp"] >= last_10_minutes
        ]
        
        return {
            "tasks_last_hour": len(recent_tasks_hour),
            "tasks_last_10_minutes": len(recent_tasks_10min),
            "current_success_rate_hour": (
                sum(1 for task in recent_tasks_hour if task["success"]) / 
                len(recent_tasks_hour) * 100
            ) if recent_tasks_hour else 0,
            "avg_response_time_10min": (
                sum(task["duration"] for task in recent_tasks_10min) / 
                len(recent_tasks_10min)
            ) if recent_tasks_10min else 0,
            "timestamp": datetime.utcnow().isoformat()
        }

# Global metrics instance
_agent_metrics = AgentMetrics()

def get_agent_metrics() -> AgentMetrics:
    """Get the global agent metrics instance"""
    return _agent_metrics
