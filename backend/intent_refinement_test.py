import requests
import json

def test_intent(message):
    url = "http://localhost:8000/chat"
    payload = {
        "message": message,
        "session_id": f"test_refinement_{message[:5]}"
    }
    
    try:
        print(f"\n[QUERY]: {message}")
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        answer = data.get('answer')
        if answer is not None:
            print(f"[ANSWER]: {answer[:150]}...")
        else:
            print(f"❌ Answer missing in response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except requests.exceptions.Timeout:
        print(f"❌ Timeout error testing '{message}' after 30s")
        return None
    except Exception as e:
        print(f"❌ Error testing '{message}': {e}")
        return None

if __name__ == "__main__":
    print("--- 🚀 STARTING INTENT REFINEMENT SMOKE TEST ---")
    
    # 1. Test Social Greeting (The specific bug reported)
    test_intent("أهلا صباح الخير")
    
    # 2. Test Vague Sales
    test_intent("بكام")
    
    # 3. Test Vague Issue
    test_intent("عندي مشكله")
    
    # 4. Test Vague Info
    test_intent("قولي عن زدني")
    
    print("\n--- ✅ SMOKE TEST COMPLETE ---")
