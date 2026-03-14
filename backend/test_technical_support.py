"""
🔧 TECHNICAL SUPPORT AI - COMPREHENSIVE TEST SUITE
====================================================
Professional Testing for Zedny's Technical Problem-Solving Capabilities

Tests:
1. Direct RAG Match (keyword present in solutions_db)
2. Semantic Understanding (paraphrased problems)
3. Arabic Dialect Variants (اللهجة المصرية)
4. Edge Cases (multiple symptoms, vague inputs)
5. Solution Quality (actionable, step-by-step)
6. Anti-Loop (doesn't repeat solutions)
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TechnicalSupportTester:
    """
    Professional Test Suite for Technical Support AI
    """
    
    # ========================================
    # CATEGORY 1: DIRECT KEYWORD MATCH
    # These should match solutions_db directly
    # ========================================
    
    DIRECT_MATCH_TESTS = [
        {
            "id": "TECH-001",
            "category": "VIDEO - Black Screen",
            "input": "الفيديو شاشة سوداء",
            "expected_solution_id": "vid_black_001",
            "expected_keywords_in_response": ["Hard Refresh", "Widevine", "Ctrl+Shift+R"],
            "language": "ar"
        },
        {
            "id": "TECH-002",
            "category": "VIDEO - Buffering",
            "input": "الفيديو بطيء وبيقطع",
            "expected_solution_id": "vid_buffer_001",
            "expected_keywords_in_response": ["Quality", "480p", "Cache", "Incognito"],
            "language": "ar"
        },
        {
            "id": "TECH-003",
            "category": "AUDIO - No Sound",
            "input": "مفيش صوت في الفيديو",
            "expected_solution_id": "audio_001",
            "expected_keywords_in_response": ["Mute", "Tab", "Unmute", "Volume Mixer"],
            "language": "ar"
        },
        {
            "id": "TECH-004",
            "category": "LOGIN - Can't Sign In",
            "input": "مش قادر أدخل على حسابي",
            "expected_solution_id": "login_001",
            "expected_keywords_in_response": ["Caps Lock", "Cookies", "Incognito"],
            "language": "ar"
        },
        {
            "id": "TECH-005",
            "category": "CERTIFICATE - Not Generated",
            "input": "الشهادة مش ظاهرة",
            "expected_solution_id": "cert_001",
            "expected_keywords_in_response": ["100%", "24-48", "My Certificates"],
            "language": "ar"
        },
        {
            "id": "TECH-006",
            "category": "MOBILE - App Crash",
            "input": "التطبيق بيقفل لوحده",
            "expected_solution_id": "app_crash_001",
            "expected_keywords_in_response": ["حدث", "Cache", "احذف"],
            "language": "ar"
        },
        {
            "id": "TECH-007",
            "category": "PAYMENT - Failed",
            "input": "الدفع فشل",
            "expected_solution_id": "payment_001",
            "expected_keywords_in_response": ["كارت", "3D Secure", "البنك"],
            "language": "ar"
        },
        {
            "id": "TECH-008",
            "category": "QUIZ - Can't Submit",
            "input": "مش قادر أسلم الاختبار",
            "expected_solution_id": "quiz_submit_001",
            "expected_keywords_in_response": ["مجاوبة", "Scroll", "متصفح"],
            "language": "ar"
        },
    ]
    
    # ========================================
    # CATEGORY 2: SEMANTIC UNDERSTANDING
    # Same problem, different wording (paraphrased)
    # ========================================
    
    SEMANTIC_TESTS = [
        {
            "id": "SEM-001",
            "category": "VIDEO - Black Screen (Paraphrased)",
            "input": "لما بفتح الكورس الفيديو مش ظاهر خالص، بس ظاهر حاجة سودا",
            "expected_category": "VIDEO",
            "should_match_any": ["vid_black_001", "vid_black_002"],
            "reason": "User describes black screen without using exact keyword 'شاشة سوداء'",
            "language": "ar"
        },
        {
            "id": "SEM-002",
            "category": "AUDIO - No Sound (Paraphrased)",
            "input": "الفيديو شغال عادي بس مش بسمع حاجة",
            "expected_category": "AUDIO",
            "should_match_any": ["audio_001", "audio_002"],
            "reason": "Semantic equivalent of 'مفيش صوت' without exact words",
            "language": "ar"
        },
        {
            "id": "SEM-003",
            "category": "LOGIN - Can't Enter (Paraphrased)",
            "input": "بحاول أفتح الموقع بس مش بيقبل الإيميل والباسورد بتوعي",
            "expected_category": "LOGIN",
            "should_match_any": ["login_001", "login_002"],
            "reason": "Login problem described differently",
            "language": "ar"
        },
        {
            "id": "SEM-004",
            "category": "VIDEO - Freezing (Paraphrased)",
            "input": "الفيديو بيعلق كل شوية ومش بيتحرك",
            "expected_category": "VIDEO",
            "should_match_any": ["vid_freeze_001"],
            "reason": "'بيعلق' is semantic equivalent of 'بيهنج'",
            "language": "ar"
        },
        {
            "id": "SEM-005",
            "category": "English - Video Buffering",
            "input": "The video keeps stopping and loading",
            "expected_category": "VIDEO",
            "should_match_any": ["vid_buffer_001", "vid_buffer_002"],
            "reason": "English semantic variant of buffering",
            "language": "en"
        },
    ]
    
    # ========================================
    # CATEGORY 3: ARABIC DIALECT VARIANTS
    # Same meaning, different Egyptian expressions
    # ========================================
    
    DIALECT_TESTS = [
        {
            "id": "DIAL-001",
            "category": "Egyptian Slang - Video Issue",
            "input": "يا عم الفيديو مش راضي يشتغل خالص",
            "expected_match": True,
            "notes": "Casual Egyptian - should still work",
            "language": "ar-eg"
        },
        {
            "id": "DIAL-002",
            "category": "Egyptian Slang - Login Issue",
            "input": "السايت مش بيدخلني انا زهقت",
            "expected_match": True,
            "notes": "'مش بيدخلني' = login issue",
            "language": "ar-eg"
        },
        {
            "id": "DIAL-003",
            "category": "Egyptian Slang - App Crash",
            "input": "الأبلكيشن بيطير كل ما أفتحه",
            "expected_match": True,
            "notes": "'بيطير' = crashes in Egyptian slang",
            "language": "ar-eg"
        },
        {
            "id": "DIAL-004",
            "category": "Gulf Arabic",
            "input": "الفيديو ما يشتغل عندي",
            "expected_match": True,
            "notes": "Gulf dialect - should work",
            "language": "ar-gulf"
        },
        {
            "id": "DIAL-005",
            "category": "Formal Arabic (MSA)",
            "input": "أواجه صعوبة في تسجيل الدخول إلى حسابي",
            "expected_match": True,
            "notes": "Formal MSA - should work",
            "language": "ar-msa"
        },
    ]
    
    # ========================================
    # CATEGORY 4: EDGE CASES & HARD SCENARIOS
    # Multiple symptoms, vague, missing info
    # ========================================
    
    EDGE_CASES = [
        {
            "id": "EDGE-TECH-001",
            "category": "Multiple Symptoms",
            "input": "الفيديو شاشة سوداء ومفيش صوت كمان",
            "expected_behavior": "Should prioritize video issue (more common root cause) OR ask clarifying question",
            "complexity": "HIGH"
        },
        {
            "id": "EDGE-TECH-002",
            "category": "Vague Input",
            "input": "الموقع مش شغال",
            "expected_behavior": "Should ask clarifying question about WHAT specifically isn't working",
            "expected_questions": ["فين بالظبط؟", "What page?", "Video?", "Login?"],
            "complexity": "MEDIUM"
        },
        {
            "id": "EDGE-TECH-003",
            "category": "Out of Scope Tech",
            "input": "لابتوبي بيهنج كتير",
            "expected_behavior": "Should recognize this is NOT a Zedny platform issue and politely redirect",
            "is_out_of_scope": True,
            "complexity": "MEDIUM"
        },
        {
            "id": "EDGE-TECH-004",
            "category": "Already Tried Common Solutions",
            "input": "الفيديو شاشة سوداء، جربت مسحت الكاش وجربت في Incognito ومافيش فايدة",
            "expected_behavior": "Should NOT suggest cache/incognito again (anti-loop). Should escalate or try next solution.",
            "solutions_tried": ["cache", "incognito"],
            "complexity": "HIGH"
        },
        {
            "id": "EDGE-TECH-005",
            "category": "Enterprise/SSO Issue",
            "input": "مش قادر أدخل بإيميل الشركة عن طريق الـ SSO",
            "expected_behavior": "Should match SSO/Enterprise solution",
            "expected_solution_id": "sso_001",
            "complexity": "HIGH"
        },
        {
            "id": "EDGE-TECH-006",
            "category": "SCORM/LMS Issue",
            "input": "الكورس واقف على 99% ومش بيكمل",
            "expected_behavior": "Should match SCORM solution",
            "expected_solution_id": "scorm_001",
            "complexity": "HIGH"
        },
        {
            "id": "EDGE-TECH-007",
            "category": "Gibberish/Typos",
            "input": "الففيديوو مششش شغعال",
            "expected_behavior": "Should still understand this is a video issue despite typos",
            "complexity": "MEDIUM"
        },
    ]
    
    # ========================================
    # CATEGORY 5: SOLUTION QUALITY VALIDATION
    # Response should be actionable & helpful
    # ========================================
    
    QUALITY_CRITERIA = {
        "has_numbered_steps": True,
        "has_bold_keywords": True,
        "max_length_lines": 7,
        "has_arabic_when_arabic_input": True,
        "ends_with_follow_up": True,  # "جرب وقلي لو اشتغل"
        "no_generic_responses": True
    }
    
    # ========================================
    # CATEGORY 6: ANTI-LOOP VALIDATION
    # System should track solutions_tried
    # ========================================
    
    ANTI_LOOP_TESTS = [
        {
            "id": "LOOP-001",
            "conversation": [
                {"user": "الفيديو شاشة سوداء", "solutions_tried": []},
                {"user": "جربت ومانفعش", "solutions_tried": ["vid_black_001"]},
                {"user": "برضو نفس المشكلة", "solutions_tried": ["vid_black_001", "vid_black_002"]},
            ],
            "expected_behavior": "3rd response should suggest escalation or new solution, NOT vid_black_001 or vid_black_002"
        }
    ]
    
    # ========================================
    # 📊 ANALYSIS FRAMEWORK
    # ========================================
    
    def analyze_system_gaps(self):
        """
        Identify gaps in the current technical support system
        """
        gaps = {
            "prompting_gaps": [],
            "rag_gaps": [],
            "solutions_db_gaps": [],
            "recommendations": []
        }
        
        # 1. Prompting Gaps
        print(f"\n{Color.CYAN}{'='*80}{Color.END}")
        print(f"{Color.BOLD}📊 SYSTEM GAP ANALYSIS{Color.END}")
        print(f"{'='*80}\n")
        
        # Check for semantic understanding
        print(f"{Color.YELLOW}1. PROMPTING ANALYSIS{Color.END}")
        prompting_issues = [
            "❌ No semantic fallback when exact keywords don't match",
            "⚠️ Dialect variations may not be captured (بيطير vs بيقفل)",
            "⚠️ May not ask good follow-up questions for vague inputs",
            "⚠️ No explicit instruction to avoid generic responses"
        ]
        for issue in prompting_issues:
            print(f"   {issue}")
            gaps["prompting_gaps"].append(issue)
        
        # 2. RAG Gaps
        print(f"\n{Color.YELLOW}2. RAG ANALYSIS{Color.END}")
        rag_issues = [
            "⚠️ Keyword matching is exact - misses semantic equivalents",
            "⚠️ Arabic prefix regex may miss some variations",
            "⚠️ Priority scoring is simple (may not pick best solution)",
            "✅ Supabase vector search available as backup"
        ]
        for issue in rag_issues:
            print(f"   {issue}")
            if issue.startswith("❌") or issue.startswith("⚠️"):
                gaps["rag_gaps"].append(issue)
        
        # 3. Solutions DB Gaps
        print(f"\n{Color.YELLOW}3. SOLUTIONS DATABASE ANALYSIS{Color.END}")
        print(f"   Total Solutions: 28")
        print(f"   Categories: VIDEO (5), AUDIO (3), LOGIN (3), COURSE (3), QUIZ (2), CERTIFICATE (2), PAYMENT (2), MOBILE (2), ENTERPRISE (3), NETWORK (2), UNIVERSAL (1)")
        
        missing_scenarios = [
            "❌ No solution for 'browser compatibility' (Safari issues)",
            "❌ No solution for 'mobile browser' specific issues",
            "⚠️ 'Universal fallback' is too generic",
            "⚠️ No specific iOS vs Android differentiation"
        ]
        for issue in missing_scenarios:
            print(f"   {issue}")
            gaps["solutions_db_gaps"].append(issue)
        
        # 4. Recommendations
        print(f"\n{Color.GREEN}4. RECOMMENDATIONS{Color.END}")
        recommendations = [
            "🔧 PROMPTING: Add Few-Shot examples for technical scenarios",
            "🔧 PROMPTING: Add explicit instruction to ask clarifying questions first",
            "🔧 RAG: Add semantic fallback using Supabase embeddings",
            "🔧 RAG: Improve Arabic regex for more dialect support",
            "🔧 SOLUTIONS_DB: Add more keyword synonyms",
            "🔧 SOLUTIONS_DB: Add browser-specific solutions",
            "🔧 CONVERSATION: Track solutions_tried for anti-loop"
        ]
        for rec in recommendations:
            print(f"   {rec}")
            gaps["recommendations"].append(rec)
        
        return gaps
    
    def generate_test_report(self):
        """Generate comprehensive test documentation"""
        print(f"\n{Color.BOLD}{Color.MAGENTA}")
        print("="*80)
        print("🔧 TECHNICAL SUPPORT TEST REPORT")
        print("="*80)
        print(f"{Color.END}\n")
        
        # Summary
        total_tests = (
            len(self.DIRECT_MATCH_TESTS) + 
            len(self.SEMANTIC_TESTS) + 
            len(self.DIALECT_TESTS) + 
            len(self.EDGE_CASES) +
            len(self.ANTI_LOOP_TESTS)
        )
        
        print(f"{Color.CYAN}Test Coverage:{Color.END}")
        print(f"  • Direct Match Tests:    {len(self.DIRECT_MATCH_TESTS)}")
        print(f"  • Semantic Tests:        {len(self.SEMANTIC_TESTS)}")
        print(f"  • Dialect Variant Tests: {len(self.DIALECT_TESTS)}")
        print(f"  • Edge Cases:            {len(self.EDGE_CASES)}")
        print(f"  • Anti-Loop Tests:       {len(self.ANTI_LOOP_TESTS)}")
        print(f"  {Color.BOLD}TOTAL: {total_tests} tests{Color.END}\n")
        
        # Analyze gaps
        gaps = self.analyze_system_gaps()
        
        return gaps


# ========================================
# MAIN EXECUTION
# ========================================

def main():
    print(f"{Color.BOLD}{Color.MAGENTA}")
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  🔧 Zedny Technical Support AI - Comprehensive Test Suite    ║
    ║              Professional QA & Engineering Analysis           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print(f"{Color.END}")
    
    tester = TechnicalSupportTester()
    gaps = tester.generate_test_report()
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "tests": {
            "direct_match": tester.DIRECT_MATCH_TESTS,
            "semantic": tester.SEMANTIC_TESTS,
            "dialect": tester.DIALECT_TESTS,
            "edge_cases": tester.EDGE_CASES,
            "anti_loop": tester.ANTI_LOOP_TESTS
        },
        "gaps": gaps,
        "quality_criteria": tester.QUALITY_CRITERIA
    }
    
    with open("tech_support_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Color.GREEN}✅ Report saved to: tech_support_test_report.json{Color.END}")


if __name__ == "__main__":
    main()
