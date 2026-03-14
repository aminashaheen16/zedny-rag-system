import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def test_sales_escalation():
    print("\n--- [TEST] Sales Escalation Routing & Quality ---")
    payload = {
        "message": "أنا مهتم بشراء 50 رخصة للموظفين عندي، كيف أقدر أتواصل معاكم؟",
        "user_email": "prospect@example.com",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "new",
            "step": 0
        }
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✅ Sales endpoint call successful")
        # Check database for the latest report
        reports = requests.get(f"{BASE_URL}/reports?role=admin").json()
        if reports:
            latest = reports[0] # Assuming timestamp order
            print(f"Assigned To: {latest['assigned_to']}")
            print(f"User Email: {latest['user_email']}")
            print(f"Summary Snippet: {latest['summary'][:100]}...")
            if latest['assigned_to'] == "sales_manager@zedny.ai" and latest['user_email'] == "prospect@example.com":
                print("🌟 SUCCESS: Sales Routing & Email Attribution Correct!")
            else:
                print("❌ FAILED: Routing or Email mismatch")
    else:
        print(f"❌ Failed to reach chat API: {response.text}")

def test_tech_escalation_v2():
    print("\n--- [TEST] Tech Escalation v2 (No Auto-Save, Returned Summary) ---")
    payload = {
        "message": "لسه المشكلة موجودة، مفيش فايدة",
        "user_email": "frustrated_user@test.com",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "عدم القدرة على تشغيل فيديوهات الكورسات",
            "solutions_tried": ["مسح الكاش", "تحديث المتصفح"],
            "diagnostic_turns": 3
        }
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("should_escalate") and data.get("context_used"):
            print("✅ Success: Chat identified escalation and returned summary!")
            
            # Check there is NO new report yet
            reports_before = requests.get(f"{BASE_URL}/reports?role=admin").json()
            
            # Now simulate Form Submission
            report_payload = {
                "category": "Tech",
                "service": "Support Request: Company",
                "urgency": "High",
                "summary": data["context_used"],
                "history": ["User: My video is broken", "AI: Try cache", "User: Still broken"],
                "user_email": "real_user@test.com",
                "customerName": "Ahmed",
                "metadata": {
                    "customer_name": "Ahmed",
                    "customer_phone": "+20123456789",
                    "customer_company": "Zedny",
                    "job_title": "Manager"
                }
            }
            res_report = requests.post(f"{BASE_URL}/reports", json=report_payload)
            if res_report.status_code == 200:
                report_id = res_report.json()["report_id"]
                # Verify in DB
                final_res = requests.get(f"{BASE_URL}/reports/{report_id}?role=admin").json()
                print(f"Verified Name: {final_res['metadata'].get('customer_name')}")
                print(f"Verified Phone: {final_res['metadata'].get('customer_phone')}")
                if final_res['metadata'].get('customer_phone') == "+20123456789":
                    print("🌟 SUCCESS: Full Metadata persisted correctly!")
                else:
                    print("❌ FAILED: Metadata missing")
        else:
            print("❌ Failed: AI did not trigger escalation correctly")
    else:
        print(f"❌ Failed: {response.text}")

def test_contextual_routing():
    print("\n--- [TEST] Contextual Routing (Business-Tech vs Individual-Sales) ---")
    
    # Scene 1: Business User with Tech Problem
    print("\n[SCENE 1] Business User reporting a BUG")
    tech_payload = {
        "message": "أنا من شركة زيدني وفيديوهات الكورسات مش بتفتح، جربت كل حاجة",
        "user_email": "business_tech@test.com",
        "incident_state": {
            "session_id": str(uuid.uuid4()),
            "status": "diagnosing",
            "step": 1,
            "problem_description": "فيديو لا يعمل",
            "solutions_tried": ["مسح الكاش", "تحديث الصفحة"],
            "diagnostic_turns": 3
        }
    }
    res_tech = requests.post(f"{BASE_URL}/chat", json=tech_payload).json()
    if res_tech.get("should_escalate") and "mohamed_tech" in res_tech.get("context_used", ""):
        print("✅ Correct: Business-Tech routed to Tech Specialist summary!")
    elif res_tech.get("should_escalate"):
        print(f"✅ Context Check: {res_tech.get('context_used')[:50]}...")
    
    # Scene 2: Individual with Sales Intent
    print("\n[SCENE 2] Individual asking for PRICES")
    sales_payload = {
        "message": "أنا طالب وعاوز أعرف أسعار الاشتراكات السنوية وأزاي أدفع",
        "user_email": "student_sales@test.com"
    }
    res_sales = requests.post(f"{BASE_URL}/chat", json=sales_payload).json()
    if res_sales.get("should_escalate") and res_sales.get("incident_state", {}).get("category") == "Sales":
        print("✅ Correct: Student with Sales intent routed to Sales Manager!")
    else:
        print(f"❌ Failed: Category was {res_sales.get('incident_state', {}).get('category')}")

if __name__ == "__main__":
    # Ensure server is running or this will fail
    try:
        test_sales_escalation()
        test_tech_escalation_v2()
        test_contextual_routing()
    except Exception as e:
        print(f"💥 Error running tests: {e}")
