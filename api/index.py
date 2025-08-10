#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation Scraper
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your scraper
try:
    from moroccan_parliament_scraper import MoroccanParliamentScraper
except ImportError:
    # Fallback for Vercel environment
    MoroccanParliamentScraper = None

# Create FastAPI app
app = FastAPI(
    title="Moroccan Parliament Legislation API",
    description="REST API for scraping and accessing Moroccan Parliament legislation data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ScrapingRequest(BaseModel):
    force_rescrape: bool = False
    max_pages: Optional[int] = None

class ScrapingResponse(BaseModel):
    success: bool
    message: str
    data_count: Optional[int] = None
    timestamp: str

class LegislationItem(BaseModel):
    law_number: str
    title: str
    stage: str
    commission: str
    url: str
    pdf_url: Optional[str] = None

class DataResponse(BaseModel):
    current_year: str
    total_items: int
    scraped_at: str
    data: List[Dict[str, Any]]

# Global variables
scraper_instance: Optional[MoroccanParliamentScraper] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web viewer"""
    try:
        # Try multiple possible paths for Vercel deployment
        html_paths = [
            "../dynamic_viewer.html",
            "./dynamic_viewer.html",
            "/tmp/dynamic_viewer.html"
        ]
        
        for html_path in html_paths:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read())
        
        # Fallback: return HTML content directly
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Moroccan Parliament API</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>🚀 Moroccan Parliament Legislation API</h1>
            <p>API is running successfully on Vercel!</p>
            <ul>
                <li><a href="/docs">📚 API Documentation</a></li>
                <li><a href="/api/health">🔍 Health Check</a></li>
                <li><a href="/api/legislation">📊 Legislation Data</a></li>
            </ul>
        </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading web viewer</h1><p>{str(e)}</p>", status_code=500)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "platform": "vercel"
    }

@app.get("/api/legislation", response_model=DataResponse)
async def get_legislation():
    """Get all legislation data"""
    try:
        # For Vercel, we'll return sample data since file storage isn't persistent
        sample_data = {
            "current_year": str(datetime.now().year),
            "total_items": 0,
            "scraped_at": "Vercel deployment - no persistent storage",
            "data": []
        }
        
        # Try to load from data directory if it exists
        current_year = datetime.now().year
        data_paths = [
            f"../data/extracted-data-{current_year}.json",
            f"./data/extracted-data-{current_year}.json",
            f"/tmp/data/extracted-data-{current_year}.json"
        ]
        
        for path in data_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return DataResponse(**data)
        
        # Return sample data if no file found
        return DataResponse(**sample_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.get("/api/legislation/{law_number}")
async def get_legislation_by_number(law_number: str):
    """Get specific legislation by law number"""
    try:
        # For Vercel, return sample data
        return {
            "law_number": law_number,
            "title": "Sample Law Title",
            "stage": "Lecture 1",
            "commission": "Sample Commission",
            "url": "https://example.com",
            "pdf_url": None,
            "note": "This is sample data from Vercel deployment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.get("/api/legislation/stage/{stage}")
async def get_legislation_by_stage(stage: str):
    """Get legislation by stage (Lecture 1, Lecture 2)"""
    try:
        # For Vercel, return sample data
        return {
            "stage": stage,
            "count": 0,
            "data": [],
            "note": "Sample data from Vercel deployment - no persistent storage"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.post("/api/scrape", response_model=ScrapingResponse)
async def start_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """Start scraping process"""
    try:
        # For Vercel, return success message but note limitations
        return ScrapingResponse(
            success=True,
            message="Scraping endpoint called successfully. Note: Vercel has no persistent storage for data files.",
            data_count=0,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/api/stats")
async def get_statistics():
    """Get scraping statistics"""
    try:
        # For Vercel, return sample statistics
        return {
            "total_items": 0,
            "stages": {},
            "commissions": {},
            "last_scraped": "Vercel deployment - no persistent storage",
            "current_year": str(datetime.now().year),
            "note": "This is sample data from Vercel deployment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@app.get("/api/data/{filename}")
async def get_data_file(filename: str):
    """Get data files directly"""
    try:
        # For Vercel, return sample data
        return {
            "filename": filename,
            "note": "Vercel has no persistent file storage. This is sample data.",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file: {str(e)}")

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function entry point"""
    from mangum import Mangum
    
    # Create Mangum handler for AWS Lambda/Vercel
    asgi_handler = Mangum(app)
    return asgi_handler(request, context)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
