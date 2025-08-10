#!/usr/bin/env python3
"""
Scraping routes for the Moroccan Parliament API
"""

from fastapi import APIRouter, Depends
from models.requests import RefreshLegislationRequest
from services.scraping_service import ScrapingService
from middleware.auth import verify_api_key

router = APIRouter()

@router.post("/legislation/refresh")
async def refresh_legislation_data(
    request: RefreshLegislationRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Refresh legislation data from source (scraping live data)
    
    **Authentication Required:** This endpoint requires a valid API key in the `X-API-Key` header.
    
    **Request Headers:**
    - `X-API-Key`: Your API key for authentication
    
    **Request Body:**
    - `max_pages` (optional): Maximum number of pages to scrape (default: 5)
    - `force_rescrape` (optional): Whether to re-scrape existing data (default: false)
    
    **Example Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/legislation/refresh" \
         -H "X-API-Key: your-secret-api-key-here" \
         -H "Content-Type: application/json" \
         -d '{"max_pages": 3, "force_rescrape": true}'
    ```
    
    **Security Note:** This endpoint can trigger web scraping operations and should be protected.
    """
    scraping_service = ScrapingService()
    return scraping_service.refresh_legislation_data(
        max_pages=request.max_pages,
        force_rescrape=request.force_rescrape
    )
