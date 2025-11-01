"""
FastAPI routes for the Astrological Insight Generator API.
"""
from fastapi import APIRouter, HTTPException, Depends
import logging

from app.api.schemas import (
    InsightRequest,
    InsightResponse,
    ZodiacInfoRequest,
    ZodiacInfoResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from app.api.dependencies import get_insight_service
from app.services.insight_service import InsightService
from app.services.validator_service import ValidationError

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["insights"])


@router.post(
    "/insight",
    response_model=InsightResponse,
    summary="Generate Astrological Insight",
    description="Generate a personalized daily astrological insight based on birth details.",
    responses={
        200: {"description": "Successfully generated insight"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def generate_insight(
    request: InsightRequest,
    insight_service: InsightService = Depends(get_insight_service),
) -> InsightResponse:
    """
    Generate a personalized astrological insight.
    
    Args:
        request: Insight request with birth details
        insight_service: Injected InsightService instance
        
    Returns:
        InsightResponse with zodiac and personalized insight
        
    Raises:
        HTTPException: If validation fails or insight generation fails
    """
    try:
        logger.info(f"Received insight request for {request.name}")
        
        result = insight_service.generate_insight(
            name=request.name,
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_place=request.birth_place,
            language=request.language,
        )
        
        return InsightResponse(**result)
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error generating insight: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate insight")


@router.post(
    "/zodiac",
    response_model=ZodiacInfoResponse,
    summary="Get Zodiac Information",
    description="Get zodiac sign information based on birth date.",
)
async def get_zodiac_info(
    request: ZodiacInfoRequest,
    insight_service: InsightService = Depends(get_insight_service),
) -> ZodiacInfoResponse:
    """
    Get zodiac information without generating an insight.
    
    Args:
        request: Request with birth date
        insight_service: Injected InsightService instance
        
    Returns:
        ZodiacInfoResponse with zodiac information
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        result = insight_service.get_zodiac_info(request.birth_date)
        return ZodiacInfoResponse(**result)
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error getting zodiac info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get zodiac information")


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health and status of the service.",
)
async def health_check(
    insight_service: InsightService = Depends(get_insight_service),
) -> HealthCheckResponse:
    """
    Health check endpoint.
    
    Args:
        insight_service: Injected InsightService instance
        
    Returns:
        HealthCheckResponse with service status
    """
    try:
        status = insight_service.health_check()
        return HealthCheckResponse(**status)
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get(
    "/",
    summary="API Root",
    description="Root endpoint with API information.",
)
async def root():
    """
    Root endpoint.
    
    Returns:
        API information
    """
    return {
        "name": "Astrological Insight Generator API",
        "version": "v1",
        "endpoints": {
            "generate_insight": "/api/v1/insight",
            "zodiac_info": "/api/v1/zodiac",
            "health": "/api/v1/health",
            "docs": "/docs",
        },
    }

