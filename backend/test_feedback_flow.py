import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("SCENARIO TEST: Video Issue → Feedback Flow")
print("=" * 70)

# Step 1: Initial Problem
print("\n[STEP 1] User: 'الفيديو بيقطع والنت عندي سريع'")
resp1 = requests.post(f"{BASE_URL}/chat", json={"message": "الفيديو بيقطع والنت عندي سريع"}, timeout=30)
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

# Step 2: Feedback - "Didn't work"
print("\n[STEP 2] User: 'حاولت ومشتغلش'")
resp2 = requests.post(f"{BASE_URL}/chat", json={
    "message": "حاولت ومشتغلش",
    "incident_state": incident_state
}, timeout=30)
if resp2.status_code == 200:
    data2 = resp2.json()
    print(f"✅ Category: {data2['incident_state']['category']}")
    print(f"✅ Status: {data2['incident_state']['status']}")
    print(f"✅ AI Response: {data2['answer'][:300]}...")
    
    # Check if it's smart feedback response
    if "فاهم" in data2['answer'] or "understand" in data2['answer'].lower():
        print("\n🎉 SUCCESS: Smart feedback response detected!")
    else:
        print("\n⚠️ WARNING: Response may not be the expected feedback handler")
else:
    print(f"❌ ERROR: {resp2.status_code}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
