# --- 🗄️ ZEDNY TECHNICAL SOLUTIONS DATABASE ---
# Each solution has a unique ID for anti-loop exclusion logic
# Used by RagService.search_local_solutions() for Hybrid Approach

from typing import List, Dict, Any

# --- 🔄 SYNONYM EXPANSION FOR BETTER MATCHING ---
VIDEO_SYNONYMS = {
    # Note: Removed 'مش ظاهر' - too generic, causes false matches with certificates
    "black_screen": ["شاشة سوداء", "black screen", "فاضي", "ضلمة", "blank", "سودا", "dark", "الفيديو اسود"],
    "buffering": ["buffering", "بيحمل", "بطيء", "بيقطع", "تقطيع", "slow", "loading", "بيلود", "بيثقل"],
    "freezing": ["freezing", "بيهنج", "واقف", "بيعلق", "frozen", "stuck", "مش بيتحرك", "hanging"],
    "not_playing": ["الفيديو مش شغال", "video not working", "مش بيشتغل", "لا يعمل", "no video"]
}

AUDIO_SYNONYMS = {
    "no_sound": ["مفيش صوت", "no sound", "no audio", "صوت", "ميوت", "mute", "مش سامع"],
    "sync_issue": ["متأخر", "مش متزامن", "out of sync", "sync", "الصوت متأخر"]
}

LOGIN_SYNONYMS = {
    "cant_login": ["مش قادر أدخل", "مش بيدخلني", "login", "تسجيل دخول", "أسجل دخول", "can't sign in", "access denied", "مش بيسجل", "مش قادر أسجل", "دخول", "دخول المنصة"],
    "password": ["باسورد", "password", "نسيت", "forgot", "reset"]
}

CERTIFICATE_SYNONYMS = {
    "not_appearing": ["شهادة", "certificate", "مش ظاهرة", "not showing", "فين الشهادة", "الشهادة اختفت"],
    "download": ["تحميل الشهادة", "download certificate", "مش بتنزل"]
}

APP_SYNONYMS = {
    "crash": ["بيقفل", "بيطير", "بينط", "crash", "بيوقع", "crashes", "force close"],
    "slow": ["بطيء", "بيثقل", "slow", "ماشي ببلاش", "lag", "laggy"]
}

# --- 🗣️ EGYPTIAN SLANG NORMALIZATION ---
EGYPTIAN_SLANG_MAP = {
    # App issues
    "بيطير": ["بيقفل", "crash"],
    "بينط": ["بيقفل", "crash"],
    "بيفصل": ["timeout", "disconnect"],
    
    # Speed issues  
    "بيثقل": ["بطيء", "slow"],
    "ماشي ببلاش": ["بطيء", "slow"],
    
    # General issues
    "بايظ": ["مش شغال", "broken"],
    "معطل": ["مش شغال", "broken"],
    "مش راضي يشتغل": ["مش شغال"],
    
    # Login issues
    "مش بيدخلني": ["login", "مش قادر أدخل"],
    "السايت": ["الموقع", "website"],
    
    # Video issues
    "بيهنج": ["freezing", "واقف"],
    "بيعلق": ["freezing", "واقف"]
}

def normalize_egyptian_slang(text: str) -> str:
    """Convert Egyptian slang to standard keywords for better matching"""
    normalized = text.lower()
    for slang, standards in EGYPTIAN_SLANG_MAP.items():
        if slang in normalized:
            normalized += " " + " ".join(standards)
    return normalized

def expand_with_synonyms(text: str) -> str:
    """Expand text with synonyms for better matching coverage"""
    expanded = text.lower()
    
    all_synonyms = {**VIDEO_SYNONYMS, **AUDIO_SYNONYMS, **LOGIN_SYNONYMS, **APP_SYNONYMS, **CERTIFICATE_SYNONYMS}
    
    for category, synonyms in all_synonyms.items():
        for syn in synonyms:
            if syn.lower() in expanded:
                # Add all synonyms from this group
                for s in synonyms:
                    if s.lower() not in expanded:
                        expanded += f" {s.lower()}"
                break
    
    return expanded

SOLUTIONS_DB: List[Dict[str, Any]] = [
    # =============================================
    # 📺 VIDEO PLAYBACK ISSUES
    # =============================================
    {
        "solution_id": "vid_black_001",
        "category": "VIDEO",
        "symptom_keywords": ["شاشة سوداء", "black screen", "مش ظاهر", "بدون كونترولز", "الفيديو مش شغال", "video not working"],
        "priority": 1,
        "solution_ar": "**الحل:** جرب الخطوات دي:\n1. اعمل **Hard Refresh** بالضغط على `Ctrl+Shift+R`\n2. روح على `chrome://components` وابحث عن **Widevine** واضغط 'Check for update'\n3. امسح الـ **Site Data** من `chrome://settings/content/all`"
    },
    {
        "solution_id": "vid_black_002",
        "category": "VIDEO",
        "symptom_keywords": ["شاشة سوداء", "black screen", "كونترولز شغالة"],
        "priority": 2,
        "solution_ar": "**الحل:** المشكلة ممكن تكون في الـ Codec:\n1. اضغط **كليك يمين** على الفيديو → **Stats for nerds** → شوف نوع الـ Codec\n2. جرب تخفض الـ **Quality** لـ 480p\n3. لو مافيش تحسن، جرب الفيديو من **متصفح تاني**"
    },
    {
        "solution_id": "vid_buffer_001",
        "category": "VIDEO",
        "symptom_keywords": ["buffering", "بيحمل", "بطيء", "بيقطع", "تقطيع", "الفيديو بطيء"],
        "priority": 1,
        "solution_ar": "**الحل:** جرب الخطوات دي:\n1. خفض الـ **Quality** يدوياً لـ 480p\n2. امسح الـ **Cache** بتاع المتصفح\n3. جرب في **Incognito Window** (عشان نستبعد الـ Extensions)"
    },
    {
        "solution_id": "vid_buffer_002",
        "category": "VIDEO",
        "symptom_keywords": ["buffering", "بطيء", "بيقطع", "نت سريع", "النت كويس"],
        "priority": 2,
        "solution_ar": "**الحل:** لو النت سريع والمشكلة مستمرة:\n1. جرب على **Mobile Data** بدل الـ WiFi\n2. غير الـ **DNS** لـ `8.8.8.8`\n3. لو في VPN شغال، **اقفله**"
    },
    {
        "solution_id": "vid_freeze_001",
        "category": "VIDEO",
        "symptom_keywords": ["freezing", "بيهنج", "واقف", "مش بيتحرك", "frozen"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الفيديو بيهنج:\n1. اقفل الـ **Tabs التانية** (الذاكرة ممكن تكون ممتلئة)\n2. امسح **Cache** بتاع المتصفح\n3. جرب في **متصفح تاني** أو **تطبيق الموبايل**"
    },
    # =============================================
    # 🔊 AUDIO ISSUES
    # =============================================
    {
        "solution_id": "audio_001",
        "category": "AUDIO",
        "symptom_keywords": ["صوت", "sound", "ميوت", "no audio", "مفيش صوت", "الصوت مش شغال"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اتأكد إن الـ **Tab** مش عليه علامة Mute (🔇)\n2. اضغط **كليك يمين** على الـ Tab → **Unmute site**\n3. شيك على **System Volume Mixer** وتأكد إن المتصفح مش ميوت"
    },
    {
        "solution_id": "audio_002",
        "category": "AUDIO",
        "symptom_keywords": ["صوت", "sound", "كل المتصفحات", "all browsers", "برضو مفيش صوت"],
        "priority": 2,
        "solution_ar": "**الحل:** لو المشكلة في كل المتصفحات:\n1. جرب **YouTube** - لو الصوت شغال يبقى المشكلة من المنصة\n2. حدث **Audio Drivers** من Device Manager\n3. جرب تغير **Audio Output Device**"
    },
    {
        "solution_id": "audio_sync_001",
        "category": "AUDIO",
        "symptom_keywords": ["sync", "متأخر", "مش متزامن", "out of sync", "الصوت متأخر"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الصوت مش متزامن مع الفيديو:\n1. اعمل **Refresh** للصفحة\n2. جرب **متصفح تاني**\n3. لو المشكلة مستمرة، بلغنا بـ ID الفيديو"
    },
    # =============================================
    # 🔐 LOGIN & ACCOUNT ISSUES
    # =============================================
    {
        "solution_id": "login_001",
        "category": "LOGIN",
        "symptom_keywords": ["تسجيل دخول", "login", "مش قادر أدخل", "wrong password", "باسورد", "مش بيدخل"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اتأكد إن **Caps Lock** مش مفعل\n2. امسح **Cookies** بتاعة الموقع\n3. جرب في **متصفح تاني** أو **Incognito**",
        "solution_en": "**Solution:**\n1. Ensure **Caps Lock** is off.\n2. Clear the site's **Cookies**.\n3. Try in **another browser** or an **Incognito Window**."
    },
    {
        "solution_id": "login_002",
        "category": "LOGIN",
        "symptom_keywords": ["تسجيل دخول", "login", "نسيت", "password reset", "نسيت الباسورد"],
        "priority": 2,
        "solution_ar": "**الحل:** لو نسيت الباسورد:\n1. اضغط على **نسيت كلمة السر**\n2. شيك على **Spam/Junk** في الإيميل\n3. الرابط صالح لـ **ساعة واحدة** بس"
    },
    {
        "solution_id": "login_locked_001",
        "category": "LOGIN",
        "symptom_keywords": ["locked", "محظور", "blocked", "account locked", "الحساب متقفل"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الحساب اتقفل:\n1. استنى **30 دقيقة** وجرب تاني\n2. لو المشكلة مستمرة، تواصل مع الدعم لفك الحظر"
    },
    # =============================================
    # 📚 COURSE ACCESS ISSUES
    # =============================================
    {
        "solution_id": "course_001",
        "category": "COURSE",
        "symptom_keywords": ["كورس", "course", "مش بيفتح", "شاشة بيضا", "مش ظاهر", "الكورس مش شغال"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اعمل **Refresh** للصفحة\n2. امسح **Cache** بتاع المتصفح\n3. جرب في **متصفح تاني**"
    },
    {
        "solution_id": "course_002",
        "category": "COURSE",
        "symptom_keywords": ["كورس", "course", "progress", "تقدم", "مش بيحفظ", "التقدم مش بيتسجل"],
        "priority": 2,
        "solution_ar": "**الحل:** لو الـ Progress مش بيتحفظ:\n1. اتأكد إن **Cookies مفعلة**\n2. استنى لحد ما يظهر **'Saved'** قبل ما تقفل الصفحة\n3. لو المشكلة مستمرة، جرب من **تطبيق الموبايل**"
    },
    {
        "solution_id": "course_missing_001",
        "category": "COURSE",
        "symptom_keywords": ["مش لاقي", "missing", "اختفى", "الكورس اختفى", "مش موجود"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الكورس اختفى:\n1. تأكد إن **الاشتراك** لسه ساري\n2. روح على **My Courses** وابحث بالاسم\n3. لو المشكلة مستمرة، تواصل مع الدعم"
    },
    # =============================================
    # 📝 QUIZ & ASSESSMENT ISSUES
    # =============================================
    {
        "solution_id": "quiz_001",
        "category": "QUIZ",
        "symptom_keywords": ["quiz", "اختبار", "مش بيحفظ", "الإجابات", "answers not saving"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اقفل **Autofill** في المتصفح\n2. اتأكد إن **الاتصال** مستقر\n3. متقفلش الصفحة قبل ما تظهر رسالة **Saved**"
    },
    {
        "solution_id": "quiz_submit_001",
        "category": "QUIZ",
        "symptom_keywords": ["submit", "مش بيتبعت", "can't submit", "مش قادر أسلم"],
        "priority": 1,
        "solution_ar": "**الحل:** لو مش قادر تسلم:\n1. اتأكد إن كل الأسئلة **مجاوبة**\n2. اعمل **Scroll للآخر** (ممكن في سؤال مش ظاهر)\n3. جرب في **متصفح تاني**"
    },
    # =============================================
    # 🏆 CERTIFICATE ISSUES
    # =============================================
    {
        "solution_id": "cert_001",
        "category": "CERTIFICATE",
        "symptom_keywords": ["شهادة", "certificate", "مش ظاهرة", "not generated", "فين الشهادة"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اتأكد إنك خلصت **100%** من الكورس\n2. استنى **24-48 ساعة** للتوليد\n3. روح على **My Certificates** في البروفايل"
    },
    {
        "solution_id": "cert_download_001",
        "category": "CERTIFICATE",
        "symptom_keywords": ["download", "تحميل", "مش بتنزل", "can't download"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الشهادة مش بتنزل:\n1. جرب **متصفح تاني**\n2. اقفل **Popup Blocker**\n3. اضغط **كليك يمين** → **Save As**"
    },
    # =============================================
    # 💳 PAYMENT ISSUES
    # =============================================
    {
        "solution_id": "payment_001",
        "category": "PAYMENT",
        "symptom_keywords": ["payment", "دفع", "فشل", "failed", "الكارت مش شغال"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. جرب **كارت تاني**\n2. اتأكد إن **3D Secure** مفعل\n3. تواصل مع البنك لو في **حد للمعاملات**"
    },
    {
        "solution_id": "payment_double_001",
        "category": "PAYMENT",
        "symptom_keywords": ["double", "مرتين", "اتخصم", "charged twice"],
        "priority": 1,
        "solution_ar": "**الحل:** لو اتخصم مرتين:\n1. خد **Screenshot** للمعاملتين\n2. تواصل مع الدعم فوراً\n3. هنراجع ونرجعلك الفلوس خلال **5-7 أيام**"
    },
    # =============================================
    # 📱 MOBILE APP ISSUES
    # =============================================
    {
        "solution_id": "app_crash_001",
        "category": "MOBILE",
        "symptom_keywords": ["app", "تطبيق", "crash", "بيقفل", "التطبيق مش شغال"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. **حدث** التطبيق لآخر نسخة\n2. امسح **Cache** بتاع التطبيق\n3. لو المشكلة مستمرة، **احذف** وثبت التطبيق من جديد"
    },
    {
        "solution_id": "app_download_001",
        "category": "MOBILE",
        "symptom_keywords": ["download", "تحميل", "offline", "مش بينزل", "الفيديو مش بينزل"],
        "priority": 1,
        "solution_ar": "**الحل:** لو الفيديو مش بينزل:\n1. تأكد إن في **مساحة كافية**\n2. استخدم **WiFi** للتحميل\n3. لو المشكلة مستمرة، جرب من **الموقع**"
    },
    # =============================================
    # 🏢 ENTERPRISE / B2B ISSUES
    # =============================================
    {
        "solution_id": "sso_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["sso", "saml", "oidc", "شركة", "corporate", "ايميل الشركة", "single sign on"],
        "priority": 1,
        "solution_ar": "**الحل (Enterprise SSO):**\n1. اتأكد إن **Token** بتاع الـ Identity Provider مش expired\n2. تحقق من **Whitelisted Callback URLs** في الـ IdP\n3. امسح **Cookies** وجرب تاني"
    },
    {
        "solution_id": "scorm_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["scorm", "lms", "completion", "99%", "مش بيكمل", "tracking"],
        "priority": 1,
        "solution_ar": "**الحل (SCORM/LMS):**\n1. المتصفح ممكن يكون بيمنع `LMSFinish()` → **Allow popups** للموقع\n2. اتأكد إن الـ Tab **مش في الـ Background** (بيعمل timeout)\n3. لو Safari → **Disable 'Prevent Cross-Site Tracking'**"
    },
    {
        "solution_id": "firewall_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["firewall", "blocked", "محظور", "شبكة الشركة", "corporate network"],
        "priority": 1,
        "solution_ar": "**الحل (Firewall/Network):**\n1. اطلب من IT إضافة `*.zedny.ai` للـ **Whitelist**\n2. افتح Ports: **443** (HTTPS) و **80** (HTTP)\n3. لو في **VPN**، جرب اقفله"
    },
    # =============================================
    # 🌐 NETWORK / CONNECTIVITY ISSUES
    # =============================================
    {
        "solution_id": "network_slow_001",
        "category": "NETWORK",
        "symptom_keywords": ["slow", "بطيء", "loading", "بيحمل ببطء"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. اختبر السرعة على **speedtest.net** (محتاج 5+ Mbps للـ HD)\n2. جرب **Mobile Data** بدل WiFi\n3. غير الـ **DNS** لـ `8.8.8.8` أو `1.1.1.1`"
    },
    {
        "solution_id": "network_error_001",
        "category": "NETWORK",
        "symptom_keywords": ["error", "خطأ", "404", "timeout", "connection"],
        "priority": 1,
        "solution_ar": "**الحل:**\n1. امسح **Cache** بتاع المتصفح\n2. جرب في **Incognito**\n3. لو المشكلة مستمرة، ممكن يكون في صيانة - تابعنا على **Social Media**",
        "solution_en": "**Solution:**\n1. Clear your browser's **Cache**.\n2. Try in an **Incognito Window**.\n3. If it persists, there might be maintenance - follow our status on Social Media."
    },
    
    # =============================================
    # 🏢 B2B ENTERPRISE ISSUES
    # =============================================
    {
        "solution_id": "sso_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["sso", "single sign-on", "corporate login", "تسجيل موحد", "شركة", "corporate", "employees", "موظفين", "enterprise"],
        "priority": 1,
        "solution_ar": "**مشكلة SSO - حل فوري:**\n1. تأكد إن الـ **IT department** فتح الـ domains دي: `*.zedny.ai`, `auth.zedny.ai`\n2. جرب **Clear Cache** + Restart Browser\n3. لو في **VPN**، جربه بدونه\n4. اتواصل مع: **info@zedny.ai** واذكر اسم الشركة",
        "solution_en": "**SSO Issue - Quick Fix:**\n1. Ensure **IT department** whitelisted: `*.zedny.ai`, `auth.zedny.ai`\n2. Try **Clear Cache** + Restart Browser\n3. If using **VPN**, try without it\n4. Contact: **info@zedny.ai** with company name"
    },
    {
        "solution_id": "scorm_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["scorm", "tracking", "progress", "99%", "stuck", "completion", "تتبع", "تقدم", "واقف", "مش بيتحرك"],
        "priority": 1,
        "solution_ar": "**مشكلة SCORM Tracking:**\n1. اطلب من الموظف يعمل **Complete** للـ course مرة تانية\n2. جرب **Clear LMS Cache** من admin panel\n3. لو المشكلة مستمرة لأكتر من موظف:\n📧 **info@zedny.ai**\n📋 اذكر: اسم الشركة + عدد الموظفين المتأثرين",
        "solution_en": "**SCORM Tracking Issue:**\n1. Ask employee to **Complete** the course again\n2. Try **Clear LMS Cache** from admin panel\n3. If affecting multiple employees:\n📧 **info@zedny.ai**\n📋 Include: Company name + Number of affected employees"
    },
    {
        "solution_id": "firewall_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["firewall", "blocked", "جدار حماية", "مبلوك", "corporate", "office", "شركة", "الأوفيس", "شبكة داخلية"],
        "priority": 1,
        "solution_ar": "**Firewall بيبلوك المنصة:**\n**اطلب من IT department يفتح:**\n- Domains: `*.zedny.ai`, `cdn.zedny.ai`, `api.zedny.ai`\n- Ports: `443 (HTTPS)`, `80 (HTTP)`\n- IP Ranges: نتواصل ونبعتهالك على **info@zedny.ai**",
        "solution_en": "**Corporate Firewall Blocking:**\n**Ask IT department to whitelist:**\n- Domains: `*.zedny.ai`, `cdn.zedny.ai`, `api.zedny.ai`\n- Ports: `443 (HTTPS)`, `80 (HTTP)`\n- IP Ranges: Contact **info@zedny.ai** for details"
    },
    {
        "solution_id": "lms_integration_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["lms", "integration", "sync", "not syncing", "متزامن", "تكامل", "successfactors", "cornerstone", "workday"],
        "priority": 1,
        "solution_ar": "**مشكلة تكامل LMS:**\nده محتاج مراجعة من الفريق التقني.\n📧 تواصل مع: **info@zedny.ai**\n📋 اذكر: \n- اسم الـ LMS (SAP, Cornerstone, etc.)\n- نوع المشكلة (Progress, Users, Courses)\n- آخر مرة اشتغل صح",
        "solution_en": "**LMS Integration Issue:**\nThis requires technical team review.\n📧 Contact: **info@zedny.ai**\n📋 Include:\n- LMS name (SAP, Cornerstone, etc.)\n- Issue type (Progress, Users, Courses)\n- Last time it worked correctly"
    },
    {
        "solution_id": "bulk_cert_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["bulk", "500", "multiple", "employees", "certificates", "جماعي", "موظفين كتير", "شهادات"],
        "priority": 1,
        "solution_ar": "**طلب Bulk Certificates:**\n1. روح على **Admin Panel** → **Bulk Actions**\n2. اختار الموظفين → **Generate Certificates**\n3. لو أكتر من 100 موظف، تواصل مع:\n📧 **enterprise@zedny.ai**\nهنعملهالك manual ونبعتها خلال 24 ساعة",
        "solution_en": "**Bulk Certificate Request:**\n1. Go to **Admin Panel** → **Bulk Actions**\n2. Select employees → **Generate Certificates**\n3. For 100+ employees, contact:\n📧 **enterprise@zedny.ai**\nWe'll process manually within 24 hours"
    },
    {
        "solution_id": "multiregion_001",
        "category": "ENTERPRISE",
        "symptom_keywords": ["regions", "countries", "time zones", "دول", "مناطق", "فروع", "branches", "international"],
        "priority": 1,
        "solution_ar": "**إعدادات Multi-Region:**\n1. من **Admin Panel** → **Settings** → **Time Zones**\n2. فعّل **Auto-detect** أو اختار Time zone لكل فرع\n3. للإعدادات المتقدمة:\n📧 **enterprise@zedny.ai**\n📋 اذكر: أسماء الفروع + Time zones بتاعتها",
        "solution_en": "**Multi-Region Setup:**\n1. Go to **Admin Panel** → **Settings** → **Time Zones**\n2. Enable **Auto-detect** or set timezone per branch\n3. For advanced configuration:\n📧 **enterprise@zedny.ai**\n📋 Include: Branch names + their time zones"
    },
    # =============================================
    # 🔧 UNIVERSAL FALLBACK
    # =============================================
    {
        "solution_id": "universal_001",
        "category": "UNIVERSAL",
        "symptom_keywords": ["مشكلة", "problem", "issue", "مش شغال", "not working"],
        "priority": 99,  # Low priority - only used if nothing else matches
        "solution_ar": "**الحل العام:**\n1. جرب في **Incognito Window**\n2. جرب على **Mobile Data** بدل WiFi\n3. لو على الموقع، جرب **التطبيق** والعكس",
        "solution_en": "**Universal Solution:**\n1. Try in an **Incognito Window**.\n2. Switch to **Mobile Data** instead of WiFi.\n3. If using the website, try the **App** and vice versa."
    }
]


def get_solutions_count() -> int:
    """Returns total number of solutions in database."""
    return len(SOLUTIONS_DB)


def get_solutions_by_category(category: str) -> List[Dict[str, Any]]:
    """Returns all solutions for a specific category."""
    return [s for s in SOLUTIONS_DB if s["category"] == category]
