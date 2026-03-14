
import requests
import json

URL = "http://127.0.0.1:8000/chat"

def test_tech_restore():
    print("\n" + "="*60)
    print("🚑 VERIFYING EMERGENCY TECH RESTORE")
    print("="*60)

    # Test Case 1: Specific Tech Issue -> Should NOT be empty and should show RAG content
    payload1 = {
        "message": "نسيت الباسورد",
        "session_id": "test_emergency_pwd",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Tech Issue (Forgot Password): '{payload1['message']}'")
    res1 = requests.post(URL, json=payload1).json()
    answer = res1.get('answer', '')
    print(f"   Answer Length: {len(answer)}")
    print(f"   Response Preview: {answer[:300]}...")
    
    if len(answer) < 50:
        print("❌ FAILED: Answer is too short or empty!")
    elif "password" in answer.lower() or "كلمة" in answer or "باسورد" in answer:
        print("✅ SUCCESS: Technical solution delivered.")
    else:
        print("⚠️ WARNING: Answer received but content might not be specific enough.")

    # Test Case 2: Vague issue -> Should trigger Discovery
    payload2 = {
        "message": "عندي مشكلة",
        "session_id": "test_emergency_vague",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Vague Issue: '{payload2['message']}'")
    res2 = requests.post(URL, json=payload2).json()
    answer2 = res2.get('answer', '')
    print(f"   Response Preview: {answer2[:200]}...")
    
    if "1️⃣" in answer2:
        print("✅ SUCCESS: Discovery menu triggered correctly.")
    else:
        print("❌ FAILED: Discovery menu NOT found in vague response.")

if __name__ == "__main__":
    test_tech_restore()
