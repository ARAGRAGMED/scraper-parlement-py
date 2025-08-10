#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from moroccan_parliament_scraper.core.legislation_scraper import MoroccanParliamentScraper

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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Moroccan Parliament Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/": "This info",
            "/health": "Health check",
            "/config": "Get current scraper configuration",
            "/scrape": "Start scraping (GET for current year, POST for custom)",
            "/status": "Get scraping status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "moroccan-parliament-scraper"}

@app.get("/config")
async def get_config():
    """Get current scraper configuration"""
    try:
        # Note: On Vercel, we can't read local files, so return default config
        return {
            "message": "Configuration endpoint",
            "note": "On Vercel, configuration is limited due to serverless constraints",
            "default_config": {
                "scraper_settings": {
                    "force_rescrape": False,
                    "enable_logs": False,
                    "save_format": "json"
                },
                "request_settings": {
                    "timeout": 30,
                    "retry_attempts": 3,
                    "delay_between_requests": 2
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting config: {str(e)}")

@app.get("/scrape")
async def scrape_current_year():
    """Scrape current year legislation"""
    try:
        # Initialize scraper with minimal settings for Vercel
        scraper = MoroccanParliamentScraper(
            force_rescrape=False,
            config_file=None  # Don't try to read config file on Vercel
        )
        
        # Get current year info
        current_year = scraper.get_current_legislative_year()
        
        return {
            "message": "Scraping started for current year",
            "current_year": current_year,
            "note": "On Vercel, full scraping is limited due to timeout constraints"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting scraper: {str(e)}")

@app.post("/scrape")
async def scrape_custom(background_tasks: BackgroundTasks):
    """Start custom scraping (POST method)"""
    try:
        return {
            "message": "Custom scraping endpoint",
            "note": "On Vercel, background tasks are limited due to serverless constraints"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/status")
async def get_status():
    """Get scraping status"""
    return {
        "status": "idle",
        "message": "API is running on Vercel",
        "constraints": [
            "Serverless environment - limited execution time",
            "No persistent storage",
            "No background tasks"
        ]
    }

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function handler"""
    from mangum import Mangum
    
    # Create Mangum handler for FastAPI
    handler = Mangum(app)
    
    # Handle the request
    return handler(request, context)
