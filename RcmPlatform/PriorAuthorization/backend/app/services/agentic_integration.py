"""
AI Assistant Integration for Prior Authorization System
Provides AI-powered capabilities for prior authorization workflows
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import uuid

# Add the agentic-core path to sys.path
agentic_core_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))),
    "AIFoundation", "AgenticFoundation", "agentic-core", "backend"
)
sys.path.insert(0, agentic_core_path)

try:
    from agentic_core import AgenticCore, create_agentic_core
    from agentic_core.tools import BaseTool
    from agentic_core.schemas import TaskType, AgentRequest, AgentResponse
    AGENTIC_CORE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Agentic Core not available: {e}")
    AGENTIC_CORE_AVAILABLE = False

logger = logging.getLogger(__name__)


class PriorAuthorizationTool(BaseTool):
    """Prior authorization request tool for agentic-core"""
    
    name = "create_prior_authorization"
    description = "Create a new prior authorization request"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute prior authorization creation"""
        patient_id = data.get("patient_id")
        provider_npi = data.get("provider_npi")
        procedure_codes = data.get("procedure_codes", [])
        diagnosis_codes = data.get("diagnosis_codes", [])
        service_date = data.get("service_date")
        medical_necessity = data.get("medical_necessity")
        
        if not patient_id or not provider_npi:
            return {
                "success": False,
                "error": "Missing required parameters: patient_id and provider_npi"
            }
        
        # Mock authorization creation (in real implementation, this would call the actual service)
        auth_request = {
            "request_id": f"AUTH{uuid.uuid4().hex[:8].upper()}",
            "patient_id": patient_id,
            "provider_npi": provider_npi,
            "procedure_codes": procedure_codes,
            "diagnosis_codes": diagnosis_codes,
            "service_date": service_date,
            "medical_necessity": medical_necessity,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": auth_request,
            "tool_name": self.name
        }


class AuthorizationStatusTool(BaseTool):
    """Authorization status check tool for agentic-core"""
    
    name = "check_authorization_status"
    description = "Check the status of a prior authorization request"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute authorization status check"""
        request_id = data.get("request_id")
        
        if not request_id:
            return {
                "success": False,
                "error": "Missing required parameter: request_id"
            }
        
        # Mock status check (in real implementation, this would query the database)
        status_result = {
            "request_id": request_id,
            "status": "approved",
            "decision_date": datetime.now().isoformat(),
            "decision_reason": "Medical necessity confirmed",
            "authorized_services": ["99213", "E11.9"],
            "authorization_number": f"AUTH{uuid.uuid4().hex[:8].upper()}",
            "expiration_date": "2024-12-31"
        }
        
        return {
            "success": True,
            "result": status_result,
            "tool_name": self.name
        }


class EDIGenerationTool(BaseTool):
    """EDI generation tool for agentic-core"""
    
    name = "generate_edi"
    description = "Generate EDI 278 (authorization request) or EDI 275 (patient information)"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute EDI generation"""
        edi_type = data.get("edi_type", "278")  # 278 for auth request, 275 for patient info
        patient_id = data.get("patient_id")
        request_id = data.get("request_id")
        
        if not patient_id:
            return {
                "success": False,
                "error": "Missing required parameter: patient_id"
            }
        
        # Mock EDI generation (in real implementation, this would use the EDI service)
        if edi_type == "278":
            edi_content = f"""ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*U*00401*{uuid.uuid4().hex[:9].upper()}*0*P*>~
GS*HS*SENDER*RECEIVER*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*1*X*005010X279A1~
ST*278*0001*005010X279A1~
BHT*0022*13*{request_id}*{datetime.now().strftime('%Y%m%d%H%M')}*{datetime.now().strftime('%H%M')}~
HL*1**20*1~
NM1*PR*2*INSURANCE COMPANY*****PI*123456789~
HL*2*1*21*1~
NM1*1P*2*PROVIDER NAME*****XX*{data.get('provider_npi', '1234567890')}~
HL*3*2*22*0~
TRN*1*{request_id}*9{data.get('provider_npi', '1234567890')}~
NM1*IL*1*PATIENT*NAME*****MI*{patient_id}~
DMG*D8*{data.get('birth_date', '19900101')}*{data.get('gender', 'M')}~
DTP*291*D8*{data.get('service_date', '20240115')}~
SE*13*0001~
GE*1*1~
IEA*1*{uuid.uuid4().hex[:9].upper()}~"""
        else:  # EDI 275
            edi_content = f"""ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *{datetime.now().strftime('%y%m%d')}*{datetime.now().strftime('%H%M')}*U*00401*{uuid.uuid4().hex[:9].upper()}*0*P*>~
GS*HS*SENDER*RECEIVER*{datetime.now().strftime('%Y%m%d')}*{datetime.now().strftime('%H%M')}*1*X*005010X212~
ST*275*0001*005010X212~
BHT*0022*13*{uuid.uuid4().hex[:9].upper()}*{datetime.now().strftime('%Y%m%d%H%M')}*{datetime.now().strftime('%H%M')}~
HL*1**20*1~
NM1*PR*2*INSURANCE COMPANY*****PI*123456789~
HL*2*1*21*1~
NM1*1P*2*PROVIDER NAME*****XX*{data.get('provider_npi', '1234567890')}~
HL*3*2*22*0~
TRN*1*{uuid.uuid4().hex[:9].upper()}*9{data.get('provider_npi', '1234567890')}~
NM1*IL*1*PATIENT*NAME*****MI*{patient_id}~
DMG*D8*{data.get('birth_date', '19900101')}*{data.get('gender', 'M')}~
SE*10*0001~
GE*1*1~
IEA*1*{uuid.uuid4().hex[:9].upper()}~"""
        
        return {
            "success": True,
            "result": {
                "edi_type": edi_type,
                "edi_content": edi_content,
                "generated_at": datetime.now().isoformat()
            },
            "tool_name": self.name
        }


class PatientLookupTool(BaseTool):
    """Patient lookup tool for agentic-core"""
    
    name = "lookup_patient"
    description = "Lookup patient information by ID or member ID"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute patient lookup"""
        patient_id = data.get("patient_id")
        member_id = data.get("member_id")
        
        if not patient_id and not member_id:
            return {
                "success": False,
                "error": "Missing required parameter: patient_id or member_id"
            }
        
        # Mock patient lookup (in real implementation, this would call the Patient microservice)
        patient_info = {
            "patient_id": patient_id or f"PAT{uuid.uuid4().hex[:8].upper()}",
            "member_id": member_id or f"MEM{uuid.uuid4().hex[:8].upper()}",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "address": "123 Main St, Anytown, CA 12345",
            "phone": "555-123-4567",
            "email": "john.doe@example.com",
            "insurance": {
                "carrier": "Blue Cross Blue Shield",
                "group_number": "12345",
                "member_number": member_id or f"MEM{uuid.uuid4().hex[:8].upper()}"
            }
        }
        
        return {
            "success": True,
            "result": patient_info,
            "tool_name": self.name
        }


class CodeLookupTool(BaseTool):
    """Healthcare code lookup tool for agentic-core"""
    
    name = "lookup_codes"
    description = "Lookup procedure codes, diagnosis codes, or service type codes"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code lookup"""
        code_type = data.get("code_type", "procedure")  # procedure, diagnosis, service_type
        search_term = data.get("search_term", "")
        code = data.get("code", "")
        
        if not search_term and not code:
            return {
                "success": False,
                "error": "Missing required parameter: search_term or code"
            }
        
        # Mock code lookup (in real implementation, this would call the codes service)
        if code_type == "procedure":
            codes = [
                {"code": "99213", "description": "Office visit, established patient, 20-29 minutes", "category": "Evaluation and Management"},
                {"code": "99214", "description": "Office visit, established patient, 30-39 minutes", "category": "Evaluation and Management"},
                {"code": "99215", "description": "Office visit, established patient, 40-54 minutes", "category": "Evaluation and Management"}
            ]
        elif code_type == "diagnosis":
            codes = [
                {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications", "category": "Endocrine"},
                {"code": "I10", "description": "Essential (primary) hypertension", "category": "Cardiovascular"},
                {"code": "M79.3", "description": "Sciatica, unspecified side", "category": "Musculoskeletal"}
            ]
        else:  # service_type
            codes = [
                {"code": "30", "description": "Health Benefit Plan Coverage", "category": "Coverage"},
                {"code": "35", "description": "Dental Care", "category": "Dental"},
                {"code": "88", "description": "Pharmacy", "category": "Pharmacy"}
            ]
        
        # Filter by search term if provided
        if search_term:
            codes = [c for c in codes if search_term.lower() in c["description"].lower()]
        
        # Filter by specific code if provided
        if code:
            codes = [c for c in codes if c["code"] == code]
        
        return {
            "success": True,
            "result": {
                "code_type": code_type,
                "codes": codes,
                "count": len(codes)
            },
            "tool_name": self.name
        }


class RealAgenticPriorAuthorization:
    """Real agentic-core integration for Prior Authorization"""
    
    def __init__(self, model_provider: str = "openai", api_key: Optional[str] = None, database_url: Optional[str] = None):
        self.model_provider = model_provider
        self.api_key = api_key or os.getenv("AI_API_KEY")
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.agentic_core = None
        self._initialize_agentic()
    
    def _initialize_agentic(self):
        """Initialize the agentic-core system"""
        if not AGENTIC_CORE_AVAILABLE:
            logger.warning("Agentic Core not available, using fallback")
            return
        
        try:
            self.agentic_core = create_agentic_core(
                model_provider=self.model_provider,
                api_key=self.api_key,
                database_url=self.database_url
            )
            self._register_tools()
            logger.info("Agentic Core initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agentic Core: {e}")
            self.agentic_core = None
    
    def _register_tools(self):
        """Register custom tools with agentic-core"""
        if not self.agentic_core:
            return
        
        tools = [
            PriorAuthorizationTool(),
            AuthorizationStatusTool(),
            EDIGenerationTool(),
            PatientLookupTool(),
            CodeLookupTool()
        ]
        
        for tool in tools:
            self.agentic_core.register_tool(tool)
            logger.info(f"Registered tool: {tool.name}")
    
    async def chat_with_prior_auth_data(self, message: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Chat with AI assistant about prior authorization data"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available",
                "response": "I'm sorry, the AI assistant is currently unavailable. Please try again later."
            }
        
        try:
            # Add prior authorization context to the message
            enhanced_message = f"""
            You are an AI assistant for a Prior Authorization system. Help users with:
            - Creating prior authorization requests
            - Checking authorization status
            - Generating EDI documents (278/275)
            - Looking up patient information
            - Finding healthcare codes (CPT, ICD-10, service types)
            - Understanding prior authorization workflows
            
            User message: {message}
            """
            
            response = await self.agentic_core.chat(
                message=enhanced_message,
                user_id=user_id,
                context=context or {}
            )
            
            return {
                "success": True,
                "response": response.get("response", "I'm sorry, I couldn't process your request."),
                "conversation_id": response.get("conversation_id"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I'm sorry, I encountered an error while processing your request."
            }
    
    async def create_prior_authorization(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a prior authorization request using AI assistance"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            result = await self.agentic_core.execute_tool(
                tool_name="create_prior_authorization",
                data=auth_data
            )
            return result
        except Exception as e:
            logger.error(f"Error creating prior authorization: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_authorization_status(self, request_id: str) -> Dict[str, Any]:
        """Check authorization status using AI assistance"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            result = await self.agentic_core.execute_tool(
                tool_name="check_authorization_status",
                data={"request_id": request_id}
            )
            return result
        except Exception as e:
            logger.error(f"Error checking authorization status: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_edi_document(self, edi_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate EDI document using AI assistance"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            result = await self.agentic_core.execute_tool(
                tool_name="generate_edi",
                data={"edi_type": edi_type, **data}
            )
            return result
        except Exception as e:
            logger.error(f"Error generating EDI: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def lookup_patient(self, patient_id: str = None, member_id: str = None) -> Dict[str, Any]:
        """Lookup patient information using AI assistance"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            data = {}
            if patient_id:
                data["patient_id"] = patient_id
            if member_id:
                data["member_id"] = member_id
            
            result = await self.agentic_core.execute_tool(
                tool_name="lookup_patient",
                data=data
            )
            return result
        except Exception as e:
            logger.error(f"Error looking up patient: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def lookup_codes(self, code_type: str, search_term: str = None, code: str = None) -> Dict[str, Any]:
        """Lookup healthcare codes using AI assistance"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            data = {"code_type": code_type}
            if search_term:
                data["search_term"] = search_term
            if code:
                data["code"] = code
            
            result = await self.agentic_core.execute_tool(
                tool_name="lookup_codes",
                data=data
            )
            return result
        except Exception as e:
            logger.error(f"Error looking up codes: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        if not self.agentic_core:
            return []
        
        try:
            tools = await self.agentic_core.get_available_tools()
            return tools
        except Exception as e:
            logger.error(f"Error getting tools: {e}")
            return []
    
    async def process_complex_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process complex prior authorization requests using AI"""
        if not self.agentic_core:
            return {
                "success": False,
                "error": "Agentic Core not available"
            }
        
        try:
            # Create a complex workflow using multiple tools
            workflow = request.get("workflow", [])
            results = []
            
            for step in workflow:
                tool_name = step.get("tool")
                data = step.get("data", {})
                
                if tool_name == "create_prior_authorization":
                    result = await self.create_prior_authorization(data)
                elif tool_name == "check_authorization_status":
                    result = await self.check_authorization_status(data.get("request_id"))
                elif tool_name == "generate_edi":
                    result = await self.generate_edi_document(data.get("edi_type"), data)
                elif tool_name == "lookup_patient":
                    result = await self.lookup_patient(data.get("patient_id"), data.get("member_id"))
                elif tool_name == "lookup_codes":
                    result = await self.lookup_codes(data.get("code_type"), data.get("search_term"), data.get("code"))
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                results.append({
                    "step": step.get("name", tool_name),
                    "result": result
                })
            
            return {
                "success": True,
                "workflow_results": results,
                "completed_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing complex request: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def close(self):
        """Close the agentic-core connection"""
        if self.agentic_core:
            await self.agentic_core.close()


class FallbackAgenticPriorAuthorization:
    """Fallback implementation when agentic-core is not available"""
    
    def __init__(self, model_provider: str = "openai", api_key: Optional[str] = None, database_url: Optional[str] = None):
        self.model_provider = model_provider
        self.api_key = api_key
        self.database_url = database_url
    
    async def chat_with_prior_auth_data(self, message: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available", "response": "AI assistant is currently unavailable."}
    
    async def create_prior_authorization(self, auth_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def check_authorization_status(self, request_id: str) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def generate_edi_document(self, edi_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def lookup_patient(self, patient_id: str = None, member_id: str = None) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def lookup_codes(self, code_type: str, search_term: str = None, code: str = None) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        return []
    
    async def process_complex_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": False, "error": "Agentic Core not available"}
    
    async def close(self):
        pass


def create_agentic_prior_authorization(
    model_provider: str = "openai",
    api_key: Optional[str] = None,
    database_url: Optional[str] = None,
    force_mock: bool = False
):
    """Factory function to create agentic prior authorization instance"""
    if force_mock or not AGENTIC_CORE_AVAILABLE:
        return FallbackAgenticPriorAuthorization(model_provider, api_key, database_url)
    else:
        return RealAgenticPriorAuthorization(model_provider, api_key, database_url) 