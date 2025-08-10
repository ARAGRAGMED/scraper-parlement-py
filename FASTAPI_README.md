# 🏛️ Moroccan Parliament Legislation Scraper - FastAPI

## 📋 **Overview**

This FastAPI application provides a RESTful API for the Moroccan Parliament Legislation Scraper. It serves scraped legislation data through optimized endpoints and includes a web interface for data visualization.

## 🚀 **Deployment**

### **Vercel Deployment**
This application is deployed on Vercel as a serverless function.

- **Live URL**: https://scraper-parlement-py-aicx.vercel.app/
- **API Base**: https://scraper-parlement-py-aicx.vercel.app/api/
- **Web Viewer**: https://scraper-parlement-py-aicx.vercel.app/

### **Local Development** (Optional)
If you want to run locally for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
cd api
uvicorn index:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 **API Endpoints**

### **Core Endpoints**
- **`GET /api/health`** - Health check
- **`GET /api/legislation`** - Get all legislation data
- **`GET /api/legislation/{law_number}`** - Get specific law by number
- **`GET /api/legislation/stage/{stage}`** - Filter by legislative stage
- **`GET /api/legislation/commission/{commission_id}`** - Filter by commission
- **`GET /api/legislation/numero/{numero}`** - Get by law number
- **`POST /api/legislation/refresh`** - Refresh/scrape legislation data
- **`GET /api/status`** - Get API status and available endpoints

### **Data Management**
- **`GET /api/commissions`** - Get all commission data
- **`GET /api/legislation/current-year`** - Get current year legislation

## 🌐 **Web Interface Features**

### **Data Viewer**
- **Interactive Table**: Sortable and searchable legislation data
- **Stage Filtering**: Filter by legislative stage (Lecture 1, Lecture 2, etc.)
- **Commission Filtering**: Filter by parliamentary commission
- **Real-time Search**: Instant search across all fields

### **Data Refresh**
- **🔄 Refresh Button**: Update data from source using `/api/legislation/refresh`
- **Automatic Updates**: Data refreshes automatically after scraping
- **Progress Indicators**: Visual feedback during data operations

## 📊 **API Response Examples**

### **Legislation Data**
```json
{
  "current_year": "2024-2025",
  "total_items": 6,
  "scraped_at": "2025-08-08T01:22:32.235437",
  "data": [...]
}
```

### **Refresh Response**
```json
{
  "status": "success",
  "message": "Data refreshed successfully",
  "data": {
    "total_items": 6,
    "scraped_at": "2025-08-10T14:45:21.588700"
  }
}
```

## 🔒 **Serverless Limitations**

**Note**: When deployed on Vercel, the `/api/legislation/refresh` endpoint has limitations:
- **Timeout**: 60 seconds maximum execution time
- **Memory**: 1024MB maximum memory usage
- **File System**: Read-only access (cannot write new data files)
- **Scope**: Limited to 5 pages for safety

For full scraping capabilities, use the local scraper script:
```bash
python run_scraper.py
```

## 📁 **Project Structure**

```
scrap-parlement/
├── api/
│   └── index.py          # Vercel serverless function (FastAPI)
├── src/
│   └── moroccan_parliament_scraper/  # Core scraper module
├── data/                 # Scraped data storage
├── config/               # Configuration files
├── dynamic_viewer.html   # Web interface
└── vercel.json          # Vercel deployment config
```

## 🚀 **Quick Start**

1. **Access the Web Interface**: Visit https://scraper-parlement-py-aicx.vercel.app/
2. **View Data**: Browse legislation data in the interactive table
3. **Refresh Data**: Use the refresh button to update from source
4. **API Access**: Use the endpoints above for programmatic access

## 📚 **Documentation**

- **API Docs**: https://scraper-parlement-py-aicx.vercel.app/docs
- **ReDoc**: https://scraper-parlement-py-aicx.vercel.app/redoc
- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **Vercel Deployment**: See `VERCEL_DEPLOY.md`
