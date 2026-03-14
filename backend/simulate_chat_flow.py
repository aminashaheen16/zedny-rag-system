import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
SESSION_ID = f"test_sim_{int(time.time())}"
USER_EMAIL = "test_user@zedny.ai"

def log(text):
    with open("simulation_log.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    # Also try to print safely
    try:
        print(text)
    except:
        pass

def send_message(message):
    url = f"{BASE_URL}/chat"
    payload = {
        "message": message,
        "department": "tech",
        "user_email": USER_EMAIL,
        "session_id": SESSION_ID
    }
    
    log(f"\n[USER]: {message}")
    try:
        response = requests.post(url, json=payload, timeout=60) # Increased timeout
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "No answer")
        state = data.get("incident_state", {})
        
        log(f"[AI]: {answer}")
        
        time.sleep(2) # Wait for log write
        log(f"[DEBUG State]: Status={state.get('status')}, Intent={state.get('step')}, Device={state.get('device_info')}")
        return data
    except Exception as e:
        log(f"[ERROR]: {e}")
        return None

def run_simulation():
    # Clear log file
    with open("simulation_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Starting Simulation with Session ID: {SESSION_ID}\n")
        
    log("-" * 60)
    
    # Turn 1: Report Issue
    send_message("الموقع مش شغال")
    log("-" * 60)
    
    # Turn 2: Provide Device Info
    send_message("laptop chrome")
    log("-" * 60)
    
    # Turn 3: User describes symptom "It freezes".
    # Expectation: AI should OFFER SOLUTION immediately, NO greetings, NO "What happens?".
    send_message("الموقع بيعلق مهنج")
    log("-" * 60)

if __name__ == "__main__":
    run_simulation()
