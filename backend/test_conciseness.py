"""
🧪 RAG CONCISENESS TEST SUITE v2.0
Tests AI response conciseness after implementing STRICT LENGTH RULES.
"""
import requests
import time
import json

API_URL = "http://localhost:8000/chat"

TEST_CASES = {
    "Identity Questions": [
        {
            "query": "مين زدني؟",
            "max_words": 50,
            "max_sentences": 3,
            "must_contain": ["منصة", "تدريب"],
            "description": "Short identity question (AR)"
        },
        {
            "query": "ايه هي زدني؟",
            "max_words": 50,
            "max_sentences": 3,
            "must_contain": ["منصة", "تدريب"],
            "description": "What is Zedny (AR)"
        },
        {
            "query": "Who is Zedny?",
            "max_words": 50,
            "max_sentences": 3,
            "must_contain": ["training", "platform"],
            "description": "Identity question (EN)"
        }
    ],
    "Feature Questions": [
        {
            "query": "ايه مميزات زدني؟",
            "max_words": 80,
            "max_bullet_points": 3,
            "must_end_with_question": False,
            "description": "Feature list request (AR)"
        },
        {
            "query": "ايه هو الـ Edutainment؟",
            "max_words": 60,
            "max_sentences": 3,
            "must_contain": ["تعليم", "ترفيه"],
            "description": "Specific concept question"
        }
    ],
    "Anti-Dump Tests": [
        {
            "query": "قولي كل حاجة عن زدني",
            "max_words": 100,
            "must_end_with_question": True,
            "description": "Open-ended dump request"
        }
    ],
    "Complex Questions": [
        {
            "query": "ازاي زدني بتساعد الشركات تحسن أداء موظفينها؟",
            "max_words": 100,
            "max_sentences": 5,
            "must_contain": ["تدريب", "موظف"],
            "description": "Complex company question"
        }
    ]
}

def count_words(text):
    return len(text.split())

def count_sentences(text):
    return text.count('.') + text.count('!') + text.count('؟') + text.count('?')

def count_bullet_points(text):
    return text.count('•') + text.count('*') + text.count('-')

def run_tests():
    print(f"\n{'='*70}")
    print(f"🧪 RAG CONCISENESS TEST SUITE v2.0 (Strict Length Rules)")
    print(f"{'='*70}\n")
    
    results = []
    total_passed = 0
    total_tests = 0
    
    for category, tests in TEST_CASES.items():
        print(f"\n📋 CATEGORY: {category}")
        print("-" * 60)
        
        for test in tests:
            total_tests += 1
            payload = {
                "message": test["query"],
                "user_email": "tester@zedny.ai"
            }
            
            try:
                start_time = time.time()
                response = requests.post(API_URL, json=payload, timeout=60)
                latency = time.time() - start_time
                
                data = response.json()
                answer = data.get("answer", "No answer")
                
                # Metrics
                word_count = count_words(answer)
                sentence_count = count_sentences(answer)
                bullet_count = count_bullet_points(answer)
                
                # Validation
                passed = True
                issues = []
                
                if "max_words" in test and word_count > test["max_words"]:
                    passed = False
                    issues.append(f"Too long: {word_count}/{test['max_words']} words")
                
                if "max_sentences" in test and sentence_count > test["max_sentences"]:
                    passed = False
                    issues.append(f"Too many sentences: {sentence_count}/{test['max_sentences']}")
                
                if "max_bullet_points" in test and bullet_count > test["max_bullet_points"]:
                    passed = False
                    issues.append(f"Too many bullets: {bullet_count}/{test['max_bullet_points']}")
                
                if "must_contain" in test:
                    for keyword in test["must_contain"]:
                        if keyword.lower() not in answer.lower():
                            passed = False
                            issues.append(f"Missing keyword: {keyword}")
                
                if "must_end_with_question" in test and test["must_end_with_question"]:
                    if "؟" not in answer[-50:] and "?" not in answer[-50:]:
                        passed = False
                        issues.append("Should end with follow-up question")
                
                if passed:
                    total_passed += 1
                
                # Print result
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"\n{status} | {test['description']}")
                print(f"     Query: {test['query']}")
                print(f"     Words: {word_count}, Sentences: {sentence_count}, Bullets: {bullet_count}")
                print(f"     Latency: {latency:.2f}s")
                if issues:
                    print(f"     ⚠️ Issues: {', '.join(issues)}")
                print(f"     Response: {answer[:150]}...")
                
                results.append({
                    "category": category,
                    "description": test["description"],
                    "passed": passed,
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "issues": issues
                })
                
            except Exception as e:
                print(f"❌ ERROR: {test['description']} - {e}")
                results.append({
                    "category": category,
                    "description": test["description"],
                    "passed": False,
                    "issues": [str(e)]
                })
            
            time.sleep(1)  # Rate limit
    
    # Summary
    print(f"\n{'='*70}")
    print(f"📊 FINAL SUMMARY: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
    print(f"{'='*70}")
    
    return results

if __name__ == "__main__":
    run_tests()
