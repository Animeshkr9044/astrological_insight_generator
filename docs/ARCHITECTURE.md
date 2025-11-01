# Architecture Overview

## Project Structure

The Astrological Insight Generator follows a clean, layered architecture pattern designed for maintainability, extensibility, and testability.

## Layer Breakdown

### 1. API Layer (`app/api/`)
**Purpose**: Handle HTTP requests and responses

- `routes.py` - FastAPI endpoints:
  - `POST /api/v1/insight` - Generate personalized insights
  - `POST /api/v1/zodiac` - Get zodiac information
  - `GET /api/v1/health` - Health check
  
- `schemas.py` - Pydantic models for request/response validation
- `dependencies.py` - Dependency injection setup

### 2. Service Layer (`app/services/`)
**Purpose**: Business logic orchestration

- `insight_service.py` - Main orchestrator that coordinates:
  - Input validation
  - Zodiac calculation
  - LLM insight generation
  - Translation
  - Response formatting

- `validator_service.py` - Input validation:
  - Date/time validation
  - Name and location sanitization
  - Language code validation

### 3. Core Layer (`app/core/`)
**Purpose**: Domain-specific logic

#### Zodiac Module (`app/core/zodiac/`)
- `calculator.py` - Zodiac sign calculation
- `traits.py` - Comprehensive trait definitions for all 12 signs
- `constants.py` - Date ranges, elements, modalities, ruling planets

#### LLM Module (`app/core/llm/`)
- `client.py` - LLM client with provider abstraction
- `prompt_builder.py` - Structured prompt generation
- `providers/` - Provider implementations:
  - `base_provider.py` - Abstract base class
  - `openai_provider.py` - OpenAI integration
  - `mock_provider.py` - Mock provider for testing

#### Translation Module (`app/core/translation/`)
- `translator.py` - Translation service (stubbed for future implementation)

### 4. Configuration Layer (`app/config/`)
**Purpose**: Centralized configuration management

- `settings.py` - Pydantic Settings for environment-based configuration

### 5. Data Layer (`app/data/`)
**Purpose**: Static data and templates

- `zodiac_signs.json` - Zodiac date ranges and metadata
- `traits.json` - Detailed trait information
- `prompt_templates.json` - LLM prompt templates

## Design Patterns

### 1. Layered Architecture
- Clear separation of concerns
- Each layer depends only on layers below it
- Easy to test individual layers

### 2. Strategy Pattern (LLM Providers)
- Abstract base class for LLM providers
- Easy to swap implementations
- No vendor lock-in

### 3. Dependency Injection
- Services are injected via FastAPI dependencies
- Improves testability
- Allows for easy mocking

### 4. Factory Pattern
- `get_translator()` factory for translation services
- `get_insight_service()` for service instantiation

## Data Flow

```
User Request → API Layer → Service Layer → Core Layer → Response
                   ↓             ↓              ↓
              Validation   Orchestration   Domain Logic
```

Detailed flow:
1. Request arrives at API endpoint
2. Pydantic validates request schema
3. `InsightService` orchestrates the process:
   - Validates inputs via `ValidatorService`
   - Calculates zodiac via `ZodiacCalculator`
   - Generates insight via `LLMClient`
   - Translates if needed via `TranslationService`
4. Response is formatted and returned

## Key Features

### Extensibility Points

1. **New LLM Providers**: Implement `BaseLLMProvider`
2. **Translation Services**: Extend `TranslationService`
3. **Zodiac Calculations**: Add moon sign/rising sign methods
4. **Caching**: Hook into `InsightService.generate_insight()`

### Error Handling

- Custom `ValidationError` for input validation
- HTTP exceptions in API layer
- Comprehensive logging throughout

### Configuration

Environment-based configuration via `.env`:
- LLM provider selection
- API keys
- Feature flags (translation, debug mode)
- Server settings

## Testing Strategy

The architecture supports multiple testing levels:

1. **Unit Tests**: Test individual components
   - Zodiac calculator
   - Validators
   - Mock provider

2. **Integration Tests**: Test layer interactions
   - Service layer with core layer
   - API endpoints with services

3. **E2E Tests**: Full request-response cycle

## Future Enhancements

### Planned Features
- Redis caching layer
- Real Panchang API integration
- Moon sign and rising sign calculations
- User profile system
- Feedback mechanism
- Vector store for astrological corpus

### Scalability Considerations
- Stateless design enables horizontal scaling
- Provider abstraction allows load distribution
- Caching layer for performance optimization

## Entry Points

### REST API (`app/main.py`)
FastAPI application with:
- Auto-generated OpenAPI documentation
- CORS middleware
- Startup/shutdown events

### CLI (`main.py`)
Command-line interface with:
- Argparse for argument handling
- Colored terminal output
- JSON output option

### Server Runner (`run.py`)
Convenient script to start the uvicorn server

## Technology Stack

- **Framework**: FastAPI
- **Validation**: Pydantic
- **LLM**: OpenAI API
- **Server**: Uvicorn
- **Configuration**: pydantic-settings + python-dotenv

## Code Quality

- Type hints throughout
- Comprehensive docstrings
- Clean separation of concerns
- DRY principles
- SOLID principles

