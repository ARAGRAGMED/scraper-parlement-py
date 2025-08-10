# 🚀 Vercel Deployment Guide (Python)

## 📋 **Prerequisites**

1. **GitHub Account** with your repository
2. **Vercel Account** (free tier available)
3. **Vercel CLI** installed (optional but recommended)

## 🚀 **Deployment Steps**

### **Step 1: Install Vercel CLI (Optional)**

```bash
npm i -g vercel
```

### **Step 2: Deploy from Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click **"New Project"**
4. Import your repository: `ARAGRAGMED/scraper-parlement-py`
5. Vercel will automatically detect it's a Python project

### **Step 3: Configure Build Settings**

Vercel will use these files automatically:
- **`vercel.json`** - Project configuration
- **`api/index.py`** - Main serverless function
- **`api/requirements.txt`** - Python dependencies

### **Step 4: Deploy**

1. Click **"Deploy"**
2. Wait for build to complete (usually 2-3 minutes)
3. Your app will be available at a Vercel URL

## 🔧 **Configuration Files Explained**

### **`vercel.json`**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"  // Python runtime
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"  // Route API calls
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"  // Route everything else
    }
  ]
}
```

### **`api/index.py`**
- **FastAPI app** wrapped for Vercel
- **Serverless function** entry point
- **Sample data** for Vercel's stateless environment

### **`api/requirements.txt`**
- **FastAPI** and dependencies
- **Mangum** for AWS Lambda compatibility
- **Scraping libraries** for functionality

## 🌐 **Accessing Your Deployed App**

After deployment, you'll get:
- **Main App**: `https://your-app-name.vercel.app`
- **API Docs**: `https://your-app-name.vercel.app/docs`
- **Health Check**: `https://your-app-name.vercel.app/api/health`

## ⚠️ **Vercel Limitations & Solutions**

### **No Persistent File Storage**
- **Problem**: Vercel is serverless, no file persistence
- **Solution**: Returns sample data with explanatory notes

### **No Background Tasks**
- **Problem**: Can't run long-running scraping processes
- **Solution**: Scraping endpoint returns success message with limitations

### **Function Timeout**
- **Problem**: 30-second function timeout
- **Solution**: Optimized for quick responses

## 🔄 **Updating Your App**

### **Automatic Updates**
Vercel automatically redeploys when you push to your main branch.

### **Manual Updates**
1. Push changes to GitHub
2. Vercel detects changes
3. Automatically rebuilds and redeploys
4. Zero-downtime updates

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Build Failures**
   - Check Vercel build logs
   - Verify Python version compatibility
   - Ensure all dependencies are in `api/requirements.txt`

2. **Import Errors**
   - Check `sys.path.insert()` in `api/index.py`
   - Verify file structure matches imports

3. **Function Timeouts**
   - Optimize response times
   - Use caching where possible
   - Consider breaking large operations

### **Useful Commands**

```bash
# Test locally with Vercel
vercel dev

# Deploy manually
vercel --prod

# Check deployment status
vercel ls
```

## 💰 **Costs & Limits**

### **Free Tier**
- **Deployments**: Unlimited
- **Bandwidth**: 100GB/month
- **Function Execution**: 100GB-hours/month
- **Function Timeout**: 30 seconds

### **Pro Plan**
- **$20/month** - Higher limits, custom domains, team features

## 🎯 **Next Steps After Deployment**

1. **Test all endpoints** using the Vercel URL
2. **Set up custom domain** (optional)
3. **Configure monitoring** and alerts
4. **Set up CI/CD** for automated testing
5. **Monitor performance** and optimize

## 🔄 **Alternative: Full Functionality with Railway**

If you need **full scraping functionality** with **persistent storage**:

1. **Use Railway** instead of Vercel
2. **Full Python support** with file storage
3. **Background task support** for scraping
4. **Persistent data storage**

## 📞 **Support**

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Python Runtime**: [vercel.com/docs/functions/serverless-functions/runtimes/python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

---

**🎉 Your Moroccan Parliament Scraper is now ready for Vercel deployment!**

**Note**: This Vercel version provides the API structure but with sample data due to Vercel's stateless nature. For full scraping functionality, consider Railway deployment.
