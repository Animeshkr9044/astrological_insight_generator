"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.routes import router
from app.config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI instance
    """
    app = FastAPI(
        title=settings.app_name,
        description="Generate personalized daily astrological insights using zodiac logic and LLM",
        version=settings.api_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router)

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.app_name}")
        logger.info(f"LLM Provider: {settings.get_effective_provider()}")
        logger.info(f"Debug mode: {settings.debug}")

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Shutting down {settings.app_name}")

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.api_version,
            "status": "running",
            "docs": "/docs",
            "api_root": "/api/v1",
        }

    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )

