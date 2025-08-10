#!/usr/bin/env python3
"""
Scraping service for handling legislation data refresh operations
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class ScrapingService:
    """Service for handling scraping operations"""
    
    def __init__(self):
        self.scraper_available = self._check_scraper_availability()
    
    def _check_scraper_availability(self) -> bool:
        """Check if the scraper module is available"""
        try:
            # Add src directory to Python path for scraper imports
            current_dir = Path(__file__).parent.parent.parent
            src_dir = current_dir / "src"
            sys.path.insert(0, str(src_dir))
            
            from moroccan_parliament_scraper.core.legislation_scraper import MoroccanParliamentScraper
            print("✅ Scraper module imported successfully!")
            return True
        except ImportError as e:
            print(f"❌ Failed to import scraper: {e}")
            print(f"Current directory: {current_dir}")
            print(f"Src directory: {src_dir}")
            print(f"Python path: {sys.path[:3]}")
            return False
    
    def refresh_legislation_data(self, max_pages: int = 5, force_rescrape: bool = False) -> Dict[str, Any]:
        """
        Refresh legislation data from source (scraping live data)
        """
        try:
            if not self.scraper_available:
                return {
                    "error": "Scraper not available",
                    "message": "Scraping functionality is not available on this platform",
                    "suggestion": "Use existing data from /api/legislation endpoint",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if we're in a serverless environment
            is_vercel = os.environ.get('VERCEL') == '1'
            
            if is_vercel:
                # Vercel serverless environment - scraping is not reliable
                return {
                    "message": "Scraping not available in Vercel serverless environment",
                    "status": "serverless_limited",
                    "timestamp": datetime.now().isoformat(),
                    "note": "Vercel serverless functions cannot reliably perform web scraping due to strict limitations",
                    "environment": "vercel_serverless",
                    "limitations": [
                        "60 second timeout limit (too short for web scraping)",
                        "1024 MB memory limit (insufficient for BeautifulSoup parsing)",
                        "Read-only file system (cannot save scraped data)",
                        "Limited network requests and external connections"
                    ],
                    "current_data_status": "Available",
                    "recommendation": "Use existing data from /api/legislation endpoint. For fresh data, run scraping locally using 'python run_scraper.py'",
                    "actions": [
                        "View current data: GET /api/legislation",
                        "Check data status: GET /api/status",
                        "Local scraping: python run_scraper.py"
                    ]
                }
            
            # For non-serverless environments, attempt actual scraping
            try:
                # Change to the project root directory if needed
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                if os.getcwd() != project_root:
                    os.chdir(project_root)
                
                from moroccan_parliament_scraper.core.legislation_scraper import MoroccanParliamentScraper
                
                scraper = MoroccanParliamentScraper(force_rescrape=force_rescrape)
                success = scraper.run(max_pages=max_pages, force_rescrape=force_rescrape)
                
                if success:
                    # Check if we got any new data
                    total_items = len(scraper.results) if hasattr(scraper, 'results') else 0
                    
                    # Check if this was a fresh scrape or just loading existing data
                    # We can determine this by checking if the scraper actually found new items
                    # vs just loaded existing data from file
                    from utils.helpers import get_data_file_path
                    data_file, _ = get_data_file_path()
                    existing_data_count = 0
                    
                    if os.path.exists(data_file):
                        try:
                            with open(data_file, 'r', encoding='utf-8') as f:
                                existing_data = json.load(f)
                                existing_data_count = len(existing_data.get('data', []))
                        except:
                            pass
                    
                    # If we have the same number of items as existing data, likely no new items were found
                    if total_items > 0 and total_items == existing_data_count and not force_rescrape:
                        return {
                            "message": "Scraping completed successfully but no new data was found",
                            "status": "success_no_new_data",
                            "timestamp": datetime.now().isoformat(),
                            "data": {
                                "total_items": total_items,
                                "scraped_at": datetime.now().isoformat(),
                                "note": f"Scraping completed but no new legislation items found. Loaded {total_items} existing items.",
                                "force_rescrape": force_rescrape,
                                "max_pages": max_pages,
                                "update_status": "no_new_items_found",
                                "existing_items_loaded": total_items
                            }
                        }
                    elif total_items > 0:
                        return {
                            "message": "Legislation refresh completed successfully",
                            "status": "success",
                            "timestamp": datetime.now().isoformat(),
                            "data": {
                                "total_items": total_items,
                                "scraped_at": datetime.now().isoformat(),
                                "note": f"Successfully processed {total_items} legislation items",
                                "force_rescrape": force_rescrape,
                                "max_pages": max_pages,
                                "update_status": "items_processed"
                            }
                        }
                    else:
                        return {
                            "message": "Scraping completed successfully but no data was updated",
                            "status": "success_no_new_data",
                            "timestamp": datetime.now().isoformat(),
                            "data": {
                                "total_items": 0,
                                "scraped_at": datetime.now().isoformat(),
                                "note": "No legislation data found or available",
                                "force_rescrape": force_rescrape,
                                "max_pages": max_pages,
                                "update_status": "no_data_available"
                            }
                        }
                else:
                    return {
                        "message": "Legislation refresh failed",
                        "status": "error",
                        "timestamp": datetime.now().isoformat(),
                        "note": "Scraper execution failed - check logs for details",
                        "force_rescrape": force_rescrape,
                        "max_pages": max_pages
                    }
                    
            except Exception as scraper_error:
                return {
                    "error": "Scraper execution error",
                    "message": str(scraper_error),
                    "error_type": type(scraper_error).__name__,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Error occurred during scraper execution"
                }
                
        except Exception as e:
            return {
                "error": "Failed to refresh legislation data",
                "message": str(e),
                "error_type": type(e).__name__,
                "timestamp": datetime.now().isoformat()
            }
