#!/usr/bin/env python3
"""
Script to run the FastAPI server.

Usage:
    python run.py
    
Or with custom settings:
    python run.py --host 0.0.0.0 --port 8000 --reload
"""
import argparse
import uvicorn

from app.config.settings import get_settings


def main():
    """Run the FastAPI server."""
    parser = argparse.ArgumentParser(description="Run the Astrological Insight Generator API server")
    
    settings = get_settings()
    
    parser.add_argument("--host", type=str, default=settings.host, help=f"Host to bind to (default: {settings.host})")
    parser.add_argument("--port", type=int, default=settings.port, help=f"Port to bind to (default: {settings.port})")
    parser.add_argument("--reload", action="store_true", default=settings.debug, help="Enable auto-reload on code changes")
    parser.add_argument("--log-level", type=str, default=settings.log_level.lower(), help="Log level")
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   Astrological Insight Generator API                     ║
╚══════════════════════════════════════════════════════════╝

🚀 Starting server...
📍 Host: {args.host}
🔌 Port: {args.port}
📚 Docs: http://{args.host}:{args.port}/docs
🔄 Reload: {args.reload}

Press Ctrl+C to stop
""")
    
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    main()

