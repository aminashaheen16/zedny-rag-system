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

def extract_questions_from_rag():
    rag_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ZEDNY_RAG_Optimized.json")
    if not os.path.exists(rag_path):
        print(f"❌ Could not find {rag_path}")
        return []

    with open(rag_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = []
    for chunk in data.get('chunks', []):
        content = chunk.get('content', '')
        # Try to find Arabic questions
        if "**السؤال:**" in content:
            q_part = content.split("**السؤال:**")[1].split("\n")[0].strip()
            if q_part:
                questions.append({
                    "text": q_part,
                    "lang": "ar",
                    "chunk_id": chunk.get('chunk_id')
                })
        # Try to find English questions
        elif "**Question:**" in content:
            q_part = content.split("**Question:**")[1].split("\n")[0].strip()
            if q_part:
                questions.append({
                    "text": q_part,
                    "lang": "en",
                    "chunk_id": chunk.get('chunk_id')
                })
        # Fallback to title if it looks like a question
        elif "?" in chunk.get('title', ''):
             questions.append({
                    "text": chunk.get('title'),
                    "lang": chunk.get('metadata', {}).get('language', 'ar'),
                    "chunk_id": chunk.get('chunk_id')
                })
    
    return questions

def run_audit(limit=20):
    all_questions = extract_questions_from_rag()
    print(f"📋 Found {len(all_questions)} potential questions in RAG.")
    
    # Take a sample (mixture of starts, middle, end)
    if len(all_questions) > limit:
        step = len(all_questions) // limit
        test_set = all_questions[::step][:limit]
    else:
        test_set = all_questions

    results = []
    
    print(f"🚀 Starting audit on {len(test_set)} samples...")
    
    for i, q_item in enumerate(test_set):
        query = q_item['text']
        lang = q_item['lang']
        print(f"\n[{i+1}/{len(test_set)}] Testing: {query} ({lang})")
        
        # 1. Retrieval
        chunks = RagService.search_knowledge_base(query)
        hit = len(chunks) > 0
        
        # 2. Answer generation (only for first 5 to save tokens, then summary)
        answer = "Skipped generation for brevity"
        if i < 5:
            context_str = "\n---\n".join(chunks) if hit else "NO CONTEXT FOUND"
            system_prompt = SALES_INFO_PROMPT.format(
                user_name="Audit Bot",
                company_name="Audit Corp",
                user_type="Lead",
                courses=[],
                BRAND_LOYALTY_INSTRUCTIONS="Professional Zedny tone.",
                OUTPUT_SANITIZATION_RULES="No markdown code blocks.",
                LANGUAGE_RULE=f"Respond in {lang}.",
                pending_topic_context="Audit Session",
                session_summary="System testing"
            )
            user_prompt = f"User Question: {query}\n\nGrounding Context:\n{context_str}"
            # Use a fast free model for audit
            answer = AIService.run_llm(system_prompt, user_prompt, model="google/gemini-2.0-flash-001", intent="INFO")
        
        results.append({
            "query": query,
            "lang": lang,
            "expected_chunk": q_item['chunk_id'],
            "hit": hit,
            "num_chunks": len(chunks),
            "answer_sample": answer[:200] + "..." if len(answer) > 200 else answer
        })
    
    # Final Report
    success_count = sum(1 for r in results if r['hit'])
    print(f"\n{'='*50}")
    print(f"📊 AUDIT SUMMARY")
    print(f"Total Tested: {len(results)}")
    print(f"Retrieval Hits: {success_count} ({success_count/len(results)*100:.1f}%)")
    print(f"{'='*50}")
    
    report_path = "RAG_AUDIT_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# RAG System Audit Report\n\n")
        f.write(f"- **Total Samples:** {len(results)}\n")
        f.write(f"- **Retrieval Hit Rate:** {success_count/len(results)*100:.1f}%\n\n")
        f.write("## Detailed Results\n\n")
        f.write("| # | Question | Lang | Hit | Chunks | Sample Answer |\n")
        f.write("|---|----------|------|-----|--------|---------------|\n")
        for i, r in enumerate(results):
            hit_str = "✅" if r['hit'] else "❌"
            f.write(f"| {i+1} | {r['query']} | {r['lang']} | {hit_str} | {r['num_chunks']} | {r['answer_sample']} |\n")
    
    print(f"📑 Report saved to {report_path}")

if __name__ == "__main__":
    run_audit(limit=30)
