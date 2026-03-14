"""
🧪 INTENT-BASED PROMPTING TEST v3.0
Tests AI response with VARIANT phrasings to verify generalization.
"""
import requests
import time

API_URL = "http://localhost:8000/chat"

# Test with DIFFERENT phrasings of the same intent
TEST_CASES = {
    "IDENTITY Intent Variants": [
        {"query": "مين زدني؟", "description": "Original phrasing"},
        {"query": "عرفني عن الشركة", "description": "Variant: عرفني"},
        {"query": "احكيلي عن زدني", "description": "Variant: احكيلي"},
        {"query": "انتوا بتعملوا ايه؟", "description": "Variant: بتعملوا"},
        {"query": "وضحلي مجالكم", "description": "Variant: وضحلي"},
    ],
    "FEATURE Intent Variants": [
        {"query": "ايه مميزات زدني؟", "description": "Original: مميزات"},
        {"query": "بتقدموا ايه؟", "description": "Variant: بتقدموا"},
        {"query": "عندكم خدمات ايه؟", "description": "Variant: خدمات"},
    ],
    "DUMP Intent Variants": [
        {"query": "قولي كل حاجة عن زدني", "description": "Original: كل حاجة"},
        {"query": "عايز اعرف كل شي عنكم", "description": "Variant: كل شي"},
    ]
}

MAX_WORDS_BY_INTENT = {
    "IDENTITY Intent Variants": 50,
    "FEATURE Intent Variants": 80,
    "DUMP Intent Variants": 60
}

def count_words(text):
    return len(text.split())

def run_tests():
    print(f"\n{'='*70}")
    print(f"🧪 INTENT-BASED PROMPTING TEST v3.0 (Variant Phrasings)")
    print(f"{'='*70}\n")
    
    total_passed = 0
    total_tests = 0
    
    for category, tests in TEST_CASES.items():
        print(f"\n📋 CATEGORY: {category}")
        print("-" * 60)
        max_words = MAX_WORDS_BY_INTENT.get(category, 60)
        
        for test in tests:
            total_tests += 1
            payload = {"message": test["query"], "user_email": "tester@zedny.ai"}
            
            try:
                start = time.time()
                response = requests.post(API_URL, json=payload, timeout=60)
                latency = time.time() - start
                
                answer = response.json().get("answer", "")
                word_count = count_words(answer)
                
                passed = word_count <= max_words
                if passed:
                    total_passed += 1
                
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"\n{status} | {test['description']}")
                print(f"     Query: {test['query']}")
                print(f"     Words: {word_count}/{max_words}, Latency: {latency:.2f}s")
                print(f"     Response: {answer[:120]}...")
                
            except Exception as e:
                print(f"❌ ERROR: {test['description']} - {e}")
            
            time.sleep(1)
    
    print(f"\n{'='*70}")
    print(f"📊 FINAL: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
    print(f"{'='*70}")

if __name__ == "__main__":
    run_tests()
