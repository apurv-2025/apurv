"""
Agent Manager - Core agent orchestration and task processing
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4

from .models import BaseModelProvider
from .tools import ToolRegistry
from .schemas import AgentRequest, AgentResponse, TaskType, AgentStatus
from .config import Settings

logger = logging.getLogger(__name__)


class AgentManager:
    """
    Main agent manager that orchestrates AI agent operations.
    """
    
    def __init__(
        self,
        model_provider: str = "openai",
        api_key: Optional[str] = None,
        settings: Optional[Settings] = None,
        **kwargs
    ):
        self.settings = settings or Settings()
        self.model_provider = model_provider
        self.api_key = api_key or self.settings.AI_API_KEY
        
        # Initialize components
        self.tool_registry = ToolRegistry()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        
        # Initialize model provider
        self._init_model_provider()
        
        logger.info(f"AgentManager initialized with model provider: {model_provider}")
    
    def _init_model_provider(self):
        """Initialize the model provider."""
        if self.model_provider == "openai":
            from .models import OpenAIModelProvider
            self.model_provider_instance = OpenAIModelProvider(
                api_key=self.api_key,
                model=self.settings.AI_MODEL_NAME
            )
        elif self.model_provider == "anthropic":
            from .models import AnthropicModelProvider
            self.model_provider_instance = AnthropicModelProvider(
                api_key=self.api_key,
                model=self.settings.AI_MODEL_NAME
            )
        else:
            self.model_provider_instance = BaseModelProvider(
                api_key=self.api_key,
                model=self.settings.AI_MODEL_NAME
            )
    
    async def process_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an agent task.
        
        Args:
            request_data: Task request data
            
        Returns:
            Task response data
        """
        task_id = request_data.get("task_id", str(uuid4()))
        task_type = request_data.get("task_type", "chat")
        user_id = request_data.get("user_id", "default_user")
        task_description = request_data.get("task_description", "")
        context = request_data.get("context", {})
        
        # Create task entry
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "user_id": user_id,
            "status": "processing",
            "created_at": datetime.utcnow(),
            "context": context
        }
        
        try:
            # Process based on task type
            if task_type == "chat":
                result = await self._process_chat_task(task_description, context)
            elif task_type == "analyze_claim":
                result = await self._process_claim_analysis(context)
            elif task_type == "analyze_rejection":
                result = await self._process_rejection_analysis(context)
            elif task_type == "generate_report":
                result = await self._process_report_generation(context)
            else:
                result = await self._process_generic_task(task_description, context)
            
            # Update task status
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["completed_at"] = datetime.utcnow()
            self.active_tasks[task_id]["result"] = result
            
            return {
                "task_id": task_id,
                "task_type": task_type,
                "status": "completed",
                "response": result.get("response", ""),
                "result": result,
                "created_at": self.active_tasks[task_id]["created_at"],
                "completed_at": self.active_tasks[task_id]["completed_at"]
            }
            
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            self.active_tasks[task_id]["status"] = "failed"
            self.active_tasks[task_id]["error"] = str(e)
            
            return {
                "task_id": task_id,
                "task_type": task_type,
                "status": "failed",
                "error": str(e),
                "created_at": self.active_tasks[task_id]["created_at"]
            }
    
    async def _process_chat_task(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a chat task."""
        try:
            # Generate response using model provider
            response = await self.model_provider_instance.generate(message, context)
            
            return {
                "response": response,
                "confidence": 0.95,
                "processing_time": 1.2
            }
        except Exception as e:
            logger.error(f"Error in chat task: {e}")
            raise
    
    async def _process_claim_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a claim analysis task."""
        claim_id = context.get("claim_id")
        
        # Simulate claim analysis
        analysis = {
            "claim_id": claim_id,
            "issues_found": 2,
            "recommendations": [
                "Verify patient eligibility",
                "Check diagnosis codes"
            ],
            "confidence_score": 0.88
        }
        
        return {
            "response": f"Analysis completed for claim {claim_id}",
            "analysis": analysis
        }
    
    async def _process_rejection_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a rejection analysis task."""
        claim_id = context.get("claim_id")
        
        # Simulate rejection analysis
        analysis = {
            "claim_id": claim_id,
            "rejection_reason": "Invalid diagnosis code",
            "suggested_fixes": [
                "Update diagnosis code to valid ICD-10 code",
                "Add supporting documentation"
            ],
            "resubmission_ready": True,
            "confidence_score": 0.92
        }
        
        return {
            "response": f"Rejection analysis completed for claim {claim_id}",
            "analysis": analysis
        }
    
    async def _process_report_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a report generation task."""
        report_type = context.get("report_type", "summary")
        
        # Simulate report generation
        report = {
            "type": report_type,
            "data": {
                "total_claims": 150,
                "total_charged": 45000,
                "total_paid": 38000,
                "collection_rate": 84.4
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return {
            "response": f"{report_type} report generated successfully",
            "report": report
        }
    
    async def _process_generic_task(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a generic task."""
        try:
            # Use model provider for generic tasks
            response = await self.model_provider_instance.generate(description, context)
            
            return {
                "response": response,
                "task_description": description,
                "context": context
            }
        except Exception as e:
            logger.error(f"Error in generic task: {e}")
            raise
    
    def register_tool(self, tool):
        """Register a tool with the agent manager."""
        self.tool_registry.register_tool(tool)
        logger.info(f"Registered tool: {tool.name}")
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get list of active tasks."""
        return list(self.active_tasks.values())
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task."""
        return self.active_tasks.get(task_id)
    
    async def close(self):
        """Close the agent manager and cleanup resources."""
        try:
            await self.model_provider_instance.close()
            logger.info("AgentManager closed successfully")
        except Exception as e:
            logger.error(f"Error closing AgentManager: {e}")


# Global instance
_agent_manager: Optional[AgentManager] = None


def get_agent_manager() -> AgentManager:
    """Get the global agent manager instance."""
    global _agent_manager
    if _agent_manager is None:
        raise RuntimeError("AgentManager not initialized. Call initialize_agent_manager() first.")
    return _agent_manager


def initialize_agent_manager(
    model_provider: str = "openai",
    api_key: Optional[str] = None,
    settings: Optional[Settings] = None
) -> AgentManager:
    """Initialize the global agent manager instance."""
    global _agent_manager
    
    if _agent_manager is not None:
        logger.warning("AgentManager already initialized")
        return _agent_manager
    
    _agent_manager = AgentManager(
        model_provider=model_provider,
        api_key=api_key,
        settings=settings
    )
    
    logger.info("AgentManager initialized globally")
    return _agent_manager 