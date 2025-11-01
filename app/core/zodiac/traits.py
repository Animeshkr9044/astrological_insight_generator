"""
Zodiac traits and personality characteristics.
"""
from typing import Dict, List

ZODIAC_TRAITS: Dict[str, Dict[str, any]] = {
    "Aries": {
        "element": "Fire",
        "modality": "Cardinal",
        "ruling_planet": "Mars",
        "positive_traits": [
            "bold",
            "energetic",
            "pioneering",
            "confident",
            "courageous",
            "enthusiastic",
        ],
        "keywords": ["leadership", "courage", "initiative", "action", "independence"],
        "strengths": [
            "Natural leaders",
            "Quick decision makers",
            "Highly motivated",
            "Direct communicators",
        ],
        "challenges": ["Impulsiveness", "Impatience", "Short temper"],
    },
    "Taurus": {
        "element": "Earth",
        "modality": "Fixed",
        "ruling_planet": "Venus",
        "positive_traits": [
            "grounded",
            "reliable",
            "patient",
            "practical",
            "devoted",
            "stable",
        ],
        "keywords": ["stability", "determination", "sensuality", "loyalty", "comfort"],
        "strengths": [
            "Extremely dependable",
            "Patient and calm",
            "Appreciation for beauty",
            "Strong work ethic",
        ],
        "challenges": ["Stubbornness", "Resistance to change", "Possessiveness"],
    },
    "Gemini": {
        "element": "Air",
        "modality": "Mutable",
        "ruling_planet": "Mercury",
        "positive_traits": [
            "versatile",
            "communicative",
            "witty",
            "curious",
            "adaptable",
            "intellectual",
        ],
        "keywords": [
            "communication",
            "duality",
            "intelligence",
            "flexibility",
            "social",
        ],
        "strengths": [
            "Excellent communicators",
            "Quick learners",
            "Highly adaptable",
            "Social butterflies",
        ],
        "challenges": ["Inconsistency", "Restlessness", "Superficiality"],
    },
    "Cancer": {
        "element": "Water",
        "modality": "Cardinal",
        "ruling_planet": "Moon",
        "positive_traits": [
            "nurturing",
            "intuitive",
            "emotional",
            "protective",
            "compassionate",
            "loyal",
        ],
        "keywords": ["emotion", "home", "family", "nurturing", "intuition"],
        "strengths": [
            "Deeply caring",
            "Strong intuition",
            "Protective of loved ones",
            "Emotionally intelligent",
        ],
        "challenges": ["Moodiness", "Over-sensitivity", "Clinginess"],
    },
    "Leo": {
        "element": "Fire",
        "modality": "Fixed",
        "ruling_planet": "Sun",
        "positive_traits": [
            "confident",
            "charismatic",
            "generous",
            "creative",
            "warm-hearted",
            "cheerful",
        ],
        "keywords": ["leadership", "creativity", "passion", "warmth", "drama"],
        "strengths": [
            "Natural born leaders",
            "Extremely generous",
            "Creative and dramatic",
            "Loyal friends",
        ],
        "challenges": ["Arrogance", "Stubbornness", "Self-centeredness"],
    },
    "Virgo": {
        "element": "Earth",
        "modality": "Mutable",
        "ruling_planet": "Mercury",
        "positive_traits": [
            "analytical",
            "practical",
            "diligent",
            "reliable",
            "modest",
            "perfectionist",
        ],
        "keywords": ["service", "health", "precision", "analysis", "improvement"],
        "strengths": [
            "Highly organized",
            "Detail-oriented",
            "Helpful and service-minded",
            "Practical problem solvers",
        ],
        "challenges": ["Over-critical", "Worry", "Perfectionism"],
    },
    "Libra": {
        "element": "Air",
        "modality": "Cardinal",
        "ruling_planet": "Venus",
        "positive_traits": [
            "diplomatic",
            "gracious",
            "fair-minded",
            "social",
            "harmonious",
            "idealistic",
        ],
        "keywords": ["balance", "harmony", "justice", "partnership", "beauty"],
        "strengths": [
            "Excellent mediators",
            "Strong sense of justice",
            "Charming and gracious",
            "Partnership-oriented",
        ],
        "challenges": ["Indecisiveness", "Avoidance of confrontation", "Self-pity"],
    },
    "Scorpio": {
        "element": "Water",
        "modality": "Fixed",
        "ruling_planet": "Pluto",
        "positive_traits": [
            "passionate",
            "resourceful",
            "brave",
            "loyal",
            "ambitious",
            "focused",
        ],
        "keywords": [
            "transformation",
            "intensity",
            "power",
            "mystery",
            "regeneration",
        ],
        "strengths": [
            "Deeply passionate",
            "Excellent strategists",
            "Loyal and trustworthy",
            "Transformative",
        ],
        "challenges": ["Jealousy", "Secretiveness", "Vindictiveness"],
    },
    "Sagittarius": {
        "element": "Fire",
        "modality": "Mutable",
        "ruling_planet": "Jupiter",
        "positive_traits": [
            "optimistic",
            "freedom-loving",
            "philosophical",
            "adventurous",
            "honest",
            "enthusiastic",
        ],
        "keywords": [
            "adventure",
            "philosophy",
            "freedom",
            "travel",
            "higher learning",
        ],
        "strengths": [
            "Optimistic outlook",
            "Love of learning",
            "Adventurous spirit",
            "Honest and direct",
        ],
        "challenges": ["Tactlessness", "Restlessness", "Overconfidence"],
    },
    "Capricorn": {
        "element": "Earth",
        "modality": "Cardinal",
        "ruling_planet": "Saturn",
        "positive_traits": [
            "responsible",
            "disciplined",
            "ambitious",
            "practical",
            "patient",
            "cautious",
        ],
        "keywords": ["ambition", "discipline", "responsibility", "structure", "time"],
        "strengths": [
            "Highly disciplined",
            "Goal-oriented",
            "Responsible and reliable",
            "Patient achievers",
        ],
        "challenges": ["Pessimism", "Stubbornness", "Unforgiving"],
    },
    "Aquarius": {
        "element": "Air",
        "modality": "Fixed",
        "ruling_planet": "Uranus",
        "positive_traits": [
            "progressive",
            "independent",
            "humanitarian",
            "original",
            "intellectual",
            "innovative",
        ],
        "keywords": [
            "innovation",
            "rebellion",
            "community",
            "individuality",
            "future",
        ],
        "strengths": [
            "Visionary thinkers",
            "Humanitarian",
            "Independent",
            "Innovative problem solvers",
        ],
        "challenges": ["Detachment", "Stubbornness", "Unpredictability"],
    },
    "Pisces": {
        "element": "Water",
        "modality": "Mutable",
        "ruling_planet": "Neptune",
        "positive_traits": [
            "compassionate",
            "artistic",
            "intuitive",
            "gentle",
            "wise",
            "musical",
        ],
        "keywords": [
            "spirituality",
            "compassion",
            "imagination",
            "dreams",
            "mysticism",
        ],
        "strengths": [
            "Highly empathetic",
            "Artistic and creative",
            "Intuitive understanding",
            "Selfless and compassionate",
        ],
        "challenges": ["Over-sensitivity", "Escapism", "Victim mentality"],
    },
}


def get_trait_summary(zodiac_sign: str) -> str:
    """
    Get a brief summary of zodiac traits for prompt building.
    
    Args:
        zodiac_sign: Name of the zodiac sign
        
    Returns:
        A formatted string summarizing key traits
    """
    if zodiac_sign not in ZODIAC_TRAITS:
        return ""
    
    traits = ZODIAC_TRAITS[zodiac_sign]
    summary = (
        f"{zodiac_sign} is a {traits['element']} sign ruled by {traits['ruling_planet']}. "
        f"Key traits: {', '.join(traits['positive_traits'][:3])}. "
        f"Keywords: {', '.join(traits['keywords'][:3])}."
    )
    return summary

