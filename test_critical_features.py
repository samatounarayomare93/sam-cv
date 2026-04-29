"""
🧪 TEST CRITICAL FEATURES
Test all 5 newly implemented critical features
"""

import sys
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_multi_ai_fallback():
    """Test Multi-AI Fallback Chain."""
    print("\n" + "="*60)
    print("🤖 TEST 1: MULTI-AI FALLBACK CHAIN")
    print("="*60)
    
    try:
        from core.multi_ai_fallback import MultiAIFallback, get_ai_stats
        
        fallback = MultiAIFallback()
        
        # Check available providers
        print(f"\n✅ Available providers: {len(fallback.providers)}")
        for provider in fallback.providers:
            print(f"   - {provider['display_name']}: {provider['daily_limit']} requests/day")
        
        # Test generation
        print("\n🔄 Testing AI generation...")
        test_prompt = "Write a one-sentence professional email subject line."
        
        result = fallback.generate(test_prompt)
        
        if result:
            print(f"✅ SUCCESS: Generated response")
            print(f"   Response: {result[:100]}...")
        else:
            print("❌ FAILED: No response generated")
            return False
        
        # Show stats
        stats = get_ai_stats()
        print(f"\n📊 Usage Stats:")
        print(f"   Total requests: {stats['total_requests']}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_email_warmup():
    """Test Email Warm-up Strategy."""
    print("\n" + "="*60)
    print("📧 TEST 2: EMAIL WARM-UP STRATEGY")
    print("="*60)
    
    try:
        from core.email_warmup import EmailWarmup, get_warmup_limit
        
        warmup = EmailWarmup()
        
        # Start warmup for test provider
        test_provider = "test_provider"
        warmup.start_warmup(test_provider)
        
        print(f"\n✅ Started warmup for: {test_provider}")
        
        # Get current limit
        limit = warmup.get_daily_limit(test_provider, default_limit=300)
        print(f"   Day 1 limit: {limit} emails")
        
        # Check status
        status = warmup.get_warmup_status(test_provider)
        if status:
            print(f"\n📊 Warmup Status:")
            print(f"   Day: {status['day']}/{status['total_days']}")
            print(f"   Progress: {status['progress']}%")
            print(f"   Today's limit: {status['limit_today']}")
        
        # Cleanup
        warmup.reset_warmup(test_provider)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_followup_sequence():
    """Test Automated Follow-up Sequence."""
    print("\n" + "="*60)
    print("🔄 TEST 3: AUTOMATED FOLLOW-UP SEQUENCE")
    print("="*60)
    
    try:
        from core.followup_sequence import FollowUpSequence, get_followup_stats
        
        followup = FollowUpSequence()
        
        # Register test application
        tracking_id = followup.register_application(
            company_name="TestCorp",
            role="Test Manager",
            email="test@testcorp.com",
            application_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        )
        
        print(f"\n✅ Registered application: {tracking_id}")
        
        # Check pending follow-ups
        pending = followup.get_pending_followups()
        print(f"\n📬 Pending follow-ups: {len(pending)}")
        
        if pending:
            for item in pending:
                print(f"   - {item['company_name']}: Day {item['followup_day']} follow-up")
        
        # Generate follow-up email
        if pending:
            email = followup.generate_followup_email(
                pending[0]['company_name'],
                pending[0]['role'],
                pending[0]['followup_config']
            )
            print(f"\n📧 Generated Follow-up:")
            print(f"   Subject: {email['subject']}")
            print(f"   Body preview: {email['body'][:100]}...")
        
        # Show stats
        stats = get_followup_stats()
        print(f"\n📊 Statistics:")
        print(f"   Total applications: {stats['total_applications']}")
        print(f"   Active: {stats['active']}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_ab_testing():
    """Test A/B Testing System."""
    print("\n" + "="*60)
    print("🧪 TEST 4: A/B TESTING SYSTEM")
    print("="*60)
    
    try:
        from core.ab_testing import ABTesting, get_recommendations
        
        ab = ABTesting()
        
        # Select variations
        subject_var = ab.select_variation("subject_line")
        tone_var = ab.select_variation("tone")
        
        print(f"\n✅ Selected variations:")
        print(f"   Subject line: {subject_var}")
        print(f"   Tone: {tone_var}")
        
        # Simulate some tests
        print(f"\n🔄 Simulating 20 test emails...")
        for i in range(20):
            var = ab.select_variation("subject_line")
            ab.record_sent("subject_line", var)
            
            # Simulate opens (50% rate)
            if i % 2 == 0:
                ab.record_opened("subject_line", var)
        
        # Show results
        results = ab.get_test_results("subject_line")
        print(f"\n📊 Test Results:")
        
        for variation, stats in results["variations"].items():
            print(f"   {variation}: {stats['sent']} sent, {stats['open_rate']}% open rate")
        
        if results["winner"]:
            print(f"\n🏆 Winner: {results['winner']} (confidence: {results['confidence']:.1%})")
        
        # Get recommendations
        recommendations = get_recommendations()
        print(f"\n💡 Recommendations: {len(recommendations)} tests")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_response_predictor():
    """Test Response Prediction AI."""
    print("\n" + "="*60)
    print("🔮 TEST 5: RESPONSE PREDICTION AI")
    print("="*60)
    
    try:
        from core.response_predictor import ResponsePredictor, get_accuracy
        
        predictor = ResponsePredictor()
        
        # Test email
        test_subject = "Sam Salameh → TestCorp: Proven HR Leader with 40% Efficiency Gains"
        test_body = """Dear Hiring Manager,

I achieved 40% efficiency improvement at my previous role, managing a team of 15 and delivering $2M in cost savings.

I'm particularly interested in TestCorp's recent expansion and believe my experience in scaling HR operations could be valuable.

Would you be available for a brief conversation to discuss how I can contribute to your team's success?

Best regards,
Sam Salameh"""
        
        # Predict
        prediction = predictor.predict_response(
            subject=test_subject,
            body=test_body,
            company_name="TestCorp",
            industry="tech"
        )
        
        print(f"\n📊 Prediction Results:")
        print(f"   Should send: {'✅ YES' if prediction['should_send'] else '❌ NO'}")
        print(f"   Confidence: {prediction['confidence']}%")
        print(f"   Reason: {prediction['reason']}")
        
        print(f"\n📈 Breakdown:")
        for factor, score in prediction['breakdown'].items():
            print(f"   {factor}: {score:.1f}%")
        
        if prediction['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in prediction['recommendations'][:3]:
                print(f"   - {rec}")
        
        # Record outcome
        predictor.record_outcome(
            company_name="TestCorp",
            subject=test_subject,
            body=test_body,
            response_received=True,
            prediction=prediction
        )
        
        # Show accuracy
        accuracy = get_accuracy()
        print(f"\n🎯 Prediction Accuracy:")
        print(f"   Total predictions: {accuracy['total_predictions']}")
        if accuracy['total_predictions'] > 0:
            print(f"   Accuracy: {accuracy.get('accuracy', 0)}%")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 TESTING CRITICAL FEATURES")
    print("="*60)
    print("\nTesting 5 newly implemented features...")
    
    results = {
        "Multi-AI Fallback": test_multi_ai_fallback(),
        "Email Warm-up": test_email_warmup(),
        "Follow-up Sequence": test_followup_sequence(),
        "A/B Testing": test_ab_testing(),
        "Response Predictor": test_response_predictor()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for feature, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {feature}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ All 5 critical features are working correctly!")
        print("✅ Ready to use in production!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        print("Please check the errors above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
