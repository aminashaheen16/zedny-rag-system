import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("TEST: 'Persistent AI' (القدرة على الإقناع) Flow")
print("=" * 80)

# Step 1: Initial Problem (Forgot Password)
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

# Step 2: User demands a human immediately
print("\n[Step 2] User: 'حولني لمهندس مش عايز ذكاء اصطناعي'")
resp2 = requests.post(f"{BASE_URL}/chat", json={
    "message": "حولني لمهندس مش عايز ذكاء اصطناعي",
    "incident_state": incident_state
}, timeout=30)

if resp2.status_code == 200:
    data2 = resp2.json()
    incident_state = data2.get("incident_state")
    print(f"✅ AI Response: {data2.get('answer')[:200]}...")
    
    # Check if AI triggered form OR gave another solution
    if data2.get('action_required') == "show_escalation_form":
         print("\n❌ FAIL: AI gave up too early! It should have tried the second solution.")
    elif "أقدر أحولك" in data2.get('answer') or "بقدر أحولك" in data2.get('answer') or "I can connect you" in data2.get('answer'):
         print("\n🎉 SUCCESS: AI acknowledged escalation request but suggested another solution first!")
    else:
         print("\n🤔 AI Response was neither escalation nor persuasion. Check logic.")
else:
    print(f"❌ Error: {resp2.status_code}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
