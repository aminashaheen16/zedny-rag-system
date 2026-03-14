"""
Test Script: Evaluating AI Response Quality After Optimizations
Tests the optimized system with real questions to verify conciseness improvements.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.rag_service import RagService
from app.services.ai_service import AIService
from app.core.prompts import SALES_INFO_PROMPT, BRAND_LOYALTY_INSTRUCTIONS

def count_words_arabic_english(text):
    """Count words in mixed Arabic/English text"""
    import re
    # Split by whitespace and common punctuation
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def test_question(question, test_name):
    """Test a single question and analyze the response"""
    print(f"\n{'='*80}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*80}")
    print(f"❓ Question: {question}")
    print(f"{'-'*80}")
    
    # 1. RAG Search
    rag_chunks = RagService.search_knowledge_base(question)
    context_str = "\n---\n".join(rag_chunks) if rag_chunks else ""
    
    print(f"📚 RAG Retrieved: {len(rag_chunks)} chunks")
    print(f"📊 Total Context Length: {len(context_str)} characters")
    
    # 2. Prepare prompt (simulating INFO intent)
    system_prompt = SALES_INFO_PROMPT.format(
        user_name="Guest",
        company_name="Visitor",
        user_type="Guest",
        courses=[],
        BRAND_LOYALTY_INSTRUCTIONS=BRAND_LOYALTY_INSTRUCTIONS
    )
    
    user_input = f"User: {question}\nHistory: []\nContext: {context_str}"
    
    # 3. Get AI Response
    print(f"\n🤖 Calling Llama 70B...")
    answer = AIService.run_llm(system_prompt, user_input, model="llama-3.3-70b-versatile")
    
    # 4. Analyze Response
    word_count = count_words_arabic_english(answer)
    line_count = len(answer.split('\n'))
    char_count = len(answer)
    
    print(f"\n✅ RESPONSE:")
    print(f"{'-'*80}")
    print(answer)
    print(f"{'-'*80}")
    
    print(f"\n📊 ANALYSIS:")
    print(f"   • Word Count: {word_count} words")
    print(f"   • Line Count: {line_count} lines")
    print(f"   • Character Count: {char_count} characters")
    
    # Quality check
    is_concise = word_count <= 100  # Target: under 100 words for identity questions
    print(f"\n🎯 QUALITY CHECK:")
    print(f"   • Concise (≤100 words): {'✅ PASS' if is_concise else '❌ FAIL'}")
    
    return {
        "question": question,
        "answer": answer,
        "word_count": word_count,
        "line_count": line_count,
        "char_count": char_count,
        "chunks_used": len(rag_chunks),
        "is_concise": is_concise
    }

def main():
    print("\n" + "="*80)
    print("🚀 ZEDNY AI RESPONSE QUALITY TEST - POST-OPTIMIZATION")
    print("="*80)
    
    # Test Cases
    test_cases = [
        ("من زدني؟", "Identity Question (Arabic)"),
        ("What is Zedny?", "Identity Question (English)"),
        ("ايه مميزات زدني؟", "Features Question"),
    ]
    
    results = []
    
    for question, test_name in test_cases:
        try:
            result = test_question(question, test_name)
            results.append(result)
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Final Summary
    print(f"\n\n{'='*80}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*80}")
    
    total_tests = len(results)
    passed = sum(1 for r in results if r['is_concise'])
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed (Concise): {passed}/{total_tests}")
    print(f"Average Word Count: {sum(r['word_count'] for r in results) / total_tests:.1f} words")
    
    print("\n📋 DETAILED RESULTS:")
    for i, r in enumerate(results, 1):
        status = "✅" if r['is_concise'] else "❌"
        print(f"   {i}. {r['question'][:50]}: {r['word_count']} words {status}")
    
    # Recommendation
    print(f"\n{'='*80}")
    print("🎯 RECOMMENDATION:")
    if passed == total_tests:
        print("   ✅ System is working OPTIMALLY! Response quality is excellent.")
        print("   ✅ Multi-Agent is NOT needed - current Unified Brain is sufficient.")
    elif passed >= total_tests * 0.7:
        print("   ⚠️  System is GOOD but could be improved.")
        print("   💡 Consider minor prompt adjustments or temperature tweaking.")
    else:
        print("   ❌ System needs improvement.")
        print("   💡 Consider Multi-Agent architecture for better control.")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
