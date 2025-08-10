#!/usr/bin/env python3
"""
Commission routes for the Moroccan Parliament API
"""

from fastapi import APIRouter

# Import services with absolute imports for Vercel compatibility
try:
    from api.services.data_service import DataService
except ImportError:
    # Fallback for local development
    from services.data_service import DataService

router = APIRouter()

@router.get("/commissions")
async def get_all_commissions():
    """Get all commissions from local database"""
    return DataService.get_all_commissions()
