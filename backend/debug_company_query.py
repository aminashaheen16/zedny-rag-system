import requests
import json

def test_company_query():
    url = "http://127.0.0.1:8000/chat"
    payload = {
        "message": "اي الشركات الي اشتغلتوا معاها",
        "department": "tech",
        "session_id": "debug-session-123",
        "incident_state": None
    }
    
    print(f"🚀 Sending query: {payload['message']}")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            print(f"--- [DEBUG] Intent: {data.get('incident_state', {}).get('category')}")
            print(f"--- [DEBUG] Context Used Size: {len(data.get('context_used', ''))}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_company_query()
