#!/usr/bin/env python3
"""
🛡️ BOT HEALTH CHECKER
=====================
Checks if the bot is running on Render and shows uptime/health status.
"""

import requests
import sys
from datetime import datetime

def check_bot_health():
    """Check if the bot is alive on Render."""
    
    print("=" * 80)
    print("🛡️ SAM JOB BOT - HEALTH CHECK")
    print("=" * 80)
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Try both possible URLs
    urls = [
        "https://sam-job-automator.onrender.com",
        "https://sam-cv-bot.onrender.com"
    ]
    
    for url in urls:
        print(f"🔍 Checking: {url}")
        try:
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                print(f"   ✅ Status: ONLINE (HTTP {response.status_code})")
                print(f"   📡 Response Time: {response.elapsed.total_seconds():.2f}s")
                print(f"   🛡️ Bot is ALIVE and running!")
                print()
                
                # Try to get stats
                try:
                    stats_response = requests.get(f"{url}/api/stats", timeout=10)
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        print(f"   📊 STATISTICS:")
                        print(f"      • Jobs Scanned: {stats.get('scanned', 'N/A')}")
                        print(f"      • Emails Sent: {stats.get('strikes', 'N/A')}")
                        print(f"      • Leads Found: {stats.get('intel', 'N/A')}")
                        print(f"      • Uptime: {stats.get('uptime', 'N/A')}")
                except Exception:
                    pass
                
                print()
                print("=" * 80)
                print("✅ BOT IS RUNNING 24/7 ON RENDER!")
                print("=" * 80)
                return True
            else:
                print(f"   ⚠️ Status: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout: Server took too long to respond")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error: Cannot reach server")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 80)
    print("❌ BOT IS NOT RESPONDING")
    print("=" * 80)
    print()
    print("🔧 TROUBLESHOOTING:")
    print("   1. Check Render dashboard: https://dashboard.render.com")
    print("   2. Check if the service is deployed and running")
    print("   3. Check Render logs for errors")
    print("   4. Make sure environment variables are set correctly")
    print()
    return False

if __name__ == "__main__":
    success = check_bot_health()
    sys.exit(0 if success else 1)
