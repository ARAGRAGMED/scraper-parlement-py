#!/usr/bin/env python3
"""
Helper utility functions for the API
"""

from datetime import datetime
from pathlib import Path

def get_data_file_path():
    """Get the current year data file path dynamically"""
    current_dir = Path(__file__).parent.parent
    current_year = datetime.now().year
    
    # Check if we're in the second half of the year (legislative year format)
    if datetime.now().month >= 9:  # September onwards
        # Use next year for legislative year (e.g., 2024-2025)
        legislative_year = f"{current_year}-{current_year + 1}"
        filename = f"extracted-data-{current_year + 1}.json"
    else:
        # Use current year for legislative year (e.g., 2024-2025)
        legislative_year = f"{current_year - 1}-{current_year}"
        filename = f"extracted-data-{current_year}.json"
    
    data_file = current_dir.parent / "data" / filename
    return str(data_file), legislative_year
