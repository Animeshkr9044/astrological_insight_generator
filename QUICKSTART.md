# 🚀 Quick Start Guide

Get the Astrological Insight Generator running in under 2 minutes!

## ⚡ Super Quick Start

```bash
# 1. Clone and navigate
cd astrological_insight_generator

# 2. Run setup script (does everything!)
./setup.sh

# That's it! Server is running at http://localhost:8000
```

## 📝 What the Setup Script Does

The `./setup.sh` script automatically:

1. ✅ Checks for Python 3.13+ and uv package manager
2. ✅ Installs all dependencies (~32 packages)
3. ✅ Initializes Qdrant vector store (in-memory)
4. ✅ Loads and indexes 31 astrological knowledge documents
5. ✅ Generates 384-dimensional embeddings using sentence-transformers
6. ✅ Starts the FastAPI server

**Total time**: ~1-2 minutes (first run includes model download)

## 🧪 Testing the API

### Option 1: Query Script (Easiest)

```bash
# Generate an insight
./query.sh --name "Ritika" --date "1995-08-20" --time "14:30" --place "Jaipur, India"

# Check health
./query.sh --health

# Get zodiac only
./query.sh --zodiac "1995-08-20"
```

### Option 2: Interactive Docs

Open your browser: **http://localhost:8000/docs**

Try the `/api/v1/insight` endpoint with:

```json
{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India",
  "language": "en"
}
```

### Option 3: curl

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

## ⚙️ Configuration

### Using OpenAI (Recommended)

1. Get your API key from: https://platform.openai.com/account/api-keys

2. Edit `.env` file:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   LLM_PROVIDER=openai
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Restart server: `./setup.sh`

### Using Mock Provider (Free Testing)

Edit `.env`:
```env
LLM_PROVIDER=mock
```

No API key needed! Perfect for development and testing.

## 🔧 Setup Script Options

```bash
# Enable auto-reload for development
./setup.sh --reload

# Custom host and port
./setup.sh --host localhost --port 8080

# Show all options
./setup.sh --help
```

## 📊 What You Get

### Vector Store (RAG)
- 🔍 **31 curated documents** with astrological knowledge
- 🎯 **Semantic search** finds relevant context for each zodiac
- ⚡ **Fast retrieval** (~30-40ms per query)
- 🧠 **Smart prompts** enhanced with retrieved knowledge

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/insight` | POST | Generate personalized insight |
| `/api/v1/zodiac` | POST | Get zodiac info only |
| `/api/v1/health` | GET | Health check with system status |
| `/docs` | GET | Interactive API documentation |

### Response Example

```json
{
  "zodiac": "Leo",
  "insight": "Happy November 1st, Ritika! Your natural charisma shines brighter than usual today...",
  "language": "en",
  "generated_at": "2025-11-01T14:30:00",
  "metadata": {
    "element": "Fire",
    "ruling_planet": "Sun",
    "modality": "Fixed"
  }
}
```

## 🐛 Troubleshooting

### Setup Script Fails

```bash
# Ensure Python 3.13+ is installed
python3 --version

# Install uv manually if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### OpenAI API Error

```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY

# Use mock provider for testing
echo "LLM_PROVIDER=mock" >> .env
```

### Server Not Starting

```bash
# Check if port is already in use
lsof -i :8000

# Use different port
./setup.sh --port 8080
```

### Vector Store Issues

```bash
# Check corpus file exists
ls -l app/data/astrological_corpus.json

# Disable vector store temporarily
echo "VECTOR_STORE_ENABLED=false" >> .env
```

## 📚 Next Steps

- 📖 Read full documentation: [README.md](README.md)
- 🎯 Learn about RAG: [VECTOR_STORE_RAG.md](docs/VECTOR_STORE_RAG.md)
- 🏗️ Understand architecture: [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 🔧 Explore configuration: [settings.py](app/config/settings.py)

## 💡 Pro Tips

1. **Development Mode**: Use `./setup.sh --reload` for hot-reloading
2. **Custom Port**: Set `PORT=3000 ./setup.sh` or edit `.env`
3. **Query Script**: Fastest way to test API without curl/browser
4. **Health Check**: Always check `/api/v1/health` first
5. **Logs**: Watch server logs for RAG context retrieval info

## 🎉 You're Ready!

The Astrological Insight Generator is now running with:
- ✅ RESTful API
- ✅ RAG-enhanced insights
- ✅ Vector search (Qdrant)
- ✅ LLM integration (OpenAI or Mock)
- ✅ Interactive documentation

Start querying and enjoy personalized astrological insights! ✨

