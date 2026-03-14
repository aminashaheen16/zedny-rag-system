"""
🛡️ FIRST MESSAGE GUARD - Test Suite
Tests the professional implementation of first-message protection.
"""

import requests
import time

API_URL = "http://127.0.0.1:8000/chat"

def test_first_message(message: str, expected_not_issue: bool = True):
    """Test a first message and verify it's NOT classified as ISSUE when expected."""
    session_id = f"test_{int(time.time() * 1000)}"
    
    try:
        response = requests.post(API_URL, json={
            "message": message,
            "session_id": session_id,
            "user_email": "test@test.com"
        }, timeout=30)
        
        data = response.json()
        answer = data.get("answer", "")[:100]
        
        # Check if response looks like ISSUE handling
        issue_indicators = [
            "أي جهاز", "المتصفح", "device", "browser", 
            "مشكلة تقنية", "technical problem",
            "1️⃣", "2️⃣"  # Discovery menu for issues
        ]
        
        looks_like_issue = any(ind in answer for ind in issue_indicators)
        
        # For first messages, we expect them NOT to be treated as issues
        if expected_not_issue:
            status = "✅ PASS" if not looks_like_issue else "❌ FAIL"
            result = "Not treated as issue" if not looks_like_issue else "WRONGLY treated as issue"
        else:
            status = "✅ PASS" if looks_like_issue else "❌ FAIL"
            result = "Correctly treated as issue" if looks_like_issue else "NOT treated as issue"
        
        print(f"\n{status}: '{message}'")
        print(f"   Result: {result}")
        print(f"   Answer: {answer}...")
        
        return not looks_like_issue if expected_not_issue else looks_like_issue
        
    except Exception as e:
        print(f"\n❌ ERROR: '{message}' - {e}")
        return False

def run_tests():
    print("\n" + "="*60)
    print("🛡️ FIRST MESSAGE GUARD - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test cases that should NOT be treated as ISSUE
    test_cases_not_issue = [
        "مين زدني",           # Identity question
        "مين انت",             # Identity question
        "ما هي زدني",          # INFO question
        "ايه هي زدني",         # INFO question
        "what is zedny",       # English INFO
        "who are you",         # English identity
        "مرحبا",              # Greeting
        "hello",              # English greeting
        "كيف أشترك",          # Question starter
        "عندي استفسار",        # Short ambiguous (should be INFO)
        "محتاج مساعدة",        # Short ambiguous (should be INFO)
        "اسعار الباقات",       # Sales inquiry
    ]
    
    print("\n📋 Testing messages that should NOT be treated as ISSUE:")
    print("-"*60)
    
    for msg in test_cases_not_issue:
        results.append(test_first_message(msg, expected_not_issue=True))
        time.sleep(2)  # Avoid rate limiting
    
    # Test cases that SHOULD be treated as ISSUE
    test_cases_issue = [
        "مش عارف أدخل الموقع ومحاولت كتير",       # Clear issue with detail
        "الفيديو مش شغال وبيطلعلي شاشة سودا",    # Clear technical issue
        "not working at all and showing error",  # Clear English issue
    ]
    
    print("\n📋 Testing messages that SHOULD be treated as ISSUE:")
    print("-"*60)
    
    for msg in test_cases_issue:
        results.append(test_first_message(msg, expected_not_issue=False))
        time.sleep(2)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "="*60)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("✅ ALL TESTS PASSED! First Message Guard is working correctly.")
    else:
        print(f"⚠️ {total - passed} tests failed. Please review the implementation.")

if __name__ == "__main__":
    run_tests()
