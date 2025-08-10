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
    
    # Construct the data file path
    # This should point to where the scraper saves its data
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_file = data_dir / f"legislation_{current_year}.json"
    
    return data_file
