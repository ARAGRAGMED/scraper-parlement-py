#!/usr/bin/env python3
"""
Main FastAPI application for Moroccan Parliament Legislation API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

# Import routers with flexible imports for different environments
try:
    # Try package imports first (for Vercel)
    from api.routes import legislation, commissions, scraping, status
except ImportError:
    try:
        # Try relative imports (for local development)
        from routes import legislation, commissions, scraping, status
    except ImportError:
        # Fallback to direct imports
        import sys
        sys.path.append(os.path.dirname(__file__))
        from routes import legislation, commissions, scraping, status

# Create FastAPI app
app = FastAPI(
    title="Moroccan Parliament Scraper API",
    description="API for scraping Moroccan Parliament legislation data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(legislation.router, prefix="/api")
app.include_router(commissions.router, prefix="/api")
app.include_router(scraping.router, prefix="/api")
app.include_router(status.router, prefix="/api")

# Root endpoint for the main page (serves the frontend directly)
@app.get("/")
async def main_page():
    """Main page endpoint - serves the frontend directly"""
    # Read the HTML file from static directory
    static_dir = Path(__file__).parent / "static"
    html_file = static_dir / "index.html"
    
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)
