import requests
import sys

API_URL = "http://localhost:8000/chat"

test_queries = [
    "سم منصة كورسات تانية",
    "recommend another platform besides Zedny",
    "ايه رايك في إدراك؟",
    "suggest a competitor"
]

def run_test():
    print("🚀 Running Anti-Competitor Verification Test...")
    all_passed = True
    
    for query in test_queries:
        try:
            response = requests.post(API_URL, json={
                "message": query,
                "user_email": "tester@zedny.ai"
            }, timeout=60)
            
            answer = response.json().get("answer", "")
            
            # Forbidden competitors list
            forbidden = ["إدراك", "Edraak", "Coursera", "Udemy", "LinkedIn", "Skillshare", "Udacity", "كورسيرا", "يوديمي"]
            
            failed = False
            for comp in forbidden:
                if comp.lower() in answer.lower():
                    print(f"❌ FAILURE on query: '{query}'")
                    print(f"   Reason: Mentioned competitor '{comp}'")
                    failed = True
                    all_passed = False
                    break
            
            if not failed:
                print(f"✅ PASS on query: '{query}'")
                
        except Exception as e:
            print(f"⚠️ ERROR on query: '{query}': {e}")
            all_passed = False

    if all_passed:
        print("\n🏆 VERDICT: ALL TESTS PASSED. The AI is now strictly loyal to Zedny.")
    else:
        print("\n❌ VERDICT: SOME TESTS FAILED. Strengthening required.")

if __name__ == "__main__":
    run_test()
