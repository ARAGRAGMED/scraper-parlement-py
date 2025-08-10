# Moroccan Parliament Legislation API

## 🏗️ **New Modular Structure**

The API has been refactored from a monolithic `index.py` file into a well-organized, maintainable structure.

## 📁 **Directory Structure**

```
api/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI app initialization and configuration
├── index.py                    # Backward compatibility entry point
├── app.py                      # Alternative entry point
├── routes/                     # API endpoint definitions
│   ├── __init__.py
│   ├── legislation.py          # Legislation-related endpoints
│   ├── commissions.py          # Commission-related endpoints
│   ├── scraping.py             # Scraping endpoints (protected)
│   └── status.py               # Status and health endpoints
├── services/                   # Business logic layer
│   ├── __init__.py
│   ├── data_service.py         # Data file operations
│   └── scraping_service.py     # Scraping operations
├── models/                     # Request/Response models
│   ├── __init__.py
│   └── requests.py             # Request models
├── middleware/                 # Middleware components
│   ├── __init__.py
│   └── auth.py                 # API key authentication
├── utils/                      # Utility functions
│   ├── __init__.py
│   └── helpers.py              # Helper functions
└── static/                     # Frontend assets
    └── index.html              # Main frontend interface
```

## 🔄 **Migration from Old Structure**

### **Before (Monolithic)**
- All code was in `api/index.py` (1689 lines)
- Mixed concerns: HTML frontend, API endpoints, business logic
- Hard to maintain and debug
- Difficult to extend

### **After (Modular)**
- **Separation of Concerns**: Each file has a single responsibility
- **Maintainability**: Easy to find and modify specific functionality
- **Extensibility**: Simple to add new features
- **Testing**: Individual components can be tested separately
- **Team Development**: Multiple developers can work on different parts

## 🚀 **How to Use**

### **1. Run the API**
```bash
# Option 1: Using the new structure
cd api
python -m uvicorn main:app --reload

# Option 2: Using the backward-compatible index.py
cd api
python -m uvicorn index:app --reload

# Option 3: Direct execution
cd api
python app.py
```

### **2. Access Endpoints**
- **Frontend**: `http://localhost:8000/`
- **API Documentation**: `http://localhost:8000/docs`
- **Status**: `http://localhost:8000/api/status`
- **Legislation**: `http://localhost:8000/api/legislation`

## 🔐 **Authentication**

The `/api/legislation/refresh` endpoint is protected and requires an API key:

```bash
curl -X POST "http://localhost:8000/api/legislation/refresh" \
     -H "X-API-Key: your-secret-api-key-here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 5, "force_rescrape": false}'
```

## 📊 **API Endpoints**

### **Public Endpoints**
- `GET /api/legislation` - Get all legislation
- `GET /api/legislation/{stage}` - Get by stage (1 or 2)
- `GET /api/legislation/commission/{id}` - Get by commission
- `GET /api/legislation/numero/{numero}` - Get by law number
- `GET /api/commissions` - Get all commissions
- `GET /api/status` - API status and documentation

### **Protected Endpoints**
- `POST /api/legislation/refresh` - Refresh data (requires API key)

## 🛠️ **Development Workflow**

### **Adding New Endpoints**
1. Create route in `api/routes/`
2. Add business logic in `api/services/`
3. Define models in `api/models/`
4. Include router in `api/main.py`

### **Example: Adding a New Commission Endpoint**
```python
# api/routes/commissions.py
@router.get("/commissions/{commission_id}/stats")
async def get_commission_stats(commission_id: str):
    return commission_service.get_stats(commission_id)

# api/services/commission_service.py
class CommissionService:
    @staticmethod
    def get_stats(commission_id: str):
        # Business logic here
        pass
```

## 🔍 **Key Benefits of New Structure**

1. **Maintainability**: Each file is focused and manageable
2. **Readability**: Clear separation of concerns
3. **Scalability**: Easy to add new features
4. **Testing**: Components can be tested in isolation
5. **Documentation**: Self-documenting structure
6. **Team Development**: Multiple developers can work simultaneously
7. **Code Reuse**: Services can be shared between routes
8. **Error Handling**: Centralized error handling in services

## 📝 **Backward Compatibility**

The old `index.py` has been preserved as `index.py.backup` and replaced with a simple import that maintains the same API interface. All existing functionality is preserved.

## 🚨 **Important Notes**

- **No features were removed** - all functionality is preserved
- **API endpoints remain the same** - no breaking changes
- **Frontend interface is identical** - same user experience
- **Scraping functionality is unchanged** - same behavior
- **Authentication remains the same** - same security model

## 🔧 **Troubleshooting**

### **Import Errors**
If you encounter import errors, ensure you're running from the correct directory:
```bash
cd /path/to/scrap-parlement
python -m uvicorn api.main:app --reload
```

### **Module Not Found**
Check that all `__init__.py` files exist in the directory structure.

### **Backward Compatibility Issues**
If you need the old monolithic structure, restore from backup:
```bash
cp api/index.py.backup api/index.py
```

## 📚 **Next Steps**

1. **Test the new structure** with your existing workflows
2. **Add new features** using the modular approach
3. **Customize the frontend** in `api/static/index.html`
4. **Extend the API** by adding new routes and services
5. **Implement caching** in the services layer if needed
6. **Add logging** to track API usage and errors

---

**The refactoring is complete!** Your API is now more maintainable, extensible, and developer-friendly while preserving all existing functionality.
