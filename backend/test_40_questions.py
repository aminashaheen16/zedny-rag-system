"""
RAG Quality Test - 40 Questions Comprehensive Test
Tests the chat API with various questions to verify RAG accuracy
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001"

# 40 Test Questions covering different categories
TEST_QUESTIONS = [
    # === INFO / General Questions (15) ===
    {"q": "ما هي منصة زدني؟", "category": "INFO", "expected_keywords": ["منصة", "تعليم", "تدريب", "Zedny"]},
    {"q": "ما هو مفهوم Edutainment؟", "category": "INFO", "expected_keywords": ["تعليم", "ترفيه", "edutainment"]},
    {"q": "ما هي مميزات منصة زدني؟", "category": "INFO", "expected_keywords": ["ميز", "منصة", "تدريب"]},
    {"q": "من هم عملاء زدني؟", "category": "INFO", "expected_keywords": ["vodafone", "بنك", "شركة", "عميل", "Bank", "Misr"]},
    {"q": "ما هي الشراكات التي لديكم؟", "category": "INFO", "expected_keywords": ["شراك", "vodafone", "بنك", "Bank", "Partners"]},
    {"q": "هل تقدمون محتوى عربي؟", "category": "INFO", "expected_keywords": ["عربي", "محتوى", "نعم", "Arabic"]},
    {"q": "ما الفرق بينكم وبين المنصات التانية؟", "category": "INFO", "expected_keywords": ["زدني", "تخصص", "عربي", "مؤسس", "ROI"]},
    {"q": "ما هي أنواع البرامج التدريبية؟", "category": "INFO", "expected_keywords": ["برنامج", "تدريب", "مهارات", "Programs"]},
    {"q": "هل لديكم تطبيق موبايل؟", "category": "INFO", "expected_keywords": ["تطبيق", "موبايل", "app", "Mobile"]},
    {"q": "كيف يمكنني التواصل معكم؟", "category": "INFO", "expected_keywords": ["تواصل", "اتصال", "email", "Contact"]},
    {"q": "هل تقديمون شهادات معتمدة؟", "category": "INFO", "expected_keywords": ["شهاد", "معتمد", "certificate", "Accredited"]},
    {"q": "ما هو Assessment Hub؟", "category": "INFO", "expected_keywords": ["assessment", "تقييم", "قياس", "Hub"]},
    {"q": "ما هي نسبة رضا العملاء؟", "category": "INFO", "expected_keywords": ["رضا", "95", "عميل", "Satisfaction"]},
    {"q": "هل يوجد محتوى للقيادة والإدارة؟", "category": "INFO", "expected_keywords": ["قياد", "إدار", "leadership", "Management"]},
    {"q": "ما هو نظام التخصيص عندكم؟", "category": "INFO", "expected_keywords": ["تخصيص", "custom", "مخصص"]},
    
    # === SALES Questions (15) ===
    {"q": "عايز أشترك في المنصة", "category": "SALES", "expected_keywords": ["اشتراك", "تواصل", "فريق", "Subscribe"]},
    {"q": "كم سعر الاشتراك؟", "category": "SALES", "expected_keywords": ["سعر", "تكلفة", "اشتراك", "Price", "Cost"]},
    {"q": "هل فيه خصومات للشركات؟", "category": "SALES", "expected_keywords": ["خصم", "شرك", "عرض", "Discount", "Corporate"]},
    {"q": "أنا من شركة وعايز أدرب الموظفين", "category": "SALES", "expected_keywords": ["شركة", "تدريب", "موظف", "Training"]},
    {"q": "ما هي باقات الاشتراك المتاحة؟", "category": "SALES", "expected_keywords": ["باقة", "اشتراك", "سعر", "Packages", "Plans"]},
    {"q": "هل يوجد اشتراك سنوي؟", "category": "SALES", "expected_keywords": ["سنوي", "اشتراك", "خصم", "Annual", "Yearly"]},
    {"q": "كيف أحجز ديمو أو عرض توضيحي؟", "category": "SALES", "expected_keywords": ["ديمو", "demo", "عرض", "حجز"]},
    {"q": "ما هو أقل عدد موظفين للاشتراك؟", "category": "SALES", "expected_keywords": ["عدد", "موظف", "اشتراك", "Employees"]},
    {"q": "هل تقديمون حلول Enterprise؟", "category": "SALES", "expected_keywords": ["enterprise", "مؤسس", "حلول"]},
    {"q": "ما هي طرق الدفع المتاحة؟", "category": "SALES", "expected_keywords": ["دفع", "payment", "طريقة"]},
    {"q": "هل فيه فترة تجريبية مجانية؟", "category": "SALES", "expected_keywords": ["تجريب", "مجان", "trial", "Free"]},
    {"q": "أريد عرض سعر لـ 100 موظف", "category": "SALES", "expected_keywords": ["سعر", "عرض", "موظف", "Offer", "Quote"]},
    {"q": "ما هو العائد على الاستثمار ROI؟", "category": "SALES", "expected_keywords": ["roi", "عائد", "استثمار", "Return"]},
    {"q": "هل يوجد خصم للعقود طويلة المدى؟", "category": "SALES", "expected_keywords": ["خصم", "عقد", "طويل", "Long-term"]},
    {"q": "كيف يمكنني التحدث مع مسؤول المبيعات؟", "category": "SALES", "expected_keywords": ["مبيعات", "تواصل", "تحدث", "representative"]},
    
    # === TECHNICAL / ISSUE Questions (10) ===
    {"q": "الفيديو مش شغال عندي", "category": "ISSUE", "expected_keywords": ["فيديو", "حل", "جرب", "Video", "Working"]},
    {"q": "نسيت كلمة السر", "category": "ISSUE", "expected_keywords": ["كلمة", "سر", "استعادة", "reset", "password"]},
    {"q": "الموقع بطيء جداً", "category": "ISSUE", "expected_keywords": ["بطيء", "سرعة", "cache", "انترنت", "Slow"]},
    {"q": "مش قادر أسجل دخول", "category": "ISSUE", "expected_keywords": ["تسجيل", "دخول", "login"]},
    {"q": "الصوت مش شغال في الفيديوهات", "category": "ISSUE", "expected_keywords": ["صوت", "فيديو", "جرب", "Sound", "Audio"]},
    {"q": "الشهادة مش ظاهرة", "category": "ISSUE", "expected_keywords": ["شهاد", "ظهور", "إتمام", "Certificate"]},
    {"q": "الكورس مش بيفتح", "category": "ISSUE", "expected_keywords": ["كورس", "فتح", "جرب", "Course"]},
    {"q": "الدفع فشل", "category": "ISSUE", "expected_keywords": ["دفع", "فشل", "بطاقة", "Payment", "Failed"]},
    {"q": "التطبيق بيقفل فجأة", "category": "ISSUE", "expected_keywords": ["تطبيق", "crash", "تحديث"]},
    {"q": "مشكلة في تتبع التقدم", "category": "ISSUE", "expected_keywords": ["تقدم", "progress", "تتبع"]},
]

def send_question(question: str, session_id: str) -> dict:
    """Send a question to the chat API and return the response"""
    payload = {
        "message": question,
        "department": "general",
        "user_email": "test@zedny.ai",
        "session_id": session_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=120) # Increased timeout to 120s
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "answer": ""}
    except Exception as e:
        return {"error": str(e), "answer": ""}


def evaluate_response(answer: str, expected_keywords: list) -> tuple:
    """Check if answer contains expected keywords"""
    answer_lower = answer.lower()
    found = []
    missing = []
    
    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            found.append(keyword)
        else:
            missing.append(keyword)
    
    score = len(found) / len(expected_keywords) if expected_keywords else 0
    return score, found, missing

def run_comprehensive_test():
    """Run all 40 questions and generate a report"""
    print("=" * 70)
    print("🧪 ZEDNY RAG QUALITY TEST - 40 QUESTIONS")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = {
        "INFO": {"passed": 0, "failed": 0, "scores": []},
        "SALES": {"passed": 0, "failed": 0, "scores": []},
        "ISSUE": {"passed": 0, "failed": 0, "scores": []}
    }
    
    detailed_results = []
    
    for i, test in enumerate(TEST_QUESTIONS, 1):
        session_id = f"test_rag_{int(time.time())}_{i}"
        question = test["q"]
        category = test["category"]
        expected = test["expected_keywords"]
        
        print(f"\n[{i}/40] Testing: {question[:50]}...")
        
        response = send_question(question, session_id)
        answer = response.get("answer", "")
        
        if "error" in response:
            print(f"   ❌ ERROR: {response['error']}")
            results[category]["failed"] += 1
            detailed_results.append({
                "question": question,
                "category": category,
                "status": "ERROR",
                "score": 0,
                "answer": response.get("error", "Unknown error")
            })
            continue
        
        score, found, missing = evaluate_response(answer, expected)
        results[category]["scores"].append(score)
        
        if score >= 0.5:  # Pass if at least 50% keywords found
            results[category]["passed"] += 1
            status = "✅ PASS"
        else:
            results[category]["failed"] += 1
            status = "❌ FAIL"
        
        print(f"   {status} (Score: {score*100:.0f}%)")
        if missing:
            print(f"   Missing: {', '.join(missing)}")
        
        detailed_results.append({
            "question": question,
            "category": category,
            "status": "PASS" if score >= 0.5 else "FAIL",
            "score": score,
            "found_keywords": found,
            "missing_keywords": missing,
            "answer_preview": answer[:200] + "..." if len(answer) > 200 else answer
        })
        
        time.sleep(1)  # Rate limiting
    
    # Generate Summary Report
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS SUMMARY")
    print("=" * 70)
    
    total_passed = 0
    total_failed = 0
    
    for cat in ["INFO", "SALES", "ISSUE"]:
        passed = results[cat]["passed"]
        failed = results[cat]["failed"]
        total = passed + failed
        avg_score = sum(results[cat]["scores"]) / len(results[cat]["scores"]) if results[cat]["scores"] else 0
        
        total_passed += passed
        total_failed += failed
        
        print(f"\n📁 {cat}:")
        print(f"   ✅ Passed: {passed}/{total} ({passed/total*100:.0f}%)")
        print(f"   📈 Avg Score: {avg_score*100:.0f}%")
    
    overall_rate = total_passed / (total_passed + total_failed) * 100 if (total_passed + total_failed) > 0 else 0
    
    print(f"\n{'=' * 70}")
    print(f"🎯 OVERALL SUCCESS RATE: {overall_rate:.1f}% ({total_passed}/{total_passed + total_failed})")
    print(f"{'=' * 70}")
    
    # Save detailed results to file
    with open("rag_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_questions": len(TEST_QUESTIONS),
                "total_passed": total_passed,
                "total_failed": total_failed,
                "success_rate": overall_rate,
                "by_category": results
            },
            "detailed_results": detailed_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Detailed results saved to: rag_test_results.json")
    
    return overall_rate

if __name__ == "__main__":
    run_comprehensive_test()
