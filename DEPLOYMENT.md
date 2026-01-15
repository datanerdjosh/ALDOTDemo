# HWBDemo Deployment Guide

This guide explains how to deploy and share your Bank Employee Portal demo with clients.

## 📋 Table of Contents
1. [Quick Local Testing](#quick-local-testing)
2. [Deployment Options](#deployment-options)
3. [User Credentials](#user-credentials)
4. [Customization](#customization)

---

## 🚀 Quick Local Testing

Before deploying, test locally:

```bash
cd HWBDemo
python3 -m http.server 8000
```

Then visit: http://localhost:8000/login.html

---

## 🌐 Deployment Options

### Option 1: Cloudflare Pages (Recommended - FREE)

**Pros:** Free, fast, HTTPS included, custom domain support
**Steps:**

1. **Create a GitHub repository:**
   ```bash
   cd HWBDemo
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/hwbdemo.git
   git push -u origin main
   ```

2. **Deploy to Cloudflare Pages:**
   - Go to https://pages.cloudflare.com
   - Sign up/login (free account)
   - Click "Create a project"
   - Connect your GitHub account
   - Select your repository
   - Build settings:
     - Framework preset: None
     - Build command: (leave empty)
     - Build output directory: `/`
   - Click "Save and Deploy"

3. **Your demo will be live at:**
   `https://hwbdemo.pages.dev` (or your custom domain)

4. **Share with clients:**
   - URL: `https://hwbdemo.pages.dev/login.html`
   - Username: `demo`
   - Password: `demo2024`

---

### Option 2: Netlify (FREE)

**Pros:** Free, easy drag-and-drop, HTTPS included

1. **Go to:** https://app.netlify.com
2. **Sign up/login** (free account)
3. **Drag and drop** the entire HWBDemo folder onto Netlify
4. **Your site is live!** You'll get a URL like: `https://random-name-123.netlify.app`
5. **Optional:** Set up a custom domain in Site settings

**Share with clients:**
- URL: `https://your-site-name.netlify.app/login.html`
- Credentials provided below

---

### Option 3: Vercel (FREE)

**Pros:** Free, fast, great for demos

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd HWBDemo
   vercel
   ```

3. **Follow prompts** (first time setup)
4. **Your demo is live!** You'll get a URL like: `https://hwbdemo.vercel.app`

---

### Option 4: GitHub Pages (FREE)

**Pros:** Free, integrated with GitHub

1. **Create a GitHub repository** (see Option 1, step 1)

2. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, folder: / (root)
   - Click Save

3. **Your site will be live at:**
   `https://YOUR_USERNAME.github.io/hwbdemo/login.html`

---

### Option 5: ngrok (Quick Temporary Share)

**Pros:** Instant sharing from your local machine
**Cons:** Temporary URL, requires keeping your computer running

1. **Install ngrok:** https://ngrok.com/download

2. **Start your local server:**
   ```bash
   cd HWBDemo
   python3 -m http.server 8000
   ```

3. **In another terminal, run ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Share the HTTPS URL** shown (e.g., `https://abc123.ngrok.io/login.html`)

**Note:** Free ngrok URLs expire after 2 hours. For longer demos, use paid ngrok or other options.

---

### Option 6: Your Own Server (VPS/Cloud)

If you have a server (AWS, DigitalOcean, etc.):

1. **Upload files via SCP:**
   ```bash
   scp -r HWBDemo/* user@your-server.com:/var/www/html/hwbdemo/
   ```

2. **Configure web server** (Apache/Nginx) to serve the directory

3. **Set up HTTPS** with Let's Encrypt:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 🔐 User Credentials

### Default Demo Accounts

You can provide these credentials to clients:

| Username | Password | Purpose |
|----------|----------|---------|
| `demo` | `demo2024` | General demo access |
| `client` | `client2024` | Client-specific demo |
| `admin` | `admin2024` | Admin demo access |

### Adding More Users

Edit `auth.js` and add users to the `DEMO_USERS` object:

```javascript
const DEMO_USERS = {
    'demo': 'demo2024',
    'client': 'client2024',
    'admin': 'admin2024',
    'newuser': 'password123',  // Add new users here
    'client2': 'secure2024'
};
```

**Security Note:** This is a simple demo authentication system. For production use, implement proper backend authentication with encrypted passwords.

---

## 🎨 Customization

### Change Demo Credentials Display

Edit `login.html` to show/hide demo credentials:

```html
<!-- Remove or comment out this section to hide credentials -->
<div class="demo-credentials">
    <p><strong>Demo Credentials:</strong></p>
    <p>Username: <code>demo</code></p>
    <p>Password: <code>demo2024</code></p>
</div>
```

### Update Branding

1. **Change bank name:** Edit the `<h1>` tags in `login.html` and `index.html`
2. **Update colors:** Modify CSS variables in `styles.css` and `login-styles.css`
3. **Add logo:** Replace the 🏦 emoji with an `<img>` tag

### Customize Chat Widget

Edit `index.html` to modify chat appearance:

```javascript
style: {
    headerColor: '#1e3c72',              // Chat header color
    userMessageBackgroundColor: '#2a5298', // User message bubble
    primaryColor: '#667eea',              // Interactive elements
    showBackgroundGradient: true
},
layout: {
    form: 'float',        // 'float' | 'fullscreen-overlay' | 'custom'
    width: '400px',       // Chat window width
    height: '600px',      // Chat window height
    showOrchestrateHeader: true
}
```

---

## 📧 Sharing with Clients

### Email Template

```
Subject: Bank Employee Portal Demo - Access Information

Hi [Client Name],

I'm excited to share our Bank Employee Portal demo with you. This demo showcases 
how our AI-powered assistant can help bank employees with their daily tasks.

🔗 Demo URL: [YOUR_DEPLOYED_URL]/login.html

🔐 Login Credentials:
   Username: demo
   Password: demo2024

💡 What to Try:
   • Ask the AI assistant about customer account inquiries
   • Explore the quick action cards on the dashboard
   • Test the chat functionality with various banking questions

The demo is available 24/7 and you can access it from any device with a web browser.

Please let me know if you have any questions or would like to schedule a walkthrough.

Best regards,
[Your Name]
```

---

## 🔒 Security Considerations

### For Demo Environments:
- ✅ Current setup is appropriate for demos
- ✅ Session-based authentication (clears on browser close)
- ✅ No sensitive data exposed

### For Production:
- ❌ Do NOT use this authentication system
- ✅ Implement proper backend authentication
- ✅ Use HTTPS (all deployment options above provide this)
- ✅ Store passwords encrypted in a database
- ✅ Implement rate limiting
- ✅ Add CSRF protection
- ✅ Use secure session management

---

## 🐛 Troubleshooting

### Chat Widget Not Loading
- Check browser console for errors
- Verify IBM watsonx Orchestrate security is disabled
- Ensure you're accessing via HTTPS (not HTTP)

### Login Not Working
- Clear browser cache and cookies
- Check that `auth.js` is loading (browser dev tools → Network tab)
- Verify credentials match those in `auth.js`

### Deployment Issues
- Ensure all files are uploaded (check file list)
- Verify `login.html` is set as the entry point
- Check that file paths are relative (no absolute paths)

---

## 📞 Support

For issues or questions:
1. Check browser console for errors (F12 → Console)
2. Verify all files are present in deployment
3. Test locally first before deploying
4. Contact your IBM watsonx Orchestrate support team for chat widget issues

---

## ✅ Pre-Deployment Checklist

- [ ] Test login locally
- [ ] Verify chat widget loads and responds
- [ ] Test on mobile device
- [ ] Update demo credentials if needed
- [ ] Customize branding (optional)
- [ ] Choose deployment platform
- [ ] Deploy and test live URL
- [ ] Prepare client communication
- [ ] Share URL and credentials with clients

---

**Recommended:** Start with Cloudflare Pages or Netlify for the easiest, free deployment with HTTPS included.