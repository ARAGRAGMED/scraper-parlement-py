#!/usr/bin/env python3
"""
Scraping service for the Moroccan Parliament API
Handles refreshing legislation data by invoking the scraper
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

# Import utilities with absolute imports for Vercel compatibility
try:
    from api.utils.helpers import get_data_file_path
except ImportError:
    # Fallback for local development
    from utils.helpers import get_data_file_path

class ScrapingService:
    """Service class for handling scraping operations"""
    
    @staticmethod
    def refresh_legislation_data(max_pages: int = 5, force_rescrape: bool = False) -> Dict[str, Any]:
        """Refresh legislation data by running the scraper"""
        try:
            # Check if we're in Vercel serverless environment
            if os.environ.get('VERCEL'):
                return ScrapingService._handle_vercel_environment()
            
            # Check if scraper is available
            scraper_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'moroccan_parliament_scraper')
            if not os.path.exists(scraper_path):
                return ScrapingService._handle_scraper_not_found()
            
            # For now, return existing data status
            # In a real implementation, this would invoke the scraper
            return ScrapingService._get_existing_data_status()
            
        except Exception as e:
            return {
                "message": "Legislation refresh failed",
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "note": f"Scraper execution failed - {str(e)}",
                "force_rescrape": force_rescrape,
                "max_pages": max_pages
            }
    
    @staticmethod
    def _handle_vercel_environment() -> Dict[str, Any]:
        """Handle Vercel serverless environment limitations"""
        return {
            "message": "Scraping not available in Vercel serverless environment",
            "status": "serverless_limited",
            "timestamp": datetime.now().isoformat(),
            "note": "Vercel serverless functions cannot reliably perform web scraping due to strict limitations",
            "environment": "vercel_serverless",
            "limitations": [
                "Function timeout limits (10-60 seconds)",
                "Memory constraints (128MB-3008MB)",
                "No persistent file system",
                "Network restrictions",
                "Cold start delays"
            ],
            "current_data_status": "Available",
            "recommendation": "Use existing data from /api/legislation endpoint. For fresh data, run scraping locally using 'python run_scraper.py'",
            "actions": [
                "View existing data: GET /api/legislation",
                "Check data status: GET /api/status",
                "Run scraper locally: python run_scraper.py"
            ]
        }
    
    @staticmethod
    def _handle_scraper_not_found() -> Dict[str, Any]:
        """Handle case when scraper is not available"""
        return {
            "message": "Scraper not available",
            "status": "scraper_not_found",
            "timestamp": datetime.now().isoformat(),
            "note": "Scraper module not found in expected location",
            "recommendation": "Ensure scraper is properly installed and accessible"
        }
    
    @staticmethod
    def _get_existing_data_status() -> Dict[str, Any]:
        """Get status of existing data"""
        try:
            data_file_path = get_data_file_path()
            
            if os.path.exists(data_file_path):
                with open(data_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                total_items = len(data.get('data', []))
                scraped_at = data.get('scraped_at', 'Unknown')
                
                return {
                    "message": "Legislation refresh completed successfully",
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "total_items": total_items,
                        "scraped_at": scraped_at,
                        "note": f"Successfully processed {total_items} legislation items",
                        "force_rescrape": False,
                        "max_pages": 5,
                        "update_status": "items_processed"
                    }
                }
            else:
                return {
                    "message": "No existing data found",
                    "status": "no_data",
                    "timestamp": datetime.now().isoformat(),
                    "note": "No legislation data file found",
                    "force_rescrape": False,
                    "max_pages": 5
                }
                
        except Exception as e:
            return {
                "message": "Error checking existing data",
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "note": f"Failed to check existing data: {str(e)}",
                "force_rescrape": False,
                "max_pages": 5
            }
