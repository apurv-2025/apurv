from openai import OpenAI
import os
from typing import Dict, Any
from sqlalchemy.orm import Session
from models.agent import Agent
from services.vector_service import VectorService

class LLMService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "test-key"))
        self.vector_service = VectorService()
    
    async def generate_response(self, agent: Agent, user_message: str, db: Session) -> Dict[str, Any]:
        try:
            # Retrieve relevant context from knowledge base
            context = await self.vector_service.search_similar(
                query=user_message,
                agent_id=agent.id,
                top_k=3
            )
            
            # Build system prompt
            system_prompt = f"""
            You are {agent.name}, a {agent.role} assistant for a medical practice.
            
            Persona: {agent.persona}
            
            Instructions: {agent.instructions}
            
            Context from knowledge base:
            {context}
            
            Always maintain HIPAA compliance and never share patient information.
            If you don't know something, say so and suggest contacting the appropriate staff member.
            """
            
            # Generate response using OpenAI
            if os.getenv("OPENAI_API_KEY") == "test-key":
                # Mock response for testing
                return {
                    "response": f"Mock response from {agent.name} for: {user_message}",
                    "confidence": 0.8
                }
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content,
                "confidence": 0.8  # Could be improved with actual confidence scoring
            }
            
        except Exception as e:
            return {
                "response": "I'm sorry, I'm having trouble processing your request right now. Please try again or contact support.",
                "confidence": 0.0
            }
