"""
OpenAI LLM provider implementation.
"""
from typing import Optional
import logging

from .base_provider import BaseLLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI API provider for text generation.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key
        self.model = model
        self.client = None

        # Lazy import to avoid errors if openai is not installed
        if api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                logger.error("OpenAI library not installed. Install with: pip install openai")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")

    def generate(self, prompt: str, max_tokens: Optional[int] = 150) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate (default: 150)
            
        Returns:
            Generated text
            
        Raises:
            Exception: If generation fails or client not initialized
        """
        if not self.client:
            raise Exception("OpenAI client not initialized. Check API key.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert astrologer providing personalized, encouraging daily insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"Failed to generate insight: {str(e)}")

    def is_available(self) -> bool:
        """
        Check if OpenAI provider is available.
        
        Returns:
            True if client is initialized and ready
        """
        return self.client is not None

