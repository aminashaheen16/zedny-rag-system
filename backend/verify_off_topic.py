import requests
import json

API_URL = "http://localhost:8000/chat"

# Test cases for off-topic queries
OFF_TOPIC_TESTS = [
    {
        "query": "ازاي أعمل كبسة سعودي؟",
        "description": "Cooking question (AR)"
    },
    {
        "query": "How to cook pasta?",
        "description": "Cooking question (EN)"
    },
    {
        "query": "مين كسب ماتش الأهلي والزمالك؟",
        "description": "Sports question (AR)"
    },
    {
        "query": "What's the weather in Cairo?",
        "description": "General weather query"
    },
    {
        "query": "Write a python script to scrape Facebook",
        "description": "Coding help (Unrelated to Zedny)"
    },
    {
        "query": "ايه رايك في تيسلا؟",
        "description": "Other company opinion"
    },
    {
        "query": "احكيلي نكتة",
        "description": "Joke request"
    }
]

def run_tests():
    print(f"\n{'='*70}")
    print(f"🧪 STRICT OFF-TOPIC REFUSAL TEST SUITE")
    print(f"{'='*70}\n")
    
    total_passed = 0
    
    for test in OFF_TOPIC_TESTS:
        payload = {
            "message": test["query"],
            "user_email": "tester@zedny.ai"
        }
        
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            answer = response.json().get("answer", "")
            
            # Refusal keywords (Check if it used the mandatory refusal phrases)
            refusal_signals_ar = ["بيعتذر منك", "أنا مخصص فقط للمساعدة", "بخصوص زدني"]
            refusal_signals_en = ["I apologize", "specialized only", "regarding Zedny"]
            
            is_refusal = any(s in answer for s in refusal_signals_ar) or any(s in answer for s in refusal_signals_en)
            
            # Heuristic: If it actually answered the question (e.g., provided a recipe), it failed.
            # Recipes usually have ingredients or steps.
            failed_keywords = ["ملعقة", "زيت", "بصل", "أرز", "recipe", "sugar", "salt", "الأهلي", "الزمالك", "درجة الحرارة", "import requests"]
            contains_info = any(k in answer for k in failed_keywords)
            
            passed = is_refusal and not contains_info
            
            if passed:
                total_passed += 1
                
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {test['description']}")
            print(f"     Query: {test['query']}")
            print(f"     Response: {answer[:150]}...")
            if not passed:
                print(f"     ⚠️ Issue: AI should have refused but {'provided info' if contains_info else 'gave a generic response'}")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ ERROR: {test['description']} - {e}")
            
    print(f"\n📊 SUMMARY: {total_passed}/{len(OFF_TOPIC_TESTS)} tests passed ({total_passed/len(OFF_TOPIC_TESTS)*100:.1f}%)")
    
if __name__ == "__main__":
    run_tests()
