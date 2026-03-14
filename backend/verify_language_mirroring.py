import requests

API_URL = "http://localhost:8000/chat"

test_cases = [
    {
        "message": "Who are you?",
        "expected_lang": "en"
    },
    {
        "message": "Tell me about Zedny features",
        "expected_lang": "en"
    },
    {
        "message": "How can Zedny help my company?",
        "expected_lang": "en"
    },
    {
        "message": "I have an issue with video loading",
        "expected_lang": "en"
    }
]

def has_arabic(text):
    return any(u'\u0600' <= c <= u'\u06FF' for c in text)

def run_tests():
    print("🚀 Verifying Language Mirroring (EN to EN)...")
    all_passed = True
    
    for test in test_cases:
        try:
            response = requests.post(API_URL, json={
                "message": test["message"],
                "user_email": "lang_test@zedny.ai"
            }, timeout=60)
            
            answer = response.json().get("answer", "")
            
            contains_arabic = has_arabic(answer)
            
            if test["expected_lang"] == "en" and contains_arabic:
                print(f"❌ FAIL: Query '{test['message']}' triggered ARABIC response.")
                print(f"   Response Preview: {answer[:100]}...")
                all_passed = False
            else:
                print(f"✅ PASS: Query '{test['message']}' responded correctly.")
                
        except Exception as e:
            print(f"⚠️ ERROR on query '{test['message']}': {e}")
            all_passed = False

    if all_passed:
        print("\n🏆 VERDICT: Language Mirroring is now STRICT and working correctly.")
    else:
        print("\n❌ VERDICT: Language Mirroring still has issues.")

if __name__ == "__main__":
    run_tests()
