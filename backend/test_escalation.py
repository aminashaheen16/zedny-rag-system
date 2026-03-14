"""
Test Script: Verify Escalation Flow
===================================
This script tests the full diagnostic failure path:
1. User reports issue ("Video not working").
2. AI suggests solution 1 -> User says "No".
3. AI suggests solution 2 -> User says "No".
4. AI suggests solution 3 -> User says "No".
5. Escalation triggers -> Verification of Report & Button Signal.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
import time

API_URL = "http://localhost:8000/chat"
SESSION_ID = f"esc_test_{int(time.time())}"

def send_msg(message, desc):
    print(f"\n[{desc}] User: {message}")
    payload = {
        "message": message,
        "user_email": "test_esc@test.com",
        "session_id": SESSION_ID
    }
    try:
        res = requests.post(API_URL, json=payload)
        data = res.json()
        ans = data.get("answer", "")
        action = data.get("action_required", None)
        print(f"[AI]: {ans[:150]}...")
        if action:
            print(f"⚠️ ACTION REQUIRED: {action}")
        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print(f"Starting Escalation Test (Session: {SESSION_ID})")
    
    # 1. Report Issue
    send_msg("الفيديو مش شغال عندي خالص", "1. Init Issue")
    
    # 2. Reject Solutions (Loop until max attempts = 3)
    # Note: We need to make sure we hit the max_solutions limit logic in chat.py
    # Each "No" response to a solution increases the counter.
    
    for i in range(3):
        time.sleep(1)
        send_msg("جربت وبردو مش شغال", f"{i+2}. Reject Solution")

    # 3. Final Check (Should trigger escalation)
    time.sleep(1)
    last_res = send_msg("لسه مش شغال، أنا زهقت", "Final Rejection")
    
    if last_res and last_res.get("action_required") == "register_details":
        print("\n✅ TEST PASSED: Escalation Triggered & Button Signal Received!")
    else:
        print("\n❌ TEST FAILED: Escalation did not trigger correctly.")
