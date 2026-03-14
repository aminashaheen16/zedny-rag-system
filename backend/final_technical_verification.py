import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def run_scenario(name, messages):
    print(f"\n--- SCENARIO: {name} ---")
    incident_state = None
    
    for i, msg in enumerate(messages):
        print(f"\n[Step {i+1}] User: '{msg}'")
        payload = {"message": msg}
        if incident_state:
            payload["incident_state"] = incident_state
            
        try:
            resp = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                incident_state = data.get("incident_state")
                print(f"✅ AI Status: {incident_state.get('status')}")
                print(f"✅ AI Intent (Simulated): {data.get('answer')[:120]}...")
            else:
                print(f"❌ Error: {resp.status_code} - {resp.text}")
                return
        except Exception as e:
            print(f"❌ Exception: {e}")
            return
        time.sleep(2)

# Test 1: Video Buffering -> Negative Feedback -> Escalation Offer
# Test 2: Forgot Password -> Rejection (Unrelated) -> Corrected Response

test_scenarios = [
    {
        "name": "Feedback Loop (Video Issue)",
        "messages": [
            "الفيديو بيقطع والنت سريع عندي", 
            "جربت ده ومشتغلش برضو",
            "لسه المشكلة موجودة"
        ]
    },
    {
        "name": "Rejection & Correction (Password Recovery)",
        "messages": [
            "نسيت الباسورد ومش عارف ادخل",
            "الحل ده ملوش اي علاقة باللي انا سألت فيه",
            "تمام هجرب"
        ]
    }
]

print("=" * 80)
print("STARTING FINAL TECHNICAL VERIFICATION")
print("=" * 80)

for scenario in test_scenarios:
    run_scenario(scenario["name"], scenario["messages"])

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
