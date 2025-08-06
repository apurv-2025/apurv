# =============================================================================
# FILE: backend/app/agent/model_factory.py
# =============================================================================
from typing import Optional
from langchain_core.language_models.base import BaseLanguageModel
from .custom_model import CustomClaimsModel
from ..config import AgentSettings

class ModelFactory:
    """Factory for creating different types of models"""
    
    @staticmethod
    def create_model(settings: AgentSettings) -> BaseLanguageModel:
        """Create a model based on configuration"""
        
        if settings.MODEL_PROVIDER == "openai":
            return ModelFactory._create_openai_model(settings)
        elif settings.MODEL_PROVIDER == "anthropic":
            return ModelFactory._create_anthropic_model(settings)
        elif settings.MODEL_PROVIDER == "custom":
            return ModelFactory._create_custom_model(settings)
        else:
            raise ValueError(f"Unsupported model provider: {settings.MODEL_PROVIDER}")
    
    @staticmethod
    def _create_openai_model(settings: AgentSettings) -> BaseLanguageModel:
        """Create OpenAI model"""
        try:
            from langchain_openai import ChatOpenAI
            
            return ChatOpenAI(
                model=settings.MODEL_NAME,
                temperature=settings.MODEL_TEMPERATURE,
                max_tokens=settings.MODEL_MAX_TOKENS,
                api_key=settings.OPENAI_API_KEY
            )
        except ImportError:
            raise ImportError("langchain-openai package is required for OpenAI models")
    
    @staticmethod
    def _create_anthropic_model(settings: AgentSettings) -> BaseLanguageModel:
        """Create Anthropic model"""
        try:
            from langchain_anthropic import ChatAnthropic
            
            return ChatAnthropic(
                model=settings.MODEL_NAME,
                temperature=settings.MODEL_TEMPERATURE,
                max_tokens=settings.MODEL_MAX_TOKENS,
                api_key=settings.ANTHROPIC_API_KEY
            )
        except ImportError:
            raise ImportError("langchain-anthropic package is required for Anthropic models")
    
    @staticmethod
    def _create_custom_model(settings: AgentSettings) -> BaseLanguageModel:
        """Create custom model"""
        if not settings.CUSTOM_MODEL_ENDPOINT:
            raise ValueError("CUSTOM_MODEL_ENDPOINT is required for custom models")
        
        return CustomClaimsModel(
            api_endpoint=settings.CUSTOM_MODEL_ENDPOINT,
            api_key=settings.CUSTOM_MODEL_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=settings.MODEL_TEMPERATURE,
            max_tokens=settings.MODEL_MAX_TOKENS
        )
