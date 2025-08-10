from http.server import BaseHTTPRequestHandler
import json

def handler(request, context):
    """Vercel Python serverless function handler"""
    try:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8"
            },
            "body": "Hello from Vercel Python! 🚀"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8"
            },
            "body": f"Error: {str(e)}"
        }
