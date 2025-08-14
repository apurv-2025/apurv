"""
Agentic Core Integration with ChargeCapture Backend
Integration with the agentic-core framework for AI-powered charge capture assistance
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
    # Create a fallback BaseTool class
    class BaseTool:
        def __init__(self):
            self.name = "fallback_tool"
            self.description = "Fallback tool when agentic-core is not available"
        
        async def execute(self, data):
            return {"success": False, "error": "Agentic core not available"}

logger = logging.getLogger(__name__)


class ChargeCaptureTool(BaseTool):
    """Charge capture tool for agentic-core"""
    
    name = "capture_charge"
    description = "Capture a new charge with validation and auto-population"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute charge capture"""
        encounter_id = data.get("encounter_id")
        patient_id = data.get("patient_id")
        provider_id = data.get("provider_id")
        cpt_code = data.get("cpt_code")
        icd_code = data.get("icd_code")
        
        if not encounter_id or not patient_id or not provider_id:
            return {
                "success": False,
                "error": "Missing required parameters: encounter_id, patient_id, provider_id"
            }
        
        # Mock charge capture result (in real implementation, this would create actual charge records)
        charge_result = {
            "charge_id": str(uuid.uuid4()),
            "encounter_id": encounter_id,
            "patient_id": patient_id,
            "provider_id": provider_id,
            "cpt_code": cpt_code or "99213",
            "icd_code": icd_code or "Z00.00",
            "status": "draft",
            "capture_method": "ai_assistant",
            "captured_at": datetime.now().isoformat(),
            "validation_errors": [],
            "suggestions": [
                "Consider adding modifier 25 if this is a separate service",
                "Verify patient insurance coverage before submission",
                "Check for any prior authorization requirements"
            ]
        }
        
        return {
            "success": True,
            "result": charge_result,
            "tool_name": self.name
        }


class ChargeValidationTool(BaseTool):
    """Charge validation tool for agentic-core"""
    
    name = "validate_charge"
    description = "Validate a charge for compliance and accuracy"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute charge validation"""
        cpt_code = data.get("cpt_code")
        icd_code = data.get("icd_code")
        modifiers = data.get("modifiers", [])
        charge_amount = data.get("charge_amount")
        
        if not cpt_code or not icd_code:
            return {
                "success": False,
                "error": "Missing required parameters: cpt_code and icd_code"
            }
        
        # Mock validation result
        validation_result = {
            "cpt_code": cpt_code,
            "icd_code": icd_code,
            "modifiers": modifiers,
            "charge_amount": charge_amount,
            "is_valid": True,
            "validation_errors": [],
            "warnings": [],
            "recommendations": [
                "CPT-ICD combination is valid",
                "Consider adding time-based modifiers if applicable",
                "Verify charge amount against fee schedule"
            ],
            "compliance_score": 95,
            "validation_date": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": validation_result,
            "tool_name": self.name
        }


class ChargeTemplateTool(BaseTool):
    """Charge template tool for agentic-core"""
    
    name = "get_charge_template"
    description = "Get charge templates for specific specialties or procedures"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute charge template retrieval"""
        specialty = data.get("specialty")
        procedure_type = data.get("procedure_type")
        
        # Mock template result
        template_result = {
            "specialty": specialty or "Primary Care",
            "procedure_type": procedure_type or "Office Visit",
            "templates": [
                {
                    "name": "Standard Office Visit",
                    "cpt_code": "99213",
                    "icd_code": "Z00.00",
                    "modifiers": [],
                    "description": "Established patient office visit, 20-29 minutes"
                },
                {
                    "name": "New Patient Visit",
                    "cpt_code": "99203",
                    "icd_code": "Z00.00",
                    "modifiers": [],
                    "description": "New patient office visit, 30-44 minutes"
                }
            ],
            "suggestions": [
                "Use 99213 for established patients with straightforward problems",
                "Use 99203 for new patients requiring moderate complexity",
                "Add modifier 25 if additional procedures are performed"
            ]
        }
        
        return {
            "success": True,
            "result": template_result,
            "tool_name": self.name
        }


class ChargeAnalysisTool(BaseTool):
    """Charge analysis tool for agentic-core"""
    
    name = "analyze_charges"
    description = "Analyze charge patterns and provide insights"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute charge analysis"""
        provider_id = data.get("provider_id")
        date_range = data.get("date_range", "30_days")
        
        # Mock analysis result
        analysis_result = {
            "provider_id": provider_id,
            "date_range": date_range,
            "total_charges": 150,
            "total_amount": 45000.00,
            "average_charge": 300.00,
            "top_cpt_codes": [
                {"code": "99213", "count": 45, "amount": 13500.00},
                {"code": "99214", "count": 30, "amount": 12000.00},
                {"code": "20610", "count": 15, "amount": 7500.00}
            ],
            "top_icd_codes": [
                {"code": "Z00.00", "count": 40, "description": "General examination"},
                {"code": "I10", "count": 25, "description": "Essential hypertension"},
                {"code": "M79.3", "count": 15, "description": "Sciatica"}
            ],
            "rejection_rate": 0.05,
            "common_rejection_reasons": [
                "Missing modifiers",
                "Invalid CPT-ICD combination",
                "Insufficient documentation"
            ],
            "recommendations": [
                "Consider using 99214 for visits with moderate complexity",
                "Add modifier 25 for separate procedures",
                "Review documentation for rejected claims"
            ],
            "analysis_date": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": analysis_result,
            "tool_name": self.name
        }


class ChargeCaptureAgenticCore:
    """Agentic Core integration for ChargeCapture"""
    
    def __init__(self):
        self.agentic_core = None
        self.tools = [
            ChargeCaptureTool(),
            ChargeValidationTool(),
            ChargeTemplateTool(),
            ChargeAnalysisTool()
        ]
        self._initialize_agentic_core()
    
    def _initialize_agentic_core(self):
        """Initialize the agentic core with charge capture tools"""
        if not AGENTIC_CORE_AVAILABLE:
            logger.warning("Agentic Core not available, using mock implementation")
            return
        
        try:
            self.agentic_core = create_agentic_core(
                name="charge_capture_assistant",
                description="AI assistant for healthcare charge capture",
                tools=self.tools,
                model_provider="openai",  # or your preferred provider
                model_name="gpt-4"  # or your preferred model
            )
            logger.info("Agentic Core initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Agentic Core: {e}")
            self.agentic_core = None
    
    async def chat(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Chat with the AI assistant"""
        if not self.agentic_core:
            return self._mock_chat_response(message)
        
        try:
            response = await self.agentic_core.chat(
                message=message,
                conversation_id=conversation_id
            )
            return {
                "success": True,
                "response": response.message,
                "conversation_id": response.conversation_id,
                "tools_used": response.tools_used if hasattr(response, 'tools_used') else []
            }
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return self._mock_chat_response(message)
    
    async def capture_charge(self, charge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Capture a new charge using AI assistance"""
        tool = ChargeCaptureTool()
        return await tool.execute(charge_data)
    
    async def validate_charge(self, charge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a charge using AI assistance"""
        tool = ChargeValidationTool()
        return await tool.execute(charge_data)
    
    async def get_charge_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get charge templates using AI assistance"""
        tool = ChargeTemplateTool()
        return await tool.execute(template_data)
    
    async def analyze_charges(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze charges using AI assistance"""
        tool = ChargeAnalysisTool()
        return await tool.execute(analysis_data)
    
    def _mock_chat_response(self, message: str) -> Dict[str, Any]:
        """Mock chat response when agentic core is not available"""
        responses = {
            "hello": "Hello! I'm your charge capture assistant. I can help you capture charges, validate codes, and analyze patterns. How can I help you today?",
            "help": "I can assist you with:\n- Capturing new charges\n- Validating CPT/ICD codes\n- Finding charge templates\n- Analyzing charge patterns\n- Providing coding recommendations",
            "capture": "To capture a charge, I'll need the encounter ID, patient ID, provider ID, and optionally CPT/ICD codes. I can help auto-populate missing information.",
            "validate": "I can validate your charges for compliance and accuracy. Just provide the CPT code, ICD code, and any modifiers.",
            "template": "I can help you find appropriate charge templates based on specialty and procedure type. What specialty are you working with?"
        }
        
        message_lower = message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return {
                    "success": True,
                    "response": response,
                    "conversation_id": str(uuid.uuid4()),
                    "tools_used": []
                }
        
        return {
            "success": True,
            "response": "I understand you're asking about charge capture. I can help you with capturing charges, validating codes, finding templates, and analyzing patterns. Could you be more specific about what you need help with?",
            "conversation_id": str(uuid.uuid4()),
            "tools_used": []
        }


# Global instance
agentic_charge_capture = ChargeCaptureAgenticCore() 