#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AUTO SETUP - ZERO INVESTMENT SYSTEM                       ║
║                    Automatic Configuration & Deployment                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

This script automatically:
1. Configures all API keys and credentials
2. Sets up GitHub Actions for 24/7 cloud deployment
3. Configures Render for free hosting
4. Optimizes for Sam Salameh's profile (Senior Network Engineer)
5. Sets up email providers and Telegram notifications

Run: python auto_setup.py
"""

import os
import sys
import json
import subprocess
import getpass
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class AutoSetup:
    """Automatic setup for the job automation system."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.env_file = self.base_dir / ".env"
        self.github_dir = self.base_dir / ".github" / "workflows"
        self.config = {}
        
    def run(self):
        """Run complete setup."""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "AUTO SETUP - ZERO INVESTMENT" + " " * 28 + "║")
        print("║" + " " * 15 + "Sam Salameh - Senior Network Engineer" + " " * 24 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        # Step 1: Get API Keys
        self._setup_api_keys()
        
        # Step 2: Setup Email
        self._setup_email()
        
        # Step 3: Setup Telegram
        self._setup_telegram()
        
        # Step 4: Setup Database
        self._setup_database()
        
        # Step 5: Create GitHub Actions
        self._setup_github_actions()
        
        # Step 6: Create Render Config
        self._setup_render()
        
        # Step 7: Save Configuration
        self._save_config()
        
        # Step 8: Test Configuration
        self._test_config()
        
        print()
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "SETUP COMPLETE!" + " " * 36 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        self._print_next_steps()
    
    def _setup_api_keys(self):
        """Setup AI API keys."""
        print("🔑 STEP 1: AI API Keys")
        print("-" * 80)
        
        print("\n1. Gemini API (Free - 60 requests/minute)")
        print("   Get key at: https://aistudio.google.com/app/apikey")
        gemini_key = input("   Enter Gemini API Key (or press Enter to skip): ").strip()
        if gemini_key:
            self.config['GEMINI_API_KEY'] = gemini_key
            print("   ✓ Gemini configured")
        
        print("\n2. Groq API (Free - 1,000,000 tokens/day)")
        print("   Get key at: https://console.groq.com/keys")
        groq_key = input("   Enter Groq API Key (or press Enter to skip): ").strip()
        if groq_key:
            self.config['GROQ_API_KEY'] = groq_key
            print("   ✓ Groq configured")
        
        if not gemini_key and not groq_key:
            print("   ⚠️ No AI keys configured - will use keyword matching only")
        
        print()
    
    def _setup_email(self):
        """Setup email providers."""
        print("📧 STEP 2: Email Providers")
        print("-" * 80)
        
        print("\n1. Brevo (Free - 300 emails/day)")
        print("   Sign up at: https://www.brevo.com")
        brevo_user = input("   Brevo SMTP Login: ").strip()
        brevo_pass = input("   Brevo SMTP Password: ").strip()
        if brevo_user and brevo_pass:
            self.config['BREVO_SMTP_LOGIN'] = brevo_user
            self.config['BREVO_SMTP_PASSWORD'] = brevo_pass
            print("   ✓ Brevo configured")
        
        print("\n2. Gmail (Free - 100 emails/day)")
        print("   Enable at: https://myaccount.google.com/apppasswords")
        gmail_user = input("   Gmail Address: ").strip()
        gmail_pass = input("   Gmail App Password: ").strip()
        if gmail_user and gmail_pass:
            self.config['GMAIL_SMTP_USER'] = gmail_user
            self.config['GMAIL_APP_PASSWORD'] = gmail_pass
            print("   ✓ Gmail configured")
        
        print("\n3. Outlook (Free - 100 emails/day)")
        outlook_user = input("   Outlook Email: ").strip()
        outlook_pass = input("   Outlook Password: ").strip()
        if outlook_user and outlook_pass:
            self.config['OUTLOOK_USER'] = outlook_user
            self.config['OUTLOOK_PASSWORD'] = outlook_pass
            print("   ✓ Outlook configured")
        
        print()
    
    def _setup_telegram(self):
        """Setup Telegram notifications."""
        print("📱 STEP 3: Telegram Notifications")
        print("-" * 80)
        
        print("\n1. Create a bot with @BotFather")
        print("   1. Message @BotFather on Telegram")
        print("   2. Send /newbot")
        print("   3. Follow instructions")
        print("   4. Copy the API token")
        
        bot_token = input("\n   Bot Token: ").strip()
        if bot_token:
            self.config['TELEGRAM_BOT_TOKEN'] = bot_token
            
            print("\n2. Get your Chat ID")
            print("   1. Message @userinfobot on Telegram")
            print("   2. Copy your ID")
            
            chat_id = input("   Chat ID: ").strip()
            if chat_id:
                self.config['TELEGRAM_CHAT_ID'] = chat_id
                print("   ✓ Telegram configured")
        
        print()
    
    def _setup_database(self):
        """Setup database configuration."""
        print("💾 STEP 4: Database")
        print("-" * 80)
        
        print("\n1. Supabase (Free - 500MB database)")
        print("   Sign up at: https://supabase.com")
        
        supabase_url = input("   Supabase URL: ").strip()
        supabase_key = input("   Supabase Anon Key: ").strip()
        
        if supabase_url and supabase_key:
            self.config['SUPABASE_URL'] = supabase_url
            self.config['SUPABASE_KEY'] = supabase_key
            print("   ✓ Supabase configured")
        else:
            print("   ⚠️ Using local SQLite database")
        
        print()
    
    def _setup_github_actions(self):
        """Create GitHub Actions workflow."""
        print("🔄 STEP 5: GitHub Actions (24/7 Cloud)")
        print("-" * 80)
        
        # Create workflow directory
        self.github_dir.mkdir(parents=True, exist_ok=True)
        
        # Create workflow file
        workflow_content = """name: Swarm Orchestrator

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  swarm-run:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install aiohttp httpx python-dotenv
    
    - name: Run Swarm
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        BREVO_SMTP_LOGIN: ${{ secrets.BREVO_SMTP_LOGIN }}
        BREVO_SMTP_PASSWORD: ${{ secrets.BREVO_SMTP_PASSWORD }}
        GMAIL_SMTP_USER: ${{ secrets.GMAIL_SMTP_USER }}
        GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
        OUTLOOK_USER: ${{ secrets.OUTLOOK_USER }}
        OUTLOOK_PASSWORD: ${{ secrets.OUTLOOK_PASSWORD }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
        SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
      run: |
        python swarm_orchestrator.py --once
    
    - name: Upload logs
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: swarm-logs
        path: swarm.log
"""
        
        workflow_file = self.github_dir / "swarm.yml"
        workflow_file.write_text(workflow_content)
        
        print("   ✓ GitHub Actions workflow created")
        print(f"   File: {workflow_file}")
        print("\n   IMPORTANT: Add secrets to GitHub:")
        print("   1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
        print("   2. Add all the secrets listed above")
        
        print()
    
    def _setup_render(self):
        """Create Render configuration."""
        print("☁️ STEP 6: Render (Free Hosting)")
        print("-" * 80)
        
        render_yaml = """services:
  - type: web
    name: swarm-orchestrator
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python swarm_orchestrator.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: GEMINI_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: BREVO_SMTP_LOGIN
        sync: false
      - key: BREVO_SMTP_PASSWORD
        sync: false
      - key: GMAIL_SMTP_USER
        sync: false
      - key: GMAIL_APP_PASSWORD
        sync: false
      - key: OUTLOOK_USER
        sync: false
      - key: OUTLOOK_PASSWORD
        sync: false
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_CHAT_ID
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
"""
        
        render_file = self.base_dir / "render.yaml"
        render_file.write_text(render_yaml)
        
        print("   ✓ Render configuration created")
        print(f"   File: {render_file}")
        print("\n   IMPORTANT: Set environment variables on Render:")
        print("   1. Go to: https://dashboard.render.com")
        print("   2. Create new Web Service")
        print("   3. Add all environment variables")
        
        print()
    
    def _save_config(self):
        """Save configuration to .env file."""
        print("💾 STEP 7: Saving Configuration")
        print("-" * 80)
        
        # Add default values
        self.config['CANDIDATE_NAME'] = 'Sam Salameh'
        self.config['CANDIDATE_EMAIL'] = self.config.get('GMAIL_SMTP_USER', '')
        self.config['MAX_PARALLEL_STRIKES'] = '5'
        self.config['MIN_MATCH_SCORE'] = '70'
        self.config['REQUEST_TIMEOUT'] = '15'
        
        # Write .env file
        env_content = "# Sam Salameh - Job Automation System\\n"
        env_content += "# Generated by Auto Setup\\n\\n"
        
        for key, value in self.config.items():
            env_content += f"{key}={value}\\n"
        
        self.env_file.write_text(env_content)
        
        print(f"   ✓ Configuration saved to {self.env_file}")
        print()
    
    def _test_config(self):
        """Test configuration."""
        print("🧪 STEP 8: Testing Configuration")
        print("-" * 80)
        
        # Test imports
        try:
            import aiohttp
            import httpx
            print("   ✓ Required packages installed")
        except ImportError:
            print("   ⚠️ Installing required packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp", "httpx", "python-dotenv"])
        
        # Test database
        try:
            from swarm_orchestrator import SwarmDatabase
            db = SwarmDatabase()
            print("   ✓ Database initialized")
        except Exception as e:
            print(f"   ⚠️ Database test failed: {e}")
        
        print()
    
    def _print_next_steps(self):
        """Print next steps."""
        print("🚀 NEXT STEPS:")
        print("-" * 80)
        print()
        print("1. PUSH TO GITHUB:")
        print("   git add .")
        print("   git commit -m 'Initial swarm setup'")
        print("   git push origin main")
        print()
        print("2. ADD GITHUB SECRETS:")
        print("   Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
        print("   Add all secrets from .env file")
        print()
        print("3. DEPLOY TO RENDER:")
        print("   Go to: https://dashboard.render.com")
        print("   Create new Web Service from GitHub repo")
        print("   Add environment variables")
        print()
        print("4. RUN LOCALLY:")
        print("   python swarm_orchestrator.py --once    # Single run")
        print("   python swarm_orchestrator.py             # Continuous")
        print()
        print("5. MONITOR:")
        print("   Check Telegram for notifications")
        print("   Check swarm.log for detailed logs")
        print()
        print("📊 EXPECTED RESULTS:")
        print("   • Jobs found: 50-100 per day")
        print("   • Applications sent: 10-20 per day")
        print("   • Cost: $0 (all free tiers)")
        print("   • Time: 100% automated")
        print()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    setup = AutoSetup()
    setup.run()
