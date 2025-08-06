# =============================================================================
# FILE: backend/app/agent/custom_model.py
# =============================================================================
from typing import List, Dict, Any, Optional
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
import requests
import json

class CustomClaimsModel(BaseLanguageModel):
    """Custom model integration for claims processing domain"""
    
    def __init__(self, 
                 api_endpoint: str,
                 api_key: Optional[str] = None,
                 model_name: str = "claims-specialist-v1",
                 temperature: float = 0.1,
                 max_tokens: int = 2000,
                 **kwargs):
        super().__init__(**kwargs)
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.claims_context = self._load_claims_context()
    
    def _generate(self,
                  messages: List[BaseMessage],
                  stop: Optional[List[str]] = None,
                  run_manager: Optional[CallbackManagerForLLMRun] = None,
                  **kwargs: Any) -> AIMessage:
        """Generate response using custom model"""
        
        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": self._convert_messages(messages),
            "context": self.claims_context,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": stop,
            **kwargs
        }
        
        # Add claims-specific instructions
        payload["system_instructions"] = self._get_claims_instructions()
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result.get("content", result.get("message", ""))
            
            return AIMessage(content=content)
            
        except requests.RequestException as e:
            raise Exception(f"Custom model API error: {str(e)}")
    
    def _convert_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        """Convert LangChain messages to API format"""
        
        converted = []
        for msg in messages:
            role = "user"
            if hasattr(msg, "type"):
                if msg.type == "ai":
                    role = "assistant"
                elif msg.type == "system":
                    role = "system"
            
            converted.append({
                "role": role,
                "content": msg.content
            })
        
        return converted
    
    def _load_claims_context(self) -> Dict[str, Any]:
        """Load claims processing domain context"""
        
        return {
            "domain": "healthcare_claims_processing",
            "knowledge_areas": [
                "EDI X12 transactions",
                "CPT and CDT procedure codes",
                "Claim validation rules",
                "Payer requirements",
                "Dental terminology",
                "Medical billing practices"
            ],
            "common_errors": [
                "Invalid NPI format",
                "Missing tooth information for dental procedures",
                "Incorrect procedure codes",
                "Date validation failures",
                "Missing diagnosis codes"
            ],
            "validation_patterns": [
                "NPI check digit validation",
                "Tooth number ranges (1-32 for permanent, A-T for primary)",
                "Procedure code format validation",
                "Date range checks",
                "Required field validation"
            ]
        }
    
    def _get_claims_instructions(self) -> str:
        """Get specialized instructions for claims processing"""
        
        return """
        You are a specialized AI assistant for healthcare claims processing with expertise in:
        
        1. EDI X12 transaction analysis (837P, 837D, 837I, 835)
        2. Claims validation and error identification
        3. Dental and medical procedure codes (CDT, CPT)
        4. Payer-specific requirements and companion guides
        5. Financial reconciliation and reporting
        
        When analyzing claims:
        - Always validate required fields and data formats
        - Check for dental-specific requirements (tooth numbers, surfaces)
        - Consider payer-specific validation rules
        - Provide actionable recommendations for fixing errors
        - Identify patterns that could indicate systemic issues
        
        Be precise, accurate, and focus on practical solutions that improve claims processing efficiency.
        """
    
    @property
    def _llm_type(self) -> str:
        return "custom_claims_model"
