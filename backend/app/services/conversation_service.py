import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from app.services.ai_service import AIService
from app.models.schemas import DeviceInfo

logger = logging.getLogger("Zedny.ConversationService")


class UserIntent(str, Enum):
    """User intent categories"""
    GREETING = "GREETING"
    INFO = "INFO"
    ISSUE = "ISSUE"
    SALES = "SALES"
    COMPLAINT = "COMPLAINT"
    OFF_TOPIC = "OFF_TOPIC"
    CATEGORY = "CATEGORY"  # Generic fallback


class ConversationMemory:
    """Smart conversation memory to track questions and answers."""
    
    @staticmethod
    def extract_qa_pairs(history: List[str]) -> List[Dict[str, str]]:
        """Extracts bot questions and user answers from conversation history."""
        qa_pairs = []
        # Look for pairs in order
        for i in range(len(history) - 1):
            if history[i].startswith("AI:") and history[i+1].startswith("User:"):
                bot_msg = history[i].replace("AI:", "").strip()
                user_msg = history[i+1].replace("User:", "").strip()
                
                # Check if the bot message was a question
                if "?" in bot_msg or any(q in bot_msg for q in ["هل", "كيف", "فين", "متى"]):
                    qa_pairs.append({
                        "question": bot_msg,
                        "answer": user_msg
                    })
        return qa_pairs

    @staticmethod
    def format_qa_context(qa_pairs: List[Dict[str, str]], lang: str = "ar") -> str:
        """Formats QA pairs into a readable block for the LLM prompt."""
        if not qa_pairs:
            return "No previous diagnostics." if lang == "en" else "لا توجد معلومات سابقة."
            
        header = "**What I already know from the user:**\n" if lang == "en" else "**المعلومات التي قدمها المستخدم سابقاً:**\n"
        context = header
        for i, qa in enumerate(qa_pairs, 1):
            q_label = "Q" if lang == "en" else "س"
            a_label = "A" if lang == "en" else "ج"
            context += f"{i}. {q_label}: {qa['question']}\n   {a_label}: {qa['answer']}\n"
        return context


class FirstMessageGuard:
    """
    🛡️ FIRST MESSAGE PROTECTION SYSTEM
    
    Professional implementation based on industry best practices for Arabic chatbots.
    Prevents the common false-positive where first messages are incorrectly classified
    as technical issues when they're actually informational queries or greetings.
    
    Key Features:
    - Weight-based scoring system
    - Pattern matching for Arabic and English
    - Confidence threshold handling
    - Semantic analysis for ambiguous cases
    """
    
    # ==========================================
    # CONFIGURATION: Weights and Patterns
    # ==========================================
    
    # Intent weights for first messages (lower = less likely)
    FIRST_MESSAGE_WEIGHTS = {
        "GREETING": 1.5,      # Boost greetings
        "INFO": 1.3,          # Boost info requests
        "SALES": 1.2,         # Boost sales inquiries
        "ISSUE": 1.2,         # Restore technical issue priority
        "OFF_TOPIC": 0.8
    }
    
    # Definitive patterns that ALWAYS indicate specific intents
    DEFINITIVE_PATTERNS = {
        "GREETING": {
            "ar": ["السلام عليكم", "صباح الخير", "مساء الخير", "أهلاً وسهلاً", "مرحباً بك"],
            "en": ["hello there", "good morning", "good evening", "hi there", "hey there"]
        },
        "INFO": {
            "ar": ["ما هي", "ما هو", "كيف يمكن", "متى", "أين", "عرفني", "اشرحلي", "فهمني"],
            "en": ["what is", "what are", "how to", "how do", "when is", "where is", "tell me about", "explain"]
        },
        "SALES": {
            "ar": ["كم سعر", "أسعار", "اشتراك", "باقة", "عرض", "خصم", "تكلفة"],
            "en": ["how much", "price", "pricing", "cost", "subscribe", "package", "discount", "trial"]
        },
        "ISSUE": {
            "ar": ["مش شغال", "مش راضي", "بيطلعلي error", "الشاشة سودا", "مش عارف أدخل", "نسيت الباسورد", "تسجيل الدخول", "مش عارف أسجل", "مش بيفتح"],
            "en": ["not working", "doesn't work", "error message", "can't login", "black screen", "forgot password", "login problem"]
        }
    }
    
    # Short generic patterns (need context to classify)
    AMBIGUOUS_PATTERNS = {
        "ar": ["مشكلة", "مساعدة", "عندي", "محتاج", "بايظ"],
        "en": ["problem", "help", "issue", "broken", "stuck"]
    }
    
    # Identity questions (ALWAYS INFO)
    IDENTITY_PATTERNS = {
        "ar": ["مين زدني", "مين انت", "ايه زدني", "انت مين", "بتعملوا ايه"],
        "en": ["who is zedny", "who are you", "what is zedny", "what do you do"]
    }
    
    @classmethod
    def protect_first_message(cls, text: str, detected_lang: str = "ar") -> Dict[str, Any]:
        """
        🛡️ Main protection method for first messages.
        """
        from app.utils.arabic_helper import normalize_arabic
        
        # 🛡️ CORE FIX: Normalize user input AND define normalized patterns for 100% match
        text_norm = normalize_arabic(text).lower().strip()
        word_count = len(text.split())
        
        # ==========================================
        # RULE 1: Identity Questions → ALWAYS INFO
        # ==========================================
        for lang_patterns in cls.IDENTITY_PATTERNS.values():
            for pattern in lang_patterns:
                if normalize_arabic(pattern).lower() in text_norm:
                    return {
                        "intent": "INFO",
                        "confidence": 0.95,
                        "override": True,
                        "reason": f"Identity question detected: '{pattern}'"
                    }
        
        # ==========================================
        # RULE 2: Definitive Patterns → High Confidence
        # ==========================================
        for intent, lang_patterns in cls.DEFINITIVE_PATTERNS.items():
            for lang, patterns in lang_patterns.items():
                for pattern in patterns:
                    if normalize_arabic(pattern).lower() in text_norm:
                        return {
                            "intent": intent,
                            "confidence": 0.9,
                            "override": True,
                            "reason": f"Definitive pattern matched: '{pattern}' → {intent}"
                        }
        
        # ==========================================
        # RULE 3: Short Messages with Ambiguous Words
        # ==========================================
        if word_count <= 6:
            # Check for ambiguous patterns
            has_ambiguous = False
            for lang, patterns in cls.AMBIGUOUS_PATTERNS.items():
                if any(normalize_arabic(p).lower() in text_norm for p in patterns):
                    has_ambiguous = True
                    break
            
            if has_ambiguous:
                return {
                    "intent": "ISSUE" if any(normalize_arabic(p).lower() in text_norm for p in ["مشكلة", "issue", "problem"]) else "INFO",
                    "confidence": 0.7,
                    "override": True,
                    "reason": f"Short message ({word_count} words) - handling as semantic intent"
                }
        
        # ==========================================
        # RULE 4: Social Greetings → GREETING
        # ==========================================
        # Boost social greetings specifically to avoid fallback to INFO
        social_greetings_ar = ["اهلا", "صباح", "مساء", "سلام", "مرحبا", "هاي", "التحية"]
        social_greetings_en = ["hi", "hello", "hey", "greeting", "morning", "evening"]
        
        if any(normalize_arabic(g).lower() in text_norm for g in social_greetings_ar) or \
           any(g in text_norm for g in social_greetings_en):
            return {
                "intent": "GREETING",
                "confidence": 0.95,
                "override": True,
                "reason": "Social greeting normalized match"
            }
            
        # ==========================================
        # RULE 5: Question Starters → INFO
        # ==========================================
        question_starters_ar = ["ما ", "كيف ", "متى ", "أين ", "هل ", "ليه ", "ايه "]
        question_starters_en = ["what ", "how ", "when ", "where ", "why ", "is ", "can "]
        
        for starter in [normalize_arabic(s) for s in question_starters_ar] + question_starters_en:
            if text_norm.startswith(starter):
                return {
                    "intent": "INFO",
                    "confidence": 0.85,
                    "override": True,
                    "reason": f"Question starter detected: '{starter.strip()}'"
                }
        
        # ==========================================
        # RULE 6: Empty/Very Short Fallback → Decided by LLM
        # ==========================================
        # We REMOVED the aggressive INFO default for 3-word messages.
        # This prevents "أهلا صباح الخير" from becoming "Who is Zedny?".
        
        return {
            "intent": None,
            "confidence": 0.0,
            "override": False,
            "reason": "No first-message protection needed - using LLM classification"
        }
    
    @classmethod
    def adjust_confidence(cls, llm_intent: str, llm_confidence: float, is_first_message: bool) -> Tuple[str, float]:
        """
        Adjusts the LLM's confidence based on first-message weights.
        
        Args:
            llm_intent: The intent returned by the LLM
            llm_confidence: The confidence score from LLM (0.0 - 1.0)
            is_first_message: Whether this is the first message in the session
        
        Returns:
            Tuple of (adjusted_intent, adjusted_confidence)
        """
        if not is_first_message:
            return llm_intent, llm_confidence
        
        weight = cls.FIRST_MESSAGE_WEIGHTS.get(llm_intent, 1.0)
        adjusted_confidence = min(llm_confidence * weight, 1.0)
        
        # If ISSUE confidence drops below threshold, switch to INFO
        if llm_intent == "ISSUE" and adjusted_confidence < 0.5:
            return "INFO", 0.6
        
        return llm_intent, adjusted_confidence


class DeviceType(str, Enum):
    """Supported device types"""
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    MOBILE = "mobile"
    TABLET = "tablet"


class Browser(str, Enum):
    """Supported browsers"""
    CHROME = "chrome"
    SAFARI = "safari"
    FIREFOX = "firefox"
    EDGE = "edge"


class ConversationService:
    """
    Service for handling conversation logic with unified strategic processing.
    Combines intent detection, entity tracking, and RAG optimization in single AI calls.
    """
    
    # Security constants
    MAX_INPUT_LENGTH = 5000
    MAX_HISTORY_ITEMS = 8
    
    # Device detection patterns for fallback
    DEVICE_PATTERNS = {
        DeviceType.LAPTOP: ["laptop", "labtob", "lap", "لابتوب", "لاب"],
        DeviceType.MOBILE: ["mobile", "mob", "phone", "موبايل", "هاتف", "iphone", "android"],
        DeviceType.DESKTOP: ["desktop", "pc", "computer", "كمبيوتر", "ديسك", "مكتب"],
        DeviceType.TABLET: ["tablet", "تابلت", "ipad"]
    }
    
    BROWSER_PATTERNS = {
        Browser.CHROME: ["chrome", "كروم"],
        Browser.SAFARI: ["safari", "سفاري"],
        Browser.FIREFOX: ["firefox", "فايرفوكس"],
        Browser.EDGE: ["edge", "ايدج"]
    }

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Comprehensive input sanitization to prevent injection attacks.
        """
        if not text:
            return ""
        
        # Length limit for security
        text = text[:ConversationService.MAX_INPUT_LENGTH]
        
        # Remove prompt injection patterns
        dangerous_patterns = [
            '"""', "'''", "```", 
            "system:", "assistant:", "user:",
            "<|", "|>", "[INST]", "[/INST]"
        ]
        for pattern in dangerous_patterns:
            text = text.replace(pattern, "")
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()

    @staticmethod
    def safe_json_extract(text: str) -> Optional[Dict[str, Any]]:
        """
        Robustly extract JSON from AI response with multiple fallback strategies.
        """
        if not text:
            return None
            
        try:
            # Match any block that looks like JSON { ... }
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, text, re.DOTALL)
            
            if match:
                clean_json = match.group(0)
                # Remove markdown artifacts
                clean_json = clean_json.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
                
        except Exception as e:
            logger.error(f"JSON extraction failed: {e} | Text preview: {text[:200]}")
        
        return None

    @staticmethod
    def needs_device_info(
        device_info: DeviceInfo, 
        intent: str, 
        is_media_issue: bool = False, 
        solutions_tried_count: int = 0
    ) -> bool:
        """
        Smart decision logic for requesting device info.
        Business Rule: Device info is LOW-VALUE metadata.
        """
        if device_info.is_collected or device_info.device_type:
            return False
        
        if intent != UserIntent.ISSUE.value:
            return False
        
        # Request only if first solution failed OR it's a media issue
        return is_media_issue or solutions_tried_count > 0

    @staticmethod
    def generate_device_question(lang: str = "ar") -> str:
        """Generate a soft, optional device info question."""
        questions = {
            "ar": "لو المشكلة مرتبطة بجهاز أو متصفح معين، قولي علشان أديك حل أدق (ده اختياري تماماً).",
            "en": "If the issue relates to a specific device or browser, let me know so I can provide a more accurate solution (completely optional)."
        }
        return questions.get(lang, questions["en"])

    @staticmethod
    def _fuzzy_match_device_info(user_msg: str) -> Tuple[Optional[str], Optional[str]]:
        """Fallback pattern matching for device information."""
        msg_lower = user_msg.lower()
        
        device_type = None
        for dtype, patterns in ConversationService.DEVICE_PATTERNS.items():
            if any(pattern in msg_lower for pattern in patterns):
                device_type = dtype.value
                break
        
        browser = None
        for btype, patterns in ConversationService.BROWSER_PATTERNS.items():
            if any(pattern in msg_lower for pattern in patterns):
                browser = btype.value
                break
        
        return device_type, browser

    @staticmethod
    def extract_device_info_from_response(user_msg: str) -> DeviceInfo:
        """Extract device information using AI + Fuzzy matching fallback."""
        if not user_msg:
            return DeviceInfo()
        
        safe_msg = ConversationService.sanitize_input(user_msg)
        
        # Tier 1: AI
        prompt = f"""Extract device information from this user message. 
Return JSON ONLY:
{{
  "device_type": "desktop/laptop/mobile/tablet/null",
  "browser": "chrome/safari/firefox/edge/null",
  "os": "windows/macos/linux/ios/android/null"
}}
User message: "{safe_msg}" """
        
        try:
            raw = AIService.run_llm(prompt, "Extract device info", model="gemini-1.5-flash")
            data = ConversationService.safe_json_extract(raw)
            if data:
                has_info = any([data.get("device_type"), data.get("browser"), data.get("os")])
                if has_info:
                    return DeviceInfo(
                        device_type=data.get("device_type"),
                        browser=data.get("browser"),
                        os=data.get("os"),
                        is_collected=True
                    )
        except Exception as e:
            logger.warning(f"AI device extraction failed: {e}")
        
        # Tier 2: Fuzzy
        device_type, browser = ConversationService._fuzzy_match_device_info(safe_msg)
        if device_type or browser:
            return DeviceInfo(device_type=device_type, browser=browser, is_collected=True)
            
        return DeviceInfo()

    @staticmethod
    def unified_strategic_brain(
        user_msg: str, 
        history: List[str], 
        summary: str, 
        entities: Dict[str, Any], 
        status: str
    ) -> Dict[str, Any]:
        """CONSOLIDATED AI CALL: Strategic analysis Turn."""
        sanitized_msg = ConversationService.sanitize_input(user_msg)
        
        # 🛡️ SHIELD: Check for first-message protection first
        # This catches greetings, identity questions, and definitive patterns deterministically
        protection_result = FirstMessageGuard.protect_first_message(sanitized_msg)
        if protection_result.get("override"):
            # If we have a definitive match, return early without hitting LLM
            return {
                "intent": protection_result["intent"],
                "confidence": protection_result["confidence"],
                "reasoning": protection_result["reason"],
                "is_media": False,
                "is_competitor": False,
                "optimized_query": sanitized_msg,
                "detected_language": "en" if all(ord(c) < 128 for c in sanitized_msg) else "ar"
            }

        recent_history = history[-ConversationService.MAX_HISTORY_ITEMS:]
        history_str = "\n".join(f"- {msg}" for msg in recent_history)
        
        system_prompt = f"""You are the **Zedny Semantic Intent Classifier**. 

## 🧠 YOUR CORE SKILL: SEMANTIC UNDERSTANDING
You understand MEANING, not keywords. You think like a human support agent.
You are FLUENT in Egyptian Arabic slang (عامية مصرية).

**USER MESSAGE:** "{sanitized_msg}"

**SESSION CONTEXT:**
- Current Session Status: {status}
- Conversation History:
{history_str}

---

## 🎯 SEMANTIC INTENT RULES

### ISSUE = User Has a PROBLEM or NEEDS HELP (MOST COMMON!)
**The user is experiencing ANY difficulty, frustration, confusion, or something isn't working.**

#### Standard Technical Problems:
- "نسيت الباسورد" → ISSUE (forgot password)
- "مش عارف أدخل" → ISSUE (can't log in)
- "الفيديو أسود" → ISSUE (video broken)

#### Egyptian Slang (عامية مصرية) - CRITICAL!
- "التطبيق بيطير" → ISSUE (بيطير = crashes/closes suddenly)
- "الموقع بايظ" → ISSUE (بايظ = broken)
- "الصفحة بتلف" → ISSUE (بتلف = keeps loading)
- "مش راضي يشتغل" → ISSUE (won't work)
- "بيهنج" → ISSUE (hangs/freezes)
- "بيقف" → ISSUE (stops/buffers)

#### "WHERE" Questions about user's stuff = ISSUE:
- "فين شهادتي" → ISSUE (Where's MY certificate = can't find it = problem)
- "فين الكورس بتاعي" → ISSUE (Where's my course)
- "مش لاقي حاجتي" → ISSUE (can't find my stuff)

#### Feedback on Solutions = ISSUE:
- "جربت ومشتغلش" → ISSUE (tried, didn't work)
- "لسه برضو" → ISSUE (still same)
- "مانفعش" → ISSUE (didn't help)

### GREETING = PURE Social Greeting ONLY
"أهلا", "صباح الخير", "hello" - WITH NO QUESTION OR REQUEST.
If user says "أهلا مش عارف أدخل" → ISSUE (not greeting!)

### SALES = Commercial Intent
"بكام", "أسعار", "عايز أشترك"

### INFO = Curious About Zedny (NO frustration)
"مين زدني", "إيه هي زدني", "what is zedny"
**Must have NO frustration or inability expressed.**

### OFF_TOPIC = Completely Unrelated
Weather, recipes, sports.

---

## 🔥 CRITICAL DEFAULT RULE:
**WHEN IN DOUBT → CHOOSE ISSUE**
If you're unsure, the user probably has a problem. 
NEVER default to GREETING or OFF_TOPIC if there's ANY hint of difficulty.

## PRIORITY ORDER:
1. **Any frustration/inability/error → ISSUE**
2. **WHERE questions about user's stuff → ISSUE**
3. **Egyptian slang about problems → ISSUE**
4. **Commercial/pricing → SALES**
5. **Pure curiosity about Zedny → INFO**
6. **ONLY pure greeting with NO request → GREETING**

---


## OUTPUT (JSON ONLY):
{{
  "intent": "GREETING|INFO|ISSUE|SALES|OFF_TOPIC",
  "is_competitor": true/false,
  "confidence": 1.0,
  "reasoning": "one sentence explaining the SEMANTIC meaning you understood",
  "is_media": true/false,
  "optimized_query": "search terms for RAG",
  "detected_language": "ar" or "en"
}}

Return ONLY valid JSON:"""


        try:
            raw = AIService.run_llm(system_prompt, "Strategic analysis", model="google/gemini-2.0-flash-001")
            data = ConversationService.safe_json_extract(raw)
            if data and data.get("intent"):
                return data
        except Exception as e:
            logger.error(f"Strategic brain failed: {e}")
        
        # Improved fallback: Critical intent detection for ambiguous messages
        issue_keywords = ["مشكلة", "مساعدة", "عندي مشكلة", "بايظ", "مش شغال", "مساعده", "issue", "problem", "help", "error", "can't", "broken"]
        sales_keywords = ["اشتراك", "سعر", "باقة", "عرض", "أسعار", "اسعار", "باقات", "عايز اشترك", "subscription", "price", "pricing", "plan", "offer", "cost"]
        
        if any(kw in sanitized_msg.lower() for kw in issue_keywords):
            fallback_intent = UserIntent.ISSUE.value
        elif any(kw in sanitized_msg.lower() for kw in sales_keywords):
            fallback_intent = UserIntent.SALES.value
        else:
            fallback_intent = UserIntent.INFO.value
        
        return {
            "intent": fallback_intent,
            "confidence": 0.5,
            "is_media": False,
            "is_competitor": False,
            "optimized_query": sanitized_msg,
            "detected_language": "en" if all(ord(c) < 128 for c in sanitized_msg) else "ar",
            "entities": {},
            "dont_repeat": []
        }

