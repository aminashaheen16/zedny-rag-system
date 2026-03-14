from app.services.ai_service import AIService
import asyncio

async def test_sales_radar():
    test_cases = [
        # --- POSITIVE B2B CASES (Should be TRUE/YES) ---
        {"msg": "عايز اشتراك لـ 50 موظف في شركتي", "expected": True, "desc": "Direct bulk purchase inquiry"},
        {"msg": "How much for enterprise training for 100 people?", "expected": True, "desc": "Enterprise inquiry"},
        {"msg": "أنا من شركة طبية وعايزين نعمل شراكة مع زدني لتدريب الموظفين", "expected": True, "desc": "Partnership/Training inquiry"},
        {"msg": "Do you offer corporate discounts?", "expected": True, "desc": "Corporate discount inquiry"},
        
        # --- NEGATIVE CASES (Should be FALSE/NO) ---
        {"msg": "أنا موظف في شركة فودافون وعندي مشكلة في دخول الكورس", "expected": False, "desc": "Support context with company name"},
        {"msg": "مفيش حد من الشركة بيرد عليا في المشكلة دي؟", "expected": False, "desc": "Complaining about support using 'company'"},
        {"msg": "عايز أتواصل مع صاحب الشركة بخصوص الباسورد بتاعي", "expected": False, "desc": "Escalating support to owner"},
        {"msg": "شركة وي مش شغالة عندي في البيت", "expected": False, "desc": "External service complaint (ISP)"},
        {"msg": "مش عارف افتح الموقع من جهاز الشركة", "expected": False, "desc": "Device context mention"},
    ]

    print("="*80)
    print(f"{'TEST CASE':<60} | {'EXPECTED':<10} | {'ACTUAL':<10}")
    print("-" * 80)

    for case in test_cases:
        actual = AIService.detect_b2b_intent(case["msg"])
        status = "✅ PASS" if actual == case["expected"] else "❌ FAIL"
        print(f"{case['msg'][:58]:<60} | {str(case['expected']):<10} | {str(actual):<10} | {status}")

if __name__ == "__main__":
    asyncio.run(test_sales_radar())
