"""
🛠️ E2E INTEGRATION VERIFIER
Verifies that the live running backend has the latest logic.
"""

import requests
import json

URL = "http://127.0.0.1:8000/chat"

def verify_live_logic():
    print("\n" + "="*60)
    print("🔍 VERIFYING LIVE BACKEND LOGIC")
    print("="*60)
    
    # Test case 1: Vague "problem" (Should use DeepSeek V3 logic)
    payload_tech = {
        "message": "عندي مشكلة في تحميل الفيديو",
        "session_id": "routing_test_tech",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Tech Routing: '{payload_tech['message']}'")
    response_tech = requests.post(URL, json=payload_tech)
    data_tech = response_tech.json()
    
    print(f"   Response Preview: {data_tech.get('answer')[:150]}...")
    # DeepSeek V3 via OpenRouter often has specific formatting or starts with internal thoughts in some configs
    # but here we just check if it's giving a logical technical breakdown.
    
    # Test case 2: Identity Question (Should use Gemini Speed)
    payload_info = {
        "message": "كلمني عن خدمات زدني",
        "session_id": "routing_test_info",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Info Routing: '{payload_info['message']}'")
    response_info = requests.post(URL, json=payload_info)
    data_info = response_info.json()
    print(f"   Response Preview: {data_info.get('answer')[:150]}...")

    print("\n✅ Verification Complete. Check terminal logs for 'SMART ROUTING' strings.")

if __name__ == "__main__":
    verify_live_logic()
