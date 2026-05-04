# 🌐 Chrome Extension Development Guide

## Sam Job Automator - Browser Extension

### Overview
Chrome extension to apply to jobs with one click from any job site.

---

## 🎯 Features

### Core Features:
1. **One-Click Apply**
   - Detect job postings
   - Extract job details
   - Apply automatically

2. **Auto-Fill Forms**
   - Fill application forms
   - Upload CV automatically
   - Submit applications

3. **Job Scraping**
   - Extract from any site
   - Save to database
   - Analyze with AI

4. **Quick Actions**
   - Save job for later
   - Mark as applied
   - Add notes

5. **Statistics**
   - Track applications
   - View success rate
   - See timeline

---

## 📁 Extension Structure

```
sam-job-automator-extension/
├── manifest.json
├── popup/
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── content/
│   ├── content.js
│   └── content.css
├── background/
│   └── background.js
├── icons/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── utils/
    ├── api.js
    └── scraper.js
```

---

## 📝 manifest.json

```json
{
  "manifest_version": 3,
  "name": "Sam Job Automator",
  "version": "1.0.0",
  "description": "Apply to jobs with one click!",
  "permissions": [
    "activeTab",
    "storage",
    "notifications"
  ],
  "host_permissions": [
    "https://*.linkedin.com/*",
    "https://*.indeed.com/*",
    "https://*.bayt.com/*",
    "https://*.glassdoor.com/*"
  ],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  },
  "content_scripts": [
    {
      "matches": [
        "https://*.linkedin.com/jobs/*",
        "https://*.indeed.com/viewjob*",
        "https://*.bayt.com/*/jobs/*"
      ],
      "js": ["content/content.js"],
      "css": ["content/content.css"]
    }
  ],
  "background": {
    "service_worker": "background/background.js"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

---

## 🎨 popup.html

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sam Job Automator</title>
  <link rel="stylesheet" href="popup.css">
</head>
<body>
  <div class="container">
    <h1>🚀 Sam Job Automator</h1>
    
    <div class="stats">
      <div class="stat-card">
        <div class="stat-number" id="totalApps">0</div>
        <div class="stat-label">Applications</div>
      </div>
      <div class="stat-card">
        <div class="stat-number" id="responses">0</div>
        <div class="stat-label">Responses</div>
      </div>
    </div>
    
    <div class="actions">
      <button id="applyBtn" class="btn btn-primary">
        ✉️ Apply to This Job
      </button>
      <button id="saveBtn" class="btn btn-secondary">
        💾 Save for Later
      </button>
      <button id="analyzeBtn" class="btn btn-secondary">
        🤖 AI Analysis
      </button>
    </div>
    
    <div class="job-info" id="jobInfo">
      <h3>Current Job:</h3>
      <p id="jobTitle">No job detected</p>
      <p id="jobCompany"></p>
      <p id="jobLocation"></p>
    </div>
    
    <div class="settings">
      <a href="#" id="settingsLink">⚙️ Settings</a>
      <a href="#" id="dashboardLink">📊 Dashboard</a>
    </div>
  </div>
  
  <script src="popup.js"></script>
</body>
</html>
```

---

## 🎨 popup.css

```css
body {
  width: 350px;
  padding: 0;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.container {
  padding: 20px;
}

h1 {
  font-size: 20px;
  margin: 0 0 20px 0;
  color: #667eea;
  text-align: center;
}

.stats {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e9ecef;
}

.job-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.job-info h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.job-info p {
  margin: 5px 0;
  font-size: 13px;
  color: #333;
}

.settings {
  display: flex;
  justify-content: space-around;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

.settings a {
  color: #667eea;
  text-decoration: none;
  font-size: 13px;
}

.settings a:hover {
  text-decoration: underline;
}
```

---

## 💻 popup.js

```javascript
// API configuration
const API_BASE = 'https://sam-job-automator.onrender.com/api';

// Load stats
async function loadStats() {
  try {
    const response = await fetch(`${API_BASE}/stats`);
    const data = await response.json();
    
    document.getElementById('totalApps').textContent = data.total_applications;
    document.getElementById('responses').textContent = data.responses;
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}

// Detect current job
async function detectJob() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, { action: 'extractJob' }, (response) => {
    if (response && response.job) {
      displayJob(response.job);
    } else {
      document.getElementById('jobTitle').textContent = 'No job detected on this page';
    }
  });
}

// Display job info
function displayJob(job) {
  document.getElementById('jobTitle').textContent = job.title;
  document.getElementById('jobCompany').textContent = job.company;
  document.getElementById('jobLocation').textContent = job.location;
}

// Apply to job
document.getElementById('applyBtn').addEventListener('click', async () => {
  const btn = document.getElementById('applyBtn');
  btn.textContent = '⏳ Applying...';
  btn.disabled = true;
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, { action: 'extractJob' }, async (response) => {
      if (response && response.job) {
        // Send to backend
        const result = await fetch(`${API_BASE}/apply`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(response.job)
        });
        
        if (result.ok) {
          btn.textContent = '✅ Applied!';
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'Application Sent!',
            message: `Applied to ${response.job.title} at ${response.job.company}`
          });
        } else {
          btn.textContent = '❌ Failed';
        }
      }
    });
  } catch (error) {
    console.error('Error applying:', error);
    btn.textContent = '❌ Error';
  }
  
  setTimeout(() => {
    btn.textContent = '✉️ Apply to This Job';
    btn.disabled = false;
  }, 3000);
});

// Save job
document.getElementById('saveBtn').addEventListener('click', async () => {
  // Implementation
  alert('Job saved for later!');
});

// AI Analysis
document.getElementById('analyzeBtn').addEventListener('click', async () => {
  // Implementation
  alert('AI analysis coming soon!');
});

// Initialize
loadStats();
detectJob();
```

---

## 📄 content.js

```javascript
// Job extractors for different sites
const extractors = {
  linkedin: () => {
    return {
      title: document.querySelector('.job-title')?.textContent?.trim(),
      company: document.querySelector('.company-name')?.textContent?.trim(),
      location: document.querySelector('.job-location')?.textContent?.trim(),
      description: document.querySelector('.job-description')?.textContent?.trim(),
      url: window.location.href,
      platform: 'LinkedIn'
    };
  },
  
  indeed: () => {
    return {
      title: document.querySelector('.jobsearch-JobInfoHeader-title')?.textContent?.trim(),
      company: document.querySelector('[data-company-name]')?.textContent?.trim(),
      location: document.querySelector('[data-testid="job-location"]')?.textContent?.trim(),
      description: document.querySelector('#jobDescriptionText')?.textContent?.trim(),
      url: window.location.href,
      platform: 'Indeed'
    };
  },
  
  bayt: () => {
    return {
      title: document.querySelector('.job-title')?.textContent?.trim(),
      company: document.querySelector('.company-name')?.textContent?.trim(),
      location: document.querySelector('.job-location')?.textContent?.trim(),
      description: document.querySelector('.job-description')?.textContent?.trim(),
      url: window.location.href,
      platform: 'Bayt'
    };
  }
};

// Detect platform
function detectPlatform() {
  const hostname = window.location.hostname;
  if (hostname.includes('linkedin.com')) return 'linkedin';
  if (hostname.includes('indeed.com')) return 'indeed';
  if (hostname.includes('bayt.com')) return 'bayt';
  return null;
}

// Extract job from current page
function extractJob() {
  const platform = detectPlatform();
  if (!platform || !extractors[platform]) {
    return null;
  }
  
  return extractors[platform]();
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractJob') {
    const job = extractJob();
    sendResponse({ job });
  }
  return true;
});

// Add floating button to page
function addFloatingButton() {
  const button = document.createElement('div');
  button.id = 'sam-job-automator-btn';
  button.innerHTML = '🚀 Quick Apply';
  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 25px;
    cursor: pointer;
    z-index: 10000;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: all 0.3s;
  `;
  
  button.addEventListener('click', () => {
    const job = extractJob();
    if (job) {
      // Send to backend
      fetch('https://sam-job-automator.onrender.com/api/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(job)
      }).then(() => {
        button.innerHTML = '✅ Applied!';
        setTimeout(() => {
          button.innerHTML = '🚀 Quick Apply';
        }, 3000);
      });
    }
  });
  
  button.addEventListener('mouseenter', () => {
    button.style.transform = 'scale(1.05)';
  });
  
  button.addEventListener('mouseleave', () => {
    button.style.transform = 'scale(1)';
  });
  
  document.body.appendChild(button);
}

// Initialize
if (detectPlatform()) {
  addFloatingButton();
}
```

---

## 🚀 Installation & Testing

### Load Extension:
1. Open Chrome
2. Go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked"
5. Select extension folder

### Test:
1. Go to LinkedIn/Indeed/Bayt
2. Open a job posting
3. Click extension icon
4. Click "Apply to This Job"

---

## 📦 Publishing

### Chrome Web Store:
1. **Developer Account** ($5 one-time)
2. **Zip extension folder**
3. **Upload to Chrome Web Store**
4. **Review process** (1-3 days)

---

## 💡 Advanced Features

### Auto-Fill Forms:
```javascript
// Fill application form
function fillForm(data) {
  document.querySelector('[name="name"]').value = data.name;
  document.querySelector('[name="email"]').value = data.email;
  document.querySelector('[name="phone"]').value = data.phone;
  // Upload CV
  const fileInput = document.querySelector('[type="file"]');
  // Trigger file upload
}
```

### Background Sync:
```javascript
// background.js
chrome.alarms.create('syncJobs', { periodInMinutes: 60 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'syncJobs') {
    // Sync with backend
  }
});
```

---

**Ready to build! 🚀**
