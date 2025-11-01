"""
FastAPI dependency injection.
"""
from functools import lru_cache
from fastapi import Depends

from app.config.settings import Settings, get_settings
from app.services.insight_service import InsightService
from app.core.vector_store import VectorStoreService


@lru_cache()
def get_cached_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return get_settings()


# Cache for vector store service (module-level singleton)
_vector_store_cache = None


def get_vector_store_service(settings: Settings = Depends(get_cached_settings)) -> VectorStoreService:
    """
    Get or create a cached vector store service instance.
    
    Args:
        settings: Settings instance (injected via dependency)
        
    Returns:
        VectorStoreService instance
    """
    global _vector_store_cache
    
    # Return cached instance if available
    if _vector_store_cache is not None:
        return _vector_store_cache
    
    service = VectorStoreService(
        enabled=settings.vector_store_enabled,
        mode=settings.vector_store_mode,
        qdrant_url=settings.qdrant_url,
        qdrant_api_key=settings.qdrant_api_key,
        embedding_model=settings.embedding_model,
        collection_name=settings.vector_collection_name,
    )
    
    # Auto-load corpus on initialization
    if service.is_available():
        service.load_corpus()
    
    # Cache the instance
    _vector_store_cache = service
    
    return service


def get_insight_service(
    settings: Settings = Depends(get_cached_settings),
    vector_store: VectorStoreService = Depends(get_vector_store_service),
) -> InsightService:
    """
    Create and return an InsightService instance.
    
    Args:
        settings: Settings instance (injected via dependency)
        vector_store: Vector store service instance (injected via dependency)
        
    Returns:
        InsightService instance configured with current settings
    """
    # Determine which provider to use
    provider = settings.get_effective_provider()
    api_key = settings.openai_api_key if provider == "openai" else None
    
    return InsightService(
        llm_provider=provider,
        api_key=api_key,
        model=settings.openai_model,
        translation_enabled=settings.translation_enabled,
        translation_mock=settings.translation_mock,
        vector_store_service=vector_store,
    )

