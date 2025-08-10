#!/usr/bin/env python3
"""
Development server runner with reload functionality
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
