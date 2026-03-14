import requests
import uuid

BASE_URL = "http://localhost:8001"

def test_natural_lead_capture():
    print(f"\n--- 🧪 TEST: Natural Language Lead Capture (Guest) ---")
    
    # Simulate a guest who starts talking and mentions their email
    guest_email = f"lead_{uuid.uuid4().hex[:6]}@zedny-test.ai"
    message = f"أهلاً، أنا مهتم بخدماتكم. اسمي أحمد وإيميلي هو {guest_email}."
    
    payload = {
        "message": message,
        "user_email": None  # No email in payload (Anonymous Guest initially)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Message sent: '{message}'")
            # The backend should have caught the email and linked it
            # We can't see the DB results directly here without more code, 
            # but we check if the session now has this email.
            print(f"🤖 AI Response: {data['answer'][:100]}...")
            
            # If our logic worked, the next save would use this email.
            # We'll check the logs in the console for '--- [LEAD CAPTURED]'
            print(f"💡 Check your console for: '--- [LEAD CAPTURED] Extracted email from talk: {guest_email}'")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_natural_lead_capture()
