# ✨ Astrological Insight Generator

Generate personalized daily astrological insights using zodiac logic and LLM-based language generation.

## 📋 Overview

This service takes a user's birth details (name, date, time, and location) and returns personalized daily astrological insights. It combines:
- **Zodiac calculation** based on birth date
- **Trait analysis** from comprehensive zodiac databases
- **LLM-based generation** for natural, personalized insights
- **Multilingual support** (English and Hindi)

## 🏗️ Architecture

The project follows a clean, layered architecture:

```
├── app/
│   ├── api/              # FastAPI routes, schemas, dependencies
│   ├── services/         # Business logic (InsightService, Validator)
│   ├── core/            
│   │   ├── zodiac/      # Zodiac calculation and traits
│   │   ├── llm/         # LLM client and providers
│   │   └── translation/ # Translation services
│   ├── data/            # JSON data files
│   └── config/          # Settings and configuration
├── tests/               # Test suite
├── main.py             # CLI interface
└── run.py              # FastAPI server runner
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip or uv package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd astrological_insight_generator
```

2. **Install dependencies**

Using pip:
```bash
pip install -e .
```

Using uv:
```bash
uv pip install -e .
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
# Required for OpenAI provider
OPENAI_API_KEY=your_openai_api_key_here

# Optional settings
LLM_PROVIDER=openai  # or "mock" for testing
DEBUG=true
```

**Note**: The mock provider works without any API keys and is great for testing!

### Running the Application

#### Option 1: REST API Server

Start the FastAPI server:
```bash
python run.py
```

Or with custom settings:
```bash
python run.py --host 0.0.0.0 --port 8000 --reload
```

Access the API:
- **Interactive Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/api/v1

#### Option 2: CLI

Generate insights directly from the command line:

```bash
# Using mock provider (no API key needed)
python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India"

# Using OpenAI provider
python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India" --provider openai

# Get zodiac info only
python main.py --zodiac-only --birth-date "1995-08-20"

# JSON output
python main.py --name "Ritika" --birth-date "1995-08-20" --birth-time "14:30" --birth-place "Jaipur, India" --json
```

## 📡 API Usage

### Generate Insight

**Endpoint**: `POST /api/v1/insight`

**Request**:
```json
{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India",
  "language": "en"
}
```

**Response**:
```json
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
```

### Get Zodiac Information

**Endpoint**: `POST /api/v1/zodiac`

**Request**:
```json
{
  "birth_date": "1995-08-20"
}
```

**Response**:
```json
{
  "sign": "Leo",
  "symbol": "♌",
  "element": "Fire",
  "modality": "Fixed",
  "ruling_planet": "Sun",
  "summary": "Leo is a Fire sign ruled by Sun. Key traits: confident, charismatic, generous."
}
```

### Health Check

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "llm_provider": "mock",
  "llm_available": true,
  "translation_enabled": false,
  "supported_languages": ["en", "hi"]
}
```

## 🔧 Configuration

Configuration is managed through environment variables or a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Astrological Insight Generator |
| `DEBUG` | Debug mode | false |
| `LLM_PROVIDER` | LLM provider (`openai`, `mock`) | openai |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `OPENAI_MODEL` | OpenAI model name | gpt-3.5-turbo |
| `TRANSLATION_ENABLED` | Enable translation | false |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

## 🧩 Key Components

### 1. Zodiac Calculator
- Calculates sun sign based on birth date
- Provides comprehensive trait information
- Extensible for moon sign and rising sign calculations

### 2. LLM Service
- Provider-agnostic architecture
- Currently supports:
  - OpenAI (GPT-3.5-turbo, GPT-4)
  - Mock provider (for testing)
- Easy to add new providers (HuggingFace, Anthropic, etc.)

### 3. Prompt Builder
- Crafts structured prompts for LLM
- Templates for different styles
- Contextual information injection

### 4. Translation Service
- Stubbed for future implementation
- Supports English and Hindi
- Ready for Google Translate or IndicTrans2 integration

### 5. Validation Service
- Comprehensive input validation
- Date, time, and name validation
- Clear error messages

## 🎯 Design Decisions

### Layered Architecture
- **API Layer**: HTTP interface and request handling
- **Service Layer**: Business logic orchestration
- **Core Layer**: Domain-specific logic (zodiac, LLM, translation)
- **Config Layer**: Centralized configuration management

### Provider Pattern for LLMs
- Abstract base class for easy provider swapping
- No vendor lock-in
- Simple to add new providers

### Mock Provider for Development
- Test without API costs
- Fast development and testing
- No external dependencies

### Pydantic for Validation
- Type-safe request/response models
- Automatic API documentation
- Runtime validation

## 🔮 Future Enhancements

- [ ] Moon sign and rising sign calculations
- [ ] Real Panchang API integration
- [ ] Caching layer (Redis)
- [ ] User profile system
- [ ] Feedback and rating system
- [ ] Vector store for astrological text corpus
- [ ] Full Hindi translation support
- [ ] Additional LLM providers (HuggingFace, Anthropic)
- [ ] Comprehensive test suite

## 📚 Project Structure

```
astrological_insight_generator/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API endpoints
│   │   ├── schemas.py             # Pydantic models
│   │   └── dependencies.py        # Dependency injection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── insight_service.py     # Main orchestrator
│   │   └── validator_service.py   # Input validation
│   ├── core/
│   │   ├── __init__.py
│   │   ├── zodiac/
│   │   │   ├── __init__.py
│   │   │   ├── calculator.py      # Zodiac logic
│   │   │   ├── traits.py          # Trait definitions
│   │   │   └── constants.py       # Date ranges, etc.
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── client.py          # LLM client
│   │   │   ├── prompt_builder.py  # Prompt engineering
│   │   │   └── providers/
│   │   │       ├── __init__.py
│   │   │       ├── base_provider.py
│   │   │       ├── openai_provider.py
│   │   │       └── mock_provider.py
│   │   └── translation/
│   │       ├── __init__.py
│   │       └── translator.py      # Translation service
│   ├── data/
│   │   ├── zodiac_signs.json      # Zodiac data
│   │   ├── traits.json            # Trait data
│   │   └── prompt_templates.json  # Prompt templates
│   └── config/
│       ├── __init__.py
│       └── settings.py            # Configuration
├── tests/
│   └── __init__.py
├── main.py                        # CLI interface
├── run.py                         # Server runner
├── pyproject.toml                 # Dependencies
├── .gitignore
└── README.md
```

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📝 Examples

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/insight" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "language": "en"
  }'
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/insight",
    json={
        "name": "Ritika",
        "birth_date": "1995-08-20",
        "birth_time": "14:30",
        "birth_place": "Jaipur, India",
        "language": "en"
    }
)

result = response.json()
print(f"Zodiac: {result['zodiac']}")
print(f"Insight: {result['insight']}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Author

Built as part of a machine learning coding assignment.

---

**Note**: This is a demonstration project. For production use, ensure proper API key management, add comprehensive tests, implement caching, and handle edge cases appropriately.
 