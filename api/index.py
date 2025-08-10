#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import json

# Add src directory to Python path for imports
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global scraper instance
scraper = None
scraping_status = {
    "is_running": False,
    "current_task": None,
    "last_update": None,
    "error": None
}

def get_scraper():
    """Get or create scraper instance"""
    global scraper
    if scraper is None and SCRAPER_AVAILABLE:
        try:
            config_path = Path(__file__).parent.parent / "config" / "scraper_config.json"
            scraper = MoroccanParliamentScraper(config_path=str(config_path))
        except Exception as e:
            print(f"Error initializing scraper: {e}")
            return None
    return scraper

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Moroccan Parliament Scraper API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "status": "running",
        "scraper_available": SCRAPER_AVAILABLE,
        "endpoints": {
            "/": "This info",
            "/health": "Health check",
            "/config": "Get current scraper configuration",
            "/scrape": "Start scraping (GET for current year, POST for custom)",
            "/status": "Get scraping status",
            "/docs": "Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "moroccan-parliament-scraper",
        "scraper_available": SCRAPER_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config")
async def get_config():
    """Get current scraper configuration"""
    if not SCRAPER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Scraper not available on Vercel")
    
    try:
        scraper_instance = get_scraper()
        if scraper_instance:
            config = scraper_instance.get_config()
            return {
                "message": "Configuration retrieved successfully",
                "config": config,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "message": "Scraper not initialized",
                "error": "Failed to initialize scraper",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "message": "Error retrieving configuration",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/scrape")
async def scrape_current_year():
    """Scrape current year legislation"""
    if not SCRAPER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Scraper not available on Vercel")
    
    if scraping_status["is_running"]:
        raise HTTPException(status_code=409, detail="Scraping already in progress")
    
    try:
        scraper_instance = get_scraper()
        if not scraper_instance:
            raise HTTPException(status_code=500, detail="Scraper not initialized")
        
        current_year = datetime.now().year
        
        # Update status
        scraping_status.update({
            "is_running": True,
            "current_task": f"Scraping year {current_year}",
            "last_update": datetime.now().isoformat(),
            "error": None
        })
        
        # Start scraping in background
        # Note: On Vercel, this will be limited by function timeout
        try:
            result = scraper_instance.scrape_legislation(year=current_year)
            scraping_status.update({
                "is_running": False,
                "current_task": None,
                "last_update": datetime.now().isoformat()
            })
            return {
                "message": "Scraping completed successfully",
                "year": current_year,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            scraping_status.update({
                "is_running": False,
                "current_task": None,
                "error": str(e),
                "last_update": datetime.now().isoformat()
            })
            raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error starting scraping: {str(e)}")

@app.post("/scrape")
async def scrape_custom(background_tasks: BackgroundTasks):
    """Start custom scraping (POST method)"""
    if not SCRAPER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Scraper not available on Vercel")
    
    if scraping_status["is_running"]:
        raise HTTPException(status_code=409, detail="Scraping already in progress")
    
    try:
        scraper_instance = get_scraper()
        if not scraper_instance:
            raise HTTPException(status_code=500, detail="Scraper not initialized")
        
        # For POST, we could accept parameters like year, force_rescrape, etc.
        # For now, we'll use default settings
        current_year = datetime.now().year
        
        # Update status
        scraping_status.update({
            "is_running": True,
            "current_task": f"Custom scraping year {current_year}",
            "last_update": datetime.now().isoformat(),
            "error": None
        })
        
        try:
            result = scraper_instance.scrape_legislation(year=current_year, force_rescrape=True)
            scraping_status.update({
                "is_running": False,
                "current_task": None,
                "last_update": datetime.now().isoformat()
            })
            return {
                "message": "Custom scraping completed successfully",
                "year": current_year,
                "force_rescrape": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            scraping_status.update({
                "is_running": False,
                "current_task": None,
                "error": str(e),
                "last_update": datetime.now().isoformat()
            })
            raise HTTPException(status_code=500, detail=f"Custom scraping failed: {str(e)}")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error starting custom scraping: {str(e)}")

@app.get("/status")
async def get_status():
    """Get scraping status"""
    return {
        "status": "idle" if not scraping_status["is_running"] else "running",
        "scraper_available": SCRAPER_AVAILABLE,
        "details": scraping_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-scraper")
async def test_scraper():
    """Test if scraper can be initialized"""
    if not SCRAPER_AVAILABLE:
        return {
            "status": "unavailable",
            "message": "Scraper modules not available on Vercel",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        scraper_instance = get_scraper()
        if scraper_instance:
            return {
                "status": "available",
                "message": "Scraper initialized successfully",
                "config_loaded": hasattr(scraper_instance, 'config'),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to initialize scraper",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error testing scraper: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )
