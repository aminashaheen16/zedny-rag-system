import os
import re
from app.core.config import supabase
from app.services.rag_service import RagService
from app.services.ai_service import AIService
from app.core.prompts import SALES_INFO_PROMPT
from app.utils.arabic_helper import normalize_arabic

def extract_questions_from_kb(limit=100):
    print(f"--- [EXTRACTING QUESTIONS FROM KB (Limit: {limit})] ---")
    try:
        res = supabase.table("knowledge_chunks").select("content").limit(limit).execute()
        if not res.data:
            return []
            
        questions = []
        for row in res.data:
            content = row['content']
            # Find patterns like **السؤال:** Video status or **Question:** How to reset
            match_ar = re.search(r'\*\*السؤال:\*\*\s*(.*)', content)
            match_en = re.search(r'\*\*Question:\*\*\s*(.*)', content)
            
            if match_ar:
                questions.append(("ar", match_ar.group(1).strip()))
            elif match_en:
                questions.append(("en", match_en.group(1).strip()))
                
        return questions
    except Exception as e:
        print(f"❌ Error extracting questions: {e}")
        return []

def run_comprehensive_test(questions):
    print(f"\n🚀 STARTING COMPREHENSIVE TEST ON {len(questions)} QUESTIONS\n")
    
    success_count = 0
    
    for i, (lang, q) in enumerate(questions):
        print(f"\n[{i+1}/{len(questions)}] testing ({lang}): {q}")
        
        # 1. Retrieval
        chunks = RagService.search_knowledge_base(q, limit=8 if any(k in normalize_arabic(q) for k in ["شركه", "شركات", "عملاء"]) else 4)
        
        if not chunks:
            print("   ❌ RETRIEVAL FAILED: No chunks found.")
            continue
            
        # 2. Formulation
        system_prompt = SALES_INFO_PROMPT.format(
            user_name="Test User",
            company_name="Test Corp",
            user_type="Lead",
            courses=[],
            BRAND_LOYALTY_INSTRUCTIONS="Speak as Zedny Assistant.",
            OUTPUT_SANITIZATION_RULES="Follow clean output rules.",
            LANGUAGE_RULE=f"Respond ONLY in {'Modern Standard Arabic' if lang == 'ar' else 'English'}.",
            pending_topic_context="None",
            session_summary="Bulk Diagnostic Test"
        )
        
        user_prompt = f"User: {q}\n\nContext from Knowledge Base:\n" + "\n---\n".join(chunks) + "\n---"
        
        # Use Claude for better synthesis in this test
        answer = AIService.run_llm(system_prompt, user_prompt, model="anthropic/claude-3.5-sonnet", intent="INFO")
        
        # 3. Simple Validation (Heuristic)
        # Check if the answer has enough length and mentions Zedny or key words
        answer_lower = answer.lower()
        has_brand = "زدني" in answer or "zedny" in answer_lower or "zedny.ai" in answer_lower
        
        if len(answer) > 50 and has_brand:
            print("   ✅ SUCCESS: Valid formulation.")
            success_count += 1
        elif len(answer) > 100:
            print("   ✅ SUCCESS: Long professional response (Manual check recommended).")
            success_count += 1
        else:
            print(f"   ⚠️ WARNING: Suspected poor response.\n   AI Response: {answer[:150]}...")
            
    print(f"\n{'='*50}")
    print(f"📊 FINAL RESULT: {success_count}/{len(questions)} passed.")
    print(f"{'='*50}")

if __name__ == "__main__":
    # Scan more chunks to find more explicit questions
    kb_questions = extract_questions_from_kb(400) 
    if kb_questions:
        run_comprehensive_test(kb_questions)
    else:
        print("❌ No questions extracted to test.")
