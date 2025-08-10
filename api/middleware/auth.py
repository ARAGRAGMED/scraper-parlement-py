#!/usr/bin/env python3
"""
Authentication middleware for the Moroccan Parliament API
"""

from fastapi import HTTPException, Depends, Header
from typing import Optional

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Verify API key from request header
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        The verified API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # For now, use a simple hardcoded key
    # In production, this should be stored securely and validated against a database
    expected_key = "your-secret-api-key-here"
    
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return x_api_key
