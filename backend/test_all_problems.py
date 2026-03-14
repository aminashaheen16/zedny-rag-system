"""
🧪 Zedny.ai Technical Support Bot - Test Script
=================================================
هذا السكريبت يحتوي على جميع المشاكل التي يمكن اختبار البوت بها.
استخدم هذه الرسائل في الشات لاختبار جودة الردود.
"""

# =============================================
# 1. VIDEO PLAYBACK ISSUES (مشاكل الفيديو)
# =============================================

VIDEO_TESTS = [
    # Arabic Tests
    "الفيديو مش شغال معايا",
    "الفيديو بيحمل بطيء جداً",
    "الفيديو شاشة سوداء ومفيش حاجة",
    "الفيديو بيعلق في النص",
    "الصوت مش شغال في الفيديو",
    "الفيديو جودته وحشة",
    "الترجمة مش ظاهرة",
    "الفيديو بيقف لوحده فجأة",
    
    # English Tests
    "The video is not playing",
    "Video is buffering too much",
    "Black screen when I open video",
    "Video freezes in the middle",
]

# =============================================
# 2. AUDIO ISSUES (مشاكل الصوت)
# =============================================

AUDIO_TESTS = [
    "مفيش صوت خالص",
    "الصوت مش مظبوط - فيه Echo",
    "الصوت متأخر عن الفيديو",
    "No audio in the course",
    "Audio echo problem",
]

# =============================================
# 3. LOGIN & ACCOUNT ISSUES (مشاكل الدخول)
# =============================================

LOGIN_TESTS = [
    "نسيت كلمة السر",
    "مش قادر أدخل حسابي",
    "الحساب مقفل",
    "الجلسة انتهت فجأة",
    "عايز أغير الإيميل بتاعي",
    "I forgot my password",
    "Can't login to my account",
    "Account is locked",
]

# =============================================
# 4. COURSE ACCESS ISSUES (مشاكل الوصول للكورسات)
# =============================================

ACCESS_TESTS = [
    "مش لاقي الكورس بتاعي",
    "الدروس اختفت",
    "الكورس مش ظاهر في حسابي",
    "التقدم بتاعي مش محفوظ",
    "Course not showing in my account",
    "My progress is not saved",
]

# =============================================
# 5. QUIZ & ASSESSMENT (مشاكل الاختبارات)
# =============================================

QUIZ_TESTS = [
    "الإجابات مش بتتحفظ",
    "التايمر سريع جداً",
    "مش قادر أبعت الاختبار",
    "الدرجة غلط",
    "الاختبار مقفل ومش بيفتح",
    "Quiz answers not saving",
    "Can't submit my test",
]

# =============================================
# 6. CERTIFICATE ISSUES (مشاكل الشهادات)
# =============================================

CERTIFICATE_TESTS = [
    "الشهادة مش ظهرت",
    "اسمي غلط في الشهادة",
    "مش قادر أنزل الشهادة",
    "فين الشهادة بتاعتي؟",
    "Certificate not generated",
    "Wrong name on certificate",
]

# =============================================
# 7. PAYMENT ISSUES (مشاكل الدفع)
# =============================================

PAYMENT_TESTS = [
    "الدفع فشل",
    "اتخصم مني مرتين",
    "الاشتراك مش مفعل",
    "السعر غلط",
    "عايز استرجع فلوسي",
    "Payment failed",
    "I was charged twice",
    "Subscription not activated",
]

# =============================================
# 8. MOBILE APP ISSUES (مشاكل تطبيق الموبايل)
# =============================================

MOBILE_TESTS = [
    "التطبيق بيقفل فجأة",
    "الفيديوهات مش بتنزل",
    "التنبيهات مش شغالة",
    "مش قادر أدخل من التطبيق",
    "App keeps crashing",
    "Can't download videos",
]

# =============================================
# 9. LIVE SESSION ISSUES (مشاكل الجلسات المباشرة)
# =============================================

LIVE_TESTS = [
    "مش قادر أدخل الجلسة",
    "الصوت فيه Echo في الجلسة",
    "بيطردني من الجلسة",
    "فين تسجيل الجلسة؟",
    "Can't join the live session",
    "Getting kicked from webinar",
]

# =============================================
# 10. DOWNLOAD ISSUES (مشاكل التحميل)
# =============================================

DOWNLOAD_TESTS = [
    "مش قادر أنزل المحتوى",
    "الفيديو المنزل مش شغال",
    "التحميلات انتهت صلاحيتها",
    "Downloaded video won't play",
    "Can't download offline content",
]

# =============================================
# 11. BROWSER ISSUES (مشاكل المتصفح)
# =============================================

BROWSER_TESTS = [
    "الموقع مش شغال على Safari",
    "مش شغال على Chrome",
    "الموقع بطيء على Firefox",
    "Site not working on Safari",
    "Issues with Edge browser",
]

# =============================================
# 12. NETWORK ISSUES (مشاكل الشبكة)
# =============================================

NETWORK_TESTS = [
    "الموقع بطيء جداً",
    "المحتوى محجوب",
    "فيه Error 404",
    "Connection timeout",
    "Site is very slow",
    "Getting 403 error",
]

# =============================================
# 13. EDGE CASES (حالات خارج الموسوعة)
# =============================================

EDGE_CASES = [
    # مشاكل غير تقليدية - لاختبار ذكاء الـ LLM
    "الخط صغير جداً ومش باين",
    "الألوان مش واضحة - عندي عمى ألوان",
    "المنصة مش شغالة بالـ Dark Mode",
    "عايز أشارك الكورس مع زميلي",
    "إزاي أطبع المحتوى؟",
    "الكورس بلغة مش بفهمها",
    "فين خدمة العملاء؟",
    "عايز أحذف حسابي",
    "How to enable dark mode?",
    "Can I share my course with colleague?",
]

# =============================================
# 14. ESCALATION TESTS (اختبار التصعيد)
# =============================================

ESCALATION_TESTS = [
    # Send these 3 times to trigger escalation
    "مش شغال",
    "بردو مش شغال",
    "جربت كل حاجة ومش شغال",
]

# =============================================
# 15. SALES/INFO TESTS (اختبار التوجيه للمبيعات)
# =============================================

SALES_TESTS = [
    # INFO - يجب أن يرد البوت
    "إيه هي خدمات Zedny؟",
    "ازاي تساعدوا الشركات؟",
    "What services do you offer?",
    
    # SALES - يجب أن يحول للفورم
    "عندي شركة وعايز أدرب الموظفين",
    "بكام الاشتراك لـ 100 موظف؟",
    "I want to speak to sales",
    "How much for 50 licenses?",
]

# =============================================
# QUICK TEST FUNCTION
# =============================================

def print_all_tests():
    """Print all test cases organized by category"""
    categories = {
        "1. الفيديو": VIDEO_TESTS,
        "2. الصوت": AUDIO_TESTS,
        "3. الدخول": LOGIN_TESTS,
        "4. الوصول للكورسات": ACCESS_TESTS,
        "5. الاختبارات": QUIZ_TESTS,
        "6. الشهادات": CERTIFICATE_TESTS,
        "7. الدفع": PAYMENT_TESTS,
        "8. تطبيق الموبايل": MOBILE_TESTS,
        "9. الجلسات المباشرة": LIVE_TESTS,
        "10. التحميل": DOWNLOAD_TESTS,
        "11. المتصفح": BROWSER_TESTS,
        "12. الشبكة": NETWORK_TESTS,
        "13. حالات خاصة": EDGE_CASES,
        "14. اختبار التصعيد": ESCALATION_TESTS,
        "15. المبيعات": SALES_TESTS,
    }
    
    print("\n" + "="*60)
    print("🧪 ZEDNY.AI TEST SCRIPT - ALL TEST CASES")
    print("="*60)
    
    for category, tests in categories.items():
        print(f"\n📌 {category}")
        print("-" * 40)
        for i, test in enumerate(tests, 1):
            print(f"   {i}. {test}")
    
    print("\n" + "="*60)
    print("✅ Total Test Cases:", sum(len(t) for t in categories.values()))
    print("="*60)

if __name__ == "__main__":
    print_all_tests()
