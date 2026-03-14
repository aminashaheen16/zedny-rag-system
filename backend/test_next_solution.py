import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("TEST: 'Try Another Solution' (جرب حل تاني) Flow")
print("=" * 80)

# Step 1: Initial Problem
print("\n[Step 1] User: 'نسيت كلمة المرور'")
resp1 = requests.post(f"{BASE_URL}/chat", json={"message": "نسيت كلمة المرور"}, timeout=30)
if resp1.status_code == 200:
    data1 = resp1.json()
    incident_state = data1.get("incident_state")
    print(f"✅ AI Response: {data1.get('answer')[:120]}...")
else:
    print(f"❌ Error: {resp1.status_code}")
    exit()

time.sleep(2)

# Step 2: Request Next Solution
print("\n[Step 2] User: 'جرب حل تاني'")
resp2 = requests.post(f"{BASE_URL}/chat", json={
    "message": "جرب حل تاني",
    "incident_state": incident_state
}, timeout=30)

if resp2.status_code == 200:
    data2 = resp2.json()
    print(f"✅ AI Response: {data2.get('answer')[:120]}...")
    # Check if AI understood it's a follow-up or apologized for no more solutions
    if "أعتذر" in data2.get('answer') or "عذراً" in data2.get('answer'):
         print("\n🎉 SUCCESS: AI understood request and apologized (if no other solution) or moved forward.")
    else:
         print("\n🤔 AI Response length: ", len(data2.get('answer')))
else:
    print(f"❌ Error: {resp2.status_code}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
