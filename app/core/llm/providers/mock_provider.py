"""
Mock LLM provider for testing without API calls.
"""
from typing import Optional
import random

from .base_provider import BaseLLMProvider


class MockProvider(BaseLLMProvider):
    """
    Mock provider that generates fake insights for testing.
    Useful for development and testing without incurring API costs.
    """

    def __init__(self):
        """Initialize mock provider with template responses."""
        self.templates = [
            "Your {trait} nature will guide you through today's challenges. {advice}",
            "As a {sign}, today is perfect for {action}. Trust your {trait} instincts.",
            "The cosmic energies favor your {trait} approach today. {advice}",
            "Your {sign} wisdom shines bright today. Focus on {focus_area}.",
            "Today calls for your natural {trait} abilities. {advice}",
        ]

        self.traits = [
            "bold",
            "grounded",
            "versatile",
            "intuitive",
            "confident",
            "analytical",
            "diplomatic",
            "passionate",
            "optimistic",
            "disciplined",
            "innovative",
            "compassionate",
        ]

        self.advice = [
            "Embrace spontaneity and avoid overthinking.",
            "Take time for self-reflection and planning.",
            "Connect with others who inspire you.",
            "Focus on what truly matters to you.",
            "Trust your instincts and move forward confidently.",
            "Balance action with thoughtful consideration.",
        ]

        self.actions = [
            "pursuing creative projects",
            "strengthening relationships",
            "taking calculated risks",
            "organizing your goals",
            "exploring new ideas",
            "nurturing your well-being",
        ]

        self.focus_areas = [
            "personal growth",
            "professional development",
            "meaningful connections",
            "self-care",
            "creative expression",
            "building stability",
        ]

    def generate(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Generate a mock insight based on the prompt.
        
        Args:
            prompt: The input prompt (analyzed for context)
            max_tokens: Not used in mock provider
            
        Returns:
            A randomly generated insight
        """
        # Extract zodiac sign from prompt if present
        sign = "unknown"
        for word in prompt.split():
            if word.strip(",.!?").capitalize() in [
                "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
            ]:
                sign = word.strip(",.!?").capitalize()
                break

        template = random.choice(self.templates)
        insight = template.format(
            trait=random.choice(self.traits),
            sign=sign,
            advice=random.choice(self.advice),
            action=random.choice(self.actions),
            focus_area=random.choice(self.focus_areas),
        )

        return insight

    def is_available(self) -> bool:
        """
        Mock provider is always available.
        
        Returns:
            True
        """
        return True

