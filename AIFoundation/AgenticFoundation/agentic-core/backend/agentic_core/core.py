"""
Agentic Core - Main entry point for the AI agent framework
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4

from .manager import AgentManager, get_agent_manager, initialize_agent_manager
from .schemas import AgentRequest, AgentResponse, TaskType, AgentStatus, Conversation, Message
from .config import Settings, get_settings
from .tools import ToolRegistry, get_global_tool_registry

logger = logging.getLogger(__name__)


class AgenticCore:
    """
    Main Agentic Core class that provides a unified interface for AI agent operations.
    """
    
    def __init__(
        self,
        model_provider: str = "openai",
        api_key: Optional[str] = None,
        settings: Optional[Settings] = None,
        **kwargs
    ):
        self.settings = settings or get_settings()
        self.model_provider = model_provider
        self.api_key = api_key or self.settings.AI_API_KEY
        
        # Initialize agent manager
        self.agent_manager = initialize_agent_manager(
            model_provider=model_provider,
            api_key=self.api_key,
            settings=self.settings
        )
        
        # Initialize tool registry
        self.tool_registry = get_global_tool_registry()
        
        # Initialize conversation storage
        self.conversations: Dict[str, Conversation] = {}
        
        logger.info(f"AgenticCore initialized with model provider: {model_provider}")
    
    async def chat(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Chat with the AI agent.
        
        Args:
            message: User message
            user_id: User identifier
            context: Additional context
            conversation_id: Conversation identifier
            
        Returns:
            Agent response
        """
        task_id = str(uuid4())
        
        # Create or get conversation
        if conversation_id and conversation_id in self.conversations:
            conversation = self.conversations[conversation_id]
        else:
            conversation = Conversation(
                user_id=user_id,
                title=message[:50] + "..." if len(message) > 50 else message,
                messages=[]
            )
            conversation_id = str(uuid4())
            conversation.conversation_id = conversation_id
            self.conversations[conversation_id] = conversation
        
        # Add user message to conversation
        user_message = Message(
            role="user",
            content=message,
            timestamp=datetime.utcnow()
        )
        conversation.messages.append(user_message)
        
        # Process the chat request
        request_data = {
            "task_id": task_id,
            "task_type": "chat",
            "user_id": user_id,
            "task_description": message,
            "context": context or {},
            "conversation_id": conversation_id
        }
        
        try:
            result = await self.agent_manager.process_task(request_data)
            
            # Add agent response to conversation
            agent_message = Message(
                role="assistant",
                content=result.get("response", ""),
                timestamp=datetime.utcnow()
            )
            conversation.messages.append(agent_message)
            conversation.updated_at = datetime.utcnow()
            
            return AgentResponse(
                task_id=task_id,
                task_type=TaskType.CHAT,
                status=AgentStatus.COMPLETED,
                response=result.get("response", ""),
                result=result.get("result"),
                created_at=result.get("created_at", datetime.utcnow()),
                completed_at=result.get("completed_at", datetime.utcnow())
            )
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return AgentResponse(
                task_id=task_id,
                task_type=TaskType.CHAT,
                status=AgentStatus.FAILED,
                response=f"Error: {str(e)}",
                error=str(e),
                created_at=datetime.utcnow()
            )
    
    async def process_task(
        self,
        task_type: TaskType,
        user_id: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a specific task.
        
        Args:
            task_type: Type of task
            user_id: User identifier
            task_description: Task description
            context: Additional context
            
        Returns:
            Agent response
        """
        task_id = str(uuid4())
        
        request_data = {
            "task_id": task_id,
            "task_type": task_type.value,
            "user_id": user_id,
            "task_description": task_description,
            "context": context or {}
        }
        
        try:
            result = await self.agent_manager.process_task(request_data)
            
            return AgentResponse(
                task_id=task_id,
                task_type=task_type,
                status=AgentStatus.COMPLETED,
                response=result.get("response", ""),
                result=result.get("result"),
                created_at=result.get("created_at", datetime.utcnow()),
                completed_at=result.get("completed_at", datetime.utcnow())
            )
            
        except Exception as e:
            logger.error(f"Error processing task: {e}")
            return AgentResponse(
                task_id=task_id,
                task_type=task_type,
                status=AgentStatus.FAILED,
                response=f"Error: {str(e)}",
                error=str(e),
                created_at=datetime.utcnow()
            )
    
    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """
        Get conversation history for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip
            
        Returns:
            List of conversations
        """
        user_conversations = [
            conv for conv in self.conversations.values()
            if conv.user_id == user_id
        ]
        
        # Sort by updated_at descending
        user_conversations.sort(key=lambda x: x.updated_at, reverse=True)
        
        return user_conversations[offset:offset + limit]
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation or None
        """
        return self.conversations.get(conversation_id)
    
    def clear_conversation_history(self, user_id: str) -> bool:
        """
        Clear conversation history for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful
        """
        try:
            # Remove conversations for the user
            conversations_to_remove = [
                conv_id for conv_id, conv in self.conversations.items()
                if conv.user_id == user_id
            ]
            
            for conv_id in conversations_to_remove:
                del self.conversations[conv_id]
            
            logger.info(f"Cleared {len(conversations_to_remove)} conversations for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing conversation history: {e}")
            return False
    
    def register_tool(self, tool):
        """
        Register a tool with the agent.
        
        Args:
            tool: Tool instance to register
        """
        self.tool_registry.register_tool(tool)
        logger.info(f"Registered tool: {tool.name}")
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools.
        
        Returns:
            List of tool schemas
        """
        tools = self.tool_registry.get_enabled_tools()
        return [tool.get_schema() for tool in tools]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific tool.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        return await self.tool_registry.execute_tool(tool_name, **kwargs)
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the health status of the agent.
        
        Returns:
            Health status information
        """
        try:
            # Test model connection
            model_connected = True  # This would be a real test in production
            
            # Get active tasks count
            active_tasks = len(self.agent_manager.get_active_tasks())
            
            # Get tools count
            tools_count = len(self.tool_registry.get_enabled_tools())
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": self.settings.APP_VERSION,
                "model_connected": model_connected,
                "active_tasks": active_tasks,
                "tools_count": tools_count,
                "conversations_count": len(self.conversations)
            }
            
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": self.settings.APP_VERSION,
                "error": str(e)
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Returns:
            Performance metrics
        """
        try:
            # Get tool usage stats
            tool_stats = self.tool_registry.get_tool_usage_stats()
            
            # Get active tasks
            active_tasks = self.agent_manager.get_active_tasks()
            
            # Calculate basic metrics
            total_tool_executions = sum(
                stats["total_executions"] for stats in tool_stats.values()
            )
            
            successful_tool_executions = sum(
                stats["successful_executions"] for stats in tool_stats.values()
            )
            
            success_rate = (
                (successful_tool_executions / total_tool_executions * 100)
                if total_tool_executions > 0 else 0
            )
            
            return {
                "total_requests": total_tool_executions,
                "success_rate": success_rate,
                "active_tasks": len(active_tasks),
                "tools_usage": tool_stats,
                "conversations_count": len(self.conversations),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self):
        """Close the agent and cleanup resources."""
        try:
            await self.agent_manager.close()
            logger.info("AgenticCore closed successfully")
        except Exception as e:
            logger.error(f"Error closing AgenticCore: {e}")


# Factory function to create AgenticCore instance
def create_agentic_core(
    model_provider: str = "openai",
    api_key: Optional[str] = None,
    settings: Optional[Settings] = None,
    **kwargs
) -> AgenticCore:
    """
    Create an AgenticCore instance.
    
    Args:
        model_provider: AI model provider
        api_key: API key for the model provider
        settings: Application settings
        **kwargs: Additional arguments
        
    Returns:
        AgenticCore instance
    """
    return AgenticCore(
        model_provider=model_provider,
        api_key=api_key,
        settings=settings,
        **kwargs
    )


# Global instance
_agentic_core: Optional[AgenticCore] = None


def get_agentic_core() -> AgenticCore:
    """Get the global AgenticCore instance."""
    global _agentic_core
    if _agentic_core is None:
        raise RuntimeError("AgenticCore not initialized. Call initialize_agentic_core() first.")
    return _agentic_core


def initialize_agentic_core(
    model_provider: str = "openai",
    api_key: Optional[str] = None,
    settings: Optional[Settings] = None
) -> AgenticCore:
    """Initialize the global AgenticCore instance."""
    global _agentic_core
    
    if _agentic_core is not None:
        logger.warning("AgenticCore already initialized")
        return _agentic_core
    
    _agentic_core = create_agentic_core(
        model_provider=model_provider,
        api_key=api_key,
        settings=settings
    )
    
    logger.info("AgenticCore initialized globally")
    return _agentic_core 