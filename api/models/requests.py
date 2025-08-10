#!/usr/bin/env python3
"""
Request models for the Moroccan Parliament API
"""

from pydantic import BaseModel, Field
from typing import Optional

class RefreshLegislationRequest(BaseModel):
    """Request model for refreshing legislation data"""
    
    max_pages: Optional[int] = Field(
        default=5,
        description="Maximum number of pages to scrape",
        ge=1,
        le=50
    )
    
    force_rescrape: Optional[bool] = Field(
        default=False,
        description="Whether to re-scrape existing data"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "max_pages": 3,
                "force_rescrape": True
            }
        }
