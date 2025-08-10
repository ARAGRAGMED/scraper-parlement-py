#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from moroccan_parliament_scraper.core.legislation_scraper import MoroccanParliamentScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

app = FastAPI(
    title="Moroccan Parliament Scraper API",
    description="API for scraping Moroccan Parliament legislation data",
    version="1.0.0"
)

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Moroccan Parliament Scraper API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "scraper_available": SCRAPER_AVAILABLE,
        "endpoints": {
            "/": "This info",
            "/health": "Health check",
            "/config": "Get current scraper configuration",
            "/scrape": "Start scraping (GET for current year, POST for custom)",
            "/status": "Get scraping status",
            "/test-scraper": "Test scraper initialization"
        }
    }

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "moroccan-parliament-scraper",
        "scraper_available": SCRAPER_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@api_router.get("/config")
async def get_config():
    """Get current scraper configuration"""
    if not SCRAPER_AVAILABLE:
        return {
            "message": "Scraper not available on Vercel",
            "note": "Scraper modules could not be imported",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
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
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "message": "Error getting config",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/scrape")
async def scrape_current_year():
    """Scrape current year legislation"""
    if not SCRAPER_AVAILABLE:
        return {
            "message": "Scraper not available on Vercel",
            "error": "Scraper modules could not be imported",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        return {
            "message": "Scraping endpoint called successfully",
            "current_year": datetime.now().year,
            "note": "On Vercel, full scraping is limited due to timeout constraints",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "message": "Error in scraping endpoint",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.post("/scrape")
async def scrape_custom(background_tasks: BackgroundTasks):
    """Start custom scraping (POST method)"""
    if not SCRAPER_AVAILABLE:
        return {
            "message": "Scraper not available on Vercel",
            "error": "Scraper modules could not be imported",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        return {
            "message": "Custom scraping endpoint",
            "note": "On Vercel, background tasks are limited due to serverless constraints",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "message": "Error in custom scraping endpoint",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@api_router.get("/status")
async def get_status():
    """Get scraping status"""
    return {
        "status": "idle",
        "message": "API is running on Vercel",
        "scraper_available": SCRAPER_AVAILABLE,
        "constraints": [
            "Serverless environment - limited execution time",
            "No persistent storage",
            "No background tasks"
        ],
        "timestamp": datetime.now().isoformat()
    }

@api_router.get("/test-scraper")
async def test_scraper():
    """Test if scraper can be initialized"""
    if not SCRAPER_AVAILABLE:
        return {
            "status": "unavailable",
            "message": "Scraper modules not available on Vercel",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        return {
            "status": "available",
            "message": "Scraper modules imported successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error testing scraper: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Include the API router
app.include_router(api_router)

# Add a root endpoint for the main page
@app.get("/")
async def main_page():
    """Main page endpoint"""
    return {
        "message": "Moroccan Parliament Scraper - Main Page",
        "api_docs": "/docs",
        "api_endpoints": "/api/",
        "frontend": "Visit the root URL for the viewer interface"
    }
