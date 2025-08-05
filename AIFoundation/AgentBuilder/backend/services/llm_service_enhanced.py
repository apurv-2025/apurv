# services/llm_service_enhanced.py
import openai
import os
import requests
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from models.agent import Agent
from services.vector_service import VectorService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")  # openai, ollama, huggingface
        self.setup_provider()
        self.vector_service = VectorService()
    
    def setup_provider(self):
        """Initialize the selected LLM provider"""
        if self.provider == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        elif self.provider == "ollama":
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            self.model = os.getenv("OLLAMA_MODEL", "llama2")
        elif self.provider == "huggingface":
            self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
            self.model = os.getenv("HF_MODEL", "microsoft/DialoGPT-medium")
    
    async def generate_response(self, agent: Agent, user_message: str, db: Session, context: Optional[str] = None) -> Dict[str, Any]:
        """Generate response using the configured LLM provider"""
        try:
            # Get context from knowledge base if not provided
            if not context:
                context = await self.vector_service.search_similar(
                    query=user_message,
                    agent_id=agent.id,
                    top_k=3
                )
            
            # Build system prompt with HIPAA compliance
            system_prompt = self._build_system_prompt(agent, context)
            
            # Check for PII/PHI before processing
            if self._contains_phi(user_message):
                return {
                    "response": "I cannot process messages containing patient health information. Please remove any personal health details and try again.",
                    "confidence": 0.0,
                    "flagged": True
                }
            
            # Generate response based on provider
            if self.provider == "openai":
                response = await self._generate_openai_response(system_prompt, user_message)
            elif self.provider == "ollama":
                response = await self._generate_ollama_response(system_prompt, user_message)
            elif self.provider == "huggingface":
                response = await self._generate_hf_response(system_prompt, user_message)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
            
            # Post-process response for compliance
            response = self._sanitize_response(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now. Please try again or contact support.",
                "confidence": 0.0,
                "error": True
            }
    
    def _build_system_prompt(self, agent: Agent, context: str) -> str:
        """Build comprehensive system prompt with compliance guidelines"""
        hipaa_guidelines = """
        HIPAA COMPLIANCE RULES:
        - Never store, repeat, or reference specific patient information (names, SSNs, DOBs, addresses)
        - If patient information is mentioned, respond with generic guidance only
        - Always remind users to follow proper data handling procedures
        - Escalate sensitive queries to human staff
        """
        
        base_prompt = f"""
        You are {agent.name}, a {agent.role} assistant for a medical practice.
        
        Persona: {agent.persona}
        
        Instructions: {agent.instructions}
        
        {hipaa_guidelines}
        
        Knowledge Base Context:
        {context}
        
        Additional Guidelines:
        - Keep responses professional and helpful
        - If you don't know something, admit it and suggest appropriate next steps
        - Always prioritize patient privacy and data security
        - For billing questions, reference general policies without patient-specific details
        - For scheduling, use general availability information
        """
        
        return base_prompt
    
    async def _generate_openai_response(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return {
            "response": response.choices[0].message.content,
            "confidence": 0.8,  # Could be enhanced with actual confidence scoring
            "provider": "openai",
            "model": self.model
        }
    
    async def _generate_ollama_response(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Generate response using local Ollama"""
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {user_message}\nAssistant:",
            "stream": False
        }
        
        response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        return {
            "response": result.get("response", ""),
            "confidence": 0.7,  # Local models might have lower confidence
            "provider": "ollama",
            "model": self.model
        }
    
    async def _generate_hf_response(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Generate response using HuggingFace API"""
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        payload = {
            "inputs": f"{system_prompt}\n\nUser: {user_message}\nAssistant:",
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        
        return {
            "response": result[0]["generated_text"].split("Assistant:")[-1].strip(),
            "confidence": 0.75,
            "provider": "huggingface",
            "model": self.model
        }
    
    def _contains_phi(self, text: str) -> bool:
        """Basic PHI detection - should be enhanced with more sophisticated methods"""
        phi_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
            r'\b\d{2}/\d{2}/\d{4}\b',  # Date of birth pattern
            r'\b\d{3}-\d{3}-\d{4}\b',  # Phone number pattern
        ]
        
        import re
        for pattern in phi_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _sanitize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Remove any potential PHI from response"""
        # This is a basic implementation - should be enhanced
        response_text = response.get("response", "")
        
        # Remove potential phone numbers, SSNs, etc.
        import re
        response_text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED]', response_text)
        response_text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[REDACTED]', response_text)
        
        response["response"] = response_text
        return response
