"""
Zodiac calculator for determining zodiac signs based on birth date.
"""
from datetime import date, datetime
from typing import Dict, Optional

from .constants import (
    ZODIAC_DATE_RANGES,
    ZODIAC_ELEMENTS,
    ZODIAC_MODALITIES,
    ZODIAC_RULING_PLANETS,
    ZODIAC_SYMBOLS,
)
from .traits import ZODIAC_TRAITS, get_trait_summary


class ZodiacCalculator:
    """
    Calculate zodiac signs and retrieve associated traits.
    """

    def __init__(self):
        self.date_ranges = ZODIAC_DATE_RANGES

    def calculate_sign(self, birth_date: date, birth_time: Optional[str] = None) -> str:
        """
        Calculate the sun sign (zodiac sign) based on birth date.
        
        Note: Currently only implements sun sign calculation.
        Future enhancements could include:
        - Moon sign (requires birth time and location)
        - Rising/Ascendant sign (requires exact birth time and location)
        
        Args:
            birth_date: Date of birth
            birth_time: Time of birth in HH:MM format (optional, for future use)
            
        Returns:
            Name of the zodiac sign
            
        Raises:
            ValueError: If unable to determine zodiac sign
        """
        month = birth_date.month
        day = birth_date.day

        for sign, ((start_month, start_day), (end_month, end_day)) in self.date_ranges.items():
            # Handle signs that span across year boundary (Capricorn)
            if start_month > end_month:
                # Capricorn: Dec 22 - Jan 19
                if (month == start_month and day >= start_day) or (
                    month == end_month and day <= end_day
                ):
                    return sign
            else:
                # Normal signs within same year
                if (month == start_month and day >= start_day) or (
                    month == end_month and day <= end_day
                ) or (start_month < month < end_month):
                    return sign

        raise ValueError(f"Unable to determine zodiac sign for date: {birth_date}")

    def get_traits(self, zodiac_sign: str) -> Dict:
        """
        Retrieve personality traits for a given zodiac sign.
        
        Args:
            zodiac_sign: Name of the zodiac sign
            
        Returns:
            Dictionary containing traits, keywords, strengths, etc.
            
        Raises:
            ValueError: If zodiac sign is invalid
        """
        if zodiac_sign not in ZODIAC_TRAITS:
            raise ValueError(f"Invalid zodiac sign: {zodiac_sign}")

        return ZODIAC_TRAITS[zodiac_sign]

    def get_element(self, zodiac_sign: str) -> str:
        """Get the element (Fire, Earth, Air, Water) for a zodiac sign."""
        return ZODIAC_ELEMENTS.get(zodiac_sign, "Unknown")

    def get_modality(self, zodiac_sign: str) -> str:
        """Get the modality (Cardinal, Fixed, Mutable) for a zodiac sign."""
        return ZODIAC_MODALITIES.get(zodiac_sign, "Unknown")

    def get_ruling_planet(self, zodiac_sign: str) -> str:
        """Get the ruling planet for a zodiac sign."""
        return ZODIAC_RULING_PLANETS.get(zodiac_sign, "Unknown")

    def get_symbol(self, zodiac_sign: str) -> str:
        """Get the symbol for a zodiac sign."""
        return ZODIAC_SYMBOLS.get(zodiac_sign, "")

    def get_trait_summary(self, zodiac_sign: str) -> str:
        """
        Get a brief summary of zodiac traits suitable for prompt building.
        
        Args:
            zodiac_sign: Name of the zodiac sign
            
        Returns:
            A formatted string summarizing key traits
        """
        return get_trait_summary(zodiac_sign)

    def get_full_profile(self, birth_date: date) -> Dict:
        """
        Get complete zodiac profile for a birth date.
        
        Args:
            birth_date: Date of birth
            
        Returns:
            Dictionary with sign, traits, element, and other metadata
        """
        sign = self.calculate_sign(birth_date)
        return {
            "sign": sign,
            "symbol": self.get_symbol(sign),
            "element": self.get_element(sign),
            "modality": self.get_modality(sign),
            "ruling_planet": self.get_ruling_planet(sign),
            "traits": self.get_traits(sign),
            "summary": self.get_trait_summary(sign),
        }


# Convenience function for quick zodiac lookup
def get_zodiac_sign(birth_date: date) -> str:
    """
    Quick function to get zodiac sign from a birth date.
    
    Args:
        birth_date: Date of birth
        
    Returns:
        Name of the zodiac sign
    """
    calculator = ZodiacCalculator()
    return calculator.calculate_sign(birth_date)

