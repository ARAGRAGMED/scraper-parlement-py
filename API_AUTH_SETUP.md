# 🔐 API Authentication Setup

The `/api/legislation/refresh` endpoint is now **protected by authentication** to prevent unauthorized access to the web scraping functionality.

## 🚀 Quick Setup

### 1. Set Your API Key

Set the `API_KEY` environment variable with your secret key:

```bash
# Option 1: Export in your shell
export API_KEY="your-secret-api-key-here"

# Option 2: Create a .env file (recommended for development)
echo "API_KEY=your-secret-api-key-here" > .env
```

### 2. Generate a Strong API Key

**Never use the default key!** Generate a strong, unique key:

```bash
# Option 1: Use openssl (recommended)
openssl rand -hex 32

# Option 2: Use Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Use online generator (less secure)
# Visit: https://generate-secret.vercel.app/32
```

### 3. Test the Protected Endpoint

```bash
# Test with your API key
curl -X POST "http://localhost:8000/api/legislation/refresh" \
     -H "X-API-Key: your-actual-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 3, "force_rescrape": false}'
```

## 🔒 Security Features

- **Header-based authentication**: Uses `X-API-Key` header
- **Environment variable**: API key stored securely in environment
- **No hardcoded keys**: Default key is just a placeholder
- **401/403 responses**: Proper HTTP status codes for auth failures

## 🚨 Security Best Practices

1. **Use a strong key**: At least 32 characters, mix of letters/numbers
2. **Keep it secret**: Never commit API keys to version control
3. **Rotate regularly**: Change your key periodically
4. **Limit access**: Only share with authorized users
5. **Monitor usage**: Watch for unusual API activity

## 📝 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Your secret API key | `your-secret-api-key-here` | ✅ Yes |

## 🐛 Troubleshooting

### "API key required" (401)
- Check that you're sending the `X-API-Key` header
- Verify the header name is exactly `X-API-Key`

### "Invalid API key" (403)
- Verify your API key matches the `API_KEY` environment variable
- Check for extra spaces or characters
- Ensure the environment variable is loaded

### "Environment variable not found"
- Restart your application after setting the environment variable
- Check that the variable name is exactly `API_KEY`

## 🔄 For Production Deployment

### Vercel
```bash
# Set in Vercel dashboard or CLI
vercel env add API_KEY
```

### Docker
```bash
docker run -e API_KEY="your-key" your-app
```

### Systemd
```bash
# In your service file
Environment="API_KEY=your-key"
```

## 📚 Example Usage

### Python Requests
```python
import requests

headers = {
    'X-API-Key': 'your-secret-api-key-here',
    'Content-Type': 'application/json'
}

response = requests.post(
    'http://localhost:8000/api/legislation/refresh',
    headers=headers,
    json={'max_pages': 5, 'force_rescrape': True}
)

print(response.json())
```

### JavaScript/Fetch
```javascript
const response = await fetch('/api/legislation/refresh', {
    method: 'POST',
    headers: {
        'X-API-Key': 'your-secret-api-key-here',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        max_pages: 3,
        force_rescrape: false
    })
});

const data = await response.json();
console.log(data);
```

---

**Remember**: Keep your API key secure and never expose it in client-side code or public repositories! 🔐
