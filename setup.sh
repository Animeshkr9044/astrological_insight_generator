#!/bin/bash

# Astrological Insight Generator - Setup & Start Script
# This script sets up the vector store, ingests data, and starts the server

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-false}"

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║   Astrological Insight Generator - Setup & Launch       ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${BLUE}🔹 $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.13+"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version found"
    
    if ! command_exists uv; then
        print_info "uv not found. Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
    print_success "uv package manager ready"
}

# Step 2: Install Dependencies
install_dependencies() {
    print_step "Installing dependencies..."
    
    if [ ! -d ".venv" ]; then
        print_info "Creating virtual environment..."
        uv venv
    fi
    
    print_info "Installing packages (this may take a minute)..."
    uv sync
    print_success "Dependencies installed"
}

# Step 3: Check Environment Configuration
check_environment() {
    print_step "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_info "Creating .env file from template..."
        cat > .env << 'EOF'
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini

# Vector Store Configuration (RAG)
VECTOR_STORE_ENABLED=true
VECTOR_STORE_MODE=memory
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_COLLECTION_NAME=astrological_knowledge

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Optional Settings
TRANSLATION_ENABLED=false
TRANSLATION_MOCK=false
LOG_LEVEL=INFO
EOF
        print_info "Please edit .env file and add your OpenAI API key"
        print_info "Or use LLM_PROVIDER=mock for testing without API key"
        echo ""
    fi
    
    # Check if OpenAI API key is set (if using openai provider)
    if grep -q "LLM_PROVIDER=openai" .env && grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
        print_error "OpenAI API key not configured in .env file"
        print_info "Either:"
        print_info "  1. Add your OpenAI API key to .env file"
        print_info "  2. Change LLM_PROVIDER=mock in .env for testing"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    print_success "Environment configured"
}

# Step 4: Initialize Vector Store & Ingest Data
initialize_vector_store() {
    print_step "Initializing Vector Store & Ingesting Data..."
    
    # Check if corpus file exists
    if [ ! -f "app/data/astrological_corpus.json" ]; then
        print_error "Corpus file not found: app/data/astrological_corpus.json"
        exit 1
    fi
    
    print_info "Running vector store initialization..."
    
    # Test vector store initialization
    uv run python3 << 'PYTHON'
import sys
import logging
from app.core.vector_store import VectorStoreService
from app.config.settings import get_settings

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    print("\n" + "="*60)
    print("VECTOR STORE INITIALIZATION")
    print("="*60 + "\n")
    
    settings = get_settings()
    
    if not settings.vector_store_enabled:
        print("⚠️  Vector store is disabled in settings")
        sys.exit(0)
    
    # Initialize vector store
    service = VectorStoreService(
        enabled=settings.vector_store_enabled,
        mode=settings.vector_store_mode,
        qdrant_url=settings.qdrant_url,
        qdrant_api_key=settings.qdrant_api_key,
        embedding_model=settings.embedding_model,
        collection_name=settings.vector_collection_name,
    )
    
    if not service.is_available():
        print("❌ Vector store initialization failed")
        sys.exit(1)
    
    print("✅ Vector store client initialized")
    print(f"   - Mode: {settings.vector_store_mode}")
    print(f"   - Embedding Model: {settings.embedding_model}")
    
    # Load corpus
    print("\n📚 Loading astrological corpus...")
    success = service.load_corpus()
    
    if success:
        collection_info = service.client.get_collection(settings.vector_collection_name)
        print(f"✅ Corpus loaded successfully")
        print(f"   - Documents: {collection_info.points_count}")
        print(f"   - Vector size: {collection_info.config.params.vectors.size}")
        
        # Test search
        print("\n🔍 Testing semantic search...")
        results = service.search("daily guidance", top_k=2)
        print(f"✅ Search working - Found {len(results)} results")
        
        print("\n" + "="*60)
        print("✅ VECTOR STORE READY")
        print("="*60 + "\n")
    else:
        print("❌ Failed to load corpus")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON
    
    if [ $? -eq 0 ]; then
        print_success "Vector store initialized and data ingested"
    else
        print_error "Vector store initialization failed"
        exit 1
    fi
}

# Step 5: Start Server
start_server() {
    print_step "Starting API server..."
    echo ""
    
    print_info "Server will start at: http://${HOST}:${PORT}"
    print_info "API Documentation: http://${HOST}:${PORT}/docs"
    print_info "Health Check: http://${HOST}:${PORT}/api/v1/health"
    echo ""
    print_info "Press Ctrl+C to stop the server"
    echo ""
    
    # Start server
    if [ "$RELOAD" = "true" ]; then
        uv run python3 run.py --host "$HOST" --port "$PORT" --reload
    else
        uv run python3 run.py --host "$HOST" --port "$PORT"
    fi
}

# Main execution
main() {
    print_header
    
    echo "Starting setup process..."
    echo ""
    
    check_prerequisites
    echo ""
    
    install_dependencies
    echo ""
    
    check_environment
    echo ""
    
    initialize_vector_store
    echo ""
    
    print_success "Setup complete! Starting server..."
    echo ""
    
    start_server
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --reload)
            RELOAD="true"
            shift
            ;;
        --help)
            echo "Usage: ./setup.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST      Host to bind to (default: 0.0.0.0)"
            echo "  --port PORT      Port to bind to (default: 8000)"
            echo "  --reload         Enable auto-reload on code changes"
            echo "  --help           Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  HOST             Host to bind to"
            echo "  PORT             Port to bind to"
            echo "  RELOAD           Enable auto-reload (true/false)"
            echo ""
            echo "Examples:"
            echo "  ./setup.sh"
            echo "  ./setup.sh --reload"
            echo "  ./setup.sh --host localhost --port 8080"
            echo "  HOST=127.0.0.1 PORT=3000 ./setup.sh"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main function
main

