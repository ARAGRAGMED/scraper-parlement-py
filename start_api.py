#!/usr/bin/env python3
"""
Startup script for the FastAPI application
"""

import uvicorn
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("🚀 Starting Moroccan Parliament Legislation API...")
    print("=" * 50)
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("🌐 Web Viewer: http://localhost:8000/")
    print("🔍 Health Check: http://localhost:8000/api/health")
    print("=" * 50)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
