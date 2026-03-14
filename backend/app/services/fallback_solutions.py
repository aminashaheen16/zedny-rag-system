from typing import Dict, Optional

GENERIC_LOGIN_SOLUTIONS = {
    "ar": """**حلول تسجيل الدخول المقترحة:**

1️⃣ **نسيت كلمة المرور:**
• اضغط على "نسيت كلمة المرور" في صفحة الدخول.
• هيوصلك رابط على الإيميل، ادخل عليه واعمل كلمة سر جديدة.

2️⃣ **مسح بيانات المتصفح (Cache):**
• اضغط Ctrl+Shift+Delete.
• اختار "Cookies and Site Data" وامسحها.
• جرب تدخل تاني.

3️⃣ **الوضع الخفي (Incognito Mode):**
• اضغط Ctrl+Shift+N وافتح المتصفح الخفي.
• جرب تسجل دخول من هناك عشان تستبعد أي إضافات بتعطل الموقع.

**جرب الخطوات دي بالترتيب وقولي لو اشتغل 🔧**""",

    "en": """**Suggested Login Solutions:**

1️⃣ **Reset Password:**
• Click "Forgot Password" on the login page.
• You will receive a reset link via email; use it to create a new password.

2️⃣ **Clear Browser Data (Cache):**
• Press Ctrl+Shift+Delete.
• Select "Cookies and Site Data" and clear them.
• Try logging in again.

3️⃣ **Use Incognito Mode:**
• Press Ctrl+Shift+N to open an incognito window.
• Try logging in from there to rule out browser extensions.

**Try these steps in order and let me know if it works 🔧**"""
}

GENERIC_VIDEO_SOLUTIONS = {
    "ar": """**حلول تشغيل الفيديوهات:**

1️⃣ **سرعة الإنترنت:**
• تأكد إن سرعة النت مستقرة.
• جرب تغير جودة الفيديو من علامة الترس (Settings) في الفيديو لـ 360p.

2️⃣ **المتصفح:**
• تأكد إنك بتستخدم آخر نسخة من Chrome أو Edge.
• جرب تفتح الفيديو من "المتصفح الخفي" (Incognito).

**قولي لو لسه الفيديو مش بيفتح 🎬**""",

    "en": """**Video Playback Solutions:**

1️⃣ **Internet Connection:**
• Ensure your connection is stable.
• Try lowering the video quality to 360p from the Settings gear icon in the player.

2️⃣ **Browser Updates:**
• Ensure you are using the latest version of Chrome or Edge.
• Try opening the video in an "Incognito Window."

**Let me know if the video still doesn't play 🎬**"""
}

# Universal fallback for any technical issue
GENERIC_BROWSER_SOLUTIONS = {
    "ar": """**حلول عامة للمشاكل التقنية:**

1️⃣ **امسح الـ Cache:**
• اضغط Ctrl+Shift+Delete
• اختار "Cookies and Site Data" وامسحها
• حاول تاني

2️⃣ **جرب متصفح تاني:**
• Chrome / Firefox / Edge

3️⃣ **الوضع الخفي (Incognito):**
• اضغط Ctrl+Shift+N وجرب

**جرب الخطوات دي بالترتيب وقولي النتيجة 🔧**""",
    
    "en": """**General Technical Solutions:**

1️⃣ **Clear Cache:**
• Press Ctrl+Shift+Delete
• Select "Cookies and Site Data" and clear
• Try again

2️⃣ **Try Different Browser:**
• Chrome / Firefox / Edge

3️⃣ **Incognito Mode:**
• Press Ctrl+Shift+N and try

**Try these steps and let me know 🔧**"""
}

class FallbackSolutions:
    """Provides generic troubleshooting steps when RAG yields no specific match."""
    
    SOLUTIONS_MAP = {
        # Login issues (English + Arabic)
        "login": GENERIC_LOGIN_SOLUTIONS,
        "signin": GENERIC_LOGIN_SOLUTIONS,
        "password": GENERIC_LOGIN_SOLUTIONS,
        "دخول": GENERIC_LOGIN_SOLUTIONS,
        "تسجيل": GENERIC_LOGIN_SOLUTIONS,
        "باسورد": GENERIC_LOGIN_SOLUTIONS,
        
        # Video issues (English + Arabic)
        "video": GENERIC_VIDEO_SOLUTIONS,
        "playback": GENERIC_VIDEO_SOLUTIONS,
        "فيديو": GENERIC_VIDEO_SOLUTIONS,
        "تشغيل": GENERIC_VIDEO_SOLUTIONS,
        "شاشة": GENERIC_VIDEO_SOLUTIONS,  # For "شاشة سودا"
    }

    @staticmethod
    def get_generic_solution(problem_description: str, lang: str = "ar") -> Optional[str]:
        """Matches problem description to a generic solution block."""
        desc_lower = problem_description.lower()
        
        # Try specific solutions first (video, login, etc.)
        for key, solutions in FallbackSolutions.SOLUTIONS_MAP.items():
            if key in desc_lower:
                return solutions.get(lang, solutions["ar"])
        
        # 🆕 UNIVERSAL FALLBACK: For any technical problem
        # If no specific match but it's clearly a technical issue, provide general browser fixes
        tech_indicators = ["مشكلة", "مش شغال", "بايظ", "معطل", "error", "problem", "issue", "broken", "not working"]
        if any(indicator in desc_lower for indicator in tech_indicators):
            print(f"--- [UNIVERSAL FALLBACK] No specific match, using general browser solutions")
            return GENERIC_BROWSER_SOLUTIONS.get(lang, GENERIC_BROWSER_SOLUTIONS["ar"])
        
        return None
