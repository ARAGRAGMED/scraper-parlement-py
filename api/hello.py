def handler(request, context):
    """Minimal Vercel Python function"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": "Hello from Vercel Python!"
    }
