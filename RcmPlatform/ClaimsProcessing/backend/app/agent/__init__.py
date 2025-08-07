# Mock agent module - AI dependencies commented out
from app.agent.models import AgentRequest, AgentResponse, TaskType, AgentStatus
# from app.agent.graph import ClaimsProcessingGraph
# from app.agent.tools import ClaimsTools
# from app.agent.state import ClaimsAgentState
# from app.agent.manager import get_agent_manager

# Mock implementations
class ClaimsProcessingGraph:
    """Mock LangGraph implementation for claims processing agent"""
    def __init__(self, llm, tools_instance):
        self.llm = llm
        self.tools = tools_instance.get_tools() if tools_instance else []
    
    async def process_request(self, request):
        return AgentResponse(
            task_id="mock-task-id",
            status=AgentStatus.COMPLETED,
            result={"message": "AI Agent functionality is currently disabled"},
            message="AI Agent is not available in this build",
            suggestions=[],
            next_actions=[],
            confidence_score=0.0,
            processing_time=0.0,
            completed_at=None
        )

class ClaimsTools:
    """Mock tools implementation"""
    def get_tools(self):
        return []

class ClaimsAgentState:
    """Mock state implementation"""
    def __init__(self, **kwargs):
        self.task_id = kwargs.get('task_id', 'mock-task')
        self.task_type = kwargs.get('task_type', TaskType.CHAT)
        self.user_id = kwargs.get('user_id', 'mock-user')
        self.description = kwargs.get('description', '')
        self.context = kwargs.get('context', {})
        self.status = kwargs.get('status', AgentStatus.PROCESSING)

def get_agent_manager():
    """Mock agent manager"""
    class MockAgentManager:
        def __init__(self):
            self.agent = None
        
        async def initialize(self):
            pass
        
        def cleanup_old_tasks(self, max_age_hours=1):
            pass
    
    return MockAgentManager()
