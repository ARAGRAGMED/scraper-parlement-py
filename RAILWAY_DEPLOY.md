# 🚀 Railway Deployment Guide

## 📋 **Prerequisites**

1. **GitHub Account** with your repository
2. **Railway Account** (free tier available)
3. **Git installed** on your machine

## 🚀 **Deployment Steps**

### **Step 1: Connect Railway to GitHub**

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository: `ARAGRAGMED/scraper-parlement-py`

### **Step 2: Configure Environment**

Railway will automatically detect your Python project and use the configuration files:
- `railway.toml` - Railway-specific configuration
- `Procfile` - Alternative process definition
- `runtime.txt` - Python version specification
- `Dockerfile` - Container configuration

### **Step 3: Deploy**

1. Railway will automatically build and deploy your app
2. Wait for the build to complete (usually 2-5 minutes)
3. Your app will be available at a Railway-provided URL

### **Step 4: Configure Environment Variables (Optional)**

In Railway dashboard, you can set:
- `PYTHON_VERSION` = `3.11`
- `PORT` = `8000` (Railway sets this automatically)

## 🔧 **Configuration Files Explained**

### **`railway.toml`**
```toml
[build]
builder = "nixpacks"  # Uses Railway's smart builder

[deploy]
startCommand = "python api.py"  # How to start your app
healthcheckPath = "/api/health"  # Health check endpoint
healthcheckTimeout = 300  # 5 minutes timeout
restartPolicyType = "on_failure"  # Auto-restart on failure

[env]
PYTHON_VERSION = "3.11"  # Python version
```

### **`Procfile`**
```
web: python api.py
```
Alternative way to specify the start command.

### **`Dockerfile`**
- Creates a lightweight Python container
- Installs dependencies
- Sets up health checks
- Exposes port 8000

## 🌐 **Accessing Your Deployed App**

After deployment, you'll get:
- **Main App**: `https://your-app-name.railway.app`
- **API Docs**: `https://your-app-name.railway.app/docs`
- **Health Check**: `https://your-app-name.railway.app/api/health`

## 📊 **Monitoring & Logs**

### **Railway Dashboard**
- View real-time logs
- Monitor resource usage
- Check deployment status
- View environment variables

### **Health Checks**
Your app includes health checks at `/api/health` that Railway uses to:
- Monitor app health
- Auto-restart on failures
- Provide status information

## 🔄 **Updating Your App**

### **Automatic Updates**
Railway automatically redeploys when you push to your main branch.

### **Manual Updates**
1. Push changes to GitHub
2. Railway detects changes
3. Automatically rebuilds and redeploys
4. Zero-downtime updates

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Build Failures**
   - Check Railway logs for error details
   - Verify all dependencies in `requirements.txt`
   - Ensure Python version compatibility

2. **Runtime Errors**
   - Check application logs in Railway dashboard
   - Verify environment variables
   - Check file paths and permissions

3. **Health Check Failures**
   - Ensure `/api/health` endpoint works
   - Check if app is binding to correct port
   - Verify startup command in `railway.toml`

### **Useful Commands**

```bash
# Check local build
docker build -t scraper-parlement .

# Test locally with Railway's port
PORT=8000 python api.py

# Check health endpoint
curl http://localhost:8000/api/health
```

## 💰 **Costs & Limits**

### **Free Tier**
- **Deployments**: Unlimited
- **Bandwidth**: 100GB/month
- **Build Time**: 500 minutes/month
- **Sleep**: Apps sleep after 5 minutes of inactivity

### **Paid Plans**
- **Starter**: $5/month - No sleep, more resources
- **Pro**: $20/month - Production-ready features

## 🎯 **Next Steps After Deployment**

1. **Test all endpoints** using the Railway URL
2. **Set up custom domain** (optional)
3. **Configure monitoring** and alerts
4. **Set up CI/CD** for automated testing
5. **Monitor performance** and optimize

## 📞 **Support**

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Community**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Report bugs in your repository

---

**🎉 Your Moroccan Parliament Scraper is now ready for cloud deployment on Railway!**
