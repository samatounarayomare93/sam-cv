"""
Automatic Render.com Deployment Script
This script automates the deployment process on Render.com
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuration
RENDER_URL = "https://render.com"
REPO_NAME = "sam-cv"  # or "Sam_Job_Automator"
SERVICE_NAME = "sam-job-automator"
REGION = "Frankfurt"
BUILD_COMMAND = "pip install -r requirements.txt"
START_COMMAND = "python run.py"

# Environment Variables (from render_env_vars.txt)
ENV_VARS = {
    "SUPABASE_URL": "https://lckiazbadymeikmxesit.supabase.co",
    "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxja2lhemJhZHltZWlrbXhlc2l0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMTcxNTUsImV4cCI6MjA5Mjg5MzE1NX0.X6XLJTCQnuf67AEWjRrGfCIbOGmnPaiVtKq9a5no1Uc",
    "GROQ_API_KEY": "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",
    "GEMINI_API_KEY": "AIzaSyC-Wp4uz6LNLsDMi0DXKRQCA8GdUDVCbkw",
    "ZOHO_SMTP_USER": "samsalameh.cv@zohomail.com",
    "ZOHO_APP_PASSWORD": "R0R6dqr5qL1g",
    "GMAIL_SMTP_USER": "samsalameh.cv@gmail.com",
    "GMAIL_APP_PASSWORD": "oimuanudzzngklnf",
    "TELEGRAM_BOT_TOKEN": "8630175054:AAGuMqlmCJAizvDlFUrsg-UletxSdOcsvn0",
    "TELEGRAM_CHAT_ID": "6639482672",
    "USE_AI_ANALYSIS": "true",
    "VERBOSE_LOGGING": "true",
    "MAX_PARALLEL_STRIKES": "3",
    "KEEP_ALIVE_ENABLED": "true"
}

def setup_driver():
    """Setup Chrome driver with options"""
    print("🔧 Setting up Chrome driver...")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_element(driver, by, value, timeout=30):
    """Wait for element to be present"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_clickable(driver, by, value, timeout=30):
    """Wait for element to be clickable"""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def deploy_to_render():
    """Main deployment function"""
    driver = None
    
    try:
        driver = setup_driver()
        
        # Step 1: Open Render.com
        print("\n" + "="*60)
        print("🚀 STEP 1: Opening Render.com...")
        print("="*60)
        driver.get(RENDER_URL)
        time.sleep(3)
        
        # Step 2: Sign in with GitHub
        print("\n" + "="*60)
        print("🔐 STEP 2: Please sign in with GitHub manually...")
        print("="*60)
        print("⚠️  MANUAL ACTION REQUIRED:")
        print("   1. Click 'Sign In' or 'Get Started'")
        print("   2. Choose 'Continue with GitHub'")
        print("   3. Approve permissions")
        print("\n   Press ENTER when you're signed in...")
        input()
        
        # Step 3: Create new Web Service
        print("\n" + "="*60)
        print("🆕 STEP 3: Creating new Web Service...")
        print("="*60)
        
        # Wait for dashboard to load
        time.sleep(3)
        
        # Click "New +" button
        try:
            new_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'New')]")
            new_button.click()
            time.sleep(2)
            
            # Click "Web Service"
            web_service = wait_for_clickable(driver, By.XPATH, "//a[contains(text(), 'Web Service')]")
            web_service.click()
            time.sleep(3)
            
            print("✅ Clicked 'New' → 'Web Service'")
        except Exception as e:
            print(f"⚠️  Could not find 'New' button automatically.")
            print(f"   Please click: New + → Web Service")
            print(f"\n   Press ENTER when done...")
            input()
        
        # Step 4: Select repository
        print("\n" + "="*60)
        print("📦 STEP 4: Selecting repository...")
        print("="*60)
        
        time.sleep(3)
        
        try:
            # Look for repository
            repo_link = wait_for_clickable(driver, By.XPATH, f"//button[contains(text(), '{REPO_NAME}')]")
            repo_link.click()
            time.sleep(2)
            print(f"✅ Selected repository: {REPO_NAME}")
        except Exception as e:
            print(f"⚠️  Could not find repository automatically.")
            print(f"   Please select: {REPO_NAME}")
            print(f"\n   Press ENTER when done...")
            input()
        
        # Step 5: Fill in the form
        print("\n" + "="*60)
        print("📝 STEP 5: Filling in the form...")
        print("="*60)
        
        time.sleep(3)
        
        # Fill Name
        try:
            name_input = driver.find_element(By.NAME, "name")
            name_input.clear()
            name_input.send_keys(SERVICE_NAME)
            print(f"✅ Name: {SERVICE_NAME}")
        except:
            print(f"⚠️  Please enter Name: {SERVICE_NAME}")
        
        # Select Region
        try:
            region_select = driver.find_element(By.NAME, "region")
            region_select.click()
            time.sleep(1)
            frankfurt = driver.find_element(By.XPATH, f"//option[contains(text(), '{REGION}')]")
            frankfurt.click()
            print(f"✅ Region: {REGION}")
        except:
            print(f"⚠️  Please select Region: {REGION}")
        
        # Fill Build Command
        try:
            build_input = driver.find_element(By.NAME, "buildCommand")
            build_input.clear()
            build_input.send_keys(BUILD_COMMAND)
            print(f"✅ Build Command: {BUILD_COMMAND}")
        except:
            print(f"⚠️  Please enter Build Command: {BUILD_COMMAND}")
        
        # Fill Start Command
        try:
            start_input = driver.find_element(By.NAME, "startCommand")
            start_input.clear()
            start_input.send_keys(START_COMMAND)
            print(f"✅ Start Command: {START_COMMAND}")
        except:
            print(f"⚠️  Please enter Start Command: {START_COMMAND}")
        
        # Select Free instance
        try:
            free_option = driver.find_element(By.XPATH, "//input[@value='free']")
            free_option.click()
            print("✅ Instance Type: Free")
        except:
            print("⚠️  Please select Instance Type: Free")
        
        print("\n   Press ENTER when form is filled...")
        input()
        
        # Step 6: Add Environment Variables
        print("\n" + "="*60)
        print("🔐 STEP 6: Adding Environment Variables...")
        print("="*60)
        
        print("\n⚠️  MANUAL ACTION REQUIRED:")
        print("   1. Scroll down to 'Environment Variables' section")
        print("   2. Click 'Add from .env'")
        print("   3. Copy ALL content from 'render_env_vars.txt'")
        print("   4. Paste it in the text box")
        print("   5. Click 'Add'")
        print("\n   Press ENTER when environment variables are added...")
        input()
        
        # Step 7: Deploy
        print("\n" + "="*60)
        print("🚀 STEP 7: Deploying...")
        print("="*60)
        
        print("\n⚠️  FINAL STEP:")
        print("   1. Scroll to the top")
        print("   2. Click the big blue 'Create Web Service' button")
        print("   3. Wait 2-3 minutes for deployment")
        print("\n   Press ENTER when deployment starts...")
        input()
        
        # Success!
        print("\n" + "="*60)
        print("🎉 DEPLOYMENT STARTED!")
        print("="*60)
        print("\n✅ Your bot is being deployed!")
        print("✅ Wait 2-3 minutes")
        print("✅ Check status on Render.com dashboard")
        print("✅ Test with: /start on @samcvbot")
        print("\n🎊 You can close this window and turn off your PC!")
        print("   Bot will run 24/7 on the cloud! ☁️")
        
        print("\nPress ENTER to close...")
        input()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease complete the deployment manually on Render.com")
        print("Follow the guide in: README_DEPLOYMENT.md")
        
    finally:
        if driver:
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            driver.quit()

if __name__ == "__main__":
    print("""
    ═══════════════════════════════════════════════════════════════
                    🚀 RENDER.COM AUTO DEPLOYMENT
    ═══════════════════════════════════════════════════════════════
    
    This script will help you deploy to Render.com automatically!
    
    ⚠️  You'll need to:
    1. Sign in with GitHub (once)
    2. Approve some steps manually
    
    The script will guide you through everything!
    
    ═══════════════════════════════════════════════════════════════
    """)
    
    input("Press ENTER to start deployment...")
    
    deploy_to_render()
