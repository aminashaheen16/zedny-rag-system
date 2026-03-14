import os
import sys
import json
from dotenv import load_dotenv

# Add the backend directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from app.services.rag_service import RagService
from app.services.ai_service import AIService
from app.core.prompts import SALES_INFO_PROMPT
from app.utils.arabic_helper import normalize_arabic

def test_rag_flow(query_text):
    print(f"\n{'='*50}")
    print(f"🔍 TESTING RAG FOR: {query_text}")
    print(f"📝 Normalized: {normalize_arabic(query_text)}")
    print(f"{'='*50}")

    # 1. TEST RETRIEVAL
    print("\n--- [STEP 1: RETRIEVAL] ---")
    chunks = RagService.search_knowledge_base(query_text)
    
    if not chunks:
        print("❌ NO CHUNKS FOUND.")
        return
    
    print(f"✅ FOUND {len(chunks)} CHUNKS.")

    # 2. TEST FORMULATION (Comparing Models)
    print("\n\n--- [STEP 2: FORMULATION COMPARISON] ---")
    context_str = "\n---\n".join(chunks)
    
    system_prompt = SALES_INFO_PROMPT.format(
        user_name="Test User",
        company_name="Test Corp",
        user_type="Lead",
        courses=[],
        BRAND_LOYALTY_INSTRUCTIONS="Speak as Zedny Assistant.",
        OUTPUT_SANITIZATION_RULES="Follow clean output rules.",
        LANGUAGE_RULE="Respond ONLY in Modern Standard Arabic.",
        pending_topic_context="None",
        session_summary="Diagnostic Test"
    )
    
    # Use the new grounding instruction logic if needed
    user_prompt = f"User: {query_text}\n\nContext from Knowledge Base:\n{context_str}\n---"
    
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-001"]
    
    for model_name in models:
        print(f"\n--- Testing Model: {model_name} ---")
        answer = AIService.run_llm(system_prompt, user_prompt, model=model_name, intent="INFO")
        print(f"AI Response:\n{answer}")

if __name__ == "__main__":
    # Test cases
    test_queries = [
        "ممكن اعرف عن خدماتكم للشركات؟", 
        "هل عندكم تدريب للمديرين؟",
        "عايز اعرف عن الشهادات اللي بتقدموها",
        "How do you measure training ROI?",
        "Do you work with government sectors?"
    ]
    for q in test_queries:
        test_rag_flow(q)
