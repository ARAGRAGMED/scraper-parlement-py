#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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
        "timestamp": datetime.now().isoformat(),
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
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config")
async def get_config():
    """Get current scraper configuration"""
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

@app.get("/scrape")
async def scrape_current_year():
    """Scrape current year legislation"""
    return {
        "message": "Scraping endpoint called successfully",
        "current_year": datetime.now().year,
        "note": "On Vercel, full scraping is limited due to timeout constraints",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/scrape")
async def scrape_custom():
    """Start custom scraping (POST method)"""
    return {
        "message": "Custom scraping endpoint",
        "note": "On Vercel, background tasks are limited due to serverless constraints",
        "timestamp": datetime.now().isoformat()
    }

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
        ],
        "timestamp": datetime.now().isoformat()
    }
