"""
🧪 Semantic Intent Classification Test
Tests if the LLM understands MEANING, not just keywords
"""
import requests
import json

API_URL = "http://localhost:8000/chat"

# Test cases: Various ways to express technical problems
# The LLM should understand ALL of these as ISSUE semantically
test_cases = [
    # Password/Access Issues (No explicit "مشكلة" keyword)
    {"msg": "نسيت الباسورد", "expected": "ISSUE", "reason": "Forgot password = can't access"},
    {"msg": "مش فاكر الرقم السري", "expected": "ISSUE", "reason": "Don't remember PIN = access issue"},
    {"msg": "I can't remember my login", "expected": "ISSUE", "reason": "Can't remember = access problem"},
    
    # Feedback on Solutions (Should stay in ISSUE mode)
    {"msg": "جربت ومشتغلش", "expected": "ISSUE", "reason": "Tried solution, didn't work"},
    {"msg": "لسه برضو", "expected": "ISSUE", "reason": "Still same problem"},
    {"msg": "It didn't help", "expected": "ISSUE", "reason": "Solution feedback"},
    
    # Frustration/Inability (Semantic understanding)
    {"msg": "مش عارف أخش على حسابي", "expected": "ISSUE", "reason": "Can't access account"},
    {"msg": "الموقع مش راضي يفتح", "expected": "ISSUE", "reason": "Site won't open"},
    {"msg": "بيطلعلي حاجة غريبة", "expected": "ISSUE", "reason": "Something strange = error"},
    
    # Video/Media Issues
    {"msg": "الشاشة سوداء", "expected": "ISSUE", "reason": "Black screen = video problem"},
    {"msg": "الصوت مش شغال", "expected": "ISSUE", "reason": "Audio not working"},
    {"msg": "الفيديو بيقف كتير", "expected": "ISSUE", "reason": "Video buffering"},
    
    # Certificate Issues
    {"msg": "فين شهادتي", "expected": "ISSUE", "reason": "Where's my certificate = can't find it"},
    {"msg": "خلصت الكورس بس مش شايف الشهادة", "expected": "ISSUE", "reason": "Finished but no certificate"},
    
    # App/Platform Issues
    {"msg": "التطبيق بيطير", "expected": "ISSUE", "reason": "App crashing (Egyptian slang)"},
    {"msg": "كل ما أفتح التطبيق يقفل", "expected": "ISSUE", "reason": "App keeps closing"},
    
    # Comparison: These should NOT be ISSUE
    {"msg": "مين زدني", "expected": "INFO", "reason": "Asking about Zedny identity"},
    {"msg": "صباح الخير", "expected": "GREETING", "reason": "Just a greeting"},
    {"msg": "بكام الاشتراك", "expected": "SALES", "reason": "Pricing inquiry"},
]

def run_tests():
    print("=" * 70)
    print("🧪 SEMANTIC INTENT CLASSIFICATION TEST")
    print("=" * 70)
    
    passed = 0
    failed = 0
    results = []
    
    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.post(API_URL, json={
                "message": test["msg"],
                "department": "tech",
                "session_id": f"test-semantic-{i}"
            }, timeout=30)
            
            data = response.json()
            
            # Check if the intent in logs matches expected
            # We'll look at the response to infer classification
            answer = data.get("answer", "")
            
            # Determine actual intent from response characteristics
            # This is indirect - we're checking behavior not raw intent
            actual = "UNKNOWN"
            
            # If response contains technical solutions → ISSUE
            if any(word in answer.lower() for word in ["hard refresh", "ctrl", "cache", "متصفح", "جرب", "حل", "خطوات"]):
                actual = "ISSUE"
            # If response contains pricing/sales info → SALES  
            elif any(word in answer.lower() for word in ["سعر", "باقة", "اشتراك", "عرض", "price"]):
                actual = "SALES"
            # If response is a greeting → GREETING
            elif any(word in answer.lower() for word in ["أهلا", "كيف أقدر أساعدك", "مرحبا", "welcome"]):
                actual = "GREETING"
            # If response contains Zedny info → INFO
            elif any(word in answer.lower() for word in ["زدني هي", "منصة", "نقدم", "خدمات"]):
                actual = "INFO"
            
            # For this test, we primarily care about ISSUE classification
            is_correct = (test["expected"] == "ISSUE" and actual == "ISSUE") or \
                        (test["expected"] != "ISSUE" and actual != "ISSUE")
            
            status = "✅ PASS" if is_correct else "❌ FAIL"
            if is_correct:
                passed += 1
            else:
                failed += 1
            
            result = {
                "query": test["msg"],
                "expected": test["expected"],
                "actual": actual,
                "reason": test["reason"],
                "status": status,
                "answer_preview": answer[:100] if answer else "No answer"
            }
            results.append(result)
            
            print(f"\n{status} Test {i}: \"{test['msg']}\"")
            print(f"   Expected: {test['expected']} | Got: {actual}")
            print(f"   Reason: {test['reason']}")
            print(f"   Answer: {answer[:80]}...")
            
        except Exception as e:
            print(f"\n❌ ERROR Test {i}: {test['msg']}")
            print(f"   Error: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTS: {passed}/{len(test_cases)} passed ({100*passed//len(test_cases)}%)")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    run_tests()
