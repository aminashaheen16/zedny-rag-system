import os
import re
from app.services.rag_service import RagService
from app.utils.arabic_helper import normalize_arabic

# Mocking the Intent Shield logic from chat.py for isolated testing
def mock_intent_shield(user_msg: str) -> str:
    vague_tech_keywords = ["مشكله", "مشكلة", "مساعدة", "مساعده", "عندي مشكله", "issue", "problem", "help", "error", "مش شغال", "بايظ", "معطل"]
    normalized_msg = normalize_arabic(user_msg)
    
    if any(normalize_arabic(k) in normalized_msg for k in vague_tech_keywords):
        return "ISSUE"
    return "OTHER"

def test_tech_scenarios():
    scenarios = [
        {
            "name": "Intent Robustness (ة vs ه)",
            "query": "عندي مشكله في الدخول", # 'ه' instead of 'ة'
            "expected_intent": "ISSUE"
        },
        {
            "name": "Local Solution Match (Video Black Screen)",
            "query": "الفيديو شاشه سوداء", # 'ه' variation
            "expected_id": "vid_black_001"
        },
        {
            "name": "Egyptian Slang Normalization",
            "query": "التطبيق بيفصل مني", # 'بيفصل' -> 'disconnect'
            "expected_match": True
        },
        {
            "name": "Enterprise Logic",
            "query": "مشكلة في دخول الموظفين للشركة",
            "expected_id": "sso_001"
        }
    ]
    
    print(f"\n🚀 STARTING TECHNICAL FLOW TEST\n")
    
    for i, s in enumerate(scenarios):
        print(f"--- Scenario {i+1}: {s['name']} ---")
        q = s['query']
        normalized = normalize_arabic(q)
        print(f"Query: {q}")
        print(f"Normalized: {normalized}")
        
        # Test Intent
        intent = mock_intent_shield(q)
        print(f"Detected Intent: {intent}")
        if "expected_intent" in s:
            if intent == s['expected_intent']:
                print("✅ Intent Match Successful")
            else:
                print(f"❌ Intent Match Failed (Expected {s['expected_intent']})")
        
        # Test Local Solution Search
        # Note: RagService.search_local_solutions uses its own internal normalization (Egyptian + Synonyms)
        # But our fix in chat.py passes normalized_msg to it.
        solution = RagService.search_local_solutions(normalized)
        
        if solution:
            print(f"Matched Solution ID: {solution.get('solution_id')}")
            if "expected_id" in s:
                if solution.get('solution_id') == s['expected_id']:
                    print("✅ Solution ID Match Successful")
                else:
                    print(f"❌ Solution ID Match Failed (Expected {s['expected_id']})")
            else:
                print("✅ Found an appropriate solution.")
        else:
            print("❌ No local solution found.")
        print("-" * 30)

if __name__ == "__main__":
    test_tech_scenarios()
