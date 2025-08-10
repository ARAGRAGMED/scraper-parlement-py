#!/usr/bin/env python3
"""
Moroccan Parliament Legislation Scraper

A comprehensive web scraper for extracting current year legislation data
from the Moroccan Parliament website with source identification,
proxy support, and configuration management.
"""

__version__ = "1.0.0"
__author__ = "Moroccan Parliament Scraper Team"
__description__ = "Enhanced scraper for Moroccan Parliament legislation with configuration management and proxy support"

# Import main classes for easy access
from .core.legislation_scraper import MoroccanParliamentScraper
from .utils.config_manager import ConfigManager

# Main exports
__all__ = [
    'MoroccanParliamentScraper',
    'ConfigManager',
]

# Package metadata
__package_info__ = {
    'name': 'moroccan_parliament_scraper',
    'version': __version__,
    'description': __description__,
    'author': __author__,
    'main_class': 'MoroccanParliamentScraper',
    'config_class': 'ConfigManager',
}
