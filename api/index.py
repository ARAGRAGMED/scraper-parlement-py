#!/usr/bin/env python3
"""
Vercel Serverless Function for Moroccan Parliament Legislation API
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
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

# Root endpoint for local development (serves dynamic_viewer.html content)
@app.get("/")
async def main_page():
    """Main page endpoint - serves dynamic_viewer.html content locally"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moroccan Parliament Scraper - Dynamic Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .api-section { background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .endpoint { background: #3498db; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; display: inline-block; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .healthy { background: #27ae60; color: white; }
        .error { background: #e74c3c; color: white; }
        button { background: #3498db; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
        button:hover { background: #2980b9; }
        .data-display { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇲🇦 Moroccan Parliament Scraper - Dynamic Viewer</h1>
        
        <div class="api-section">
            <h2>API Status</h2>
            <div id="health-status" class="status">Checking...</div>
            <button onclick="checkHealth()">Check Health</button>
        </div>

        <div class="api-section">
            <h2>Available Endpoints</h2>
            <div class="endpoint">GET /api/</div>
            <div class="endpoint">GET /api/health</div>
            <div class="endpoint">GET /api/config</div>
            <div class="endpoint">GET /api/scrape</div>
            <div class="endpoint">POST /api/scrape</div>
            <div class="endpoint">GET /api/status</div>
            <div class="endpoint">GET /api/test-scraper</div>
        </div>

        <div class="api-section">
            <h2>Test API</h2>
            <button onclick="testEndpoint('/api/')">Test API Root</button>
            <button onclick="testEndpoint('/api/config')">Test Config</button>
            <button onclick="testEndpoint('/api/status')">Test Status</button>
            <div id="api-response" class="data-display"></div>
        </div>
    </div>

    <script>
        async function checkHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                const statusDiv = document.getElementById('health-status');
                statusDiv.className = 'status healthy';
                statusDiv.innerHTML = `✅ Healthy - ${data.service} - ${data.timestamp}`;
            } catch (error) {
                const statusDiv = document.getElementById('health-status');
                statusDiv.className = 'status error';
                statusDiv.innerHTML = `❌ Error: ${error.message}`;
            }
        }

        async function testEndpoint(endpoint) {
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                const responseDiv = document.getElementById('api-response');
                responseDiv.innerHTML = `<strong>${endpoint}:</strong><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                const responseDiv = document.getElementById('api-response');
                responseDiv.innerHTML = `<strong>${endpoint}:</strong><br><span style="color: red;">Error: ${error.message}</span>`;
            }
        }

        // Check health on page load
        window.onload = function() {
            checkHealth();
        };
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)
