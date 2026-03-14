import sys
import os
from unittest.mock import MagicMock

# Mocking modules that might fail in a script environment
sys.modules['app.core.config'] = MagicMock()
sys.modules['app.services.ai_service'] = MagicMock()

from app.services.rag_service import RagService
from app.core.solutions_db import SOLUTIONS_DB

def test_rag_precision():
    scenarios = [
        {
            "name": "Generic Vague (Shared Keywords)",
            "query": "مش شغال",
            "expected_discovery": True
        },
        {
            "name": "Specific Video Issue",
            "query": "الفيديو مش شغال",
            "expected_id": "vid_black_001"
        },
        {
            "name": "Specific Login Issue",
            "query": "الحساب مش شغال تسجيل دخول",
            "expected_id": "login_001"
        },
        {
            "name": "Ambiguous but targeted",
            "query": "عندي مشكلة في الشهادة",
            "expected_id": "cert_001"
        }
    ]

    print("\n--- 🧪 RAG PRECISION TEST ---")
    for s in scenarios:
        print(f"\nTesting: {s['name']} ('{s['query']}')")
        
        # In chat.py, vague check happens BEFORE local solution search in most cases
        # but here we test the the internal search quality
        result = RagService.search_local_solutions(s['query'])
        
        if result:
            print(f"Result: {result['solution_id']} (Category: {result['category']})")
            if "expected_id" in s:
                if result['solution_id'] == s['expected_id']:
                    print("✅ MATCH CORRECT")
                else:
                    print(f"❌ MISMATCH (Expected {s['expected_id']})")
        else:
            print("Result: No match found.")
            if s.get("expected_discovery"):
                print("✅ CORRECTLY FUNNELED TO DISCOVERY (No premature match)")

if __name__ == "__main__":
    test_rag_precision()
