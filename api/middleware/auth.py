#!/usr/bin/env python3
"""
Authentication middleware for API key verification
"""

import os
from fastapi import HTTPException, Header

# Authentication configuration
API_KEY = os.environ.get("API_KEY", "your-secret-api-key-here")
API_KEY_NAME = "X-API-Key"

async def verify_api_key(x_api_key: str = Header(None, alias=API_KEY_NAME)):
    """Verify API key for protected endpoints"""
    if not x_api_key:
        raise HTTPException(
            status_code=401, 
            detail="API key required",
            headers={"WWW-Authenticate": f"{API_KEY_NAME}"}
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=403, 
            detail="Invalid API key",
            headers={"WWW-Authenticate": f"{API_KEY_NAME}"}
        )
    
    return x_api_key
