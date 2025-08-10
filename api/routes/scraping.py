#!/usr/bin/env python3
"""
Scraping routes for the Moroccan Parliament API
"""

from fastapi import APIRouter, Depends, HTTPException
from models.requests import RefreshLegislationRequest

# Import services and middleware with absolute imports for Vercel compatibility
try:
    from api.services.scraping_service import ScrapingService
    from api.middleware.auth import verify_api_key
except ImportError:
    # Fallback for local development
    from services.scraping_service import ScrapingService
    from middleware.auth import verify_api_key

router = APIRouter()

@router.post("/legislation/refresh")
async def refresh_legislation_data(
    request: RefreshLegislationRequest,
    api_key: str = Depends(verify_api_key)
):
    """Refresh legislation data by running the scraper"""
    try:
        result = ScrapingService.refresh_legislation_data(
            max_pages=request.max_pages,
            force_rescrape=request.force_rescrape
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
