"""
Simple Automatic Render.com Deployment
Opens browser and guides you through the process
"""

import time
import webbrowser
import subprocess

print("""
═══════════════════════════════════════════════════════════════
🤖 AUTOMATIC RENDER.COM DEPLOYMENT
═══════════════════════════════════════════════════════════════

This will:
✅ Open Render.com in your browser
✅ Open environment variables in Notepad
✅ Give you step-by-step instructions

You just need to:
⚠️ Sign in with GitHub
⚠️ Follow the steps shown

═══════════════════════════════════════════════════════════════
""")

print("🚀 Starting in 3 seconds...")
time.sleep(3)

# Step 1: Open environment variables
print("\n📝 Opening environment variables...")
subprocess.Popen(['notepad.exe', 'render_env_vars.txt'])
time.sleep(2)

# Step 2: Open Render.com
print("🌐 Opening Render.com...")
webbrowser.open('https://dashboard.render.com/select-repo?type=web')
time.sleep(3)

print("""
═══════════════════════════════════════════════════════════════
📋 FOLLOW THESE STEPS ON RENDER.COM:
═══════════════════════════════════════════════════════════════

1️⃣ SIGN IN:
   • Click "Sign In" or "Continue with GitHub"
   • Approve GitHub permissions

2️⃣ SELECT REPOSITORY:
   • Find: "sam-cv" or "Sam_Job_Automator"
   • Click "Connect"

3️⃣ FILL THE FORM:
   
   Name: sam-job-automator
   Region: Frankfurt
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python run.py
   Instance Type: Free

4️⃣ ADD ENVIRONMENT VARIABLES:
   • Scroll to "Environment Variables"
   • Click "Add from .env"
   • Go to Notepad window
   • Press Ctrl+A (select all)
   • Press Ctrl+C (copy)
   • Back to Render
   • Press Ctrl+V (paste)
   • Click "Add"

5️⃣ DEPLOY:
   • Click "Create Web Service"
   • Wait 2-3 minutes

6️⃣ TEST:
   • Open Telegram
   • Send /start to @samcvbot
   • Bot should reply!

7️⃣ DONE:
   • Turn off your PC!
   • Bot runs 24/7 on cloud! 🎉

═══════════════════════════════════════════════════════════════
""")

print("\n✅ Browser and Notepad are open!")
print("✅ Follow the steps above!")
print("\n💡 Tip: Keep this window open for reference")
