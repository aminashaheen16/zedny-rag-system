import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Quick Single Test
print("=" * 60)
print("QUICK TEST - Video Buffering (Arabic)")
print("=" * 60)

response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "الفيديو بيقطع والنت عندي سريع جدا"}
)

if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS")
    print(f"Category: {data['incident_state']['category']}")
    print(f"Status: {data['incident_state']['status']}")
    print(f"AI Response (first 200 chars): {data['answer'][:200]}...")
else:
    print(f"❌ ERROR {response.status_code}")
    print(response.text[:500])

print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
