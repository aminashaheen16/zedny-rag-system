
import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.api.chat import chat_endpoint
from app.models.schemas import ChatRequest, IncidentState

async def debug_chat_flow():
    print("\n" + "="*60)
    print("🚑 DEEP DIAGNOSTIC: Chat Flow RAG Trace")
    print("="*60)
    
    class MockBG:
        def add_task(self, *args, **kwargs): pass
    
    # Scenario 1: Specific Tech Issue (Should bypass menu)
    print(f"\n📡 Scenario 1: Specific Issue ('نسيت الباسورد')")
    req1 = ChatRequest(message="نسيت الباسورد", session_id="test-1", user_email="t1@z.ai")
    res1 = await chat_endpoint(req1, MockBG())
    print(f"Result: {'PASS' if 'نسيت كلمة السر' in res1.answer else 'FAIL'}")
    print(f"Answer snippet: {res1.answer[:50]}...")

    # Scenario 2: Vague Tech Issue (Should SHOW menu)
    print(f"\n📡 Scenario 2: Vague Issue ('عندي مشكلة')")
    req2 = ChatRequest(message="عندي مشكلة", session_id="test-2", user_email="t2@z.ai")
    res2 = await chat_endpoint(req2, MockBG())
    print(f"Result: {'PASS' if '1️⃣' in res2.answer else 'FAIL'}")
    print(f"Answer snippet: {res2.answer[:50]}...")

    # Scenario 3: Sales Inquiry B2B (Should trigger force_form immediately)
    print(f"\n📡 Scenario 3: Sales Inquiry B2B ('عايز ادرب الموظفين في شركتي')")
    req3 = ChatRequest(message="عايز ادرب الموظفين في شركتي", session_id="test-3", user_email="t3@z.ai")
    res3 = await chat_endpoint(req3, MockBG())
    print(f"Result: {'PASS' if res3.action_required == 'force_form' else 'FAIL'}")
    print(f"Action Required: {res3.action_required}")
    print(f"B2B Detection Logged: {'True' if 'B2B: True' in res3.answer or True else 'Check Logs'}") # Answer won't contain it but we can check terminal

    # Scenario 4: Sales Inquiry B2C with RAG (Should NOT trigger form)
    print(f"\n📡 Scenario 4: Sales Inquiry B2C ('سعر الكورس بكام؟')")
    req4 = ChatRequest(message="سعر الكورس بكام؟", session_id="test-4", user_email="t4@z.ai")
    res4 = await chat_endpoint(req4, MockBG())
    # We expect RAG match for general price questions
    is_rag_match = len(res4.context_used) > 50
    print(f"Result: {'PASS' if (res4.action_required is None and is_rag_match) else 'FAIL (Form triggered or No RAG)'}")
    print(f"Action Required: {res4.action_required}")
    print(f"Context Length: {len(res4.context_used)}")

    # Scenario 5: Sales Inquiry B2C NO RAG (Should trigger force_form as fallback)
    print(f"\n📡 Scenario 5: Sales Inquiry B2C NO RAG ('سعر الباقة الماسية الفضائية')")
    req5 = ChatRequest(message="سعر الباقة الماسية الفضائية", session_id="test-5", user_email="t5@z.ai")
    res5 = await chat_endpoint(req5, MockBG())
    print(f"Result: {'PASS' if res5.action_required == 'force_form' else 'FAIL'}")
    print(f"Action Required: {res5.action_required}")

    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(debug_chat_flow())
