import json

def handler(request, context):
    """Simple test handler for Vercel"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from Vercel!",
            "timestamp": "2025-08-10T15:30:00Z"
        })
    }
