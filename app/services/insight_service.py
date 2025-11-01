"""
Main insight service orchestrator.
"""
from datetime import date, datetime
from typing import Dict, Optional
import logging

from app.core.zodiac.calculator import ZodiacCalculator
from app.core.llm.client import LLMClient
from app.core.translation.translator import get_translator
from app.services.validator_service import ValidatorService, ValidationError

logger = logging.getLogger(__name__)


class InsightService:
    """
    Main service for orchestrating insight generation.
    
    This service coordinates between:
    - Input validation
    - Zodiac calculation
    - LLM-based insight generation
    - Translation (if needed)
    - Response formatting
    """

    def __init__(
        self,
        llm_provider: str = "mock",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        translation_enabled: bool = False,
        translation_mock: bool = False,
    ):
        """
        Initialize the insight service.
        
        Args:
            llm_provider: LLM provider name ("openai", "mock")
            api_key: API key for LLM provider
            model: Model name
            translation_enabled: Whether translation is enabled
            translation_mock: Whether to use mock translation
        """
        self.validator = ValidatorService()
        self.zodiac_calculator = ZodiacCalculator()
        self.llm_client = LLMClient(
            provider_name=llm_provider,
            api_key=api_key,
            model=model,
        )
        self.translator = get_translator(
            enabled=translation_enabled,
            mock=translation_mock,
        )

    def generate_insight(
        self,
        name: str,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        language: str = "en",
    ) -> Dict:
        """
        Generate a personalized astrological insight.
        
        Args:
            name: User's name
            birth_date: Birth date in YYYY-MM-DD format
            birth_time: Birth time in HH:MM format
            birth_place: Birth place
            language: Preferred language code
            
        Returns:
            Dictionary containing insight and metadata
            
        Raises:
            ValidationError: If input validation fails
            Exception: If insight generation fails
        """
        logger.info(f"Generating insight for {name}")

        # Step 1: Validate inputs
        try:
            validated_name, validated_date, validated_time, validated_place, validated_lang = (
                self.validator.validate_insight_request(
                    name, birth_date, birth_time, birth_place, language
                )
            )
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise

        # Step 2: Calculate zodiac sign
        try:
            zodiac_sign = self.zodiac_calculator.calculate_sign(validated_date, validated_time)
            logger.info(f"Calculated zodiac sign: {zodiac_sign}")
        except Exception as e:
            logger.error(f"Error calculating zodiac sign: {e}")
            raise Exception(f"Failed to calculate zodiac sign: {str(e)}")

        # Step 3: Get zodiac traits
        try:
            traits = self.zodiac_calculator.get_traits(zodiac_sign)
            trait_summary = self.zodiac_calculator.get_trait_summary(zodiac_sign)
        except Exception as e:
            logger.error(f"Error getting zodiac traits: {e}")
            raise Exception(f"Failed to get zodiac traits: {str(e)}")

        # Step 4: Build prompt and generate insight
        try:
            prompt_builder = self.llm_client.get_prompt_builder()
            prompt = prompt_builder.build_insight_prompt(
                name=validated_name,
                zodiac_sign=zodiac_sign,
                traits=traits,
                birth_date=validated_date,
                current_date=date.today(),
            )
            
            logger.debug(f"Generated prompt: {prompt}")
            
            insight = self.llm_client.generate_insight(prompt)
            logger.info("Successfully generated insight")
            
        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            raise Exception(f"Failed to generate insight: {str(e)}")

        # Step 5: Translate if needed
        if validated_lang != "en":
            try:
                insight = self.translator.translate(insight, validated_lang)
                logger.info(f"Translated insight to {validated_lang}")
            except Exception as e:
                logger.warning(f"Translation failed, using English: {e}")
                validated_lang = "en"

        # Step 6: Format and return response
        response = {
            "zodiac": zodiac_sign,
            "insight": insight,
            "language": validated_lang,
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "element": traits["element"],
                "ruling_planet": traits["ruling_planet"],
                "modality": traits["modality"],
            },
        }

        return response

    def get_zodiac_info(self, birth_date: str) -> Dict:
        """
        Get zodiac information without generating an insight.
        
        Args:
            birth_date: Birth date in YYYY-MM-DD format
            
        Returns:
            Dictionary with zodiac information
            
        Raises:
            ValidationError: If date is invalid
        """
        validated_date = self.validator.validate_date(birth_date)
        profile = self.zodiac_calculator.get_full_profile(validated_date)
        
        return {
            "sign": profile["sign"],
            "symbol": profile["symbol"],
            "element": profile["element"],
            "modality": profile["modality"],
            "ruling_planet": profile["ruling_planet"],
            "summary": profile["summary"],
        }

    def health_check(self) -> Dict:
        """
        Check the health status of the service.
        
        Returns:
            Dictionary with service status
        """
        return {
            "status": "healthy",
            "llm_provider": self.llm_client.provider_name,
            "llm_available": self.llm_client.is_provider_available(),
            "translation_enabled": self.translator.enabled,
            "supported_languages": self.translator.get_supported_languages(),
        }

