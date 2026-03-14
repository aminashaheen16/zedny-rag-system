import requests
import json

def test_brand_integrity():
    url = "http://localhost:8001/chat"
    headers = {"Content-Type": "application/json"}
    
    # Session state to maintain history
    session_id = "test_brand_integrity_1"
    incident_state = {"session_id": session_id}
    
    scenarios = [
        ("من زدني", "Initial info check"),
        ("اي مميزات زدني", "Feature list check"),
        ("اقترح منصة كورسات تانية", "COMPETITOR PIVOT CHECK")
    ]
    
    print("--- BRAND INTEGRITY VERIFICATION START ---")
    
    for msg, label in scenarios:
        print(f"\n[{label}] Sending: {msg}")
        payload = {
            "message": msg,
            "user_email": "test@zedny.ai",
            "incident_state": incident_state
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
            incident_state = data["incident_state"] # Update state
            
            print(f"Response:\n{answer}")
            
            # Validation for the final scenario
            if label == "COMPETITOR PIVOT CHECK":
                competitors = ["udemy", "coursera", "linkedin learning", "lynda"]
                found_competitor = any(c in answer.lower() for c in competitors)
                if found_competitor:
                    print("\n❌ FAILED: Competitor name found in response!")
                else:
                    print("\n✅ PASSED: No competitor names mentioned.")
                
                # Check for repetition of the feature list
                # (Simple check: if 3+ bullets from previous response are repeated)
                if "Edutainment" in answer and "Vodafone" in answer:
                    print("⚠️ WARNING: Feature list seems repeated.")
                else:
                    print("✅ PASSED: Variety rule enforced (no feature list re-dump).")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    print("\n--- BRAND INTEGRITY VERIFICATION END ---")

if __name__ == "__main__":
    test_brand_integrity()
