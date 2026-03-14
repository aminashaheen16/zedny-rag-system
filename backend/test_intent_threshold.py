import requests
import json
import time

API_URL = "http://localhost:8001/chat"

def test_intent_threshold():
    # This query contains "مش" which is a technical keyword, 
    # but the intent is actually informational inquiry.
    queries = [
        "أنا مش فاهم يعني إيه التعليم الترفيهي؟",
        "كورس القيادة شغال إزاي؟",
        "ليه مش عارف أشوف أسعار الباقات؟"
    ]
    
    print("🚀 --- TESTING INTENT-BASED RAG TRIGGERING --- 🚀\n")
    
    for query in queries:
        print(f"🔍 Testing Query: \"{query}\"")
        payload = {
            "message": query,
            "user_email": "tester@zedny.ai",
            "session_id": f"intent_test_{int(time.time())}"
        }
        
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            context = data.get("context_used", "")
            
            # Check if RAG was used
            if context and len(context) > 20:
                print("✅ RAG HIT: Context was retrieved.")
            else:
                print("❌ RAG SKIPPED: It likely fell into ISSUE intent and bypassed RAG.")
            
            # Also check answer tone
            answer = data.get("answer", "")
            print(f"   [AI Snippet]: {answer[:80]}...")
        else:
            print(f"❌ API ERROR: {response.status_code}")
        print("-" * 50)

if __name__ == "__main__":
    test_intent_threshold()
