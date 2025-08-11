"""
Tools - Agent tool system
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all agent tools."""
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.enabled = True
        self.created_at = datetime.utcnow()
        self.last_used = None
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool's parameter schema."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "enabled": self.enabled,
            "parameters": self._get_parameters_schema()
        }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema for the tool."""
        return {}
    
    def update_last_used(self):
        """Update the last used timestamp."""
        self.last_used = datetime.utcnow()


class ToolRegistry:
    """Registry for managing agent tools."""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.execution_history: List[Dict[str, Any]] = []
    
    def register_tool(self, tool: BaseTool):
        """Register a tool with the registry."""
        if tool.name in self.tools:
            logger.warning(f"Tool {tool.name} already registered, overwriting")
        
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool from the registry."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.info(f"Unregistered tool: {tool_name}")
            return True
        return False
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self.tools.values())
    
    def get_enabled_tools(self) -> List[BaseTool]:
        """Get all enabled tools."""
        return [tool for tool in self.tools.values() if tool.enabled]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        if not tool.enabled:
            raise ValueError(f"Tool {tool_name} is disabled")
        
        execution_id = str(uuid4())
        start_time = datetime.utcnow()
        
        try:
            # Execute the tool
            result = await tool.execute(**kwargs)
            
            # Update tool usage
            tool.update_last_used()
            
            # Record execution
            execution_record = {
                "execution_id": execution_id,
                "tool_name": tool_name,
                "parameters": kwargs,
                "result": result,
                "start_time": start_time,
                "end_time": datetime.utcnow(),
                "status": "success"
            }
            self.execution_history.append(execution_record)
            
            logger.info(f"Tool {tool_name} executed successfully")
            return result
            
        except Exception as e:
            # Record failed execution
            execution_record = {
                "execution_id": execution_id,
                "tool_name": tool_name,
                "parameters": kwargs,
                "error": str(e),
                "start_time": start_time,
                "end_time": datetime.utcnow(),
                "status": "failed"
            }
            self.execution_history.append(execution_record)
            
            logger.error(f"Tool {tool_name} execution failed: {e}")
            raise
    
    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent tool execution history."""
        return self.execution_history[-limit:]
    
    def get_tool_usage_stats(self) -> Dict[str, Any]:
        """Get tool usage statistics."""
        stats = {}
        for tool_name, tool in self.tools.items():
            executions = [e for e in self.execution_history if e["tool_name"] == tool_name]
            stats[tool_name] = {
                "total_executions": len(executions),
                "successful_executions": len([e for e in executions if e["status"] == "success"]),
                "failed_executions": len([e for e in executions if e["status"] == "failed"]),
                "last_used": tool.last_used,
                "enabled": tool.enabled
            }
        return stats


# Built-in tools
class SearchTool(BaseTool):
    """Tool for searching information."""
    
    def __init__(self):
        super().__init__(
            name="search",
            description="Search for information on the web"
        )
    
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute a web search."""
        # Simulate search functionality
        await asyncio.sleep(0.5)
        
        return {
            "query": query,
            "results": [
                {
                    "title": f"Search result for: {query}",
                    "url": f"https://example.com/search?q={query}",
                    "snippet": f"This is a simulated search result for '{query}'"
                }
            ],
            "total_results": 1
        }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "Search query",
                "required": True
            }
        }


class CalculatorTool(BaseTool):
    """Tool for mathematical calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations"
        )
    
    async def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """Execute a mathematical calculation."""
        try:
            # Safe evaluation of mathematical expressions
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")
            
            result = eval(expression)
            
            return {
                "expression": expression,
                "result": result,
                "type": "calculation"
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "type": "calculation_error"
            }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate",
                "required": True
            }
        }


class FileReadTool(BaseTool):
    """Tool for reading files."""
    
    def __init__(self):
        super().__init__(
            name="file_read",
            description="Read content from files"
        )
    
    async def execute(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """Read a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "file_path": file_path,
                "content": content,
                "size": len(content),
                "type": "file_read"
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "error": str(e),
                "type": "file_read_error"
            }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read",
                "required": True
            }
        }


class DateTimeTool(BaseTool):
    """Tool for date and time operations."""
    
    def __init__(self):
        super().__init__(
            name="datetime",
            description="Get current date and time information"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Get current date and time."""
        now = datetime.utcnow()
        
        return {
            "current_time": now.isoformat(),
            "timestamp": now.timestamp(),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "timezone": "UTC"
        }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {}


class WeatherTool(BaseTool):
    """Tool for weather information."""
    
    def __init__(self):
        super().__init__(
            name="weather",
            description="Get weather information for a location"
        )
    
    async def execute(self, location: str, **kwargs) -> Dict[str, Any]:
        """Get weather for a location."""
        # Simulate weather API call
        await asyncio.sleep(0.3)
        
        return {
            "location": location,
            "temperature": 22,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 10,
            "forecast": [
                {"day": "Today", "high": 25, "low": 18, "condition": "Sunny"},
                {"day": "Tomorrow", "high": 23, "low": 16, "condition": "Partly Cloudy"}
            ],
            "type": "weather"
        }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "location": {
                "type": "string",
                "description": "Location to get weather for",
                "required": True
            }
        }


# Function-based tool decorator
def tool(name: str, description: str, version: str = "1.0.0"):
    """Decorator to create a tool from a function."""
    def decorator(func: Callable):
        class FunctionTool(BaseTool):
            def __init__(self):
                super().__init__(name, description, version)
                self.func = func
            
            async def execute(self, **kwargs) -> Dict[str, Any]:
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = await func(**kwargs)
                    else:
                        result = func(**kwargs)
                    
                    return {
                        "result": result,
                        "type": "function_tool"
                    }
                except Exception as e:
                    return {
                        "error": str(e),
                        "type": "function_tool_error"
                    }
        
        return FunctionTool()
    return decorator


# Global tool registry instance
_global_tool_registry: Optional[ToolRegistry] = None


def get_global_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance."""
    global _global_tool_registry
    if _global_tool_registry is None:
        _global_tool_registry = ToolRegistry()
        # Register default tools
        _global_tool_registry.register_tool(SearchTool())
        _global_tool_registry.register_tool(CalculatorTool())
        _global_tool_registry.register_tool(DateTimeTool())
        _global_tool_registry.register_tool(WeatherTool())
    return _global_tool_registry 