import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_scenario(name, message, session_id=None):
    print(f"\n--- 🧪 TEST: {name} ---")
    payload = {
        "message": message,
        "session_id": session_id,
        "user_email": "test_senior@zedny.ai"
    }
    
    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=25)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"⏱️ Time: {elapsed:.2f}s")
            print(f"🤖 AI: {data['answer'][:200]}...")
            print(f"🎯 Intent: {data['incident_state']['category']}")
            print(f"🔍 Status: {data['incident_state']['status']}")
            return data['incident_state']['session_id']
        else:
            print(f"❌ FAILED: {response.status_code} | {response.text}")
    except Exception as e:
        print(f"💥 ERROR: {e}")
    return None

if __name__ == "__main__":
    print("🚀 Starting Final Production Validation...")
    
    # 1. Test General Knowledge (RAG)
    sid = test_scenario("General Knowledge (RAG)", "مين زدني؟")
    
    # 2. Test Competitor Pivot
    test_scenario("Competitor Pivot", "ليه أشترك في زدني مش في يوديمي؟", session_id=sid)
    
    # 3. Test Technical Semantic Detection (No Keywords)
    test_scenario("Technical Diagnostic", "الفيديو بيقطع ومش عارف أشوف الكورس", session_id=sid)
    
    print("\n✅ Validation Run Complete.")
