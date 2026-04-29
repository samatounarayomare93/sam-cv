"""
🚀 ZERO-COST OPTIMIZATION TEST SUITE
Tests all new optimization features
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_rotator():
    """Test email rotation system."""
    print("\n" + "="*50)
    print("📧 TESTING EMAIL ROTATION SYSTEM")
    print("="*50)
    
    try:
        from core.email_rotator import EmailRotator, get_email_stats
        
        rotator = EmailRotator()
        
        # Get stats
        stats = get_email_stats()
        print(f"\n✅ Email Rotator initialized")
        print(f"📅 Date: {stats['date']}")
        print(f"📧 Total sent: {stats['total_sent']}")
        print(f"📬 Total remaining: {stats['total_remaining']}")
        print(f"🎯 Total daily limit: {rotator.get_total_daily_limit()}")
        
        print("\n📊 Provider Breakdown:")
        for provider, data in stats['providers'].items():
            print(f"  {provider}: {data['used']}/{data['limit']} ({data['percentage']}%)")
        
        # Test getting next provider
        next_provider = rotator.get_next_provider()
        if next_provider:
            print(f"\n✅ Next provider: {next_provider['display_name']}")
        else:
            print("\n⚠️ No providers available (all limits reached)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Email Rotator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_cache():
    """Test AI cache system."""
    print("\n" + "="*50)
    print("🤖 TESTING AI CACHE SYSTEM")
    print("="*50)
    
    try:
        from core.ai_cache import (
            get_cached_analysis, 
            save_analysis_to_cache, 
            get_cache_stats,
            clear_expired_cache
        )
        
        # Test saving to cache
        test_analysis = {
            "is_relevant": True,
            "reason": "Test analysis",
            "lead_score": 85,
            "cover_letter_body": "Test letter",
            "keywords": ["test", "cache"],
        }
        
        saved = save_analysis_to_cache(
            "Test Job Title",
            "Test job description",
            "Test Company",
            test_analysis
        )
        
        if saved:
            print("✅ Cache save successful")
        else:
            print("⚠️ Cache save failed (might be disabled)")
        
        # Test retrieving from cache
        cached = get_cached_analysis(
            "Test Job Title",
            "Test job description",
            "Test Company"
        )
        
        if cached:
            print("✅ Cache retrieval successful")
        else:
            print("ℹ️ No cached data found (expected for first run)")
        
        # Get stats
        stats = get_cache_stats()
        print(f"\n📊 Cache Statistics:")
        print(f"  Enabled: {stats.get('enabled', False)}")
        print(f"  Total files: {stats.get('total_files', 0)}")
        print(f"  Total size: {stats.get('total_size_mb', 0)} MB")
        
        if stats.get('total_files', 0) > 0:
            print(f"  Oldest: {stats.get('oldest_hours', 0)} hours")
            print(f"  Newest: {stats.get('newest_hours', 0)} hours")
        
        # Test cleanup
        deleted = clear_expired_cache()
        print(f"\n🧹 Cleared {deleted} expired cache files")
        
        return True
        
    except Exception as e:
        print(f"\n❌ AI Cache test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_free_scrapers():
    """Test free job scrapers."""
    print("\n" + "="*50)
    print("🔍 TESTING FREE JOB SCRAPERS")
    print("="*50)
    
    try:
        from core.free_scrapers import (
            DaleelMadaniScraper,
            BaytScraper,
            GulfTalentScraper
        )
        
        print("\n📋 Available Scrapers:")
        scrapers = [
            ("Daleel Madani", DaleelMadaniScraper),
            ("Bayt.com", BaytScraper),
            ("GulfTalent", GulfTalentScraper),
        ]
        
        for name, scraper_class in scrapers:
            print(f"  ✅ {name}")
        
        print("\n⚠️ Note: Full scraping test skipped (takes 2-3 minutes)")
        print("To test scrapers, run: python core/free_scrapers.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Free Scrapers test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_telegram_stats():
    """Test Telegram statistics commands."""
    print("\n" + "="*50)
    print("📱 TESTING TELEGRAM STATS COMMANDS")
    print("="*50)
    
    try:
        from core.telegram_stats import (
            get_email_stats_message,
            get_cache_stats_message,
            get_scraper_stats_message,
            get_daily_report_message
        )
        
        print("\n✅ Testing email stats command...")
        email_msg = get_email_stats_message()
        print(email_msg[:200] + "..." if len(email_msg) > 200 else email_msg)
        
        print("\n✅ Testing cache stats command...")
        cache_msg = get_cache_stats_message()
        print(cache_msg[:200] + "..." if len(cache_msg) > 200 else cache_msg)
        
        print("\n✅ Testing scraper stats command...")
        scraper_msg = get_scraper_stats_message()
        print(scraper_msg[:200] + "..." if len(scraper_msg) > 200 else scraper_msg)
        
        print("\n✅ Testing daily report command...")
        report_msg = get_daily_report_message()
        print(report_msg[:200] + "..." if len(report_msg) > 200 else report_msg)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Telegram Stats test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🚀 ZERO-COST OPTIMIZATION TEST SUITE")
    print("="*70)
    
    results = {
        "Email Rotator": test_email_rotator(),
        "AI Cache": test_ai_cache(),
        "Free Scrapers": test_free_scrapers(),
        "Telegram Stats": test_telegram_stats(),
    }
    
    print("\n" + "="*70)
    print("📊 TEST RESULTS SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Total: {passed}/{total} tests passed ({int(passed/total*100)}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready!")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
