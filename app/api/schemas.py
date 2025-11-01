"""
API request and response schemas using Pydantic.
"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, field_validator


class InsightRequest(BaseModel):
    """
    Request schema for generating an astrological insight.
    """
    name: str = Field(..., description="User's name", min_length=2, max_length=100)
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format", pattern=r"^\d{4}-\d{2}-\d{2}$")
    birth_time: str = Field(..., description="Birth time in HH:MM format (24-hour)", pattern=r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$")
    birth_place: str = Field(..., description="Birth place (city, country)", min_length=2, max_length=200)
    language: Optional[str] = Field(default="en", description="Preferred language (en, hi)")

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        """Validate language code."""
        if v not in ["en", "hi"]:
            raise ValueError("Language must be 'en' or 'hi'")
        return v.lower()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ritika",
                    "birth_date": "1995-08-20",
                    "birth_time": "14:30",
                    "birth_place": "Jaipur, India",
                    "language": "en"
                }
            ]
        }
    }


class ZodiacMetadata(BaseModel):
    """
    Metadata about the zodiac sign.
    """
    element: str = Field(..., description="Zodiac element (Fire, Earth, Air, Water)")
    ruling_planet: str = Field(..., description="Ruling planet")
    modality: str = Field(..., description="Modality (Cardinal, Fixed, Mutable)")


class InsightResponse(BaseModel):
    """
    Response schema for generated insight.
    """
    zodiac: str = Field(..., description="Zodiac sign")
    insight: str = Field(..., description="Generated personalized insight")
    language: str = Field(..., description="Language of the insight")
    generated_at: str = Field(..., description="ISO timestamp of generation")
    metadata: ZodiacMetadata = Field(..., description="Additional zodiac metadata")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zodiac": "Leo",
                    "insight": "Your innate leadership and warmth will shine today. Embrace spontaneity and avoid overthinking.",
                    "language": "en",
                    "generated_at": "2024-11-01T10:30:00",
                    "metadata": {
                        "element": "Fire",
                        "ruling_planet": "Sun",
                        "modality": "Fixed"
                    }
                }
            ]
        }
    }


class ZodiacInfoRequest(BaseModel):
    """
    Request schema for getting zodiac information only.
    """
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format", pattern=r"^\d{4}-\d{2}-\d{2}$")


class ZodiacInfoResponse(BaseModel):
    """
    Response schema for zodiac information.
    """
    sign: str = Field(..., description="Zodiac sign")
    symbol: str = Field(..., description="Zodiac symbol")
    element: str = Field(..., description="Element")
    modality: str = Field(..., description="Modality")
    ruling_planet: str = Field(..., description="Ruling planet")
    summary: str = Field(..., description="Brief summary of traits")


class HealthCheckResponse(BaseModel):
    """
    Response schema for health check.
    """
    status: str = Field(..., description="Service status")
    llm_provider: str = Field(..., description="Current LLM provider")
    llm_available: bool = Field(..., description="Whether LLM is available")
    translation_enabled: bool = Field(..., description="Whether translation is enabled")
    supported_languages: list[str] = Field(..., description="Supported language codes")


class ErrorResponse(BaseModel):
    """
    Response schema for errors.
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

