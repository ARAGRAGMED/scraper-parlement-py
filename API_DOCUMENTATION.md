# 🔌 API Documentation

Comprehensive technical documentation for the Moroccan Parliament Legislation API endpoints, request/response formats, and integration examples.

## 📋 **API Overview**

- **Base URL**: `http://localhost:8000` (local) / `https://your-domain.vercel.app` (production)
- **API Version**: v1.0.0
- **Authentication**: API Key (X-API-Key header) for protected endpoints
- **Response Format**: JSON
- **Rate Limiting**: None (local deployment)

## 🔐 **Authentication**

### **Protected Endpoints**
The following endpoints require authentication:
- `POST /api/legislation/refresh`

### **Authentication Method**
Include your API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-api-key-here" \
     -H "Content-Type: application/json" \
     -X POST "http://localhost:8000/api/legislation/refresh"
```

### **Default API Key**
- **Development**: `your-secret-api-key-here`
- **Production**: Set `API_KEY` environment variable

### **Setting Custom API Key**
```bash
# Local development
export API_KEY="your-custom-key-here"

# Vercel deployment
# Set in Vercel dashboard: Settings → Environment Variables
```

## 📚 **Endpoint Reference**

### **1. Home Page**

#### **GET /**
Serves the interactive web interface.

**Response**: HTML content
**Authentication**: Not required

**Example**:
```bash
curl http://localhost:8000/
```

---

### **2. Legislation Data**

#### **GET /api/legislation**
Retrieves all legislation data from the local database.

**Response**: JSON with total count, current year, and scraped data
**Authentication**: Not required

**Response Format**:
```json
{
  "total_count": 150,
  "current_year": 2025,
  "data": [
    {
      "law_number": "03.25",
      "title": "Law Title",
      "stage": "Lecture 1",
      "commission": "Commission Name",
      "ministry": "Ministry Name",
      "url": "https://parliament.ma/...",
      "pdf_url": "https://parliament.ma/pdf/...",
      "scraped_at": "2024-01-15T10:30:00Z",
      "premiere_lecture": { ... },
      "deuxieme_lecture": { ... }
    }
  ]
}
```

**Example**:
```bash
curl http://localhost:8000/api/legislation
```

---

#### **GET /api/legislation/{stage}**
Filters legislation by parliamentary stage.

**Parameters**:
- `stage` (path): Legislative stage (1 = Lecture 1, 2 = Lecture 2)

**Response**: JSON array of legislation items
**Authentication**: Not required

**Example**:
```bash
# Get first reading items
curl http://localhost:8000/api/legislation/1

# Get second reading items
curl http://localhost:8000/api/legislation/2
```

---

#### **GET /api/legislation/commission/{commission_id}**
Filters legislation by specific commission.

**Parameters**:
- `commission_id` (path): Commission ID (e.g., 65 for justice)

**Response**: JSON array of legislation items
**Authentication**: Not required

**Example**:
```bash
# Get justice commission legislation
curl http://localhost:8000/api/legislation/commission/65

# Get finance commission legislation
curl http://localhost:8000/api/legislation/commission/64
```

---

#### **GET /api/legislation/numero/{numero}**
Finds specific legislation by law number.

**Parameters**:
- `numero` (path): Law number (e.g., "123-45")

**Response**: Single legislation item or 404 if not found
**Authentication**: Not required

**Example**:
```bash
curl http://localhost:8000/api/legislation/numero/03.25
```

---

### **3. Commission Information**

#### **GET /api/commissions**
Retrieves list of all available parliamentary commissions.

**Response**: JSON array of commission objects
**Authentication**: Not required

**Response Format**:
```json
[
  {
    "id": "65",
    "name": "Commission de la justice, de la législation et des droits de l'homme"
  },
  {
    "id": "64",
    "name": "Commission des finances et du développement économique"
  }
]
```

**Example**:
```bash
curl http://localhost:8000/api/commissions
```

---

### **4. Data Refresh (Protected)**

#### **POST /api/legislation/refresh**
Triggers web scraping to refresh legislation data.

**Request Body**:
```json
{
  "max_pages": 5,
  "force_rescrape": false
}
```

**Parameters**:
- `max_pages` (integer, optional): Maximum pages to scrape (default: 5)
- `force_rescrape` (boolean, optional): Override existing data (default: false)

**Response**: JSON with operation status
**Authentication**: Required (X-API-Key header)

**Response Format**:
```json
{
  "success": true,
  "message": "Data refresh completed successfully",
  "scraped_items": 25,
  "skipped_items": 10,
  "total_pages": 3
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/legislation/refresh" \
     -H "X-API-Key: your-secret-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 3, "force_rescrape": true}'
```

---

### **5. API Status**

#### **GET /api/status**
Provides comprehensive API health status and endpoint documentation.

**Response**: JSON with API status and documentation
**Authentication**: Not required

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "database": {
    "status": "connected",
    "file_path": "data/extracted-data-2025.json",
    "last_updated": "2024-01-15T10:30:00Z"
  },
  "endpoints": {
    "public": [
      "GET / - Home page",
      "GET /api/legislation - All legislation",
      "GET /api/commissions - All commissions",
      "GET /api/legislation/{stage} - Legislation by stage",
      "GET /api/legislation/commission/{commission_id} - Legislation by commission",
      "GET /api/legislation/numero/{numero} - Legislation by number",
      "GET /api/status - API status"
    ],
    "protected": [
      "POST /api/legislation/refresh - Refresh data (requires API key)"
    ]
  },
  "configuration": {
    "api_key_required": true,
    "max_pages_default": 5,
    "force_rescrape_default": false
  }
}
```

**Example**:
```bash
curl http://localhost:8000/api/status
```

---

## 📊 **Data Models**

### **Legislation Item**
```json
{
  "law_number": "string",
  "title": "string",
  "stage": "string",
  "commission": "string",
  "commission_id": "string",
  "ministry": "string",
  "ministry_id": "string",
  "url": "string",
  "pdf_url": "string",
  "pdf_filename": "string",
  "scraped_at": "string (ISO 8601)",
  "page": "integer",
  "premiere_lecture": {
    "bureau_de_la_chambre": {
      "texte_source": "string",
      "date_depot": "string",
      "texte_depose": "string",
      "pdf_link": "string"
    },
    "commission": {
      "commission_name": "string",
      "submission_date": "string"
    }
  },
  "deuxieme_lecture": {
    "transfer_date": "string",
    "commission": {
      "commission_name": "string",
      "submission_date": "string"
    },
    "rapport_section": {
      "section_title": "string",
      "files": [
        {
          "title": "string",
          "pdf_url": "string",
          "filename": "string",
          "size": "string"
        }
      ]
    }
  }
}
```

### **Commission**
```json
{
  "id": "string",
  "name": "string"
}
```

### **Refresh Request**
```json
{
  "max_pages": "integer (optional)",
  "force_rescrape": "boolean (optional)"
}
```

### **Refresh Response**
```json
{
  "success": "boolean",
  "message": "string",
  "scraped_items": "integer",
  "skipped_items": "integer",
  "total_pages": "integer"
}
```

---

## 🔧 **Error Handling**

### **HTTP Status Codes**
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### **Error Response Format**
```json
{
  "detail": "Error description",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Common Error Scenarios**

#### **Missing API Key**
```json
{
  "detail": "API key required for this endpoint",
  "status_code": 401
}
```

#### **Invalid Commission ID**
```json
{
  "detail": "Commission not found",
  "status_code": 404
}
```

#### **Invalid Law Number**
```json
{
  "detail": "Legislation not found",
  "status_code": 404
}
```

---

## 📱 **Integration Examples**

### **JavaScript/Node.js**

#### **Fetch All Legislation**
```javascript
async function fetchLegislation() {
  try {
    const response = await fetch('http://localhost:8000/api/legislation');
    const data = await response.json();
    console.log(`Total items: ${data.total_count}`);
    return data.data;
  } catch (error) {
    console.error('Error fetching legislation:', error);
  }
}
```

#### **Refresh Data with Authentication**
```javascript
async function refreshData(apiKey, maxPages = 5) {
  try {
    const response = await fetch('http://localhost:8000/api/legislation/refresh', {
      method: 'POST',
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ max_pages: maxPages })
    });
    
    const result = await response.json();
    console.log('Refresh result:', result);
    return result;
  } catch (error) {
    console.error('Error refreshing data:', error);
  }
}
```

#### **Filter by Commission**
```javascript
async function getCommissionLegislation(commissionId) {
  try {
    const response = await fetch(`http://localhost:8000/api/legislation/commission/${commissionId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching commission data:', error);
  }
}
```

### **Python**

#### **Using requests library**
```python
import requests

# Fetch all legislation
response = requests.get('http://localhost:8000/api/legislation')
legislation = response.json()

# Refresh data with authentication
headers = {'X-API-Key': 'your-secret-api-key-here'}
data = {'max_pages': 3, 'force_rescrape': False}
response = requests.post('http://localhost:8000/api/legislation/refresh', 
                        headers=headers, json=data)
result = response.json()

# Filter by stage
response = requests.get('http://localhost:8000/api/legislation/1')
lecture1_items = response.json()
```

#### **Using aiohttp (async)**
```python
import aiohttp
import asyncio

async def fetch_legislation():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/api/legislation') as response:
            data = await response.json()
            return data

# Run the async function
legislation = asyncio.run(fetch_legislation())
```

### **cURL Examples**

#### **Basic Data Retrieval**
```bash
# Get all legislation
curl http://localhost:8000/api/legislation

# Get first reading items
curl http://localhost:8000/api/legislation/1

# Get justice commission items
curl http://localhost:8000/api/legislation/commission/65

# Find specific law
curl http://localhost:8000/api/legislation/numero/03.25
```

#### **Protected Operations**
```bash
# Refresh data (requires API key)
curl -X POST "http://localhost:8000/api/legislation/refresh" \
     -H "X-API-Key: your-secret-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 5, "force_rescrape": false}'
```

---

## 🚀 **Performance Tips**

### **Client-Side Optimization**
- Use pagination if implemented in future versions
- Implement client-side caching for frequently accessed data
- Use appropriate HTTP methods (GET for data retrieval, POST for operations)

### **Rate Limiting**
- The API currently has no rate limiting
- Be respectful with scraping operations
- Consider implementing delays between requests in your client code

### **Caching Strategies**
- Cache commission lists (rarely changes)
- Cache legislation data with appropriate TTL
- Use ETags if implemented in future versions

---

## 🔮 **Future Enhancements**

### **Planned Features**
- **Pagination**: Large dataset handling
- **Search API**: Full-text search capabilities
- **Webhooks**: Real-time notifications
- **Rate Limiting**: API usage controls
- **Caching Headers**: ETags and cache control
- **Bulk Operations**: Multiple item operations

### **API Versioning**
- Current: v1.0.0
- Future versions will maintain backward compatibility
- Deprecation notices will be provided in advance

---

## 🆘 **Support & Troubleshooting**

### **Common Issues**

#### **CORS Errors**
If you're getting CORS errors from a web application:
- The API includes CORS middleware
- Ensure your request includes proper headers
- Check if your domain is in the allowed origins

#### **Import Errors**
If you encounter import errors when running the API:
```bash
cd api
python3 -c "from main import app; print('OK')"
```

#### **Authentication Issues**
- Verify API key is correct
- Check `X-API-Key` header is present
- Ensure environment variable is set correctly

### **Getting Help**
- **API Documentation**: `/docs` endpoint (Swagger UI)
- **ReDoc Documentation**: `/redoc` endpoint
- **Status Endpoint**: `/api/status` for comprehensive info
- **GitHub Issues**: Report bugs and request features

---

**🎯 This API provides a clean, RESTful interface to Moroccan Parliament legislation data with comprehensive documentation and examples for easy integration.**
