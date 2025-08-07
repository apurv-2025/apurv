# =============================================================================
# FILE: backend/app/agent/manager.py (Mock Version)
# =============================================================================
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session

# Mock imports - AI dependencies commented out
# from .graph import ClaimsProcessingGraph
# from .tools import ClaimsTools
# from .model_factory import ModelFactory
# from ..config import agent_settings
from ..database.connection import SessionLocal

logger = logging.getLogger(__name__)

class AgentManager:
    """Mock agent manager - AI functionality disabled"""
    
    def __init__(self):
        # self.settings = agent_settings
        self.agent = None
        self.tools = None
        self.active_tasks: Dict[str, Any] = {}
        self.task_history: Dict[str, Any] = {}
        
    async def initialize(self):
        """Mock initialization"""
        logger.info("Mock agent initialized - AI functionality disabled")
        self.agent = None
    
    async def process_task(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Mock task processing - AI functionality disabled"""
        
        task_id = request.get("task_id") or f"task_{datetime.utcnow().timestamp()}"
        
        # Track active task
        self.active_tasks[task_id] = {
            "start_time": datetime.utcnow(),
            "request": request,
            "status": "processing"
        }
        
        # Mock response
        mock_response = {
            "task_id": task_id,
            "status": "completed",
            "result": {"message": "AI Agent functionality is currently disabled"},
            "message": "AI Agent is not available in this build",
            "suggestions": [],
            "next_actions": [],
            "confidence_score": 0.0,
            "processing_time": 0.0,
            "completed_at": datetime.utcnow()
        }
        
        # Update task tracking
        self.active_tasks[task_id]["status"] = "completed"
        self.active_tasks[task_id]["end_time"] = datetime.utcnow()
        
        # Move to history
        self.task_history[task_id] = self.active_tasks.pop(task_id)
        
        return mock_response
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a task"""
        
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        elif task_id in self.task_history:
            return self.task_history[task_id]
        else:
            return None
    
    def get_active_tasks(self) -> Dict[str, Any]:
        """Get all active tasks"""
        return self.active_tasks.copy()
    
    def cleanup_old_tasks(self, max_age_hours: int = 24):
        """Clean up old tasks from history"""
        
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for task_id, task_info in self.task_history.items():
            if task_info.get("end_time", datetime.utcnow()) < cutoff_time:
                to_remove.append(task_id)
        
        for task_id in to_remove:
            del self.task_history[task_id]
        
        logger.info(f"Cleaned up {len(to_remove)} old tasks")

# Global agent manager instance
_agent_manager = None

def get_agent_manager() -> AgentManager:
    """Get the global agent manager instance"""
    global _agent_manager
    if _agent_manager is None:
        _agent_manager = AgentManager()
    return _agent_manager
