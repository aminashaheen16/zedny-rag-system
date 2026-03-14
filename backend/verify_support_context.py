import requests
import json
import time

API_URL = "http://localhost:8000/chat"

def run_test():
    print("🚀 Running Technical Support Context Persistence Test...")
    
    session_id = f"test_context_{int(time.time())}"
    user_email = "ctx_tester@zedny.ai"
    
    # CASE 1: Progressive Discovery
    turns = [
        {
            "msg": "error massage when i login",
            "check": ["login", "effectively", "detail"],
            "desc": "Initial login error report"
        },
        {
            "msg": "error 404 on web Browser",
            "check": ["404", "browser", "cache", "incognito", "isolate"],
            "desc": "Adding 404 and Browser context"
        }
    ]
    
    incident_state = None
    
    for i, turn in enumerate(turns):
        print(f"\n--- Turn {i+1}: {turn['desc']} ---")
        print(f"User: {turn['msg']}")
        
        payload = {
            "message": turn["msg"],
            "user_email": user_email,
            "session_id": session_id,
            "incident_state": incident_state
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            data = response.json()
            answer = data.get("answer", "")
            incident_state = data.get("incident_state")
            
            print(f"AI: {answer}")
            
            # Anti-Redundancy Check: In the second turn, it should NOT ask "where" or "what device" if already told.
            if i == 1:
                generic_questions = ["Where exactly is the problem", "Zedny mobile app", "web browser", "Specify the exact"]
                found_redundancy = any(q.lower() in answer.lower() for q in generic_questions)
                
                # However, it SHOULD contain the specific 404 logic
                found_context = "404" in answer or "browser" in answer.lower()
                
                if found_redundancy:
                    print(f"❌ FAIL: AI asked redundant questions after context was provided.")
                elif not found_context:
                    print(f"❌ FAIL: AI did not incorporate the new '404' context.")
                else:
                    print(f"✅ PASS: AI incorporated context and avoided redundancy.")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            break

if __name__ == "__main__":
    run_test()
