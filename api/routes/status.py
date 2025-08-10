#!/usr/bin/env python3
"""
Status routes for the Moroccan Parliament API
"""

from fastapi import APIRouter
from datetime import datetime
from utils.helpers import get_data_file_path

router = APIRouter()

@router.get("/status")
async def get_api_status():
    """Check API endpoint status and health with detailed documentation"""
    return {
        "status": "healthy",
        "service": "Moroccan Parliament Legislation API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {
                "path": "/api/legislation",
                "method": "GET",
                "description": "Get all legislation from local database",
                "status": "active",
                "response_format": {
                    "total_items": "int",
                    "current_year": "string",
                    "scraped_at": "string (ISO timestamp)",
                    "data": "array of legislation items",
                    "status": "success|empty",
                    "message": "string"
                }
            },
            {
                "path": "/api/commissions",
                "method": "GET",
                "description": "Get all available commissions",
                "status": "active",
                "response_format": {
                    "commissions": "array of commission objects",
                    "total_count": "int",
                    "status": "success"
                }
            },
            {
                "path": "/api/legislation/{stage}",
                "method": "GET", 
                "description": "Get legislation by stage (1 or 2)",
                "status": "active",
                "response_format": {
                    "stage": "string (1 or 2)",
                    "total_items": "int",
                    "data": "array of legislation items",
                    "status": "success|empty"
                }
            },
            {
                "path": "/api/legislation/commission/{commission_id}",
                "method": "GET",
                "description": "Get legislation by commission ID",
                "status": "active",
                "response_format": {
                    "commission_id": "string",
                    "commission_name": "string",
                    "total_items": "int",
                    "data": "array of legislation items",
                    "status": "success|empty"
                }
            },
            {
                "path": "/api/legislation/numero/{numero}",
                "method": "GET",
                "description": "Get legislation by law number",
                "status": "active",
                "response_format": {
                    "numero": "string",
                    "data": "legislation item object or null",
                    "status": "success|not_found"
                }
            },
            {
                "path": "/api/legislation/refresh",
                "method": "POST",
                "description": "Refresh data from source (scraping) - PROTECTED ENDPOINT",
                "status": "active",
                "authentication": "Required - X-API-Key header",
                "request_headers": {
                    "X-API-Key": "string (required) - Your API key for authentication"
                },
                "request_body": {
                    "max_pages": "int (optional, default: 5)",
                    "force_rescrape": "boolean (optional, default: false)"
                },
                "response_formats": {
                    "success": {
                        "message": "Legislation refresh completed successfully",
                        "status": "success",
                        "timestamp": "string (ISO timestamp)",
                        "data": {
                            "total_items": "int",
                            "scraped_at": "string (ISO timestamp)",
                            "note": "Successfully processed X legislation items",
                            "force_rescrape": "boolean",
                            "max_pages": "int",
                            "update_status": "items_processed"
                        }
                    },
                    "success_no_new_data": {
                        "message": "Scraping completed successfully but no new data was found",
                        "status": "success_no_new_data",
                        "timestamp": "string (ISO timestamp)",
                        "data": {
                            "total_items": "int",
                            "scraped_at": "string (ISO timestamp)",
                            "note": "Scraping completed but no new legislation items found. Loaded X existing items.",
                            "force_rescrape": "boolean",
                            "max_pages": "int",
                            "update_status": "no_new_items_found",
                            "existing_items_loaded": "int"
                        }
                    },
                    "error": {
                        "message": "Legislation refresh failed",
                        "status": "error",
                        "timestamp": "string (ISO timestamp)",
                        "note": "Scraper execution failed - check logs for details",
                        "force_rescrape": "boolean",
                        "max_pages": "int"
                    },
                    "serverless_limited": {
                        "message": "Scraping not available in Vercel serverless environment",
                        "status": "serverless_limited",
                        "timestamp": "string (ISO timestamp)",
                        "note": "Vercel serverless functions cannot reliably perform web scraping due to strict limitations",
                        "environment": "vercel_serverless",
                        "limitations": ["array of limitation strings"],
                        "current_data_status": "Available",
                        "recommendation": "Use existing data from /api/legislation endpoint. For fresh data, run scraping locally using 'python run_scraper.py'",
                        "actions": ["array of available actions"]
                    }
                },
                "notes": [
                    "🔒 PROTECTED ENDPOINT: Requires valid API key in X-API-Key header",
                    "When force_rescrape=false (default): Skips existing items, faster execution",
                    "When force_rescrape=true: Re-scrapes all items, slower but comprehensive",
                    "max_pages limits the number of pages to scrape for safety",
                    "Returns existing data count when no new items found"
                ]
            },
            {
                "path": "/api/status",
                "method": "GET",
                "description": "Check API health status and documentation",
                "status": "active"
            }
        ],
        "database": {
            "status": "connected",
            "type": "local",
            "data_file": get_data_file_path()[0],
            "legislative_year": get_data_file_path()[1],
            "last_update": datetime.now().isoformat()
        },
        "commissions": {
            "total_count": 21,
            "types": [
                "Permanent Commissions (11)",
                "Thematic Working Groups (10)"
            ]
        },
        "scraping_modes": {
            "normal": {
                "description": "Skip existing items, only scrape new ones",
                "use_case": "Regular updates, faster execution",
                "force_rescrape": False
            },
            "force_rescrape": {
                "description": "Re-scrape all items regardless of existing data",
                "use_case": "Complete refresh, data validation",
                "force_rescrape": True
            }
        },
        "update_statuses": {
            "items_processed": "New or updated items were found and processed",
            "no_new_items_found": "Scraping completed but no new items found, existing data loaded",
            "no_data_available": "No legislation data found or available",
            "no_updates_needed": "All existing items were already up-to-date"
        }
    }
