#!/usr/bin/env python3
"""
Moroccan Parliament Legislation API - Main Entry Point
This file has been refactored for better maintainability.

The old monolithic code has been split into:
- api/main.py - FastAPI app initialization
- api/routes/ - API endpoint definitions
- api/services/ - Business logic
- api/models/ - Request/Response models
- api/middleware/ - Authentication and middleware
- api/utils/ - Helper functions
- api/static/ - Frontend HTML

For backward compatibility, this file now imports from the new structure.
"""

# Import the FastAPI app from the new structure
from main import app

# Export the app for compatibility
__all__ = ['app']
