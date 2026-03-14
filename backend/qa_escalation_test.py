import asyncio
import sys
import os
import uuid
from datetime import datetime

# Setup paths for importing from app
sys.path.append(os.getcwd())

# Mock/Load Config
from app.core.config import supabase, RESEND_API_KEY, SUPPORT_EMAIL
from app.services.ai_service import AIService
from app.services.supabase_service import SupabaseService
from app.models.schemas import EscalationReport

async def run_professional_qa_test():
    print("\n" + "="*50)
    print("🚀 ZEDNY SYSTEM QA: ESCALATION & PERSISTENCE TEST")
    print("="*50)

    # 1. SETUP REALISTIC TECHNICAL DATA
    report_id = str(uuid.uuid4())
    test_report = EscalationReport(
        id=report_id,
        category="Technical Support",
        service="Video Processing API",
        urgency="High",
        summary="SYSTEM TEST: Verifying new 'Fuzzy' routing logic & Tech email dispatch.",
        history=[
            "User: The video upload is stuck at 99%.",
            "Bot: Have you tried a different browser?",
            "User: Yes, Chrome and Firefox. Still failing. This is urgent for our launch."
        ],
        timestamp=datetime.now().isoformat(),
        user_email="mohammedrawan653@gmail.com",
        assigned_to="mohammedrawan653@gmail.com", # Simulate Mohamed's inbox
        metadata={
            "user_phone": "+201099887766",
            "company_name": "Alpha Tech Solutions"
        }
    )

    # 2. TEST PILLAR A: DASHBOARD PERSISTENCE
    print("\n[PILLAR A] - DASHBOARD PERSISTENCE")
    try:
        SupabaseService.save_report(test_report)
        print(f"✅ Report saved to Supabase (ID: {report_id})")
        
        # Verify from DB
        res = supabase.table("reports").select("*").eq("id", report_id).execute()
        if res.data:
            db_metadata = res.data[0].get('metadata', {})
            print(f"✅ Data Integrity Verified: Company Name in DB Metadata: {db_metadata.get('company_name')}")
        else:
            print("❌ Verification Failed: Lead not found in DB.")
    except Exception as e:
        print(f"❌ Supabase Error: {e}")

    # 3. TEST PILLAR B: MULTI-DEPARTMENT DISPATCH
    print("\n[PILLAR B] - MULTI-DEPARTMENT DISPATCH")
    
    # Test Case 1: Sales Escalation
    print("\n -> Testing SALES Routing...")
    sales_report = test_report.copy()
    sales_report.category = "Sales Inquiry"
    sales_report.id = str(uuid.uuid4())
    await AIService.send_escalation_email(sales_report)

    # Test Case 2: Technical Escalation
    print("\n -> Testing TECHNICAL Routing...")
    tech_report = test_report.copy()
    tech_report.category = "Technical Bug"
    tech_report.id = str(uuid.uuid4())
    await AIService.send_escalation_email(tech_report)

    print("\n✅ Multi-Department testing complete. Check console logs.")

    print("\n" + "="*50)
    print("🏁 QA TEST COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(run_professional_qa_test())
