#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web viewer"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Moroccan Parliament API</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .endpoint h3 { margin: 0 0 10px 0; color: #34495e; }
            .endpoint p { margin: 5px 0; color: #7f8c8d; }
            .status { background: #27ae60; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Moroccan Parliament Legislation API</h1>
            <p style="text-align: center; color: #7f8c8d;">API is running successfully on Vercel!</p>
            
            <div class="endpoint">
                <h3>📚 API Documentation</h3>
                <p><a href="/docs">Interactive API Docs (Swagger UI)</a></p>
                <p><a href="/redoc">ReDoc Documentation</a></p>
            </div>
            
            <div class="endpoint">
                <h3>🔍 Health Check</h3>
                <p><a href="/api/health">/api/health</a></p>
                <span class="status">Live</span>
            </div>
            
            <div class="endpoint">
                <h3>📊 Legislation Data</h3>
                <p><a href="/api/legislation">/api/legislation</a></p>
                <p><a href="/api/stats">/api/stats</a></p>
            </div>
            
            <div class="endpoint">
                <h3>🔧 Development</h3>
                <p>This is a serverless deployment on Vercel</p>
                <p>For full functionality, run locally with: <code>python3 api.py</code></p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "platform": "vercel",
        "message": "API is running successfully on Vercel"
    }

@app.get("/api/legislation", response_model=DataResponse)
async def get_legislation():
    """Get all legislation data"""
    # For Vercel, return sample data since file storage isn't persistent
    sample_data = {
        "current_year": str(datetime.now().year),
        "total_items": 0,
        "scraped_at": "Vercel deployment - no persistent storage",
        "data": []
    }
    
    return DataResponse(**sample_data)

@app.get("/api/legislation/{law_number}")
async def get_legislation_by_number(law_number: str):
    """Get specific legislation by law number"""
    return {
        "law_number": law_number,
        "title": "Sample Law Title",
        "stage": "Lecture 1",
        "commission": "Sample Commission",
        "url": "https://example.com",
        "pdf_url": None,
        "note": "This is sample data from Vercel deployment"
    }

@app.get("/api/legislation/stage/{stage}")
async def get_legislation_by_stage(stage: str):
    """Get legislation by stage (Lecture 1, Lecture 2)"""
    return {
        "stage": stage,
        "count": 0,
        "data": [],
        "note": "Sample data from Vercel deployment - no persistent storage"
    }

@app.post("/api/scrape", response_model=ScrapingResponse)
async def start_scraping(request: ScrapingRequest):
    """Start scraping process"""
    return ScrapingResponse(
        success=True,
        message="Scraping endpoint called successfully. Note: Vercel has no persistent storage for data files.",
        data_count=0,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/stats")
async def get_statistics():
    """Get scraping statistics"""
    return {
        "total_items": 0,
        "stages": {},
        "commissions": {},
        "last_scraped": "Vercel deployment - no persistent storage",
        "current_year": str(datetime.now().year),
        "note": "This is sample data from Vercel deployment"
    }

@app.get("/api/data/{filename}")
async def get_data_file(filename: str):
    """Get data files directly"""
    return {
        "filename": filename,
        "note": "Vercel has no persistent file storage. This is sample data.",
        "timestamp": datetime.now().isoformat()
    }

# Vercel serverless function handler - this is required for Vercel to work
def handler(request, context):
    """Vercel serverless function entry point"""
    from mangum import Mangum
    
    # Create Mangum handler for AWS Lambda/Vercel
    asgi_handler = Mangum(app)
    return asgi_handler(request, context)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
