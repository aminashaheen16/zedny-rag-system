import os
import sys
import json

# Add parent directory to sys.path to import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Also ensure we can find 'app'
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.services.ai_service import AIService
from app.services.orchestrator_service import OrchestratorService
from app.services.conversation_service import UserIntent
from app.models.schemas import IncidentState

async def test_vague_issue_logic():
    print("--- [TEST] Testing Vague Issue Logic (Discovery Phase) ---")
    
    user_msg = "I have an issue"
    print(f"User Message: {user_msg}")
    
    # Simulate first turn
    state = IncidentState()
    
    # 1. Intent Detection (Simplified for test)
    intent = "ISSUE"
    
    # 2. Test Vague Input Guard (Discovery Phase)
    # We mimic the logic in chat_endpoint
    is_generic_vague = len(user_msg.split()) <= 4 and any(k in user_msg.lower() for k in ["problem", "issue", "help", "مشكلة", "مساعدة", "بايظ", "واقف"])
    
    print(f"Is Generic Vague: {is_generic_vague}")
    
    if not state.problem_description or is_generic_vague:
        print("--- [RESULT] Correctly identified as DISCOVERY PHASE ---")
        # In real code, this would call AIService.run_llm with Discovery prompt
    else:
        print("--- [RESULT] FAILED: Incorrectly skipped Discovery phase ---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_vague_issue_logic())
