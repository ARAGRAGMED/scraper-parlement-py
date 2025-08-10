# 🇲🇦 Moroccan Parliament Legislation API

A modern, modular FastAPI application for scraping and serving Moroccan Parliament legislation data with a clean, maintainable architecture.

## 🏗️ **Architecture Overview**

The API has been refactored from a monolithic structure into a well-organized, maintainable modular architecture:

```
api/
├── main.py              # Main FastAPI application entry point
├── index.py             # Backward compatibility entry point
├── routes/              # API endpoint definitions
│   ├── legislation.py   # Legislation data endpoints
│   ├── commissions.py   # Commission information endpoints
│   ├── scraping.py      # Data refresh/scraping endpoints
│   └── status.py        # API health and documentation endpoints
├── services/            # Business logic layer
│   ├── data_service.py  # Data retrieval and filtering
│   └── scraping_service.py # Web scraping operations
├── models/              # Data models and validation
│   └── requests.py      # Request/response models
├── middleware/          # Authentication and middleware
│   └── auth.py         # API key authentication
├── utils/               # Utility functions
│   └── helpers.py      # Helper functions
└── static/              # Frontend assets
    └── index.html       # Interactive web interface
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Installation**
```bash
# Clone the repository
git clone <your-repo-url>
cd scrap-parlement

# Install dependencies
pip install -r requirements.txt
```

### **Running the API**
```bash
# Navigate to API directory
cd api

# Start the server
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Or use the backward-compatible entry point
python3 -m uvicorn index:app --host 0.0.0.0 --port 8000
```

### **Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Interactive Frontend**: http://localhost:8000/
- **ReDoc Documentation**: http://localhost:8000/redoc

## 📚 **API Endpoints**

### **Public Endpoints**

#### **GET /** - Home Page
- Serves the interactive web interface
- No authentication required

#### **GET /api/legislation** - All Legislation
- Returns all legislation data from local database
- Response includes total count, current year, and scraped data

#### **GET /api/commissions** - All Commissions
- Returns list of all available parliamentary commissions
- Includes commission IDs and names

#### **GET /api/legislation/{stage}** - Legislation by Stage
- Filter legislation by stage (1 = Lecture 1, 2 = Lecture 2)
- Example: `/api/legislation/1` for first reading items

#### **GET /api/legislation/commission/{commission_id}** - Legislation by Commission
- Filter legislation by specific commission
- Example: `/api/legislation/commission/65` for justice commission

#### **GET /api/legislation/numero/{numero}** - Legislation by Law Number
- Find specific legislation by law number
- Example: `/api/legislation/numero/123-45`

#### **GET /api/status** - API Health & Documentation
- Comprehensive API status and endpoint documentation
- Database connection status and configuration info

### **Protected Endpoints**

#### **POST /api/legislation/refresh** - Refresh Data (🔒 Protected)
- Triggers web scraping to refresh legislation data
- **Authentication Required**: `X-API-Key` header
- **Request Body**:
  ```json
  {
    "max_pages": 5,
    "force_rescrape": false
  }
  ```

## 🔐 **Authentication**

Protected endpoints require an API key in the `X-API-Key` header:

```bash
curl -X POST "http://localhost:8000/api/legislation/refresh" \
     -H "X-API-Key: your-secret-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 3, "force_rescrape": true}'
```

**Default API Key**: `your-secret-api-key-here` (change in production)

## 🎯 **Key Features**

### **Data Management**
- **Dynamic Data Loading**: Automatically detects current legislative year
- **Smart Filtering**: Filter by stage, commission, or search terms
- **PDF Integration**: Direct links to legislation PDFs when available
- **Stage Tracking**: Detailed tracking of legislation through parliamentary stages

### **Web Scraping**
- **Intelligent Scraping**: Skips existing items for faster updates
- **Force Re-scraping**: Option to refresh all data
- **Vercel Compatibility**: Graceful handling of serverless limitations
- **Local Execution**: Full scraping capabilities when run locally

### **User Interface**
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Filters**: Real-time search and filtering
- **Collapsible Sections**: Detailed stage information on demand
- **Statistics Dashboard**: Overview of legislation counts and status

## 🛠️ **Development**

### **Project Structure Benefits**
- **Separation of Concerns**: Routes, services, and models are clearly separated
- **Easy Testing**: Each module can be tested independently
- **Maintainability**: Code is organized and easy to navigate
- **Extensibility**: New features can be added without affecting existing code

### **Adding New Endpoints**
1. Create new route in `api/routes/`
2. Add business logic in `api/services/`
3. Define models in `api/models/`
4. Include router in `api/main.py`

### **Adding New Services**
1. Create service class in `api/services/`
2. Implement business logic methods
3. Import and use in route handlers

## 🚀 **Deployment**

### **Local Development**
```bash
cd api
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Production (Vercel)**
The API is configured for Vercel deployment with:
- Serverless function optimization
- Automatic API documentation generation
- Static file serving for frontend

### **Environment Variables**
```bash
# Required for protected endpoints
API_KEY=your-production-api-key-here

# Vercel deployment
VERCEL=1
```

## 📊 **Data Structure**

### **Legislation Item**
```json
{
  "law_number": "123-45",
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
```

### **Stage Information**
```json
{
  "bureau_de_la_chambre": { ... },
  "commission": { ... },
  "seance_pleniere": { ... }
}
```

## 🔧 **Configuration**

### **Scraper Configuration**
- **Max Pages**: Limit pages to scrape (default: 5)
- **Force Re-scraping**: Override existing data (default: false)
- **Commission Mapping**: Predefined commission IDs and names

### **Data Storage**
- **Dynamic File Naming**: Based on current legislative year
- **JSON Format**: Structured data storage
- **Automatic Backup**: Original data preserved during updates

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Ensure you're in the api directory
cd api

# Test imports
python3 -c "from main import app; print('OK')"
```

#### **Authentication Issues**
- Verify API key is correct
- Check `X-API-Key` header is present
- Ensure API key environment variable is set

#### **Scraping Limitations on Vercel**
- Vercel has 60-second timeout limits
- Use existing data endpoints for production
- Run scraping locally for data updates

### **Debug Mode**
Open browser console and call:
```javascript
debugRapportSections()
```

## 📈 **Performance**

### **Optimizations**
- **Lazy Loading**: Data loaded on demand
- **Efficient Filtering**: Client-side filtering for better performance
- **Caching**: Static data served efficiently
- **Minimal Dependencies**: Lightweight, fast startup

### **Scalability**
- **Modular Design**: Easy to add new features
- **Stateless Architecture**: Suitable for horizontal scaling
- **API-First Design**: Can be consumed by multiple clients

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Follow the modular structure** for new code
4. **Test thoroughly** before submitting
5. **Submit pull request** with clear description

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

- **API Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues
- **Questions**: Check the comprehensive `/api/status` endpoint

---

**🎉 The refactoring is complete!** Your API is now more maintainable, extensible, and developer-friendly while preserving all existing functionality.
