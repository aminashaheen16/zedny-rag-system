import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("SCENARIO TEST: Wrong Solution Detection")
print("=" * 70)

# Step 1: Initial Problem - Forgot Password
print("\n[STEP 1] User: 'نسيت الباسورد'")
resp1 = requests.post(f"{BASE_URL}/chat", json={"message": "نسيت الباسورد"}, timeout=30)
if resp1.status_code == 200:
    data1 = resp1.json()
    print(f"✅ Category: {data1['incident_state']['category']}")
    print(f"✅ Status: {data1['incident_state']['status']}")
    print(f"✅ AI Response: {data1['answer'][:150]}...")
    incident_state = data1['incident_state']
else:
    print(f"❌ ERROR: {resp1.status_code}")
    exit()

time.sleep(2)

# Step 2: User says "This solution is not related"
print("\n[STEP 2] User: 'الحل دا ملوش علاقة بنسيان الباسورد'")
resp2 = requests.post(f"{BASE_URL}/chat", json={
    "message": "الحل دا ملوش علاقة بنسيان الباسورد",
    "incident_state": incident_state
}, timeout=30)
if resp2.status_code == 200:
    data2 = resp2.json()
    print(f"✅ Category: {data2['incident_state']['category']}")
    print(f"✅ Status: {data2['incident_state']['status']}")
    print(f"✅ AI Response: {data2['answer'][:300]}...")
    
    # Check if it's the apology/escalation response
    if "أعتذر" in data2['answer'] or "apologize" in data2['answer'].lower():
        print("\n🎉 SUCCESS: Wrong solution apology detected!")
    elif "نسيت الباسورد" in data2['answer'] or "password" in data2['answer'].lower():
        print("\n🎉 SUCCESS: AI understood the original problem!")
    else:
        print("\n⚠️ Response may need review")
else:
    print(f"❌ ERROR: {resp2.status_code}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
