#!/usr/bin/env python3
"""
📧 EMAIL PROVIDER HEALTH CHECKER
═══════════════════════════════════════════════════════════════════════════════
Tests all configured email providers and measures their health
Helps identify which providers are working and which need attention
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import time
import smtplib
import logging
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [EMAIL-HEALTH] %(levelname)s - %(message)s"
)


class EmailProviderHealthChecker:
    """Health checker for email providers"""
    
    def __init__(self):
        self.results = {}
    
    def test_smtp_connection(
        self,
        name: str,
        server: str,
        port: int,
        username: str,
        password: str,
        use_ssl: bool = False
    ) -> Tuple[bool, str, float]:
        """Test SMTP connection"""
        start_time = time.time()
        
        try:
            if use_ssl:
                smtp = smtplib.SMTP_SSL(server, port, timeout=10)
            else:
                smtp = smtplib.SMTP(server, port, timeout=10)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            
            smtp.login(username, password)
            smtp.quit()
            
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            
            return True, "OK", elapsed
            
        except smtplib.SMTPAuthenticationError as e:
            elapsed = (time.time() - start_time) * 1000
            return False, f"Auth Failed: {e}", elapsed
            
        except smtplib.SMTPConnectError as e:
            elapsed = (time.time() - start_time) * 1000
            return False, f"Connection Failed: {e}", elapsed
            
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, f"Error: {type(e).__name__}: {e}", elapsed
    
    def test_api_endpoint(
        self,
        name: str,
        api_key: str,
        endpoint: str
    ) -> Tuple[bool, str, float]:
        """Test API endpoint"""
        import requests
        
        start_time = time.time()
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code in [200, 401]:  # 401 means API key works but needs proper endpoint
                return True, "OK", elapsed
            else:
                return False, f"HTTP {response.status_code}", elapsed
                
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, f"Error: {e}", elapsed
    
    def check_gmail(self) -> Dict:
        """Check Gmail SMTP"""
        username = os.getenv("GMAIL_SMTP_USER", "").strip()
        password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
        
        if not username or not password:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing credentials"
            }
        
        success, message, elapsed = self.test_smtp_connection(
            "Gmail",
            "smtp.gmail.com",
            465,
            username,
            password,
            use_ssl=True
        )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "smtp.gmail.com:465"
        }
    
    def check_brevo(self) -> Dict:
        """Check Brevo SMTP"""
        username = os.getenv("BREVO_SMTP_LOGIN", "").strip()
        password = os.getenv("BREVO_SMTP_PASSWORD", "").strip()
        
        if not username or not password:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing credentials"
            }
        
        # Try port 2525 first (works on Render)
        success, message, elapsed = self.test_smtp_connection(
            "Brevo",
            "smtp-relay.brevo.com",
            2525,
            username,
            password,
            use_ssl=False
        )
        
        if not success:
            # Try port 587 as fallback
            success, message, elapsed = self.test_smtp_connection(
                "Brevo",
                "smtp-relay.brevo.com",
                587,
                username,
                password,
                use_ssl=False
            )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "smtp-relay.brevo.com:2525/587"
        }
    
    def check_zoho(self) -> Dict:
        """Check Zoho SMTP"""
        username = os.getenv("ZOHO_SMTP_USER", "").strip()
        password = os.getenv("ZOHO_APP_PASSWORD", "").strip()
        
        if not username or not password:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing credentials"
            }
        
        # Try port 465 (SSL)
        success, message, elapsed = self.test_smtp_connection(
            "Zoho",
            "smtp.zoho.com",
            465,
            username,
            password,
            use_ssl=True
        )
        
        if not success:
            # Try port 587 (TLS) as fallback
            success, message, elapsed = self.test_smtp_connection(
                "Zoho",
                "smtp.zoho.com",
                587,
                username,
                password,
                use_ssl=False
            )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "smtp.zoho.com:465/587"
        }
    
    def check_resend(self) -> Dict:
        """Check Resend API"""
        api_key = os.getenv("RESEND_API_KEY", "").strip()
        
        if not api_key:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing API key"
            }
        
        success, message, elapsed = self.test_api_endpoint(
            "Resend",
            api_key,
            "https://api.resend.com/emails"
        )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "api.resend.com"
        }
    
    def check_yahoo(self) -> Dict:
        """Check Yahoo SMTP"""
        username = os.getenv("YAHOO_SMTP_USER", "").strip()
        password = os.getenv("YAHOO_APP_PASSWORD", "").strip()
        
        if not username or not password:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing credentials"
            }
        
        success, message, elapsed = self.test_smtp_connection(
            "Yahoo",
            "smtp.mail.yahoo.com",
            465,
            username,
            password,
            use_ssl=True
        )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "smtp.mail.yahoo.com:465"
        }
    
    def check_outlook(self) -> Dict:
        """Check Outlook SMTP"""
        username = os.getenv("OUTLOOK_USER", "").strip()
        password = os.getenv("OUTLOOK_PASSWORD", "").strip()
        
        if not username or not password:
            return {
                "configured": False,
                "status": "NOT_CONFIGURED",
                "message": "Missing credentials"
            }
        
        success, message, elapsed = self.test_smtp_connection(
            "Outlook",
            "smtp-mail.outlook.com",
            587,
            username,
            password,
            use_ssl=False
        )
        
        return {
            "configured": True,
            "status": "OK" if success else "ERROR",
            "message": message,
            "response_time_ms": elapsed,
            "server": "smtp-mail.outlook.com:587"
        }
    
    def run_all_checks(self) -> Dict:
        """Run all email provider checks"""
        print("\n" + "="*80)
        print("📧 EMAIL PROVIDER HEALTH CHECK")
        print("="*80 + "\n")
        
        providers = {
            "Gmail": self.check_gmail,
            "Brevo": self.check_brevo,
            "Zoho": self.check_zoho,
            "Resend": self.check_resend,
            "Yahoo": self.check_yahoo,
            "Outlook": self.check_outlook,
        }
        
        results = {}
        configured_count = 0
        working_count = 0
        
        for name, check_func in providers.items():
            print(f"Testing {name}...", end=" ")
            
            try:
                result = check_func()
                results[name] = result
                
                if result["configured"]:
                    configured_count += 1
                    
                    if result["status"] == "OK":
                        working_count += 1
                        elapsed = result.get("response_time_ms", 0)
                        
                        # Color code by response time
                        if elapsed < 200:
                            speed = "⚡ Fast"
                        elif elapsed < 500:
                            speed = "✅ Good"
                        else:
                            speed = "⚠️ Slow"
                        
                        print(f"✅ OK ({elapsed:.0f}ms) {speed}")
                    else:
                        print(f"❌ {result['message']}")
                else:
                    print("⏭️ Not configured")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                results[name] = {
                    "configured": False,
                    "status": "ERROR",
                    "message": str(e)
                }
        
        print("\n" + "="*80)
        print(f"Summary: {working_count}/{configured_count} providers working")
        
        if working_count == 0:
            print("Status: 🔴 CRITICAL - No email providers working!")
        elif working_count < 2:
            print("Status: 🟠 WARNING - Only 1 provider working (need 2+ for redundancy)")
        elif working_count < configured_count:
            print("Status: 🟡 GOOD - Most providers working")
        else:
            print("Status: 🟢 EXCELLENT - All providers working!")
        
        print("="*80 + "\n")
        
        # Recommendations
        if working_count == 0:
            print("⚠️ RECOMMENDATIONS:")
            print("1. Check your .env file for correct credentials")
            print("2. Verify app-specific passwords are enabled")
            print("3. Check firewall/network settings")
            print("4. Try running: python check_env.py")
        elif working_count < 2:
            print("💡 RECOMMENDATIONS:")
            print("1. Configure at least 2 email providers for redundancy")
            print("2. Check failed providers and fix credentials")
            print("3. Consider using Resend API (3000 free emails/month)")
        
        return results


def main():
    """Main entry point"""
    checker = EmailProviderHealthChecker()
    results = checker.run_all_checks()
    
    # Count working providers
    working = sum(1 for r in results.values() if r.get("status") == "OK")
    
    # Exit with appropriate code
    sys.exit(0 if working >= 1 else 1)


if __name__ == "__main__":
    main()
