# IBM Cloud Code Engine Deployment Guide

Complete step-by-step guide to deploy your Bank Employee Portal demo to IBM Cloud Code Engine.

## 📋 Prerequisites

- IBM Cloud account with Code Engine access
- IBM Cloud CLI installed
- Docker installed (for local testing - optional)
- Code Engine CLI plugin

---

## 🚀 Quick Deployment (3 Methods)

### Method 1: Using IBM Cloud Console (Easiest - No CLI Required)

#### Step 1: Prepare Your Code
Your code is already prepared with:
- ✅ `Dockerfile` - Container configuration
- ✅ `nginx.conf` - Web server configuration
- ✅ `.dockerignore` - Optimized build

#### Step 2: Create a GitHub Repository

1. **Initialize Git in HWBDemo folder:**
   ```bash
   cd HWBDemo
   git init
   git add .
   git commit -m "Initial commit - Bank Employee Portal"
   ```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name: `hwbdemo` (or your preferred name)
   - Make it Public or Private
   - Don't initialize with README (we already have files)
   - Click "Create repository"

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/hwbdemo.git
   git branch -M main
   git push -u origin main
   ```

#### Step 3: Deploy to Code Engine via Console

1. **Go to IBM Cloud Console:**
   - Navigate to https://cloud.ibm.com
   - Login with your IBM Cloud account

2. **Open Code Engine:**
   - Click the hamburger menu (☰) in top-left
   - Select "Code Engine"
   - Or search for "Code Engine" in the search bar

3. **Create a Project (if you don't have one):**
   - Click "Create project"
   - Name: `hwbdemo-project` (or your choice)
   - Select your resource group
   - Select location: `us-south` (or closest to you)
   - Click "Create"

4. **Create an Application:**
   - Inside your project, click "Applications"
   - Click "Create"
   - Choose "Source code" as the starting point

5. **Configure the Application:**
   
   **General:**
   - Name: `bank-portal-demo`
   - Choose "Source code" option
   
   **Code:**
   - Code repo URL: `https://github.com/YOUR_USERNAME/hwbdemo`
   - Branch name: `main`
   - Context directory: `/` (leave as root)
   
   **Strategy:**
   - Strategy: `Dockerfile`
   - Dockerfile: `Dockerfile` (default)
   - Timeout: `600` seconds
   
   **Output:**
   - Registry server: `us.icr.io` (or your region)
   - Registry access: Select your Container Registry
   - Namespace: Select or create a namespace (e.g., `hwbdemo`)
   - Repository: `bank-portal`
   - Tag: `latest`
   
   **Resources & scaling:**
   - CPU: `0.25 vCPU` (sufficient for demo)
   - Memory: `0.5 GB` (sufficient for demo)
   - Min instances: `0` (scales to zero when not in use - saves money!)
   - Max instances: `1` (or more if you expect high traffic)
   - Concurrency: `100`
   - Request timeout: `300` seconds
   
   **Optional - Domain mappings:**
   - Leave default (Code Engine will provide a URL)
   - Or add custom domain if you have one

6. **Create the Application:**
   - Review your settings
   - Click "Create"
   - Wait 3-5 minutes for the build and deployment

7. **Access Your Application:**
   - Once deployed, you'll see a green checkmark
   - Click on the application name
   - Find the "Application URL" (looks like: `https://bank-portal-demo.xxx.us-south.codeengine.appdomain.cloud`)
   - Your demo is live at: `[YOUR_URL]/login.html`

---

### Method 2: Using IBM Cloud CLI (Faster for Updates)

#### Step 1: Install IBM Cloud CLI

**macOS:**
```bash
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh
```

**Linux:**
```bash
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
```

**Windows:**
Download from: https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases

#### Step 2: Install Code Engine Plugin

```bash
ibmcloud plugin install code-engine
```

#### Step 3: Login to IBM Cloud

```bash
ibmcloud login
# Or with SSO:
ibmcloud login --sso
```

Select your account when prompted.

#### Step 4: Target Code Engine

```bash
# List your projects
ibmcloud ce project list

# Create a new project (if needed)
ibmcloud ce project create --name hwbdemo-project

# Target your project
ibmcloud ce project select --name hwbdemo-project
```

#### Step 5: Build and Deploy

**Option A: Build from GitHub (Recommended)**

```bash
cd HWBDemo

# Create application from GitHub
ibmcloud ce application create \
  --name bank-portal-demo \
  --build-source https://github.com/YOUR_USERNAME/hwbdemo \
  --build-context-dir . \
  --build-dockerfile Dockerfile \
  --port 8080 \
  --min-scale 0 \
  --max-scale 1 \
  --cpu 0.25 \
  --memory 0.5G
```

**Option B: Build from Local Directory**

```bash
cd HWBDemo

# Build and push image to IBM Container Registry
ibmcloud ce build create \
  --name bank-portal-build \
  --source . \
  --dockerfile Dockerfile \
  --image us.icr.io/YOUR_NAMESPACE/bank-portal:latest

# Create application from the image
ibmcloud ce application create \
  --name bank-portal-demo \
  --image us.icr.io/YOUR_NAMESPACE/bank-portal:latest \
  --port 8080 \
  --min-scale 0 \
  --max-scale 1 \
  --cpu 0.25 \
  --memory 0.5G
```

#### Step 6: Get Your Application URL

```bash
ibmcloud ce application get --name bank-portal-demo
```

Look for the URL in the output. Your demo is at: `[URL]/login.html`

---

### Method 3: Using Docker + IBM Container Registry

#### Step 1: Build Docker Image Locally

```bash
cd HWBDemo

# Build the image
docker build -t bank-portal:latest .

# Test locally (optional)
docker run -p 8080:8080 bank-portal:latest
# Visit http://localhost:8080/login.html
```

#### Step 2: Push to IBM Container Registry

```bash
# Login to IBM Cloud
ibmcloud login

# Target Container Registry
ibmcloud cr region-set us-south

# Create a namespace (if you don't have one)
ibmcloud cr namespace-add hwbdemo

# Tag your image
docker tag bank-portal:latest us.icr.io/hwbdemo/bank-portal:latest

# Login to Container Registry
ibmcloud cr login

# Push the image
docker push us.icr.io/hwbdemo/bank-portal:latest
```

#### Step 3: Deploy to Code Engine

```bash
# Select your Code Engine project
ibmcloud ce project select --name hwbdemo-project

# Create application from the image
ibmcloud ce application create \
  --name bank-portal-demo \
  --image us.icr.io/hwbdemo/bank-portal:latest \
  --port 8080 \
  --min-scale 0 \
  --max-scale 1 \
  --cpu 0.25 \
  --memory 0.5G \
  --registry-secret icr-secret
```

---

## 🔄 Updating Your Deployment

### Update via Console:
1. Go to Code Engine → Your Project → Applications
2. Click on your application
3. Click "Configuration" tab
4. Click "Edit and create new revision"
5. Make changes and click "Create"

### Update via CLI:

**If using GitHub source:**
```bash
# Just push changes to GitHub
cd HWBDemo
git add .
git commit -m "Update demo"
git push

# Trigger rebuild in Code Engine
ibmcloud ce application update --name bank-portal-demo --build-source https://github.com/YOUR_USERNAME/hwbdemo
```

**If using Container Registry:**
```bash
# Rebuild and push
cd HWBDemo
docker build -t us.icr.io/hwbdemo/bank-portal:latest .
docker push us.icr.io/hwbdemo/bank-portal:latest

# Update application
ibmcloud ce application update --name bank-portal-demo --image us.icr.io/hwbdemo/bank-portal:latest
```

---

## 💰 Cost Optimization

Code Engine pricing is based on:
- vCPU-seconds
- GB-seconds of memory
- HTTP requests

**Cost-Saving Tips:**

1. **Scale to Zero:** Set `min-scale: 0` so the app scales down when not in use
   ```bash
   ibmcloud ce application update --name bank-portal-demo --min-scale 0
   ```

2. **Right-Size Resources:** For a demo, 0.25 vCPU and 0.5GB memory is sufficient

3. **Free Tier:** IBM Cloud Code Engine includes:
   - First 100,000 vCPU-seconds per month FREE
   - First 200,000 GB-seconds per month FREE
   - First 100,000 HTTP requests per month FREE

**Estimated Cost for Demo:**
- With scale-to-zero and light usage: **$0-5/month**
- With constant running: **~$10-15/month**

---

## 🔒 Security & Custom Domain

### Add Custom Domain:

1. **Via Console:**
   - Go to your application
   - Click "Domain mappings"
   - Click "Create"
   - Enter your domain (e.g., `demo.yourdomain.com`)
   - Follow DNS configuration instructions

2. **Via CLI:**
   ```bash
   ibmcloud ce application bind --name bank-portal-demo --domain demo.yourdomain.com
   ```

### Enable HTTPS:
Code Engine automatically provides HTTPS for all applications (both default and custom domains).

---

## 🐛 Troubleshooting

### Application Won't Start:

**Check logs:**
```bash
ibmcloud ce application logs --name bank-portal-demo
```

**Common issues:**
- Port mismatch: Ensure Dockerfile exposes 8080
- Build failure: Check Dockerfile syntax
- Memory issues: Increase memory allocation

### Build Fails:

```bash
# Check build logs
ibmcloud ce build logs --name bank-portal-build

# Common fixes:
# - Verify Dockerfile exists
# - Check .dockerignore isn't excluding needed files
# - Ensure nginx.conf is present
```

### Can't Access Application:

```bash
# Check application status
ibmcloud ce application get --name bank-portal-demo

# Restart application
ibmcloud ce application update --name bank-portal-demo --rebuild
```

---

## 📊 Monitoring

### View Application Metrics:

**Via Console:**
1. Go to your application
2. Click "Monitoring" tab
3. View CPU, memory, and request metrics

**Via CLI:**
```bash
# Get application details
ibmcloud ce application get --name bank-portal-demo

# View recent logs
ibmcloud ce application logs --name bank-portal-demo --tail 100
```

---

## 🎯 Best Practices

1. **Use GitHub Integration:** Easiest for updates and version control
2. **Enable Scale-to-Zero:** Saves costs when demo isn't being used
3. **Set Resource Limits:** Prevents unexpected costs
4. **Use Tags:** Tag images with versions (e.g., `v1.0`, `v1.1`)
5. **Monitor Usage:** Check Code Engine dashboard regularly
6. **Backup Code:** Keep your code in GitHub

---

## 📧 Sharing with Clients

Once deployed, share:

**URL:** `https://your-app-url.codeengine.appdomain.cloud/login.html`

**Credentials:**
- Username: `demo`
- Password: `demo2024`

**Email Template:**
```
Subject: Bank Employee Portal Demo - Now Live on IBM Cloud

Hi [Client Name],

Your demo is now hosted on IBM Cloud Code Engine and available 24/7:

🔗 URL: https://your-app-url.codeengine.appdomain.cloud/login.html

🔐 Login:
   Username: demo
   Password: demo2024

This deployment includes:
✅ Enterprise-grade IBM Cloud infrastructure
✅ Automatic HTTPS encryption
✅ Auto-scaling based on demand
✅ 99.9% uptime SLA

The demo is ready for your review. Let me know if you have any questions!

Best regards,
[Your Name]
```

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] IBM Cloud account ready
- [ ] Code Engine project created
- [ ] Application deployed
- [ ] Application URL obtained
- [ ] Tested login functionality
- [ ] Tested chat widget
- [ ] Shared URL with clients
- [ ] Monitoring enabled

---

## 🆘 Support Resources

- **IBM Cloud Code Engine Docs:** https://cloud.ibm.com/docs/codeengine
- **IBM Cloud Support:** https://cloud.ibm.com/unifiedsupport/supportcenter
- **Code Engine CLI Reference:** https://cloud.ibm.com/docs/codeengine?topic=codeengine-cli

---

**Congratulations! Your demo is now running on enterprise-grade IBM Cloud infrastructure! 🎉**