import requests
import json
import uuid
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_test_case(name, messages, expected_category, expected_action=None):
    print(f"\n========================================")
    print(f"[TEST] Scenario: {name}")
    print(f"========================================")
    session_id = str(uuid.uuid4())
    
    current_state = None
    
    for i, msg in enumerate(messages):
        # Don't print the actual message to avoid Unicode errors
        print(f"   [User Message #{i+1}]")
        
        payload = {
            "message": msg,
            "session_id": session_id,
            "user_email": "test_stress@zedny.com"
        }
        
        # Pass state logic
        if current_state:
            payload["incident_state"] = current_state

        try:
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            if response.status_code != 200:
                print(f"   [ERROR] HTTP {response.status_code}")
                return
            
            data = response.json()
            # Safely truncate answer without printing Arabic
            answer_len = len(data.get("answer", ""))
            current_state = data.get("incident_state")
            action = data.get("action_required")
            should_escalate = data.get("should_escalate")
            
            category = current_state.get("category") if current_state else "Unknown"
            status = current_state.get("status") if current_state else "Unknown"
            
            print(f"   [AI Response Length: {answer_len} chars]")
            print(f"   -> Category: {category} | Status: {status}")
            
            if action:
                print(f"   -> Action: {action}")
            
            # Verification on First Turn (as requested)
            if i == 0:
                if category == expected_category:
                    print(f"   [PASS] Initial Classification = {expected_category}")
                else:
                    print(f"   [FAIL] Expected {expected_category}, got {category}")
            
            # Verification of Action (if expected)
            if expected_action and action == expected_action:
                 print(f"   [PASS] Action {expected_action} triggered")
            elif expected_action and action != expected_action:
                 print(f"   [FAIL] Expected action {expected_action}, got {action}")

        except Exception as e:
            print(f"   [EXCEPTION] {str(e)[:100]}")

def main():
    print("\n" + "="*60)
    print(" COMPREHENSIVE FLOW TEST - User Journey Analysis")
    print("="*60)
    
    # CASE 1: Clear Technical Issue (Arabic)
    run_test_case(
        "Tech - Video Buffering (AR)", 
        ["الفيديو بيقطع والنت عندي سريع جدا", "جربت ومنفعش"], 
        "Tech"
    )

    # CASE 2: Clear Technical Issue (English)
    run_test_case(
        "Tech - Certificate Download (EN)", 
        ["I cannot download my certificate, it fails", "Yes I tried that"], 
        "Tech"
    )

    # CASE 3: Sales Radar (B2B Intent)
    run_test_case(
        "Sales Radar - B2B Training (AR)", 
        ["عندي شركة وعايز ادرب 50 موظف"], 
        "Sales",
        expected_action="show_escalation_form"
    )

    # CASE 4: General Inquiry (Non-Tech)
    run_test_case(
        "General Info - Course Inquiry (AR)", 
        ["ايه الكورسات المتاحة عندكم؟"], 
        "General"
    )

    # CASE 5: Ambiguous Tech (Login Issue)
    run_test_case(
        "Tech - Login Issue (AR)",
        ["مش عارف ادخل حسابي"], 
        "Tech"
    )

    # CASE 6: Sales - Individual Pricing (Should NOT trigger B2B)
    run_test_case(
        "Sales - Individual Pricing (EN)",
        ["How much is the subscription for individuals?"],
        "Sales"
    )
    
    # CASE 7: Multiple Tech Issues
    run_test_case(
        "Tech - Multi-Step (EN)",
        ["My password is not working", "I tried resetting it", "Still can't login"],
        "Tech"
    )

    print("\n" + "="*60)
    print(" TEST SUITE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
