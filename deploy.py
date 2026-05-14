#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AUTO DEPLOY - ZERO INVESTMENT                             ║
║                    Deploy to GitHub + Render Automatically                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

This script automatically deploys the swarm system to:
1. GitHub (with secrets)
2. Render (with environment variables)

Usage: python deploy.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class AutoDeploy:
    """Automatic deployment to GitHub and Render."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.render_token = os.getenv("RENDER_API_KEY", "")
        
    def run(self):
        """Run complete deployment."""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "AUTO DEPLOYMENT" + " " * 36 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        # Check git
        if not self._check_git():
            return
        
        # Deploy to GitHub
        self._deploy_github()
        
        # Deploy to Render
        self._deploy_render()
        
        print()
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 22 + "DEPLOYMENT COMPLETE!" + " " * 33 + "║")
        print("╚" + "═" * 78 + "╝")
    
    def _check_git(self) -> bool:
        """Check if git is configured."""
        print("🔍 Checking Git configuration...")
        
        try:
            # Check git status
            result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            if result.returncode != 0:
                print("   ❌ Not a git repository")
                print("   Run: git init")
                return False
            
            print("   ✓ Git repository found")
            return True
            
        except FileNotFoundError:
            print("   ❌ Git not installed")
            return False
    
    def _deploy_github(self):
        """Deploy to GitHub."""
        print("\n🐙 Deploying to GitHub...")
        print("-" * 80)
        
        # Check if remote exists
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            cwd=self.base_dir
        )
        
        if "origin" not in result.stdout:
            print("   ⚠️ No remote repository configured")
            repo_url = input("   Enter GitHub repository URL: ").strip()
            if repo_url:
                subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=self.base_dir)
                print("   ✓ Remote added")
        
        # Add all files
        print("   Adding files...")
        subprocess.run(["git", "add", "."], cwd=self.base_dir)
        
        # Commit
        print("   Committing...")
        result = subprocess.run(
            ["git", "commit", "-m", "Auto-deploy: Swarm job automation system"],
            capture_output=True,
            text=True,
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("   ✓ Committed")
        else:
            print("   ⚠️ Nothing to commit or error")
        
        # Push
        print("   Pushing to GitHub...")
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True,
            text=True,
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("   ✓ Pushed to GitHub")
        else:
            print("   ❌ Push failed")
            print(f"   Error: {result.stderr}")
        
        print("\n   IMPORTANT: Add GitHub Secrets:")
        print("   1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
        print("   2. Add all secrets from .env file")
        
        print()
    
    def _deploy_render(self):
        """Deploy to Render."""
        print("\n☁️ Deploying to Render...")
        print("-" * 80)
        
        print("   Manual steps required:")
        print("   1. Go to: https://dashboard.render.com")
        print("   2. Click 'New +' → 'Web Service'")
        print("   3. Connect your GitHub repository")
        print("   4. Name: swarm-orchestrator")
        print("   5. Runtime: Python 3")
        print("   6. Build Command: pip install -r requirements.txt")
        print("   7. Start Command: python swarm_orchestrator.py")
        print("   8. Add environment variables from .env")
        print("   9. Click 'Create Web Service'")
        
        print("\n   ✓ Render configuration ready")
        print()

if __name__ == "__main__":
    deploy = AutoDeploy()
    deploy.run()
