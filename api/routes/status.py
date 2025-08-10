#!/usr/bin/env python3
"""
Status routes for the Moroccan Parliament API
"""

from fastapi import APIRouter
from datetime import datetime

# Import utilities with absolute imports for Vercel compatibility
try:
    from api.utils.helpers import get_data_file_path
except ImportError:
    # Fallback for local development
    from utils.helpers import get_data_file_path

router = APIRouter()

@router.get("/status")
async def get_api_status():
    """Get comprehensive API status and documentation"""
    try:
        # Get data file information
        data_file_path = get_data_file_path()
        
        # Check if data file exists and get its info
        import os
        data_status = "not_found"
        last_updated = None
        
        if os.path.exists(data_file_path):
            data_status = "connected"
            last_updated = datetime.fromtimestamp(os.path.getmtime(data_file_path)).isoformat()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": {
                "status": data_status,
                "file_path": str(data_file_path),
                "last_updated": last_updated
            },
            "endpoints": {
                "public": [
                    "GET / - Home page",
                    "GET /api/legislation - All legislation",
                    "GET /api/commissions - All commissions",
                    "GET /api/legislation/{stage} - Legislation by stage",
                    "GET /api/legislation/commission/{commission_id} - Legislation by commission",
                    "GET /api/legislation/numero/{numero} - Legislation by number",
                    "GET /api/status - API status"
                ],
                "protected": [
                    "POST /api/legislation/refresh - Refresh data (requires API key)"
                ]
            },
            "configuration": {
                "api_key_required": True,
                "max_pages_default": 5,
                "force_rescrape_default": False
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
