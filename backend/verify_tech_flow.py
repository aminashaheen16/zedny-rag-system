import asyncio
import uuid
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import BackgroundTasks
from app.api.chat import chat_endpoint
from app.models.schemas import ChatRequest, IncidentState

async def test_full_diag_flow():
    thread_id = str(uuid.uuid4())
    email = "test@example.com"
    bg = BackgroundTasks()
    
    print("\n🚀 STARTING TECH FLOW VERIFICATION")
    print("="*50)
    
    # 1. First Message: Report Problem
    print("\n[TURN 1] User: عندي مشكلة في تشغيل الفيديو")
    req1 = ChatRequest(message="عندي مشكلة في تشغيل الفيديو", email=email, thread_id=thread_id)
    resp1 = await chat_endpoint(req1, bg)
    print(f"AI: {resp1.answer}")
    assert resp1.incident_state.status == "solution_offered"
    assert len(resp1.incident_state.tried_solution_ids) == 1
    
    # 2. Second Message: Negative Feedback
    print("\n[TURN 2] User: مجربتش حل تاني؟ ده منفعتش")
    req2 = ChatRequest(message="مجربتش حل تاني؟ ده منفعتش", email=email, thread_id=thread_id)
    resp2 = await chat_endpoint(req2, bg)
    print(f"AI: {resp2.answer}")
    assert len(resp2.incident_state.tried_solution_ids) == 2
    
    # 3. Third Message: Negative Feedback
    print("\n[TURN 3] User: لسه مش شغال")
    req3 = ChatRequest(message="لسه مش شغال", email=email, thread_id=thread_id)
    resp3 = await chat_endpoint(req3, bg)
    print(f"AI: {resp3.answer}")
    assert len(resp3.incident_state.tried_solution_ids) == 3
    
    # 4. Fourth Message: Escalation Check
    print("\n[TURN 4] User: مفيش فايدة")
    req4 = ChatRequest(message="مفيش فايدة", email=email, thread_id=thread_id)
    resp4 = await chat_endpoint(req4, bg)
    print(f"AI: {resp4.answer}")
    assert resp4.should_escalate == True
    assert resp4.action_required == "show_escalation_form"
    
    print("\n✅ Verification Successful: State machine and escalation logic are working correctly.")

if __name__ == "__main__":
    asyncio.run(test_full_diag_flow())
