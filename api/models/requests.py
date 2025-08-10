#!/usr/bin/env python3
"""
Request models for API endpoints
"""

from pydantic import BaseModel
from typing import Optional

class RefreshLegislationRequest(BaseModel):
    max_pages: Optional[int] = 5
    force_rescrape: Optional[bool] = False
