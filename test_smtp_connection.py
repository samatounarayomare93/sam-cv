#!/usr/bin/env python3
"""
🔍 SMTP CONNECTION TEST
Tests SMTP server connectivity
"""

import socket
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 SMTP CONNECTION TEST")
print("=" * 60)

def test_port(host, port, timeout=5):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_smtp_login(server, port, email, password, use_ssl=False):
    """Test SMTP login"""
    try:
        if use_ssl:
            smtp = smtplib.SMTP_SSL(server, port, timeout=10)
        else:
            smtp = smtplib.SMTP(server, port, timeout=10)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        
        smtp.login(email, password)
        smtp.quit()
        return True
    except Exception as e:
        print(f"  ❌ Login failed: {e}")
        return False

# Test Zoho
print("\n📧 TESTING ZOHO SMTP:")
print("-" * 60)
zoho_user = os.getenv('ZOHO_SMTP_USER', '')
zoho_pass = os.getenv('ZOHO_APP_PASSWORD', '')

if zoho_user and zoho_pass:
    print(f"  Email: {zoho_user}")
    print(f"  Server: smtp.zoho.com")
    
    # Test port 587
    print("\n  Testing port 587 (STARTTLS)...")
    if test_port('smtp.zoho.com', 587):
        print("  ✅ Port 587 is open")
        if test_smtp_login('smtp.zoho.com', 587, zoho_user, zoho_pass):
            print("  ✅ Login successful!")
        else:
            print("  ❌ Login failed")
    else:
        print("  ❌ Port 587 is blocked")
    
    # Test port 465
    print("\n  Testing port 465 (SSL)...")
    if test_port('smtp.zoho.com', 465):
        print("  ✅ Port 465 is open")
        if test_smtp_login('smtp.zoho.com', 465, zoho_user, zoho_pass, use_ssl=True):
            print("  ✅ Login successful!")
        else:
            print("  ❌ Login failed")
    else:
        print("  ❌ Port 465 is blocked")
else:
    print("  ⚠️ Zoho credentials not set")

# Test Brevo
print("\n📧 TESTING BREVO SMTP:")
print("-" * 60)
brevo_user = os.getenv('BREVO_SMTP_LOGIN', '')
brevo_pass = os.getenv('BREVO_SMTP_PASSWORD', '')

if brevo_user and brevo_pass:
    print(f"  Email: {brevo_user}")
    print(f"  Server: smtp-relay.brevo.com")
    
    # Test port 587
    print("\n  Testing port 587 (STARTTLS)...")
    if test_port('smtp-relay.brevo.com', 587):
        print("  ✅ Port 587 is open")
        if test_smtp_login('smtp-relay.brevo.com', 587, brevo_user, brevo_pass):
            print("  ✅ Login successful!")
        else:
            print("  ❌ Login failed")
    else:
        print("  ❌ Port 587 is blocked")
    
    # Test port 2525
    print("\n  Testing port 2525 (Alternative)...")
    if test_port('smtp-relay.brevo.com', 2525):
        print("  ✅ Port 2525 is open")
        if test_smtp_login('smtp-relay.brevo.com', 2525, brevo_user, brevo_pass):
            print("  ✅ Login successful!")
        else:
            print("  ❌ Login failed")
    else:
        print("  ❌ Port 2525 is blocked")
else:
    print("  ⚠️ Brevo credentials not set")

print("\n" + "=" * 60)
print("💡 RECOMMENDATION:")
print("=" * 60)
print("If all SMTP ports are blocked, the bot will use:")
print("  ✅ Brevo HTTP API (Port 443) - Always works")
print("  ✅ Gmail API (Port 443) - Works if token is valid")
print("\nBoth methods bypass firewall restrictions!")
print("=" * 60)
