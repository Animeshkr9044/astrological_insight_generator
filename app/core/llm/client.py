"""
LLM client for managing different providers.
"""
from typing import Optional
import logging

from .providers.base_provider import BaseLLMProvider
from .providers.openai_provider import OpenAIProvider
from .providers.mock_provider import MockProvider
from .prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Main LLM client that manages different providers.
    
    This class implements the strategy pattern for easy provider swapping.
    """

    def __init__(
        self,
        provider_name: str = "mock",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize LLM client with specified provider.
        
        Args:
            provider_name: Name of provider ("openai", "mock")
            api_key: API key for the provider (if needed)
            model: Model name (provider-specific)
        """
        self.provider_name = provider_name
        self.provider = self._initialize_provider(provider_name, api_key, model)
        self.prompt_builder = PromptBuilder()

    def _initialize_provider(
        self,
        provider_name: str,
        api_key: Optional[str],
        model: Optional[str],
    ) -> BaseLLMProvider:
        """
        Initialize the specified provider.
        
        Args:
            provider_name: Name of provider
            api_key: API key
            model: Model name
            
        Returns:
            Initialized provider instance
            
        Raises:
            ValueError: If provider name is invalid
        """
        provider_name = provider_name.lower()

        if provider_name == "openai":
            if not api_key:
                logger.warning("OpenAI API key not provided, falling back to mock provider")
                return MockProvider()
            return OpenAIProvider(api_key=api_key, model=model or "gpt-3.5-turbo")

        elif provider_name == "mock":
            return MockProvider()

        else:
            raise ValueError(
                f"Unknown provider: {provider_name}. Supported: 'openai', 'mock'"
            )

    def generate_insight(self, prompt: str, max_tokens: Optional[int] = 150) -> str:
        """
        Generate insight using the configured provider.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated insight text
            
        Raises:
            Exception: If provider is not available or generation fails
        """
        if not self.provider.is_available():
            raise Exception(f"Provider '{self.provider_name}' is not available")

        try:
            insight = self.provider.generate(prompt, max_tokens)
            return insight
        except Exception as e:
            logger.error(f"Failed to generate insight: {e}")
            raise

    def is_provider_available(self) -> bool:
        """
        Check if the current provider is available.
        
        Returns:
            True if provider is ready to use
        """
        return self.provider.is_available()

    def get_prompt_builder(self) -> PromptBuilder:
        """
        Get the prompt builder instance.
        
        Returns:
            PromptBuilder instance
        """
        return self.prompt_builder

    def switch_provider(
        self,
        provider_name: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Switch to a different provider.
        
        Args:
            provider_name: Name of new provider
            api_key: API key for the provider
            model: Model name
        """
        logger.info(f"Switching provider from '{self.provider_name}' to '{provider_name}'")
        self.provider_name = provider_name
        self.provider = self._initialize_provider(provider_name, api_key, model)

