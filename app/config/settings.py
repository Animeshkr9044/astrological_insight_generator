"""
Application settings and configuration management.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Settings are loaded from:
    1. Environment variables
    2. .env file (if present)
    3. Default values
    """

    # Application Settings
    app_name: str = "Astrological Insight Generator"
    api_version: str = "v1"
    debug: bool = False
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LLM Settings
    llm_provider: str = "openai"  # "openai", "mock"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    llm_max_tokens: int = 150
    llm_temperature: float = 0.7
    
    # Translation Settings
    translation_enabled: bool = False
    translation_mock: bool = False
    
    # Caching Settings (for future use)
    cache_enabled: bool = False
    cache_ttl: int = 86400  # 24 hours in seconds
    
    # Logging
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_llm_config(self) -> dict:
        """
        Get LLM configuration as a dictionary.
        
        Returns:
            Dictionary with LLM settings
        """
        return {
            "provider": self.llm_provider,
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "max_tokens": self.llm_max_tokens,
            "temperature": self.llm_temperature,
        }

    def is_openai_configured(self) -> bool:
        """
        Check if OpenAI is properly configured.
        
        Returns:
            True if OpenAI API key is set
        """
        return bool(self.openai_api_key and self.openai_api_key != "your_openai_api_key_here")

    def get_effective_provider(self) -> str:
        """
        Get the effective LLM provider based on configuration.
        
        If OpenAI is selected but not configured, falls back to mock.
        
        Returns:
            Provider name to use
        """
        if self.llm_provider == "openai" and not self.is_openai_configured():
            return "mock"
        return self.llm_provider


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings instance
    """
    return settings

