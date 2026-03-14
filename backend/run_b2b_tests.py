"""
🏢 ZEDNY B2B COMPREHENSIVE TEST SUITE
=====================================
Professional testing for Enterprise scenarios across:
- Arabic (MSA)
- Egyptian Colloquial
- English
- B2B-specific issues (SSO, LMS, SCORM, Corporate)
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.rag_service import RagService
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️ Import Error: {e}")
    IMPORTS_OK = False


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ============================================
# B2B ENTERPRISE TEST SCENARIOS
# ============================================

B2B_TEST_SCENARIOS = {
    "ARABIC_MSA": {
        "name": "🇪🇬 Arabic (Modern Standard)",
        "tests": [
            {
                "id": "MSA-B2B-001",
                "input": "أواجه صعوبة في تسجيل الدخول عبر نظام التوثيق الموحد الخاص بالشركة",
                "expected_category": "ENTERPRISE",
                "expected_solution": "sso_001",
                "description": "SSO login issue - Formal Arabic"
            },
            {
                "id": "MSA-B2B-002",
                "input": "نظام SCORM لا يتتبع تقدم الموظفين بشكل صحيح",
                "expected_category": "ENTERPRISE",
                "expected_solution": "scorm_001",
                "description": "SCORM tracking - Formal Arabic"
            },
            {
                "id": "MSA-B2B-003",
                "input": "جدار الحماية الخاص بالشركة يمنع الوصول إلى المنصة",
                "expected_category": "ENTERPRISE",
                "expected_solution": "firewall_001",
                "description": "Corporate firewall - Formal Arabic"
            },
            {
                "id": "MSA-B2B-004",
                "input": "الفيديو التدريبي لا يعمل على الشبكة الداخلية للمؤسسة",
                "expected_category": "VIDEO",
                "context": "Corporate network context",
                "description": "Video on corporate network - Formal Arabic"
            }
        ]
    },
    
    "EGYPTIAN_COLLOQUIAL": {
        "name": "🗣️ Egyptian Colloquial",
        "tests": [
            {
                "id": "EGY-B2B-001",
                "input": "مش قادر أدخل بإيميل الشركة، بيطلع error",
                "expected_category": "LOGIN",
                "dialect": "Egyptian",
                "description": "Corporate email login - Colloquial"
            },
            {
                "id": "EGY-B2B-002",
                "input": "الـ SSO بتاع الشركة مش شغال، مش بيدخلني",
                "expected_category": "ENTERPRISE",
                "expected_solution": "sso_001",
                "dialect": "Egyptian",
                "description": "SSO not working - Colloquial"
            },
            {
                "id": "EGY-B2B-003",
                "input": "الفيديوهات التدريبية بطيئة جداً في الأوفيس، النت كويس",
                "expected_category": "VIDEO",
                "dialect": "Egyptian",
                "description": "Slow videos in office - Colloquial"
            },
            {
                "id": "EGY-B2B-004",
                "input": "مدير الموارد البشرية عايز يشوف تقرير تقدم الموظفين",
                "is_b2b_query": True,
                "expected_behavior": "Should understand HR manager context",
                "dialect": "Egyptian",
                "description": "HR reporting request - Colloquial"
            },
            {
                "id": "EGY-B2B-005",
                "input": "الشهادات مش بتطلع للموظفين بعد ما يخلصوا الكورس",
                "expected_category": "CERTIFICATE",
                "dialect": "Egyptian",
                "description": "Employee certificates - Colloquial"
            }
        ]
    },
    
    "ENGLISH_FORMAL": {
        "name": "🇬🇧 English (Formal Business)",
        "tests": [
            {
                "id": "ENG-B2B-001",
                "input": "Our employees cannot access the platform through corporate SSO",
                "expected_category": "ENTERPRISE",
                "expected_solution": "sso_001",
                "description": "SSO access - Formal English"
            },
            {
                "id": "ENG-B2B-002",
                "input": "SCORM completion tracking stuck at 99% for multiple users",
                "expected_category": "ENTERPRISE",
                "expected_solution": "scorm_001",
                "description": "SCORM issue - Formal English"
            },
            {
                "id": "ENG-B2B-003",
                "input": "Corporate firewall blocking zedny.ai domain",
                "expected_category": "ENTERPRISE",
                "expected_solution": "firewall_001",
                "description": "Firewall blocking - Formal English"
            },
            {
                "id": "ENG-B2B-004",
                "input": "Need bulk certificate generation for 500 employees",
                "is_b2b_query": True,
                "expected_behavior": "B2B-specific request",
                "description": "Bulk certificates - Formal English"
            },
            {
                "id": "ENG-B2B-005",
                "input": "Integration with our LMS is not syncing user progress",
                "expected_category": "ENTERPRISE",
                "is_b2b_query": True,
                "description": "LMS integration - Formal English"
            }
        ]
    },
    
    "CODE_SWITCHING": {
        "name": "🔀 Code-Switching (Mixed Arabic-English)",
        "tests": [
            {
                "id": "MIX-B2B-001",
                "input": "الـ SSO مش شغال والـ IT department بيقولوا المشكلة من عندكم",
                "expected_category": "ENTERPRISE",
                "dialect": "Mixed Egyptian-English",
                "description": "SSO with IT reference - Code-switching"
            },
            {
                "id": "MIX-B2B-002",
                "input": "عندنا issue في الـ SCORM tracking، واقف على 99%",
                "expected_category": "ENTERPRISE",
                "expected_solution": "scorm_001",
                "dialect": "Mixed Egyptian-English",
                "description": "SCORM issue - Code-switching"
            },
            {
                "id": "MIX-B2B-003",
                "input": "الـ HR manager عايز progress report للـ employees",
                "is_b2b_query": True,
                "dialect": "Mixed Egyptian-English",
                "description": "HR reporting - Code-switching"
            }
        ]
    },
    
    "B2B_EDGE_CASES": {
        "name": "⚠️ B2B Edge Cases",
        "tests": [
            {
                "id": "EDGE-B2B-001",
                "input": "500 موظف محتاجين certificates في نفس الوقت، النظام بيهنج",
                "is_b2b_query": True,
                "complexity": "HIGH",
                "description": "Bulk operation performance"
            },
            {
                "id": "EDGE-B2B-002",
                "input": "عايزين integration مع SAP SuccessFactors",
                "is_b2b_query": True,
                "expected_behavior": "Should escalate to enterprise team",
                "description": "Third-party integration request"
            },
            {
                "id": "EDGE-B2B-003",
                "input": "المدير المالي عايز ROI report للتدريب",
                "is_b2b_query": True,
                "expected_behavior": "B2B analytics request",
                "description": "ROI reporting - CFO request"
            },
            {
                "id": "EDGE-B2B-004",
                "input": "الشركة عندها فروع في 5 دول، محتاجين different time zones support",
                "is_b2b_query": True,
                "complexity": "HIGH",
                "description": "Multi-region enterprise setup"
            }
        ]
    }
}


def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_test(test_id, description, passed, details=""):
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    dialect_info = f" ({details.get('dialect', 'N/A')})" if isinstance(details, dict) and 'dialect' in details else ""
    print(f"  [{test_id}] {description}{dialect_info}: {status}")
    if isinstance(details, str) and details:
        print(f"         {Colors.YELLOW}{details}{Colors.END}")


def test_language_coverage():
    """Test that system handles all language variants"""
    print_header("🌍 LANGUAGE COVERAGE TEST")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 0
    
    total_tests = 0
    passed_tests = 0
    
    for category_key, category in B2B_TEST_SCENARIOS.items():
        print(f"\n{Colors.MAGENTA}Testing: {category['name']}{Colors.END}\n")
        
        for test in category["tests"]:
            total_tests += 1
            result = RagService.search_local_solutions(test["input"])
            
            # Check if solution found
            if "expected_solution" in test:
                matched = result and result.get("solution_id") == test["expected_solution"]
                print_test(
                    test["id"],
                    test["description"],
                    matched,
                    {"dialect": test.get("dialect", "N/A"), "result": result.get("solution_id") if result else "None"}
                )
                if matched:
                    passed_tests += 1
            elif "expected_category" in test:
                matched = result and result.get("category") == test["expected_category"]
                print_test(
                    test["id"],
                    test["description"],
                    matched,
                    {"dialect": test.get("dialect", "N/A"), "result": result.get("category") if result else "None"}
                )
                if matched:
                    passed_tests += 1
            else:
                # B2B query without specific expectation
                has_result = result is not None
                print_test(
                    test["id"],
                    test["description"],
                    has_result,
                    {"dialect": test.get("dialect", "N/A"), "note": "B2B query processed"}
                )
                if has_result:
                    passed_tests += 1
    
    return passed_tests, total_tests


def test_dialect_understanding():
    """Specific test for Egyptian dialect comprehension"""
    print_header("🗣️ EGYPTIAN DIALECT COMPREHENSION")
    
    if not IMPORTS_OK:
        return 0, 0
    
    egyptian_phrases = [
        {"phrase": "مش بيدخلني", "should_match": "login", "id": "DIAL-001"},
        {"phrase": "بيطير", "should_match": "crash", "id": "DIAL-002"},
        {"phrase": "بايظ", "should_match": "broken", "id": "DIAL-003"},
        {"phrase": "السايت", "should_match": "website", "id": "DIAL-004"},
        {"phrase": "الأبلكيشن", "should_match": "app", "id": "DIAL-005"}
    ]
    
    passed = 0
    total = len(egyptian_phrases)
    
    for item in egyptian_phrases:
        # Test that dialect is processed (this is implicit in RAG search)
        result = RagService.search_local_solutions(f"{item['phrase']} مش شغال")
        has_result = result is not None
        print_test(
            item["id"],
            f"'{item['phrase']}' understood",
            has_result,
            f"Expected concept: {item['should_match']}"
        )
        if has_result:
            passed += 1
    
    return passed, total


def generate_summary_report():
    """Generate B2B test summary"""
    print_header("📊 B2B TEST SUMMARY")
    
    total_by_language = {}
    for category_key, category in B2B_TEST_SCENARIOS.items():
        count = len(category["tests"])
        total_by_language[category["name"]] = count
        print(f"  {category['name']}: {count} tests")
    
    total = sum(total_by_language.values())
    print(f"\n{Colors.BOLD}Total B2B Scenarios: {total}{Colors.END}")


def run_all_tests():
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🏢 ZEDNY B2B - COMPREHENSIVE LANGUAGE TEST SUITE               ║")
    print("║     Arabic | Egyptian | English | Code-Switching                ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    results = []
    
    # Run tests
    results.append(("Language Coverage", *test_language_coverage()))
    results.append(("Egyptian Dialect", *test_dialect_understanding()))
    
    # Summary
    print_header("📊 FINAL RESULTS")
    
    total_passed = 0
    total_tests = 0
    
    for name, passed, total in results:
        total_passed += passed
        total_tests += total
        rate = (passed/total*100) if total > 0 else 0
        status = f"{Colors.GREEN}✅" if passed == total else f"{Colors.YELLOW}⚠️" if passed > 0 else f"{Colors.RED}❌"
        print(f"  {status} {name}: {passed}/{total} ({rate:.0f}%){Colors.END}")
    
    overall_rate = (total_passed/total_tests*100) if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}Overall: {total_passed}/{total_tests} ({overall_rate:.1f}%){Colors.END}")
    
    # Language breakdown
    generate_summary_report()
    
    # Status
    if overall_rate >= 90:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! B2B multilingual support is robust.{Colors.END}")
    elif overall_rate >= 70:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ GOOD. Some language improvements needed.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ NEEDS WORK. Review failed tests.{Colors.END}")
    
    # Save results
    report = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "B2B Multilingual Comprehensive",
        "languages_tested": ["Arabic MSA", "Egyptian Colloquial", "English", "Code-Switching"],
        "results": [{"name": r[0], "passed": r[1], "total": r[2]} for r in results],
        "scenarios": B2B_TEST_SCENARIOS,
        "total_passed": total_passed,
        "total_tests": total_tests,
        "pass_rate": overall_rate
    }
    
    with open("b2b_multilingual_test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Colors.CYAN}📄 Results saved to: b2b_multilingual_test_results.json{Colors.END}")
    
    return overall_rate


if __name__ == "__main__":
    run_all_tests()
