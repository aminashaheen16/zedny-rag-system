
import sys
import os
import re

# Set up paths to import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.services.rag_service import RagService
from app.core.solutions_db import SOLUTIONS_DB

def debug_rag_v2():
    problems = ["نسيت الباسورد", "لا استطيع تسجيل الدخول"]
    
    for problem in problems:
        print(f"\n--- DEBUGGING: '{problem}' ---")
        problem_lower = problem.lower()
        
        for solution in SOLUTIONS_DB:
            for keyword in solution["symptom_keywords"]:
                k_lower = keyword.lower()
                parts = k_lower.split()
                flex_pattern = r'\s+'.join([rf'(?:ال)?{re.escape(p)}' for p in parts])
                pattern = rf"(?:^|\s|[البلوفك])?{flex_pattern}(?:\s|$)"
                
                match = re.search(pattern, problem_lower)
                if match:
                    print(f"✅ MATCH: Keyword '{keyword}' matches problem with pattern '{pattern}'")
                    print(f"   Solution ID: {solution['solution_id']}")

if __name__ == "__main__":
    debug_rag_v2()
