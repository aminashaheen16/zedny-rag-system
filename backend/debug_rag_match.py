# 🧪 Debug RAG Matching
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.services.rag_service import RagService

def debug_issue(text):
    print(f"\n📡 DEBUG: Problem = '{text}'")
    solution = RagService.search_local_solutions(text)
    if solution:
        print(f"✅ FOUND: {solution['solution_id']}")
    else:
        print("❌ NOT FOUND")

if __name__ == "__main__":
    debug_issue("نسيت الباسورد")
    debug_issue("لا استطيع تسجيل الدخول")
    debug_issue("مش عارف ادخل")
    debug_issue("الفيديو مش شغال")
