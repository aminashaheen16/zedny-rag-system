
import requests
import json

URL = "http://127.0.0.1:8000/chat"

def test_tech_restore_v3():
    print("\n" + "="*60)
    print("🚑 FINAL VERIFICATION V3: EMERGENCY TECH RESTORE")
    print("="*60)

    # Test Case 1: "نسيت الباسورد"
    payload1 = {
        "message": "نسيت الباسورد",
        "session_id": "v3_verify_pwd",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Tech Issue (Forgot Password): '{payload1['message']}'")
    res1 = requests.post(URL, json=payload1).json()
    answer1 = res1.get('answer', '')
    print(f"   Response: {answer1[:300]}...")
    
    if "نسيت كلمة السر" in answer1 or "باسورد" in answer1:
        if "هل" in answer1 and len(answer1) < 100: # If it's just a question
             print("⚠️ WARNING: Delivered a question, not the full steps yet.")
        else:
             print("✅ SUCCESS: Technical solution delivered (RAG Hit).")
    else:
        print("❌ FAILED: RAG solution for password NOT delivered.")

    # Test Case 2: "لا استطيع تسجيل الدخول"
    payload2 = {
        "message": "لا استطيع تسجيل الدخول",
        "session_id": "v3_verify_login",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Login Issue (Arabic): '{payload2['message']}'")
    res2 = requests.post(URL, json=payload2).json()
    answer2 = res2.get('answer', '')
    print(f"   Response: {answer2[:300]}...")
    
    if "كوكيز" in answer2 or "متصفح" in answer2 or "Caps Lock" in answer2:
        print("✅ SUCCESS: Login solution delivered (RAG Hit).")
    else:
        print("❌ FAILED: Login solution NOT delivered.")

    # Test Case 3: Vague issue
    payload3 = {
        "message": "عندي مشكلة",
        "session_id": "v3_verify_vague",
        "user_email": "verify@test.com"
    }
    print(f"\n📡 Testing Vague Issue: '{payload3['message']}'")
    res3 = requests.post(URL, json=payload3).json()
    answer3 = res3.get('answer', '')
    if "1️⃣" in answer3:
        print("✅ SUCCESS: Discovery menu triggered correctly.")
    else:
        print("❌ FAILED: Discovery menu NOT found.")

if __name__ == "__main__":
    test_tech_restore_v3()
