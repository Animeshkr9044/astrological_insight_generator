"""
CLI for the Astrological Insight Generator.

This provides a command-line interface for generating insights without running the API server.
"""
import argparse
import json
import sys
from datetime import date

from app.services.insight_service import InsightService
from app.services.validator_service import ValidationError
from app.config.settings import get_settings


def setup_parser() -> argparse.ArgumentParser:
    """
    Set up the argument parser for the CLI.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Astrological Insight Generator - Generate personalized daily insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate an insight (using mock provider by default)
  python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India"
  
  # Generate an insight with OpenAI (requires OPENAI_API_KEY in .env)
  python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India" --provider openai
  
  # Get zodiac info only
  python main.py --zodiac-only --birth-date "1995-08-20"
  
  # Generate insight in Hindi (currently returns English if translation not configured)
  python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India" --language hi
        """,
    )

    # Required for insight generation
    parser.add_argument("--name", type=str, help="User's name")
    parser.add_argument("--birth-date", type=str, required=True, help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--birth-time", type=str, help="Birth time (HH:MM in 24-hour format)")
    parser.add_argument("--birth-place", type=str, help="Birth place (city, country)")
    
    # Optional
    parser.add_argument("--language", type=str, default="en", choices=["en", "hi"], help="Output language (default: en)")
    parser.add_argument("--provider", type=str, default=None, choices=["openai", "mock"], help="LLM provider (default: from config)")
    parser.add_argument("--zodiac-only", action="store_true", help="Only show zodiac information, don't generate insight")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    return parser


def print_colored(text: str, color: str = "default"):
    """Print colored text to terminal."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "bold": "\033[1m",
        "end": "\033[0m",
    }
    
    if color in colors:
        print(f"{colors[color]}{text}{colors['end']}")
    else:
        print(text)


def format_output(result: dict, json_output: bool = False):
    """Format and print the result."""
    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "="*60)
        print_colored(f"✨ Zodiac: {result.get('sign') or result.get('zodiac')}", "cyan")
        
        if "insight" in result:
            print_colored(f"\n💫 Daily Insight:", "magenta")
            print(f"{result['insight']}\n")
            
            if "metadata" in result:
                meta = result["metadata"]
                print_colored("📊 Details:", "blue")
                print(f"  Element: {meta.get('element', 'N/A')}")
                print(f"  Ruling Planet: {meta.get('ruling_planet', 'N/A')}")
                print(f"  Modality: {meta.get('modality', 'N/A')}")
        else:
            # Zodiac info only
            print(f"  Symbol: {result.get('symbol', 'N/A')}")
            print(f"  Element: {result.get('element', 'N/A')}")
            print(f"  Ruling Planet: {result.get('ruling_planet', 'N/A')}")
            print(f"  Modality: {result.get('modality', 'N/A')}")
            if "summary" in result:
                print(f"\n{result['summary']}")
        
        print("="*60 + "\n")


def main():
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    # Get settings
    settings = get_settings()
    
    # Override provider if specified
    provider = args.provider or settings.get_effective_provider()
    
    if args.verbose:
        print(f"Using LLM provider: {provider}")
    
    # Create insight service
    try:
        insight_service = InsightService(
            llm_provider=provider,
            api_key=settings.openai_api_key if provider == "openai" else None,
            model=settings.openai_model,
            translation_enabled=settings.translation_enabled,
            translation_mock=settings.translation_mock,
        )
    except Exception as e:
        print_colored(f"Error initializing service: {e}", "red")
        sys.exit(1)

    try:
        # Zodiac info only
        if args.zodiac_only:
            result = insight_service.get_zodiac_info(args.birth_date)
            format_output(result, args.json)
            return

        # Full insight generation
        if not args.name or not args.birth_time or not args.birth_place:
            print_colored("Error: --name, --birth-time, and --birth-place are required for insight generation", "red")
            print("Use --zodiac-only if you only want zodiac information\n")
            parser.print_help()
            sys.exit(1)

        result = insight_service.generate_insight(
            name=args.name,
            birth_date=args.birth_date,
            birth_time=args.birth_time,
            birth_place=args.birth_place,
            language=args.language,
        )
        
        format_output(result, args.json)

    except ValidationError as e:
        print_colored(f"Validation Error: {e}", "red")
        sys.exit(1)
    except Exception as e:
        print_colored(f"Error: {e}", "red")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
