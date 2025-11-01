"""
Prompt builder for generating LLM prompts.
"""
from datetime import date
from typing import Dict, Optional


class PromptBuilder:
    """
    Build structured prompts for LLM insight generation.
    """

    def build_insight_prompt(
        self,
        name: str,
        zodiac_sign: str,
        traits: Dict,
        birth_date: date,
        current_date: Optional[date] = None,
        additional_context: Optional[str] = None,
    ) -> str:
        """
        Create a structured prompt for generating personalized daily insights.
        
        Args:
            name: User's name
            zodiac_sign: Zodiac sign
            traits: Dictionary of zodiac traits
            birth_date: User's birth date
            current_date: Current date (defaults to today)
            additional_context: Additional context from vector store (RAG)
            
        Returns:
            Formatted prompt string
        """
        if current_date is None:
            current_date = date.today()

        # Extract key traits for the prompt
        positive_traits = ", ".join(traits.get("positive_traits", [])[:3])
        keywords = ", ".join(traits.get("keywords", [])[:3])
        element = traits.get("element", "")
        ruling_planet = traits.get("ruling_planet", "")

        prompt = f"""Generate a personalized daily astrological insight for {name}, a {zodiac_sign}.

Zodiac Information:
- Sign: {zodiac_sign}
- Element: {element}
- Ruling Planet: {ruling_planet}
- Key Traits: {positive_traits}
- Keywords: {keywords}

Date: {current_date.strftime('%B %d, %Y')}"""

        # Add vector store context if available
        if additional_context:
            prompt += f"\n\n{additional_context}"

        prompt += f"""

Guidelines:
1. Create a personalized, encouraging message (30-50 words)
2. Reference {zodiac_sign} characteristics naturally
3. Be positive and actionable
4. Use a warm, conversational tone
5. Focus on opportunities and guidance for the day
6. Avoid generic predictions

Generate the insight:"""

        return prompt

    def build_simple_prompt(self, zodiac_sign: str, trait_summary: str) -> str:
        """
        Create a simpler prompt for quick insight generation.
        
        Args:
            zodiac_sign: Zodiac sign
            trait_summary: Brief summary of traits
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""As an expert astrologer, generate a brief daily insight for a {zodiac_sign}.

Context: {trait_summary}

Create a personalized, encouraging message (30-50 words) that:
- Reflects {zodiac_sign} characteristics
- Provides actionable guidance for today
- Maintains a warm, supportive tone

Insight:"""

        return prompt

    def build_custom_prompt(
        self,
        zodiac_sign: str,
        context: Dict,
        template: Optional[str] = None,
    ) -> str:
        """
        Build a custom prompt using a template and context.
        
        Args:
            zodiac_sign: Zodiac sign
            context: Dictionary of context variables
            template: Optional custom template
            
        Returns:
            Formatted prompt string
        """
        if template is None:
            template = """Generate a daily astrological insight for a {zodiac_sign}.

Context:
{context_str}

Provide a personalized, encouraging message (30-50 words)."""

        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
        
        prompt = template.format(
            zodiac_sign=zodiac_sign,
            context_str=context_str,
            **context
        )

        return prompt

