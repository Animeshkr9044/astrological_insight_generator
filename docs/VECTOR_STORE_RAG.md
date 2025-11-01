# Vector Store & RAG Implementation

## Overview

This document describes the **Retrieval-Augmented Generation (RAG)** implementation using **Qdrant** vector database and **sentence-transformers** for embedding generation.

## Architecture

### Components

1. **Vector Store Service** (`app/core/vector_store/vector_service.py`)
   - Manages Qdrant client (in-memory or server mode)
   - Generates embeddings using sentence-transformers
   - Performs semantic search over astrological knowledge corpus

2. **Astrological Corpus** (`app/data/astrological_corpus.json`)
   - 31 curated documents covering:
     - Zodiac-specific traits and daily guidance
     - Elemental wisdom (Fire, Earth, Air, Water)
     - Modality insights (Cardinal, Fixed, Mutable)

3. **RAG Integration** (in `InsightService`)
   - Retrieves relevant context before LLM generation
   - Enhances prompts with retrieved knowledge
   - Improves personalization and accuracy

## Configuration

### Environment Variables

Add to your `.env` file:

```env
# Vector Store Configuration
VECTOR_STORE_ENABLED=true
VECTOR_STORE_MODE=memory  # or "server" for remote Qdrant
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_COLLECTION_NAME=astrological_knowledge

# For server mode (optional)
# QDRANT_URL=http://localhost:6333
# QDRANT_API_KEY=your_api_key
```

### Settings

All settings are configurable in `app/config/settings.py`:

```python
vector_store_enabled: bool = True
vector_store_mode: str = "memory"  # "memory" or "server"
qdrant_url: Optional[str] = None
qdrant_api_key: Optional[str] = None
embedding_model: str = "all-MiniLM-L6-v2"
vector_collection_name: str = "astrological_knowledge"
```

## Usage

### Automatic Integration

The vector store is **automatically initialized** when the API starts. No additional setup required!

```python
# The service automatically:
# 1. Loads the embedding model
# 2. Initializes Qdrant client
# 3. Loads the astrological corpus
# 4. Creates embeddings for all documents
# 5. Stores vectors in Qdrant
```

### API Endpoint

The `/api/v1/insight` endpoint automatically uses RAG when vector store is enabled:

```bash
curl -X POST http://localhost:8000/api/v1/insight \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "language": "en"
  }'
```

### Health Check

Check if vector store is available:

```bash
curl http://localhost:8000/api/v1/health
```

Response includes:

```json
{
  "status": "healthy",
  "llm_provider": "openai",
  "llm_available": true,
  "translation_enabled": false,
  "supported_languages": ["en", "hi"],
  "vector_store_enabled": true
}
```

## How RAG Works

### Retrieval Process

1. **User makes request** with birth details
2. **System calculates zodiac sign** (e.g., "Leo")
3. **Vector store retrieves** relevant knowledge:
   ```python
   query = f"Daily guidance and personality insights for {zodiac_sign}"
   results = vector_store.search(query, zodiac=zodiac_sign, top_k=3)
   ```
4. **Context is formatted** and added to LLM prompt
5. **LLM generates** personalized insight using retrieved context

### Search Example

For a Leo user, the system retrieves:

```
Relevant Astrological Knowledge:

1. Leo individuals radiate confidence and charisma. They have a 
   natural flair for drama and creativity...

2. Leo's innate leadership shines brightest when inspiring others. 
   Your creative energy and enthusiasm are contagious...
```

This context is then provided to the LLM to generate a more accurate and personalized insight.

## Embedding Model

We use **all-MiniLM-L6-v2** from sentence-transformers:

- **Size**: ~80MB
- **Dimensions**: 384
- **Speed**: Fast inference
- **Quality**: Good for semantic search
- **Language**: English

### Alternative Models

You can change the embedding model:

```env
EMBEDDING_MODEL=paraphrase-MiniLM-L6-v2  # Another good option
# EMBEDDING_MODEL=all-mpnet-base-v2       # Higher quality, slower
```

## Vector Store Modes

### In-Memory Mode (Default)

- **Pros**: Fast, no setup required, great for development
- **Cons**: Data lost on restart, limited by RAM
- **Use case**: Development, testing, small deployments

```env
VECTOR_STORE_MODE=memory
```

### Server Mode

- **Pros**: Persistent, scalable, production-ready
- **Cons**: Requires running Qdrant server
- **Use case**: Production deployments

#### Setup Qdrant Server

Using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Then configure:

```env
VECTOR_STORE_MODE=server
QDRANT_URL=http://localhost:6333
```

## Corpus Management

### Current Corpus

Located at `app/data/astrological_corpus.json`:

- 31 documents
- Covers all 12 zodiac signs
- Includes elemental and modality wisdom
- Categorized by type (personality, daily_guidance, etc.)

### Adding New Documents

Edit `astrological_corpus.json`:

```json
{
  "corpus": [
    {
      "id": "unique_id",
      "zodiac": "Leo",
      "category": "daily_guidance",
      "text": "Your knowledge text here..."
    }
  ]
}
```

Restart the server to reload the corpus.

### Corpus Structure

```json
{
  "id": "doc_identifier",
  "zodiac": "ZodiacSign | Fire Signs | etc.",
  "category": "personality | daily_guidance | elemental_wisdom | modality_wisdom",
  "text": "The knowledge content..."
}
```

## Performance

### Benchmarks (M1 Mac)

- **Initial load**: ~3-4 seconds
  - Loading embedding model: ~3s
  - Generating embeddings for 31 docs: ~0.1s
  - Creating Qdrant collection: <0.1s

- **Search query**: ~30-40ms
  - Embedding generation: ~20ms
  - Vector search: ~10ms

- **Memory usage**: ~200MB
  - Embedding model: ~80MB
  - Qdrant (in-memory): ~10MB
  - Vectors (31 docs × 384 dims): <1MB

## Troubleshooting

### Vector Store Not Loading

Check logs for:
```
INFO - Vector store service initialized successfully
INFO - Successfully loaded 31 documents into vector store
```

If not appearing:
- Ensure dependencies installed: `uv sync`
- Check `VECTOR_STORE_ENABLED=true` in `.env`
- Verify corpus file exists at `app/data/astrological_corpus.json`

### No Results from Search

- Lower the `score_threshold` (default 0.5)
- Check zodiac sign spelling
- Verify corpus contains documents for that zodiac

### Server Mode Connection Failed

- Ensure Qdrant server is running: `docker ps`
- Check URL: `curl http://localhost:6333/health`
- Verify firewall settings

## API Integration

### Python Client Example

```python
from app.core.vector_store import VectorStoreService

# Initialize
service = VectorStoreService(
    enabled=True,
    mode="memory",
    embedding_model="all-MiniLM-L6-v2",
)

# Load corpus
service.load_corpus()

# Search
results = service.search(
    query="leadership qualities",
    zodiac="Leo",
    top_k=3,
    score_threshold=0.5,
)

# Get context for insight
context = service.get_context_for_insight(
    zodiac="Leo",
    name="Ritika",
    birth_place="Jaipur",
    top_k=3,
)
```

## Future Enhancements

Potential improvements:

1. **User Feedback Loop**: Store user ratings to improve retrieval
2. **Personalized Corpus**: Add user-specific documents over time
3. **Multi-lingual Support**: Add Hindi corpus documents
4. **Temporal Relevance**: Weight recent documents higher
5. **Hybrid Search**: Combine keyword + semantic search
6. **Query Expansion**: Generate multiple queries for better coverage

## References

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Sentence Transformers](https://www.sbert.net/)
- [all-MiniLM-L6-v2 Model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

