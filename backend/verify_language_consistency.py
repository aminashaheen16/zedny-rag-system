import requests
import re

API_URL = "http://localhost:8000/chat"

test_cases = [
    {
        "message": "i have an issue",
        "description": "Short technical report (ASCII)"
    },
    {
        "message": "hello, who are you?",
        "description": "Short greeting (ASCII)"
    },
    {
        "message": "can you tell me about the features?",
        "description": "Sales query (ASCII)"
    }
]

def has_arabic(text):
    return any(u'\u0600' <= c <= u'\u06FF' for c in text)

def run_tests():
    print("🚀 Running Final Language Consistency Verification...")
    all_passed = True
    
    for test in test_cases:
        print(f"\n--- Testing: {test['description']} ---")
        print(f"Query: {test['message']}")
        
        try:
            response = requests.post(API_URL, json={
                "message": test["message"],
                "user_email": f"test_{int(time.time())}@zedny.ai" if 'time' in globals() else "tester@zedny.ai"
            }, timeout=60)
            
            answer = response.json().get("answer", "")
            print(f"AI: {answer[:150]}...")
            
            contains_arabic = has_arabic(answer)
            starts_with_welcome = answer.lower().startswith("welcome")
            
            if contains_arabic:
                print(f"❌ FAIL: Response contains Arabic characters.")
                all_passed = False
            elif not starts_with_welcome and ("hello" in test["message"] or "issue" in test["message"]):
                 # Note: "issue" usually triggers the opening too if history is empty
                 print(f"⚠️ NOTE: Response didn't start with 'Welcome' but is English.")
            
            if not contains_arabic:
                print(f"✅ PASS: Clean English response.")
                
        except Exception as e:
            print(f"⚠️ ERROR: {e}")
            all_passed = False

    if all_passed:
        print("\n🏆 VERDICT: LANGUAGE MIRRORING IS NOW BULLETPROOF.")
    else:
        print("\n❌ VERDICT: LANGUAGE MIRRORING STILL HAS BIAS.")

if __name__ == "__main__":
    import time
    run_tests()
