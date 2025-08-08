# =============================================================================
# FILE: backend/app/agent/graph.py
# =============================================================================
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.schema import BaseMessage
from typing import Dict, List, Any
import json
import uuid
from datetime import datetime, timedelta

from .state import SchedulingAgentState, TaskType, AgentStatus
from .tools import SchedulingTools

class SchedulingAgentGraph:
    """LangGraph implementation for scheduling agent"""
    
    def __init__(self, llm, tools_instance: SchedulingTools):
        self.llm = llm
        self.tools = tools_instance.get_tools()
        self.tool_executor = ToolExecutor(self.tools)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(SchedulingAgentState)
        
        # Add nodes
        workflow.add_node("analyze_task", self._analyze_task)
        workflow.add_node("plan_execution", self._plan_execution)
        workflow.add_node("execute_tools", self._execute_tools)
        workflow.add_node("synthesize_results", self._synthesize_results)
        workflow.add_node("generate_insights", self._generate_insights)
        workflow.add_node("finalize_response", self._finalize_response)
        workflow.add_node("handle_error", self._handle_error)
        
        # Define edges
        workflow.set_entry_point("analyze_task")
        
        workflow.add_edge("analyze_task", "plan_execution")
        workflow.add_edge("plan_execution", "execute_tools")
        workflow.add_edge("execute_tools", "synthesize_results")
        workflow.add_edge("synthesize_results", "generate_insights")
        workflow.add_edge("generate_insights", "finalize_response")
        workflow.add_edge("finalize_response", END)
        workflow.add_edge("handle_error", END)
        
        # Conditional edges for error handling
        workflow.add_conditional_edges(
            "execute_tools",
            self._should_retry_or_continue,
            {
                "continue": "synthesize_results",
                "retry": "execute_tools",
                "error": "handle_error"
            }
        )
        
        return workflow.compile()
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process an agent request through the graph"""
        
        task_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        try:
            # Simple processing without LangGraph for now
            task_type = TaskType(request.get("task_type", "general_query"))
            description = request["task_description"]
            
            # Analyze the task description
            description_lower = description.lower()
            
            if any(word in description_lower for word in ["schedule", "book", "appointment"]):
                task_type = TaskType.SCHEDULE_APPOINTMENT
                message = "I can help you schedule an appointment. Please provide the patient name, practitioner name, and preferred date/time."
                suggestions = ["Provide patient details", "Specify practitioner", "Choose appointment date"]
            elif any(word in description_lower for word in ["available", "availability", "find", "slot"]):
                task_type = TaskType.FIND_AVAILABILITY
                message = "I can help you find available time slots. Please specify the practitioner and date."
                suggestions = ["Specify practitioner", "Choose date", "Set duration"]
            elif any(word in description_lower for word in ["report", "summary", "statistics"]):
                task_type = TaskType.GENERATE_REPORT
                message = "I can generate scheduling reports for you. What type of report would you like?"
                suggestions = ["Daily report", "Weekly report", "Monthly report"]
            else:
                message = "Hello! I'm your AI scheduling assistant. I can help you with scheduling appointments, finding availability, generating reports, and more. How can I assist you today?"
                suggestions = ["Schedule appointment", "Find availability", "Generate report"]
            
            # Create response
            response = {
                "task_id": task_id,
                "status": AgentStatus.COMPLETED,
                "result": {"task_type": task_type.value, "description": description},
                "message": message,
                "suggestions": suggestions,
                "next_actions": ["Provide more details", "Ask follow-up questions"],
                "confidence_score": 0.8,
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "completed_at": datetime.now().isoformat()
            }
            
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
            return error_response
    
    def _analyze_task(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the user's request and determine the task type"""
        state["current_step"] = "analyze_task"
        state["steps_completed"].append("analyze_task")
        
        # Analyze the task description to determine what tools to use
        description = state["description"].lower()
        
        if any(word in description for word in ["schedule", "book", "appointment"]):
            state["task_type"] = TaskType.SCHEDULE_APPOINTMENT
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["reschedule", "change", "move"]):
            state["task_type"] = TaskType.RESCHEDULE_APPOINTMENT
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["cancel", "remove"]):
            state["task_type"] = TaskType.CANCEL_APPOINTMENT
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["available", "availability", "find", "slot"]):
            state["task_type"] = TaskType.FIND_AVAILABILITY
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["report", "summary", "statistics"]):
            state["task_type"] = TaskType.GENERATE_REPORT
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["analyze", "insights", "patterns"]):
            state["task_type"] = TaskType.ANALYZE_SCHEDULE
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        elif any(word in description for word in ["optimize", "improve", "suggestions"]):
            state["task_type"] = TaskType.OPTIMIZE_SCHEDULE
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        else:
            state["task_type"] = TaskType.GENERAL_QUERY
            state["steps_remaining"] = ["plan_execution", "execute_tools", "synthesize_results", "generate_insights", "finalize_response"]
        
        state["updated_at"] = datetime.now()
        return state
    
    def _plan_execution(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Plan the execution steps based on the task type"""
        state["current_step"] = "plan_execution"
        state["steps_completed"].append("plan_execution")
        
        # Plan which tools to use based on task type
        if state["task_type"] == TaskType.SCHEDULE_APPOINTMENT:
            state["context"]["planned_tools"] = ["get_patient_info", "get_practitioner_info", "find_availability", "schedule_appointment"]
        
        elif state["task_type"] == TaskType.RESCHEDULE_APPOINTMENT:
            state["context"]["planned_tools"] = ["get_appointment", "find_availability", "reschedule_appointment"]
        
        elif state["task_type"] == TaskType.CANCEL_APPOINTMENT:
            state["context"]["planned_tools"] = ["get_appointment", "cancel_appointment"]
        
        elif state["task_type"] == TaskType.FIND_AVAILABILITY:
            state["context"]["planned_tools"] = ["get_practitioner_info", "find_availability"]
        
        elif state["task_type"] == TaskType.GENERATE_REPORT:
            state["context"]["planned_tools"] = ["generate_schedule_report"]
        
        elif state["task_type"] == TaskType.ANALYZE_SCHEDULE:
            state["context"]["planned_tools"] = ["analyze_schedule"]
        
        elif state["task_type"] == TaskType.OPTIMIZE_SCHEDULE:
            state["context"]["planned_tools"] = ["optimize_schedule"]
        
        else:
            state["context"]["planned_tools"] = ["search_appointments", "get_dashboard_stats"]
        
        state["updated_at"] = datetime.now()
        return state
    
    def _execute_tools(self, state: SchedulingAgentState) -> SchedulingAgentState:
        """Execute the planned tools"""
        state.current_step = "execute_tools"
        state.steps_completed.append("execute_tools")
        
        planned_tools = state.context.get("planned_tools", [])
        
        for tool_name in planned_tools:
            try:
                # Prepare tool arguments based on context
                args = self._prepare_tool_args(tool_name, state)
                
                # Execute the tool
                result = self._execute_single_tool(tool_name, args)
                
                # Store the result
                state.tool_results[tool_name] = result
                
            except Exception as e:
                state.tool_errors[tool_name] = str(e)
                state.error_message = f"Error executing {tool_name}: {str(e)}"
        
        state.updated_at = datetime.now()
        return state
    
    def _synthesize_results(self, state: SchedulingAgentState) -> SchedulingAgentState:
        """Synthesize the tool results into a coherent response"""
        state.current_step = "synthesize_results"
        state.steps_completed.append("synthesize_results")
        
        # Combine all tool results
        combined_results = {}
        for tool_name, result in state.tool_results.items():
            try:
                if isinstance(result, str):
                    combined_results[tool_name] = json.loads(result)
                else:
                    combined_results[tool_name] = result
            except:
                combined_results[tool_name] = result
        
        state.result = combined_results
        state.updated_at = datetime.now()
        return state
    
    def _generate_insights(self, state: SchedulingAgentState) -> SchedulingAgentState:
        """Generate insights and suggestions based on the results"""
        state.current_step = "generate_insights"
        state.steps_completed.append("generate_insights")
        
        insights = []
        suggestions = []
        
        # Generate insights based on task type and results
        if state.task_type == TaskType.SCHEDULE_APPOINTMENT:
            if "schedule_appointment" in state.tool_results:
                result = state.tool_results["schedule_appointment"]
                if isinstance(result, str):
                    result = json.loads(result)
                if result.get("success"):
                    insights.append("Appointment scheduled successfully")
                    suggestions.append("Send confirmation email to patient")
                    suggestions.append("Add to calendar")
        
        elif state.task_type == TaskType.ANALYZE_SCHEDULE:
            if "analyze_schedule" in state.tool_results:
                result = state.tool_results["analyze_schedule"]
                if isinstance(result, str):
                    result = json.loads(result)
                
                utilization = result.get("utilization_rate", 0)
                if utilization < 50:
                    insights.append("Low schedule utilization detected")
                    suggestions.append("Consider marketing campaigns")
                elif utilization > 90:
                    insights.append("High schedule utilization detected")
                    suggestions.append("Consider adding more availability")
        
        elif state.task_type == TaskType.OPTIMIZE_SCHEDULE:
            if "optimize_schedule" in state.tool_results:
                result = state.tool_results["optimize_schedule"]
                if isinstance(result, str):
                    result = json.loads(result)
                
                for suggestion in result.get("suggestions", []):
                    suggestions.append(suggestion)
        
        state.suggestions = suggestions
        state.updated_at = datetime.now()
        return state
    
    def _finalize_response(self, state: SchedulingAgentState) -> SchedulingAgentState:
        """Finalize the response and calculate confidence score"""
        state.current_step = "finalize_response"
        state.steps_completed.append("finalize_response")
        
        # Calculate confidence score
        state.confidence_score = self._calculate_confidence_score(state)
        
        # Generate next actions
        state.next_actions = self._generate_next_actions(state)
        
        # Set status to completed
        state.status = AgentStatus.COMPLETED
        state.updated_at = datetime.now()
        
        return state
    
    def _handle_error(self, state: SchedulingAgentState) -> SchedulingAgentState:
        """Handle errors in the workflow"""
        state.current_step = "handle_error"
        state.status = AgentStatus.FAILED
        state.error_message = state.error_message or "An unknown error occurred"
        state.updated_at = datetime.now()
        return state
    
    def _should_retry_or_continue(self, state: SchedulingAgentState) -> str:
        """Determine if we should retry, continue, or handle error"""
        if state.error_message:
            return "error"
        
        # Check if we have any tool errors
        if state.tool_errors:
            # If more than half of tools failed, retry
            if len(state.tool_errors) > len(state.tool_results) / 2:
                return "retry"
            else:
                return "continue"
        
        return "continue"
    
    def _prepare_tool_args(self, tool_name: str, state: SchedulingAgentState) -> Dict[str, Any]:
        """Prepare arguments for tool execution"""
        args = {}
        
        if tool_name == "get_appointment" and "appointment_id" in state.context:
            args["appointment_id"] = state.context["appointment_id"]
        
        elif tool_name == "get_patient_info" and "patient_id" in state.context:
            args["patient_id"] = state.context["patient_id"]
        
        elif tool_name == "get_practitioner_info" and "practitioner_id" in state.context:
            args["practitioner_id"] = state.context["practitioner_id"]
        
        elif tool_name == "find_availability":
            args["practitioner_id"] = state.context.get("practitioner_id", 1)
            args["date"] = state.context.get("date", datetime.now().date().isoformat())
            args["duration_minutes"] = state.context.get("duration_minutes", 60)
        
        elif tool_name == "schedule_appointment":
            args["patient_id"] = state.context.get("patient_id", 1)
            args["practitioner_id"] = state.context.get("practitioner_id", 1)
            args["start_time"] = state.context.get("start_time", datetime.now().isoformat())
            args["end_time"] = state.context.get("end_time", (datetime.now() + timedelta(hours=1)).isoformat())
            args["appointment_type"] = state.context.get("appointment_type", "CONSULTATION")
        
        elif tool_name == "generate_schedule_report":
            args["report_type"] = state.context.get("report_type", "daily")
            args["date"] = state.context.get("date", datetime.now().date().isoformat())
        
        elif tool_name == "analyze_schedule":
            args["practitioner_id"] = state.context.get("practitioner_id")
            args["days"] = state.context.get("days", 7)
        
        elif tool_name == "optimize_schedule":
            args["practitioner_id"] = state.context.get("practitioner_id")
            args["optimization_type"] = state.context.get("optimization_type", "general")
        
        return args
    
    def _execute_single_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a single tool"""
        # Find the tool
        tool = None
        for t in self.tools:
            if t.name == tool_name:
                tool = t
                break
        
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        # Execute the tool
        result = tool._run(**args)
        return result
    
    def _calculate_confidence_score(self, state: SchedulingAgentState) -> float:
        """Calculate confidence score based on results and errors"""
        base_score = 0.8
        
        # Reduce score for errors
        if state.tool_errors:
            error_penalty = len(state.tool_errors) * 0.1
            base_score -= error_penalty
        
        # Increase score for successful tool executions
        if state.tool_results:
            success_bonus = len(state.tool_results) * 0.05
            base_score += success_bonus
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score))
    
    def _generate_next_actions(self, state: SchedulingAgentState) -> List[str]:
        """Generate suggested next actions"""
        actions = []
        
        if state.task_type == TaskType.SCHEDULE_APPOINTMENT:
            actions.append("Send confirmation email")
            actions.append("Add to calendar")
            actions.append("Set up reminders")
        
        elif state.task_type == TaskType.ANALYZE_SCHEDULE:
            actions.append("Generate detailed report")
            actions.append("Optimize schedule")
            actions.append("Review practitioner availability")
        
        elif state.task_type == TaskType.OPTIMIZE_SCHEDULE:
            actions.append("Implement suggested changes")
            actions.append("Monitor performance")
            actions.append("Review in 1 week")
        
        return actions
    
    def _generate_final_message(self, state: SchedulingAgentState) -> str:
        """Generate the final response message"""
        if state.status == AgentStatus.FAILED:
            return f"I encountered an error while processing your request: {state.error_message}"
        
        if state.task_type == TaskType.SCHEDULE_APPOINTMENT:
            if "schedule_appointment" in state.tool_results:
                result = state.tool_results["schedule_appointment"]
                if isinstance(result, str):
                    result = json.loads(result)
                if result.get("success"):
                    return f"✅ {result.get('message', 'Appointment scheduled successfully')}"
        
        elif state.task_type == TaskType.ANALYZE_SCHEDULE:
            if "analyze_schedule" in state.tool_results:
                result = state.tool_results["analyze_schedule"]
                if isinstance(result, str):
                    result = json.loads(result)
                return f"📊 Schedule analysis completed. Found {result.get('total_appointments', 0)} appointments with {result.get('utilization_rate', 0):.1f}% utilization."
        
        elif state.task_type == TaskType.OPTIMIZE_SCHEDULE:
            if "optimize_schedule" in state.tool_results:
                result = state.tool_results["optimize_schedule"]
                if isinstance(result, str):
                    result = json.loads(result)
                suggestions = result.get("suggestions", [])
                return f"🔧 Schedule optimization complete. {len(suggestions)} suggestions generated."
        
        return "I've completed your request. Check the results above for details." 