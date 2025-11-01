"""
Base abstract class for LLM providers.
"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    This allows easy swapping between different LLM providers
    (OpenAI, HuggingFace, Anthropic, etc.)
    """

    @abstractmethod
    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Generate text based on the given prompt.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
            
        Raises:
            Exception: If generation fails
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is properly configured and available.
        
        Returns:
            True if provider is ready to use, False otherwise
        """
        pass

