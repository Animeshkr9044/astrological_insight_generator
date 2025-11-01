"""
FastAPI dependency injection.
"""
from functools import lru_cache

from app.config.settings import Settings, get_settings
from app.services.insight_service import InsightService


@lru_cache()
def get_cached_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return get_settings()


def get_insight_service(settings: Settings = None) -> InsightService:
    """
    Create and return an InsightService instance.
    
    Args:
        settings: Settings instance (optional, will use default if not provided)
        
    Returns:
        InsightService instance configured with current settings
    """
    if settings is None:
        settings = get_cached_settings()
    
    # Determine which provider to use
    provider = settings.get_effective_provider()
    api_key = settings.openai_api_key if provider == "openai" else None
    
    return InsightService(
        llm_provider=provider,
        api_key=api_key,
        model=settings.openai_model,
        translation_enabled=settings.translation_enabled,
        translation_mock=settings.translation_mock,
    )

