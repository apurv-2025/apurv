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
from datetime import datetime

from .state import ClaimsAgentState
from .tools import ClaimsTools
from ..schemas.agent import TaskType, AgentStatus, AgentResponse

class ClaimsProcessingGraph:
    """LangGraph implementation for claims processing agent"""
    
    def __init__(self, llm, tools_instance: ClaimsTools):
        self.llm = llm
        self.tools = tools_instance.get_tools()
        self.tool_executor = ToolExecutor(self.tools)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the graph
        workflow = StateGraph(ClaimsAgentState)
        
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
    
    async def process_request(self, request: Dict[str, Any]) -> AgentResponse:
        """Process an agent request through the graph"""
        
        # Initialize state
        state = ClaimsAgentState(
            task_id=str(uuid.uuid4()),
            task_type=TaskType(request["task_type"]),
            user_id=request["user_id"],
            description=request["task_description"],
            context=request.get("context", {}),
            status=AgentStatus.PROCESSING
        )
        
        # Add claim data if provided
        if "claim_id" in request:
            state.context["claim_id"] = request["claim_id"]
        
        if "file_path" in request:
            state.context["file_path"] = request["file_path"]
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(state)
            
            # Create response
            response = AgentResponse(
                task_id=final_state.task_id,
                status=final_state.status,
                result=final_state.result,
                message=self._generate_final_message(final_state),
                suggestions=final_state.suggestions,
                next_actions=final_state.next_actions,
                confidence_score=final_state.confidence_score,
                processing_time=(final_state.updated_at - final_state.created_at).total_seconds(),
                completed_at=final_state.updated_at
            )
            
            return response
            
        except Exception as e:
            # Handle errors
            error_response = AgentResponse(
                task_id=state.task_id,
                status=AgentStatus.FAILED,
                message=f"Error processing request: {str(e)}",
                suggestions=["Check the request parameters and try again"],
                next_actions=["Contact support if the error persists"]
            )
            return error_response
    
    def _analyze_task(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Analyze the incoming task and understand requirements"""
        
        state.add_thought(f"Analyzing task: {state.task_type} - {state.description}")
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze this claims processing task:
        
        Task Type: {state.task_type}
        Description: {state.description}
        Context: {json.dumps(state.context, indent=2)}
        
        Based on this information:
        1. What specific actions need to be taken?
        2. What tools will be required?
        3. What information do we need to gather?
        4. Are there any potential challenges or edge cases?
        
        Provide a structured analysis.
        """
        
        # Get LLM analysis
        messages = [SystemMessage(content="You are an expert claims processing analyst."), 
                   HumanMessage(content=analysis_prompt)]
        
        response = self.llm.invoke(messages)
        
        state.add_thought(f"Task analysis complete: {response.content}")
        state.processed_data["task_analysis"] = response.content
        
        return state
    
    def _plan_execution(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Plan the execution strategy"""
        
        state.add_thought("Planning execution strategy")
        
        # Determine tools needed based on task type
        if state.task_type == TaskType.PROCESS_CLAIM:
            state.processed_data["required_tools"] = ["process_edi_file", "validate_claim"]
        elif state.task_type == TaskType.VALIDATE_CLAIM:
            state.processed_data["required_tools"] = ["get_claim", "validate_claim"]
        elif state.task_type == TaskType.ANALYZE_REJECTION:
            state.processed_data["required_tools"] = ["get_claim", "analyze_rejection"]
        elif state.task_type == TaskType.GENERATE_REPORT:
            state.processed_data["required_tools"] = ["generate_report"]
        elif state.task_type == TaskType.ANSWER_QUESTION:
            state.processed_data["required_tools"] = ["search_claims", "get_dashboard_stats"]
        else:
            state.processed_data["required_tools"] = ["get_dashboard_stats"]
        
        state.add_action(f"Planned to use tools: {state.processed_data['required_tools']}")
        
        return state
    
    def _execute_tools(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Execute the required tools"""
        
        state.add_thought("Executing tools based on plan")
        
        tool_results = {}
        required_tools = state.processed_data.get("required_tools", [])
        
        for tool_name in required_tools:
            try:
                state.add_action(f"Executing tool: {tool_name}")
                
                # Prepare tool arguments based on context and task type
                tool_args = self._prepare_tool_args(tool_name, state)
                
                # Execute tool
                tool_result = self._execute_single_tool(tool_name, tool_args)
                tool_results[tool_name] = tool_result
                
                state.tools_used.append(tool_name)
                state.add_thought(f"Tool {tool_name} executed successfully")
                
            except Exception as e:
                error_msg = f"Error executing tool {tool_name}: {str(e)}"
                state.errors.append(error_msg)
                state.add_thought(error_msg)
        
        state.processed_data["tool_results"] = tool_results
        
        return state
    
    def _synthesize_results(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Synthesize the results from tool executions"""
        
        state.add_thought("Synthesizing results from tool executions")
        
        tool_results = state.processed_data.get("tool_results", {})
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        Synthesize the following tool execution results for the task:
        
        Task: {state.task_type} - {state.description}
        
        Tool Results:
        {json.dumps(tool_results, indent=2)}
        
        Based on these results:
        1. What is the main outcome?
        2. Are there any issues or concerns?
        3. What insights can be derived?
        4. What are the next recommended actions?
        
        Provide a clear, structured synthesis.
        """
        
        messages = [
            SystemMessage(content="You are an expert claims processing analyst. Synthesize tool results into actionable insights."),
            HumanMessage(content=synthesis_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        state.processed_data["synthesis"] = response.content
        state.add_thought("Results synthesis complete")
        
        return state
    
    def _generate_insights(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Generate insights and recommendations"""
        
        state.add_thought("Generating insights and recommendations")
        
        synthesis = state.processed_data.get("synthesis", "")
        tool_results = state.processed_data.get("tool_results", {})
        
        # Extract specific insights based on task type
        if state.task_type == TaskType.VALIDATE_CLAIM:
            self._extract_validation_insights(state, tool_results)
        elif state.task_type == TaskType.ANALYZE_REJECTION:
            self._extract_rejection_insights(state, tool_results)
        elif state.task_type == TaskType.GENERATE_REPORT:
            self._extract_report_insights(state, tool_results)
        
        # Generate suggestions
        suggestions_prompt = f"""
        Based on the task results and synthesis, provide 3-5 specific, actionable suggestions:
        
        Task: {state.task_type}
        Synthesis: {synthesis}
        
        Focus on practical next steps that would improve the claims processing workflow.
        """
        
        messages = [
            SystemMessage(content="You are a claims processing optimization expert."),
            HumanMessage(content=suggestions_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse suggestions from response
        suggestions_text = response.content
        state.suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip() and not s.strip().startswith('#')]
        
        # Calculate confidence score
        state.confidence_score = self._calculate_confidence_score(state)
        
        return state
    
    def _finalize_response(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Finalize the response and prepare output"""
        
        state.add_thought("Finalizing response")
        
        # Prepare final result
        state.result = {
            "task_summary": {
                "type": state.task_type,
                "description": state.description,
                "status": "completed"
            },
            "execution_summary": {
                "tools_used": state.tools_used,
                "actions_taken": len(state.actions_taken),
                "insights_generated": len(state.insights)
            },
            "data": state.processed_data.get("tool_results", {}),
            "insights": state.insights,
            "errors": state.errors,
            "warnings": state.warnings
        }
        
        # Generate next actions
        state.next_actions = self._generate_next_actions(state)
        
        # Update status
        if state.errors:
            state.status = AgentStatus.REQUIRES_HUMAN if len(state.errors) > 2 else AgentStatus.COMPLETED
        else:
            state.status = AgentStatus.COMPLETED
        
        state.add_action("Response finalized")
        
        return state
    
    def _handle_error(self, state: ClaimsAgentState) -> ClaimsAgentState:
        """Handle errors and prepare error response"""
        
        state.status = AgentStatus.FAILED
        state.add_thought("Handling error state")
        
        state.result = {
            "error": True,
            "errors": state.errors,
            "partial_results": state.processed_data.get("tool_results", {}),
            "recovery_suggestions": [
                "Check input parameters",
                "Verify claim data exists",
                "Retry with corrected information",
                "Contact technical support if issue persists"
            ]
        }
        
        return state
    
    def _should_retry_or_continue(self, state: ClaimsAgentState) -> str:
        """Determine whether to retry, continue, or error out"""
        
        if len(state.errors) > 3:
            return "error"
        elif len(state.errors) > 0 and not state.processed_data.get("tool_results"):
            return "retry"
        else:
            return "continue"
    
    def _prepare_tool_args(self, tool_name: str, state: ClaimsAgentState) -> Dict[str, Any]:
        """Prepare arguments for tool execution based on context"""
        
        args = {}
        
        if tool_name == "get_claim" and "claim_id" in state.context:
            args["claim_id"] = state.context["claim_id"]
        elif tool_name == "validate_claim" and "claim_id" in state.context:
            args["claim_id"] = state.context["claim_id"]
        elif tool_name == "process_edi_file" and "file_path" in state.context:
            args["file_path"] = state.context["file_path"]
            args["payer_id"] = state.context.get("payer_id", 1)
        elif tool_name == "analyze_rejection" and "claim_id" in state.context:
            args["claim_id"] = state.context["claim_id"]
        elif tool_name == "generate_report":
            args["report_type"] = state.context.get("report_type", "dashboard")
        elif tool_name == "search_claims":
            args.update({
                "status": state.context.get("status"),
                "claim_type": state.context.get("claim_type"),
                "limit": state.context.get("limit", 10)
            })
        
        return args
    
    def _execute_single_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a single tool with given arguments"""
        
        # Find the tool by name
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        
        # Execute the tool
        return tool.run(args) if args else tool.run({})
    
    def _extract_validation_insights(self, state: ClaimsAgentState, tool_results: Dict[str, Any]):
        """Extract insights from validation results"""
        
        validation_result = tool_results.get("validate_claim")
        if validation_result:
            try:
                result_data = json.loads(validation_result)
                if not result_data.get("is_valid", False):
                    errors = result_data.get("errors", [])
                    state.add_insight(
                        "validation_error",
                        f"Claim validation failed with {len(errors)} errors",
                        0.9
                    )
                    
                    # Categorize errors
                    error_categories = {}
                    for error in errors:
                        category = self._categorize_error(error)
                        error_categories[category] = error_categories.get(category, 0) + 1
                    
                    state.processed_data["error_categories"] = error_categories
                else:
                    state.add_insight(
                        "validation_success",
                        "Claim passed all validation checks",
                        0.95
                    )
            except json.JSONDecodeError:
                state.warnings.append("Could not parse validation results")
    
    def _extract_rejection_insights(self, state: ClaimsAgentState, tool_results: Dict[str, Any]):
        """Extract insights from rejection analysis"""
        
        rejection_analysis = tool_results.get("analyze_rejection")
        if rejection_analysis:
            try:
                analysis_data = json.loads(rejection_analysis)
                errors = analysis_data.get("rejection_errors", [])
                
                if errors:
                    state.add_insight(
                        "rejection_pattern",
                        f"Identified {len(errors)} rejection reasons",
                        0.85
                    )
                    
                    # Check for common patterns
                    common_issues = analysis_data.get("common_patterns", [])
                    if common_issues:
                        state.add_insight(
                            "pattern_recognition",
                            f"Found common patterns: {', '.join(common_issues)}",
                            0.8
                        )
            except json.JSONDecodeError:
                state.warnings.append("Could not parse rejection analysis")
    
    def _extract_report_insights(self, state: ClaimsAgentState, tool_results: Dict[str, Any]):
        """Extract insights from report generation"""
        
        report_result = tool_results.get("generate_report")
        if report_result:
            try:
                report_data = json.loads(report_result)
                
                if "financial_summary" in report_data:
                    financial = report_data["financial_summary"]
                    collection_rate = financial.get("collection_rate", 0)
                    
                    if collection_rate < 80:
                        state.add_insight(
                            "financial_concern",
                            f"Collection rate is low at {collection_rate:.1f}%",
                            0.9
                        )
                    elif collection_rate > 95:
                        state.add_insight(
                            "financial_excellent",
                            f"Excellent collection rate at {collection_rate:.1f}%",
                            0.95
                        )
                
                if "status_distribution" in report_data:
                    rejected_count = report_data["status_distribution"].get("rejected", 0)
                    total_claims = sum(report_data["status_distribution"].values())
                    
                    if total_claims > 0:
                        rejection_rate = (rejected_count / total_claims) * 100
                        if rejection_rate > 10:
                            state.add_insight(
                                "high_rejection_rate",
                                f"High rejection rate at {rejection_rate:.1f}%",
                                0.85
                            )
            except json.JSONDecodeError:
                state.warnings.append("Could not parse report data")
    
    def _categorize_error(self, error: str) -> str:
        """Categorize an error message"""
        
        error_lower = error.lower()
        
        if "npi" in error_lower:
            return "Provider Information"
        elif "date" in error_lower:
            return "Date/Time Issues"
        elif "procedure" in error_lower or "code" in error_lower:
            return "Procedure Codes"
        elif "tooth" in error_lower:
            return "Dental Specific"
        elif "patient" in error_lower:
            return "Patient Information"
        elif "charge" in error_lower or "amount" in error_lower:
            return "Financial Data"
        else:
            return "Other"
    
    def _calculate_confidence_score(self, state: ClaimsAgentState) -> float:
        """Calculate confidence score based on execution results"""
        
        base_score = 0.7
        
        # Increase confidence if no errors
        if not state.errors:
            base_score += 0.2
        
        # Decrease confidence for each error
        base_score -= len(state.errors) * 0.1
        
        # Increase confidence if insights were generated
        if state.insights:
            base_score += len(state.insights) * 0.05
        
        # Decrease confidence for warnings
        base_score -= len(state.warnings) * 0.05
        
        return max(0.1, min(1.0, base_score))
    
    def _generate_next_actions(self, state: ClaimsAgentState) -> List[str]:
        """Generate recommended next actions based on task results"""
        
        next_actions = []
        
        if state.task_type == TaskType.VALIDATE_CLAIM:
            if state.errors:
                next_actions.append("Review and fix validation errors")
                next_actions.append("Resubmit claim after corrections")
            else:
                next_actions.append("Submit validated claim to payer")
        
        elif state.task_type == TaskType.ANALYZE_REJECTION:
            next_actions.append("Apply suggested fixes to rejected claim")
            next_actions.append("Re-validate claim after corrections")
            next_actions.append("Monitor for similar rejection patterns")
        
        elif state.task_type == TaskType.PROCESS_CLAIM:
            next_actions.append("Review processed claim data")
            next_actions.append("Validate claim before submission")
        
        elif state.task_type == TaskType.GENERATE_REPORT:
            next_actions.append("Review report findings")
            next_actions.append("Address any identified issues")
            next_actions.append("Schedule follow-up analysis")
        
        # Add general actions based on insights
        for insight in state.insights:
            if insight["type"] == "validation_error":
                next_actions.append("Focus on data quality improvements")
            elif insight["type"] == "high_rejection_rate":
                next_actions.append("Implement rejection prevention measures")
            elif insight["type"] == "financial_concern":
                next_actions.append("Review payer contracts and reimbursement rates")
        
        return list(set(next_actions))  # Remove duplicates
    
    def _generate_final_message(self, state: ClaimsAgentState) -> str:
        """Generate the final message for the response"""
        
        if state.status == AgentStatus.COMPLETED:
            if state.errors:
                return f"Task completed with {len(state.errors)} issues. Please review the errors and suggested actions."
            else:
                return f"Task completed successfully. Generated {len(state.insights)} insights and {len(state.suggestions)} recommendations."
        
        elif state.status == AgentStatus.FAILED:
            return f"Task failed due to multiple errors. Please check the error details and try again."
        
        elif state.status == AgentStatus.REQUIRES_HUMAN:
            return f"Task requires human intervention due to complex issues. Please review the results and take manual action."
        
        else:
            return "Task processing completed."
