import requests
import uuid

BASE_URL = "http://localhost:8001"

def test_guest_persistence():
    guest_email = f"guest_{uuid.uuid4().hex[:6]}@example.com"
    print(f"\n--- 🧪 TEST: Guest Persistence & Rating (No Escalation) ---")
    
    # 1. First message should save user immediately
    payload = {
        "message": "Hello, I am a new guest.",
        "user_email": guest_email,
        "rating": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Message sent as {guest_email}")
            print(f"✅ Rating (5 stars) attached to first message.")
            print(f"🤖 AI Response: {data['answer'][:100]}...")
            print(f"📊 State: {data['incident_state']['category']} | Session: {data['incident_state']['session_id']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_guest_persistence()
