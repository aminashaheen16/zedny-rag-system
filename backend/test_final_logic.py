
import requests
import json

URL = "http://127.0.0.1:8000/chat"

def test_discovery_logic():
    print("\n" + "="*60)
    print("🔍 VERIFYING LANGUAGE & DISCOVERY LOGIC")
    print("="*60)

    # Test Case 1: Greeting -> Should show Discovery Menu in Arabic
    payload1 = {
        "message": "اهلا",
        "session_id": "test_welcome_ar",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Greeting (Arabic): '{payload1['message']}'")
    res1 = requests.post(URL, json=payload1).json()
    print(f"   Response: {res1.get('answer')[:100]}...")
    
    # Test Case 2: Specific Question on First Turn -> Should answer directly
    payload2 = {
        "message": "مين زدني",
        "session_id": "test_identity_direct",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Identity (Arabic/Direct): '{payload2['message']}'")
    res2 = requests.post(URL, json=payload2).json()
    print(f"   Response: {res2.get('answer')[:200]}...")

    # Test Case 3: Mixed Language / English Greeting -> English Menu
    payload3 = {
        "message": "Hello",
        "session_id": "test_welcome_en",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Greeting (English): '{payload3['message']}'")
    res3 = requests.post(URL, json=payload3).json()
    print(f"   Response: {res3.get('answer')[:100]}...")

if __name__ == "__main__":
    test_discovery_logic()
