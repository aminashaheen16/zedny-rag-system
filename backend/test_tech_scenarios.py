"""
Technical Support Stress Test - Multi-Turn Simulations
Tests complex scenarios like SSO, SCORM, and Video glitches with multi-step diagnostics.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"

SCENARIOS = [
    {
        "name": "SSO Login Failure (Enterprise)",
        "turns": [
            "مش عارف ادخل بالايميل بتاع الشركة (SSO)",
            "اللابتوب بتاعي ويندوز وكروم",
            "لسه مش شغال",
            "برضو مانفعش",
            "جربت ولسه"
        ],
        "expected_flow": "Diagnostic -> Solution 1 -> Solution 2 -> Solution 3 -> Escalation"
    },
    {
        "name": "SCORM Package Not Loading",
        "turns": [
            "الكورس مش بيفتح وبيطلع شاشة بيضا",
            "ايباد سفاري",
            "لسه",
            "جربت مش نافع",
            "استمر"
        ],
        "expected_flow": "Diagnostic -> Solution 1 -> Solution 2 -> Solution 3 -> Escalation"
    },
    {
        "name": "Video Stuttering (Firewall Issue)",
        "turns": [
            "الفيديو بيقطع ومش بيحمل للاخر",
            "ماك بوك وسافاري",
            "لسه بيقطع",
            "مانفعش",
            "كمل"
        ],
        "expected_flow": "Diagnostic -> Solution 1 -> Solution 2 -> Solution 3 -> Escalation"
    }
]

def log(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback for Windows console encoding issues
        print(text.encode('ascii', 'ignore').decode('ascii'))

def run_simulation(scenario):
    session_id = f"stress_{int(time.time())}_{scenario['name'][:5]}"
    log(f"\n--- [SCENARIO]: {scenario['name']} ---")
    log("-" * 50)
    
    current_state = None
    
    for i, msg in enumerate(scenario['turns']):
        log(f"TURN {i+1} [USER]: {msg}")
        
        payload = {
            "message": msg,
            "department": "tech",
            "user_email": "tester@zedny.ai",
            "session_id": session_id,
            "incident_state": current_state
        }
        
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=120)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer")
                current_state = data.get("incident_state", {})
                
                log(f"AI ({elapsed:.1f}s): {answer[:150]}...")
                log(f"STATE: Step={current_state.get('step')}, Status={current_state.get('status')}, SolCount={len(current_state.get('solutions_tried', []))}")
                
                if "تقرير تصعيد فني" in answer or current_state.get("step") == 2:
                    log("[ESCALATED] Report generated successfully.")
                    break
            else:
                log(f"ERROR: HTTP {response.status_code}")
                break
        except Exception as e:
            log(f"EXCEPTION: {e}")
            break
        
        time.sleep(1) # Breath between turns

def main():
    log("=" * 60)
    log("ZEDNY TECHNICAL SUPPORT STRESS TEST")
    log("=" * 60)
    
    for scenario in SCENARIOS:
        run_simulation(scenario)
        log("=" * 60)

if __name__ == "__main__":
    main()
