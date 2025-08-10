#!/usr/bin/env python3
"""
Utility functions for the Moroccan Parliament API
"""

import os
from pathlib import Path
from datetime import datetime

def get_data_file_path() -> Path:
    """
    Get the path to the current year's legislation data file
    
    Returns:
        Path object pointing to the data file
    """
    # Get the current year
    current_year = datetime.now().year
    
    # First, try to find the file in the api directory (for Vercel deployment)
    api_dir = Path(__file__).parent.parent
    api_data_file = api_dir / f"extracted-data-{current_year}.json"
    
    if api_data_file.exists():
        return api_data_file
    
    # If not found in api directory, try the parent data directory (for local development)
    data_dir = Path(__file__).parent.parent.parent / "data"
    
    # Try the actual filename first, then fallback to the expected format
    data_file = data_dir / f"extracted-data-{current_year}.json"
    
    # If that doesn't exist, try the expected format
    if not data_file.exists():
        data_file = data_dir / f"legislation_{current_year}.json"
    
    return data_file
