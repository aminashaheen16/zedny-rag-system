"""
🧪 EXECUTABLE TEST SCRIPT - Technical Support AI
================================================
This script tests all scenarios against the LIVE AI service.
Run this after starting the backend server.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test if imports work
try:
    from app.core.solutions_db import (
        SOLUTIONS_DB, 
        normalize_egyptian_slang, 
        expand_with_synonyms,
        EGYPTIAN_SLANG_MAP,
        VIDEO_SYNONYMS,
        AUDIO_SYNONYMS,
        LOGIN_SYNONYMS,
        APP_SYNONYMS
    )
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
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_test(test_id, description, passed, details=""):
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"  [{test_id}] {description}: {status}")
    if details:
        print(f"         {Colors.YELLOW}{details}{Colors.END}")


def test_synonym_expansion():
    """Test 1: Synonym Expansion Function"""
    print_header("TEST 1: Synonym Expansion Function")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 3
    
    passed = 0
    total = 3
    
    # Test 1.1: Video synonym expansion
    test_input = "الفيديو مش ظاهر"
    result = expand_with_synonyms(test_input)
    has_synonyms = "black screen" in result.lower() or "شاشة سوداء" in result.lower()
    print_test("SYN-001", f"Video: '{test_input}' expands to include 'black screen'", has_synonyms, f"Result: {result[:80]}...")
    if has_synonyms: passed += 1
    
    # Test 1.2: Audio synonym expansion
    test_input = "مفيش صوت"
    result = expand_with_synonyms(test_input)
    has_synonyms = "no sound" in result.lower() or "no audio" in result.lower()
    print_test("SYN-002", f"Audio: '{test_input}' expands to include 'no sound'", has_synonyms, f"Result: {result[:80]}...")
    if has_synonyms: passed += 1
    
    # Test 1.3: Login synonym expansion
    test_input = "مش قادر أدخل"
    result = expand_with_synonyms(test_input)
    has_synonyms = "login" in result.lower()
    print_test("SYN-003", f"Login: '{test_input}' expands to include 'login'", has_synonyms, f"Result: {result[:80]}...")
    if has_synonyms: passed += 1
    
    return passed, total


def test_egyptian_slang():
    """Test 2: Egyptian Slang Normalization"""
    print_header("TEST 2: Egyptian Slang Normalization")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 4
    
    passed = 0
    total = 4
    
    # Test 2.1: بيطير = crash
    test_input = "التطبيق بيطير"
    result = normalize_egyptian_slang(test_input)
    has_crash = "crash" in result.lower() or "بيقفل" in result
    print_test("SLANG-001", f"'{test_input}' → includes 'crash/بيقفل'", has_crash, f"Result: {result}")
    if has_crash: passed += 1
    
    # Test 2.2: بايظ = broken
    test_input = "الموقع بايظ"
    result = normalize_egyptian_slang(test_input)
    has_broken = "مش شغال" in result or "broken" in result.lower()
    print_test("SLANG-002", f"'{test_input}' → includes 'مش شغال/broken'", has_broken, f"Result: {result}")
    if has_broken: passed += 1
    
    # Test 2.3: بيهنج = freezing
    test_input = "الفيديو بيهنج"
    result = normalize_egyptian_slang(test_input)
    has_freeze = "freezing" in result.lower() or "واقف" in result
    print_test("SLANG-003", f"'{test_input}' → includes 'freezing/واقف'", has_freeze, f"Result: {result}")
    if has_freeze: passed += 1
    
    # Test 2.4: مش بيدخلني = login
    test_input = "السايت مش بيدخلني"
    result = normalize_egyptian_slang(test_input)
    has_login = "login" in result.lower() or "مش قادر أدخل" in result
    print_test("SLANG-004", f"'{test_input}' → includes 'login'", has_login, f"Result: {result}")
    if has_login: passed += 1
    
    return passed, total


def test_local_rag_matching():
    """Test 3: Local RAG Solution Matching"""
    print_header("TEST 3: Local RAG Solution Matching")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 6
    
    passed = 0
    total = 6
    
    test_cases = [
        {
            "id": "RAG-001",
            "input": "الفيديو شاشة سوداء",
            "expected_category": "VIDEO",
            "description": "Direct match: Black screen"
        },
        {
            "id": "RAG-002",
            "input": "التطبيق بيطير",  # Egyptian slang for crash
            "expected_category": "MOBILE",
            "description": "Egyptian slang: App crash"
        },
        {
            "id": "RAG-003",
            "input": "مفيش صوت في الفيديو",
            "expected_category": "AUDIO",
            "description": "Direct match: No audio"
        },
        {
            "id": "RAG-004",
            "input": "مش قادر أسجل دخول",
            "expected_category": "LOGIN",
            "description": "Semantic: Login issue"
        },
        {
            "id": "RAG-005",
            "input": "الفيديو واقف ومش بيتحرك",  # Freezing
            "expected_category": "VIDEO",
            "description": "Semantic: Video freezing"
        },
        {
            "id": "RAG-006",
            "input": "الشهادة مش ظاهرة",
            "expected_category": "CERTIFICATE",
            "description": "Direct match: Certificate"
        },
    ]
    
    for test in test_cases:
        result = RagService.search_local_solutions(test["input"])
        if result:
            matched = result.get("category") == test["expected_category"]
            print_test(
                test["id"], 
                test["description"], 
                matched,
                f"Expected: {test['expected_category']}, Got: {result.get('category', 'None')}"
            )
            if matched: passed += 1
        else:
            print_test(test["id"], test["description"], False, "No solution found!")
    
    return passed, total


def test_anti_loop():
    """Test 4: Anti-Loop Exclusion"""
    print_header("TEST 4: Anti-Loop Exclusion")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 2
    
    passed = 0
    total = 2
    
    # Test 4.1: First search returns vid_black_001
    result1 = RagService.search_local_solutions("الفيديو شاشة سوداء")
    first_id = result1.get("solution_id") if result1 else None
    is_vid_black = first_id and first_id.startswith("vid_black")
    print_test("LOOP-001", "First search returns video solution", is_vid_black, f"Got: {first_id}")
    if is_vid_black: passed += 1
    
    # Test 4.2: Second search with exclusion returns DIFFERENT solution
    if first_id:
        result2 = RagService.search_local_solutions("الفيديو شاشة سوداء", exclude_ids=[first_id])
        second_id = result2.get("solution_id") if result2 else None
        is_different = second_id and second_id != first_id
        print_test("LOOP-002", "Second search (with exclusion) returns different solution", is_different, f"Got: {second_id}")
        if is_different: passed += 1
    else:
        print_test("LOOP-002", "Second search (with exclusion) returns different solution", False, "First search failed")
    
    return passed, total


def test_solutions_database():
    """Test 5: Solutions Database Quality"""
    print_header("TEST 5: Solutions Database Quality")
    
    if not IMPORTS_OK:
        print(f"{Colors.RED}❌ Cannot test - imports failed{Colors.END}")
        return 0, 3
    
    passed = 0
    total = 3
    
    # Test 5.1: Database has solutions
    has_solutions = len(SOLUTIONS_DB) > 0
    print_test("DB-001", f"Database has solutions", has_solutions, f"Count: {len(SOLUTIONS_DB)}")
    if has_solutions: passed += 1
    
    # Test 5.2: All solutions have required fields
    required_fields = ["solution_id", "category", "symptom_keywords", "solution_ar"]
    all_valid = all(
        all(field in sol for field in required_fields) 
        for sol in SOLUTIONS_DB
    )
    print_test("DB-002", "All solutions have required fields", all_valid)
    if all_valid: passed += 1
    
    # Test 5.3: Category coverage
    categories = set(sol["category"] for sol in SOLUTIONS_DB)
    expected_categories = {"VIDEO", "AUDIO", "LOGIN", "CERTIFICATE", "MOBILE", "PAYMENT"}
    has_coverage = expected_categories.issubset(categories)
    print_test("DB-003", "Database covers all main categories", has_coverage, f"Categories: {categories}")
    if has_coverage: passed += 1
    
    return passed, total


def run_all_tests():
    """Run all test suites"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🧪 ZEDNY TECHNICAL SUPPORT AI - COMPREHENSIVE TEST SUITE        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    results = []
    
    # Run all tests
    results.append(("Synonym Expansion", *test_synonym_expansion()))
    results.append(("Egyptian Slang", *test_egyptian_slang()))
    results.append(("Local RAG Matching", *test_local_rag_matching()))
    results.append(("Anti-Loop", *test_anti_loop()))
    results.append(("Solutions Database", *test_solutions_database()))
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
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
    
    if overall_rate >= 90:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! System is production-ready.{Colors.END}")
    elif overall_rate >= 70:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ GOOD. Some improvements needed.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ NEEDS WORK. Review failed tests.{Colors.END}")
    
    # Save results
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": [{"name": r[0], "passed": r[1], "total": r[2]} for r in results],
        "total_passed": total_passed,
        "total_tests": total_tests,
        "pass_rate": overall_rate
    }
    
    with open("tech_support_test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Colors.CYAN}📄 Results saved to: tech_support_test_results.json{Colors.END}")
    
    return overall_rate


if __name__ == "__main__":
    run_all_tests()
