import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_chat_flow():
    print("\n--- Testing Course Inquiry Flow ---\n")
    
    # 1. First message: "أي الكورسات اللي بتقدموها؟"
    message1 = "أي الكورسات اللي بتقدموها؟"
    payload1 = {
        "message": message1,
        "user_email": "test_user@example.com"
    }
    
    print(f"User: {message1}")
    try:
        response1 = requests.post(f"{BASE_URL}/chat", json=payload1)
        response1.raise_for_status()
        data1 = response1.json()
        print(f"AI: {data1.get('answer')}\n")
        
        # 2. Extract session_id or incident_state to maintain context
        incident_state = data1.get("incident_state")
        
        # 3. Second message: "أنا لو بشتغل معلمة أي الكورسات اللي عندكم تفيدني"
        message2 = "أنا لو بشتغل معلمة أي الكورسات اللي عندكم تفيدني"
        payload2 = {
            "message": message2,
            "incident_state": incident_state,
            "user_email": "test_user@example.com"
        }
        
        print(f"User: {message2}")
        response2 = requests.post(f"{BASE_URL}/chat", json=payload2)
        response2.raise_for_status()
        data2 = response2.json()
        print(f"AI: {data2.get('answer')}\n")
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_chat_flow()
