"""
Input validation service.
"""
from datetime import datetime, date
from typing import Optional, Tuple
import re


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ValidatorService:
    """
    Service for validating user input data.
    """

    @staticmethod
    def validate_date(date_string: str) -> date:
        """
        Validate and parse birth date string.
        
        Args:
            date_string: Date string in YYYY-MM-DD format
            
        Returns:
            Parsed date object
            
        Raises:
            ValidationError: If date format is invalid or date is in the future
        """
        if not date_string:
            raise ValidationError("Birth date is required")

        try:
            birth_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                "Invalid date format. Expected YYYY-MM-DD (e.g., 1995-08-20)"
            )

        # Check if date is in the future
        if birth_date > date.today():
            raise ValidationError("Birth date cannot be in the future")

        # Check if date is too far in the past (more than 150 years)
        years_ago = (date.today() - birth_date).days / 365.25
        if years_ago > 150:
            raise ValidationError("Birth date seems unrealistic (more than 150 years ago)")

        return birth_date

    @staticmethod
    def validate_time(time_string: str) -> str:
        """
        Validate birth time string.
        
        Args:
            time_string: Time string in HH:MM format
            
        Returns:
            Validated time string
            
        Raises:
            ValidationError: If time format is invalid
        """
        if not time_string:
            raise ValidationError("Birth time is required")

        # Check format with regex
        time_pattern = r"^([0-1][0-9]|2[0-3]):([0-5][0-9])$"
        if not re.match(time_pattern, time_string):
            raise ValidationError(
                "Invalid time format. Expected HH:MM in 24-hour format (e.g., 14:30)"
            )

        return time_string

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validate user name.
        
        Args:
            name: User's name
            
        Returns:
            Validated and sanitized name
            
        Raises:
            ValidationError: If name is invalid
        """
        if not name or not name.strip():
            raise ValidationError("Name is required")

        name = name.strip()

        # Check length
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")

        if len(name) > 100:
            raise ValidationError("Name must be less than 100 characters")

        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            raise ValidationError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )

        return name

    @staticmethod
    def validate_location(location: str) -> str:
        """
        Validate birth location.
        
        Args:
            location: Birth place string
            
        Returns:
            Validated location
            
        Raises:
            ValidationError: If location is invalid
        """
        if not location or not location.strip():
            raise ValidationError("Birth place is required")

        location = location.strip()

        # Check length
        if len(location) < 2:
            raise ValidationError("Birth place must be at least 2 characters long")

        if len(location) > 200:
            raise ValidationError("Birth place must be less than 200 characters")

        return location

    @staticmethod
    def validate_language(language: str) -> str:
        """
        Validate language code.
        
        Args:
            language: Language code (e.g., 'en', 'hi')
            
        Returns:
            Validated language code
            
        Raises:
            ValidationError: If language is not supported
        """
        supported_languages = ["en", "hi"]
        
        if not language:
            return "en"  # Default to English

        language = language.lower().strip()

        if language not in supported_languages:
            raise ValidationError(
                f"Language '{language}' not supported. Supported languages: {', '.join(supported_languages)}"
            )

        return language

    def validate_insight_request(
        self,
        name: str,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        language: Optional[str] = "en",
    ) -> Tuple[str, date, str, str, str]:
        """
        Validate all fields of an insight request.
        
        Args:
            name: User's name
            birth_date: Birth date string
            birth_time: Birth time string
            birth_place: Birth place string
            language: Language code
            
        Returns:
            Tuple of (validated_name, validated_date, validated_time, validated_place, validated_language)
            
        Raises:
            ValidationError: If any field is invalid
        """
        validated_name = self.validate_name(name)
        validated_date = self.validate_date(birth_date)
        validated_time = self.validate_time(birth_time)
        validated_place = self.validate_location(birth_place)
        validated_language = self.validate_language(language or "en")

        return (
            validated_name,
            validated_date,
            validated_time,
            validated_place,
            validated_language,
        )

