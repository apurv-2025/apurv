"""
Model Providers - AI model integration
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)


class BaseModelProvider(ABC):
    """Base class for model providers."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = httpx.AsyncClient(timeout=30.0)
    
    @abstractmethod
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response from the model."""
        pass
    
    async def test_connection(self) -> bool:
        """Test the connection to the model provider."""
        try:
            # Simple test with a short prompt
            response = await self.generate("Hello", {})
            return bool(response)
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def close(self):
        """Close the model provider and cleanup resources."""
        await self.client.aclose()


class OpenAIModelProvider(BaseModelProvider):
    """OpenAI model provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        super().__init__(api_key, model)
        self.base_url = "https://api.openai.com/v1"
        self.api_key = api_key or self.api_key
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response using OpenAI API."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        try:
            # Build messages
            messages = [{"role": "user", "content": prompt}]
            
            # Add context if provided
            if context:
                context_message = f"Context: {context}\n\nUser message: {prompt}"
                messages = [{"role": "user", "content": context_message}]
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Return a fallback response
            return f"I apologize, but I encountered an error processing your request: {str(e)}"


class AnthropicModelProvider(BaseModelProvider):
    """Anthropic model provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key, model)
        self.base_url = "https://api.anthropic.com/v1"
        self.api_key = api_key or self.api_key
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response using Anthropic API."""
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        try:
            # Build the message
            message = prompt
            if context:
                message = f"Context: {context}\n\nUser: {prompt}"
            
            response = await self.client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": message
                        }
                    ]
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data["content"][0]["text"]
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            # Return a fallback response
            return f"I apologize, but I encountered an error processing your request: {str(e)}"


class MockModelProvider(BaseModelProvider):
    """Mock model provider for testing and development."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "mock-model"):
        super().__init__(api_key, model)
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a mock response."""
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Generate different responses based on prompt content
        prompt_lower = prompt.lower()
        
        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I'm your AI assistant. How can I help you today?"
        elif "claim" in prompt_lower:
            return "I can help you with claims processing. What specific claim would you like me to analyze?"
        elif "rejection" in prompt_lower:
            return "I can help you analyze claim rejections and suggest fixes. Which rejection would you like me to examine?"
        elif "report" in prompt_lower:
            return "I can generate various reports including financial summaries, rejection analysis, and performance metrics. What type of report would you like?"
        elif "help" in prompt_lower:
            return """I can help you with:
• Analyzing claims for issues and providing recommendations
• Processing claim rejections and suggesting fixes
• Generating various types of reports
• Searching claims by different criteria
• Answering questions about your claims data

What would you like me to help you with?"""
        else:
            return f"I understand you're asking about: {prompt}. Let me help you with that. This is a mock response for development purposes."
    
    async def test_connection(self) -> bool:
        """Test the mock connection."""
        return True


class CustomModelProvider(BaseModelProvider):
    """Custom model provider for custom endpoints."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "custom", endpoint: str = None, headers: Dict[str, str] = None):
        super().__init__(api_key, model)
        self.endpoint = endpoint
        self.headers = headers or {}
    
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response using a custom API endpoint."""
        if not self.endpoint:
            raise ValueError("Custom endpoint URL is required")
        
        try:
            # Prepare the request payload
            payload = {
                "prompt": prompt,
                "model": self.model,
                "context": context or {}
            }
            
            # Add API key to headers if provided
            headers = self.headers.copy()
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = await self.client.post(
                self.endpoint,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract response based on common patterns
            if "response" in data:
                return data["response"]
            elif "text" in data:
                return data["text"]
            elif "content" in data:
                return data["content"]
            elif "message" in data:
                return data["message"]
            else:
                return str(data)
                
        except Exception as e:
            logger.error(f"Custom API error: {e}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"


# Factory function to create model providers
def create_model_provider(
    provider_type: str,
    api_key: Optional[str] = None,
    model: str = None,
    **kwargs
) -> BaseModelProvider:
    """
    Factory function to create model providers.
    
    Args:
        provider_type: Type of provider (openai, anthropic, mock, custom)
        api_key: API key for the provider
        model: Model name
        **kwargs: Additional provider-specific arguments
        
    Returns:
        Model provider instance
    """
    if provider_type == "openai":
        return OpenAIModelProvider(api_key=api_key, model=model or "gpt-4")
    elif provider_type == "anthropic":
        return AnthropicModelProvider(api_key=api_key, model=model or "claude-3-sonnet-20240229")
    elif provider_type == "mock":
        return MockModelProvider(api_key=api_key, model=model or "mock-model")
    elif provider_type == "custom":
        return CustomModelProvider(
            api_key=api_key,
            model=model or "custom",
            endpoint=kwargs.get("endpoint"),
            headers=kwargs.get("headers")
        )
    else:
        raise ValueError(f"Unknown provider type: {provider_type}") 