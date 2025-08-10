#!/usr/bin/env python3
"""
FastAPI Application for Moroccan Parliament Legislation Scraper
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from moroccan_parliament_scraper import MoroccanParliamentScraper

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

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

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
        with open("dynamic_viewer.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Web viewer not found</h1>", status_code=404)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Configuration endpoints removed for security - config should be managed locally

@app.get("/api/legislation", response_model=DataResponse)
async def get_legislation():
    """Get all legislation data"""
    try:
        data_file = f"data/extracted-data-{datetime.now().year}.json"
        if not os.path.exists(data_file):
            raise HTTPException(status_code=404, detail="No data found. Run scraper first.")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return DataResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.get("/api/legislation/{law_number}")
async def get_legislation_by_number(law_number: str):
    """Get specific legislation by law number"""
    try:
        data_file = f"data/extracted-data-{datetime.now().year}.json"
        if not os.path.exists(data_file):
            raise HTTPException(status_code=404, detail="No data found. Run scraper first.")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data.get('data', []):
            if item.get('law_number') == law_number:
                return item
        
        raise HTTPException(status_code=404, detail=f"Law {law_number} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

@app.get("/api/legislation/stage/{stage}")
async def get_legislation_by_stage(stage: str):
    """Get legislation by stage (Lecture 1, Lecture 2)"""
    try:
        data_file = f"data/extracted-data-{datetime.now().year}.json"
        if not os.path.exists(data_file):
            raise HTTPException(status_code=404, detail="No data found. Run scraper first.")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        filtered_data = [
            item for item in data.get('data', [])
            if item.get('stage', '').lower() == stage.lower()
        ]
        
        return {
            "stage": stage,
            "count": len(filtered_data),
            "data": filtered_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")



@app.post("/api/scrape", response_model=ScrapingResponse)
async def start_scraping(request: ScrapingRequest, background_tasks: BackgroundTasks):
    """Start scraping process"""
    try:
        # Create scraper instance
        scraper = MoroccanParliamentScraper(
            force_rescrape=request.force_rescrape
        )
        
        # Run scraper
        success = scraper.run(max_pages=request.max_pages)
        
        if success:
            # Get updated data count
            data_file = f"data/extracted-data-{datetime.now().year}.json"
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data_count = len(data.get('data', []))
            else:
                data_count = 0
            
            return ScrapingResponse(
                success=True,
                message="Scraping completed successfully",
                data_count=data_count,
                timestamp=datetime.now().isoformat()
            )
        else:
            return ScrapingResponse(
                success=False,
                message="Scraping failed or no new data found",
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/api/stats")
async def get_statistics():
    """Get scraping statistics"""
    try:
        data_file = f"data/extracted-data-{datetime.now().year}.json"
        if not os.path.exists(data_file):
            return {
                "status": "no_data",
                "message": "No data found. Run scraper first."
            }
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Calculate statistics
        total_items = len(data.get('data', []))
        stages = {}
        commissions = {}
        
        for item in data.get('data', []):
            stage = item.get('stage', 'Unknown')
            commission = item.get('commission', 'Unknown')
            
            stages[stage] = stages.get(stage, 0) + 1
            commissions[commission] = commissions.get(commission, 0) + 1
        
        return {
            "total_items": total_items,
            "stages": stages,
            "commissions": commissions,
            "last_scraped": data.get('scraped_at'),
            "current_year": data.get('current_year')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@app.get("/api/data/{filename}")
async def get_data_file(filename: str):
    """Get data files directly"""
    data_dir = Path("data")
    file_path = data_dir / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
