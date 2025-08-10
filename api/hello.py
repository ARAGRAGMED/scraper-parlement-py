def handler(request, context):
    """Vercel Python serverless function handler"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
        },
        "body": "Hello from Vercel Python! 🚀"
    }
