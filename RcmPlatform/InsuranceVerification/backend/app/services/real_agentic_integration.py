"""
Real Agentic Core Integration with InsuranceVerification Backend
Proper integration with the actual agentic-core from ClaimsProcessing
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

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


class InsuranceVerificationTool(BaseTool):
    """Insurance verification tool for agentic-core"""
    
    name = "verify_insurance"
    description = "Verify insurance coverage and eligibility for a member"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute insurance verification"""
        member_id = data.get("member_id")
        provider_npi = data.get("provider_npi")
        service_type = data.get("service_type", "30")
        
        if not member_id or not provider_npi:
            return {
                "success": False,
                "error": "Missing required parameters: member_id and provider_npi"
            }
        
        # Mock verification result (in real implementation, this would call actual insurance APIs)
        verification_result = {
            "member_id": member_id,
            "provider_npi": provider_npi,
            "service_type": service_type,
            "is_eligible": True,
            "coverage_details": {
                "deductible": "$500",
                "copay": "$25",
                "coinsurance": "20%",
                "out_of_pocket_max": "$5000"
            },
            "benefits": {
                "office_visits": "Covered",
                "specialist_visits": "Covered",
                "preventive_care": "Covered at 100%",
                "prescription_drugs": "Covered with copay"
            },
            "verification_date": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": verification_result,
            "tool_name": self.name
        }


class InsuranceExtractionTool(BaseTool):
    """Insurance information extraction tool for agentic-core"""
    
    name = "extract_insurance_info"
    description = "Extract insurance information from uploaded documents"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute insurance information extraction"""
        file_path = data.get("file_path")
        file_type = data.get("file_type", "image")
        
        if not file_path:
            return {
                "success": False,
                "error": "Missing required parameter: file_path"
            }
        
        # Mock extraction result (in real implementation, this would use OCR/ML)
        extraction_result = {
            "file_path": file_path,
            "file_type": file_type,
            "extracted_info": {
                "patient_name": "John Doe",
                "member_id": "123456789",
                "group_number": "GRP001",
                "plan_name": "Premium Health Plan",
                "insurance_company": "Health Insurance Co",
                "effective_date": "01/01/2024",
                "phone_number": "1-800-HEALTH"
            },
            "confidence_score": 0.95,
            "extraction_date": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": extraction_result,
            "tool_name": self.name
        }


class EligibilityCheckTool(BaseTool):
    """Eligibility check tool for agentic-core"""
    
    name = "check_eligibility"
    description = "Check patient eligibility for specific services"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute eligibility check"""
        member_id = data.get("member_id")
        service_type = data.get("service_type")
        provider_npi = data.get("provider_npi")
        
        if not member_id or not service_type:
            return {
                "success": False,
                "error": "Missing required parameters: member_id and service_type"
            }
        
        # Mock eligibility result (in real implementation, this would call eligibility APIs)
        eligibility_result = {
            "member_id": member_id,
            "service_type": service_type,
            "provider_npi": provider_npi,
            "is_eligible": True,
            "eligibility_date": datetime.now().isoformat(),
            "service_details": {
                "service_description": "Office Visit",
                "coverage_level": "Primary",
                "authorization_required": False,
                "benefit_percentage": "100%"
            }
        }
        
        return {
            "success": True,
            "result": eligibility_result,
            "tool_name": self.name
        }


class EDIAnalysisTool(BaseTool):
    """EDI analysis tool for agentic-core"""
    
    name = "analyze_edi"
    description = "Analyze EDI 270/271 transactions"
    
    async def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute EDI analysis"""
        edi_content = data.get("edi_content")
        transaction_type = data.get("transaction_type", "270")
        
        if not edi_content:
            return {
                "success": False,
                "error": "Missing required parameter: edi_content"
            }
        
        # Mock EDI analysis result (in real implementation, this would parse EDI)
        analysis_result = {
            "transaction_type": transaction_type,
            "edi_content": edi_content[:100] + "..." if len(edi_content) > 100 else edi_content,
            "analysis": {
                "segments_found": ["ISA", "GS", "ST", "BHT", "HL", "NM1", "DMG", "DTP", "SE", "GE", "IEA"],
                "member_info": {
                    "member_id": "123456789",
                    "subscriber_name": "John Doe",
                    "date_of_birth": "1980-01-01"
                },
                "provider_info": {
                    "provider_npi": "1234567890",
                    "provider_name": "Dr. Smith"
                },
                "service_type": "30",
                "request_date": datetime.now().isoformat()
            },
            "validation": {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
        }
        
        return {
            "success": True,
            "result": analysis_result,
            "tool_name": self.name
        }


class RealAgenticInsuranceVerification:
    """Real integration with AgenticCore for InsuranceVerification"""
    
    def __init__(self, model_provider: str = "openai", api_key: Optional[str] = None, database_url: Optional[str] = None):
        if not AGENTIC_CORE_AVAILABLE:
            raise ImportError("Agentic Core is not available. Please ensure it's properly installed.")
        
        self.model_provider = model_provider
        self.api_key = api_key
        self.database_url = database_url
        self.agentic = None
        self._initialize_agentic()
    
    def _initialize_agentic(self):
        """Initialize the agentic core with insurance-specific tools"""
        try:
            # Create agentic core instance
            self.agentic = create_agentic_core(
                model_provider=self.model_provider,
                api_key=self.api_key,
                database_url=self.database_url
            )
            
            # Register insurance-specific tools
            self._register_tools()
            
            logger.info("Agentic Core initialized successfully with insurance tools")
            
        except Exception as e:
            logger.error(f"Failed to initialize Agentic Core: {e}")
            raise
    
    def _register_tools(self):
        """Register insurance-specific tools with agentic core"""
        try:
            # Register our custom tools
            tools = [
                InsuranceVerificationTool(),
                InsuranceExtractionTool(),
                EligibilityCheckTool(),
                EDIAnalysisTool()
            ]
            
            for tool in tools:
                self.agentic.register_tool(tool)
            
            logger.info(f"Registered {len(tools)} insurance-specific tools")
            
        except Exception as e:
            logger.error(f"Failed to register tools: {e}")
            raise
    
    async def chat_with_insurance_data(self, message: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Chat with AI agent about insurance verification"""
        try:
            response = await self.agentic.chat(
                message=message,
                user_id=user_id,
                context=context or {}
            )
            
            return {
                "response": response.response,
                "conversation_id": response.conversation_id,
                "timestamp": datetime.now().isoformat(),
                "task_id": getattr(response, 'task_id', None)
            }
            
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now.",
                "conversation_id": None,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def verify_insurance_coverage(self, member_id: str, provider_npi: str, service_type: str = "30") -> Dict[str, Any]:
        """Verify insurance coverage using AI agent"""
        try:
            response = await self.agentic.process_task(
                task_type="verify_insurance",
                user_id="system",
                task_description=f"Verify insurance coverage for member {member_id} with provider {provider_npi} for service type {service_type}",
                context={
                    "member_id": member_id,
                    "provider_npi": provider_npi,
                    "service_type": service_type
                }
            )
            
            return {
                "success": True,
                "result": response.result,
                "task_type": "verify_insurance",
                "processing_time": getattr(response, 'processing_time', None)
            }
            
        except Exception as e:
            logger.error(f"Insurance verification failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": "verify_insurance"
            }
    
    async def extract_insurance_information(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extract insurance information using AI agent"""
        try:
            response = await self.agentic.process_task(
                task_type="extract_insurance_info",
                user_id="system",
                task_description=f"Extract insurance information from {file_type} file at {file_path}",
                context={
                    "file_path": file_path,
                    "file_type": file_type
                }
            )
            
            return {
                "success": True,
                "result": response.result,
                "task_type": "extract_insurance_info",
                "processing_time": getattr(response, 'processing_time', None)
            }
            
        except Exception as e:
            logger.error(f"Insurance extraction failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": "extract_insurance_info"
            }
    
    async def check_patient_eligibility(self, member_id: str, service_type: str, provider_npi: str = None) -> Dict[str, Any]:
        """Check patient eligibility using AI agent"""
        try:
            response = await self.agentic.process_task(
                task_type="check_eligibility",
                user_id="system",
                task_description=f"Check eligibility for member {member_id} for service type {service_type}",
                context={
                    "member_id": member_id,
                    "service_type": service_type,
                    "provider_npi": provider_npi
                }
            )
            
            return {
                "success": True,
                "result": response.result,
                "task_type": "check_eligibility",
                "processing_time": getattr(response, 'processing_time', None)
            }
            
        except Exception as e:
            logger.error(f"Eligibility check failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": "check_eligibility"
            }
    
    async def analyze_edi_transaction(self, edi_content: str, transaction_type: str = "270") -> Dict[str, Any]:
        """Analyze EDI transaction using AI agent"""
        try:
            response = await self.agentic.process_task(
                task_type="analyze_edi",
                user_id="system",
                task_description=f"Analyze {transaction_type} EDI transaction",
                context={
                    "edi_content": edi_content,
                    "transaction_type": transaction_type
                }
            )
            
            return {
                "success": True,
                "result": response.result,
                "task_type": "analyze_edi",
                "processing_time": getattr(response, 'processing_time', None)
            }
            
        except Exception as e:
            logger.error(f"EDI analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_type": "analyze_edi"
            }
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        try:
            tools = await self.agentic.get_available_tools()
            return tools
        except Exception as e:
            logger.error(f"Failed to get available tools: {e}")
            return []
    
    async def process_complex_verification(self, verification_request: Dict[str, Any]) -> Dict[str, Any]:
        """Process complex insurance verification with multiple steps"""
        try:
            member_id = verification_request.get("member_id")
            provider_npi = verification_request.get("provider_npi")
            service_types = verification_request.get("service_types", ["30"])
            
            results = []
            
            for service_type in service_types:
                result = await self.verify_insurance_coverage(member_id, provider_npi, service_type)
                results.append(result)
            
            # Combine results
            combined_result = {
                "member_id": member_id,
                "provider_npi": provider_npi,
                "verification_results": results,
                "overall_eligible": all(r.get("success", False) for r in results),
                "timestamp": datetime.now().isoformat()
            }
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Complex verification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def close(self):
        """Close the agentic core connection"""
        if self.agentic:
            await self.agentic.close()


# Fallback to mock implementation if agentic-core is not available
class FallbackAgenticInsuranceVerification:
    """Fallback implementation when agentic-core is not available"""
    
    def __init__(self, model_provider: str = "openai", api_key: Optional[str] = None, database_url: Optional[str] = None):
        logger.warning("Using fallback mock implementation - Agentic Core not available")
        from .agentic_integration import AgenticInsuranceVerification as MockAgentic
        self.mock_agentic = MockAgentic(model_provider, api_key, database_url)
    
    async def chat_with_insurance_data(self, message: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.mock_agentic.chat_with_insurance_data(message, user_id, context)
    
    async def verify_insurance_coverage(self, member_id: str, provider_npi: str, service_type: str = "30") -> Dict[str, Any]:
        return await self.mock_agentic.verify_insurance_coverage(member_id, provider_npi, service_type)
    
    async def extract_insurance_information(self, file_path: str, file_type: str) -> Dict[str, Any]:
        return await self.mock_agentic.extract_insurance_information(file_path, file_type)
    
    async def check_patient_eligibility(self, member_id: str, service_type: str, provider_npi: str = None) -> Dict[str, Any]:
        return await self.mock_agentic.check_patient_eligibility(member_id, service_type, provider_npi)
    
    async def analyze_edi_transaction(self, edi_content: str, transaction_type: str = "270") -> Dict[str, Any]:
        return await self.mock_agentic.analyze_edi_transaction(edi_content, transaction_type)
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        return await self.mock_agentic.get_available_tools()
    
    async def process_complex_verification(self, verification_request: Dict[str, Any]) -> Dict[str, Any]:
        return await self.mock_agentic.process_complex_verification(verification_request)
    
    async def close(self):
        pass


# Factory function to create the appropriate implementation
def create_agentic_insurance_verification(
    model_provider: str = "openai",
    api_key: Optional[str] = None,
    database_url: Optional[str] = None,
    force_mock: bool = False
):
    """Create an agentic insurance verification instance"""
    if force_mock or not AGENTIC_CORE_AVAILABLE:
        return FallbackAgenticInsuranceVerification(model_provider, api_key, database_url)
    else:
        return RealAgenticInsuranceVerification(model_provider, api_key, database_url)


# Global instance
agentic_insurance_verification = create_agentic_insurance_verification() 