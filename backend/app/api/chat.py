import json
import uuid
import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, IncidentState, EscalationReport
from app.services.supabase_service import SupabaseService
from app.services.ai_service import AIService
from app.services.rag_service import RagService
from app.services.conversation_service import ConversationService, UserIntent, ConversationMemory, FirstMessageGuard
from app.services.orchestrator_service import OrchestratorService
from app.services.fallback_solutions import FallbackSolutions
from app.core.prompts import SALES_INFO_PROMPT, SUPPORT_ENGINEER_V2_PROMPT, BRAND_LOYALTY_INSTRUCTIONS, TECH_BRAIN_PROMPT, OUTPUT_SANITIZATION_RULES
from app.core.config import USE_MULTI_AGENT
from app.utils.arabic_helper import normalize_arabic
from app.services.tech_service import TechService
from app.services.technical_orchestrator import TechnicalOrchestrator
import re
import traceback
import logging

# Set up local logging to file for 500 errors
logging.basicConfig(filename='chat_errors.log', level=logging.ERROR)

def is_pure_english(text: str) -> bool:
    """Returns True if the text contains Latin characters and NO Arabic characters."""
    has_latin = bool(re.search(r'[a-zA-Z]', text))
    has_arabic = bool(re.search(r'[\u0600-\u06FF]', text))
    return has_latin and not has_arabic

def contains_arabic(text: str) -> bool:
    """Returns True if the text contains any Arabic characters."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def clean_ai_response(text: str) -> str:
    """
    Cleans the AI response from leaked JSON or logic tags.
    Ensures end-user only sees the actual response content.
    """
    if not text:
        return ""
    
    # 1. Strip Markdown JSON blocks ONLY if they are separate from content
    # We use a safer replacement that doesn't eat the whole string if it's mixed
    text = re.sub(r'```json\s*\{[\s\S]*?\}\s*```', '', text)
    
    # 2. Specifically target the logic tags we use in prompts
    forbidden_markers = [
        r'\{"INTENT":.*\}', 
        r'\{"worked":.*\}',
        r'INTENT:.*',
        r'LENGTH_RULE:.*',
        r'### 🌍 LANGUAGE RULE:.*',
        r'COMPETITOR_MENTION:.*',
        r'نوع الاستعلام:.*',
        r'المرحلة:.*',
        r'تصنيف:.*'
    ]
    for pattern in forbidden_markers:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # 3. Final cleanup: Remove lingering backticks and leading/trailing whitespace
    text = text.replace('```', '').replace('`', '').strip()
    
    # EMERGENCY FALLBACK: If cleaning resulted in empty text but original had content,
    # return a safe portion of the original text instead of nothing.
    if not text and len(text.strip()) == 0:
        # This usually happens if the AI responded ONLY with the logic tags we filtered.
        return "أعتذر، حدث خطأ في معالجة الرد. هل يمكنك توضيح سؤالك؟" if not is_pure_english(text) else "I apologize, an error occurred while processing the response. Could you clarify your question?"

    return text

router = APIRouter()

@router.post("/rate")
async def submit_rating(payload: dict):
    # Expects: {"session_id": "...", "rating": 5, "message": "...", "history": [...], "user_email": "..."}
    try:
        session_id = payload.get("session_id")
        rating = payload.get("rating")
        message = payload.get("message", "")
        history = payload.get("history", [])
        user_email = payload.get("user_email")
        
        if session_id and rating is not None:
            SupabaseService.save_rating(
                rating=rating, 
                session_id=session_id, 
                user_email=user_email,
                message=message, 
                history=history
            )
            return {"status": "success", "message": "Rating saved to DB"}
        else:
             print("--- [RATING ERROR] Missing session_id or rating in payload")
             return {"status": "error", "message": "Missing required fields"}
    except Exception as e:
        print(f"--- [RATING EXCEPTION] {e}")
        return {"status": "error", "message": str(e)}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    user_msg = request.message
    
    # 0.5 ENSURE USER EXISTS (Data Integrity)
    # Save every user (Guest or Registered) to DB immediately
    # This ensures we capture emails/phones from the start
    if request.user_email:
        SupabaseService.ensure_user_exists(request.user_email, role="Guest")
    
    # 0. SESSION PERSISTENCE: Load existing session from DB if session_id provided
    state = None
    if request.session_id and not request.incident_state:
        # Try to load existing session from database
        loaded_state = SupabaseService.load_session(request.session_id)
        if loaded_state:
            state = loaded_state
            print(f"--- [SESSION LOADED] Restored session {request.session_id} with {len(state.history)} messages")
    
    # If no loaded state, use provided incident_state or create new
    if state is None:
        state = request.incident_state or IncidentState()
    
    # Link session to user email for long-term memory
    user_email_for_session = request.user_email  # Store for later save
    
    # 1. CRM: Fetch full user context
    user_mem = {"user_type": "Guest", "name": "Guest", "company": "Visitor", "enrolled_courses": [], "technical_profile": {}}
    if request.user_email and "@" in request.user_email:
        user_mem = SupabaseService.get_user_profile(request.user_email)
        
        # Merge real-time technical profile
        if request.technical_profile:
            user_mem["technical_profile"] = request.technical_profile
            # Save the live tech updates back to CRM metadata
            clean_mem = {k: v for k, v in user_mem.items() if k != "name"}
            SupabaseService.save_user_memory(request.user_email, clean_mem)
    elif request.technical_profile:
        # Guests also get their live device info used in the session
        user_mem["technical_profile"] = request.technical_profile

    # 2. Handle Ratings
    if request.rating is not None:
        SupabaseService.save_rating(
            rating=request.rating, 
            session_id=state.session_id, 
            user_email=request.user_email,
            message=user_msg, 
            history=state.history
        )

    # 3. Memory Architecture: Sliding Window & Summarization
    if len(state.history) > 20:
        state.summary = AIService.generate_conversation_summary(state.history, state.summary)
        state.history = state.history[-10:] 

    # ============================================================
    # 4. Intent Classification: LLM-based or Multi-Agent
    # ============================================================
    # 🧠 SEMANTIC FIRST: Let the LLM classify semantically
    # Keywords are now ONLY a safety net, not primary classification
    
    # Normalize message for logging
    normalized_msg = normalize_arabic(user_msg)
    print(f"--- [DEBUG] Normalized Message: '{normalized_msg}'")
    
    # 🛡️ SAFETY NET KEYWORDS: Only used if LLM fails
    # These are NOT for primary classification - the LLM should understand semantically
    safety_net_keywords = {
        "ISSUE": ["مشكلة", "باسورد", "password", "نسيت", "forgot", "مش شغال", "error", "help"],
        "SALES": ["سعر", "اشتراك", "بكم", "pricing", "subscription"]
    }
    
    forced_intent = None  # Proactive check below
    is_global_b2b = False
    
    # 🚨 PRE-BRAIN DETECTION FLAGS
    # Simplified keywords just for broad categorization if needed
    tech_keywords = [
        "باسورد", "password", "فيديو", "video", "شاشة", "screen",
        "شهادة", "certificate", "صوت", "بافر", "buffering"
    ]
    is_technical_content = any(k in user_msg.lower() for k in tech_keywords)
    is_feedback = False  # Now strictly determined by LLM for Tech, or multi-agent for others

    
    # 🧠 CONTEXT-AWARE TECH INTENT INTERPRETATION (LLM-Powered)
    # Only triggered if we were already in a tech diagnostic flow or high confidence tech match
    extracted_problem = None
    user_intent_type = None
    is_continuation = False
    
    if (state.category == "Tech" or is_technical_content) and len(state.history) >= 2:
        print(f"--- [LLM INTENT] Analyzing technical context for User: {user_msg[:50]}...")
        # Call LLM with deeper history (last 15 messages)
        interpretation = AIService.interpret_tech_intent(user_msg, state.history[-15:])
        
        user_intent_type = interpretation.get("intent")
        extracted_problem = interpretation.get("core_problem_extraction")
        
        if user_intent_type in ["REJECTION", "NEGATIVE_FEEDBACK", "FOLLOW_UP", "REQUEST_NEXT_SOLUTION", "ESCALATION_AGREEMENT"]:
            is_continuation = True
            # 🛑 LOCK THE DEPARTMENT: Ensure we don't fall back to general orchestration
            forced_intent = "ISSUE"
            state.category = "Tech"
            
        if user_intent_type == "REJECTION":
            is_feedback = True # Force feedback logic to override fresh search with raw message
            print(f"--- [LLM INTENT] REJECTION detected. Core problem: {extracted_problem}")
        elif user_intent_type == "NEGATIVE_FEEDBACK":
            is_feedback = True
            print(f"--- [LLM INTENT] NEGATIVE_FEEDBACK detected.")
        elif user_intent_type == "ESCALATION_AGREEMENT":
            print(f"--- [LLM INTENT] ESCALATION_AGREEMENT detected.")
        elif user_intent_type == "REQUEST_NEXT_SOLUTION":
            print(f"--- [LLM INTENT] REQUEST_NEXT_SOLUTION detected.")
        elif user_intent_type == "FOLLOW_UP":
            print(f"--- [LLM INTENT] FOLLOW_UP detected.")
            
    # If LLM says it's a continuation, skip new semantic search with raw message
    if is_continuation:
        print(f"--- [CONTEXT AWARE] LLM confirmed tech continuation ({user_intent_type}). skipping raw search.")

    
    # 4.1 PROACTIVE SALES RADAR (Global)
    try:
        is_global_b2b = AIService.detect_b2b_intent(user_msg)
        if is_global_b2b:
            print(f"--- [PROACTIVE SALES RADAR] B2B Intent Detected.")
    except Exception as b2b_err:
        print(f"--- [B2B RADAR ERROR] {b2b_err}")
        is_global_b2b = False
    
    # 4.2 PROACTIVE TECH SEMANTIC CHECK
    # Check if this is a technical issue BEFORE the brain classifies it
    # Use balanced threshold (0.6) for initial routing to improve recall
    try:
        print(f"--- [PROACTIVE TECH CHECK] Searching isolated index...")
        proactive_sol = TechService.search(user_msg, threshold=0.6)
        if proactive_sol and proactive_sol.get("score", 0) > 0.8: # Only force if highly confident
            forced_intent = "ISSUE"
            print(f"--- [PROACTIVE HIT] Found high-confidence semantic match (>0.8). Forcing ISSUE path.")
        elif is_technical_content:
            # Fallback to keyword-based force if explicit tech words found
            # But let the brain verify if it's just a general question
            print(f"--- [PROACTIVE ALERT] Keywords matched tech. Proceeding with Brain verification.")
    except Exception as tech_err:
        print(f"--- [PROACTIVE TECH ERROR] {tech_err}")


    if USE_MULTI_AGENT:
        print("--- [ORCHESTRATION] Using Multi-Agent Architecture ---")
        orch_result = await OrchestratorService.process_interaction(
            user_msg, state.history, state.summary, state.entities.dict(), state.status, user_mem
        )
        # - [x] Revert aggressive `FirstMessageGuard` overrides [2026-02-02]
        # - [x] Clean up prompt leaks ("نوع الاستعلام") [2026-02-02]
        # - [x] Restore direct diagnostic/RAG flow for technical issues [2026-02-02]
        #
        # ## Phase 11: Final Quality Reversion ⚖️ [SUCCESS]
        # - [x] Revert to single high-quality model priority (Claude 3.5 lead) [2026-02-02]
        # - [x] Remove forced Discovery/Welcome menus for direct support [2026-02-02]
        # - [x] Strip internal classification/thought headers from responses [2026-02-02]
        # - [x] Implement RAG priority override for technical stability [2026-02-02]
        # Map Orchestrator output back to our pipeline variables
        intent = orch_result["intent"]
        original_intent = intent
        is_media_issue = orch_result["is_media"]
        optimized_query = orch_result["optimized_query"]
        brain_result = orch_result # For status sync later if needed
    else:
        brain_result = ConversationService.unified_strategic_brain(
            user_msg, state.history, state.summary, state.entities.dict(), state.status
        )
        intent = brain_result.get("intent", "INFO").upper()
        # Apply Shield if triggered
        if forced_intent:
            intent = forced_intent
            
        original_intent = intent
        is_media_issue = brain_result.get("is_media", False)
        optimized_query = user_msg # 🎯 STABILITY: Uses original message for embedding to avoid AI "optimizing" away keywords
        confidence = brain_result.get("confidence", 1.0)
        detected_lang = brain_result.get("detected_language", "ar")
        is_competitor = brain_result.get("is_competitor", False)
    
    # ============================================================
    # 🛡️ Intent Processing
    # ============================================================
    # Confidence and detected_lang are now straight from the brain/orchestrator

    # If intent protection already extracted these, it's fine.
    # We maintain this for standard flows.
    if not is_competitor: 
        is_competitor = brain_result.get("is_competitor", False)
    if not detected_lang:
        detected_lang = brain_result.get("detected_language", "ar")
    
    # 🕵️‍♂️ LANGUAGE OVERRIDE (Ultra-Stable):
    # If the message contains Arabic, force 'ar' to prevent AI misclassification on first turn.
    if contains_arabic(user_msg):
        detected_lang = "ar"
        print(f"--- [LANGUAGE OVERRIDE] Forced 'ar' for Arabic query: '{user_msg}'")
    elif is_pure_english(user_msg):
        detected_lang = "en"
        print(f"--- [LANGUAGE OVERRIDE] Forced 'en' for pure Latin query: '{user_msg}'")
    
    # =============================================================================
    # 🔒 LANGUAGE LOCKING: Set on first message, use it for ALL subsequent responses
    # =============================================================================
    if not state.language:
        # First message - lock the language for this session
        state.language = detected_lang
        print(f"--- [LANGUAGE LOCKED] Session language set to: {state.language}")
    else:
        # Use the locked language, don't let it flip-flop
        detected_lang = state.language
        print(f"--- [LANGUAGE STABLE] Using locked language: {detected_lang}")
    
    # =============================================================================
    # 🔄 FOLLOW-UP & AFFIRMATION DETECTION: (DialogFlow / Lex Pattern)
    # =============================================================================
    affirmative_patterns = ["yes", "yeah", "yep", "sure", "ok", "أه", "ايوه", "تمام", "نعم", "ماشي"]
    negative_patterns = ["no", "nope", "not now", "لا", "مش دلوقتي", "لأ"]
    
    is_affirmative = False
    is_negative = False
    is_follow_up = False
    
    msg_words = user_msg.lower().split()
    if len(msg_words) <= 3:
        is_affirmative = any(p in user_msg.lower() for p in affirmative_patterns)
        is_negative = any(p in user_msg.lower() for p in negative_patterns)

    # (is_global_b2b already checked proactively at the top)
        
    # 🎯 CASE 1: Confirmation of a pending topic (e.g. ROI, Pricing)
    if state.current_phase == "awaiting_confirmation" and (is_affirmative or is_negative):
        is_follow_up = True
        if is_affirmative:
            # Continue the pending topic
            intent = UserIntent.SALES.value if "sales" in (state.pending_topic or "").lower() else UserIntent.INFO.value
            print(f"--- [AFFIRMATION] User confirmed interest in: {state.pending_topic}")
            # Inject context into query for RAG
            optimized_query = f"{state.pending_topic} details"
        else:
            # User said NO - go back to discovery
            state.current_phase = "discovery"
            state.pending_topic = None
            intent = UserIntent.GREETING.value
            print(f"--- [REJECTION] User declined topic. Resetting to discovery.")

    # 🎯 CASE 2: Technical follow-up (the "still" case)
    elif state.awaiting_clarification and len(msg_words) <= 6:
        follow_up_patterns = ["still", "لسه", "it's not working", "مش شغال", "same", "نفس المشكلة", "didn't work", "مفيش فايدة"]
        if any(p in user_msg.lower() for p in follow_up_patterns) or user_msg.isdigit():
            is_follow_up = True
            intent = UserIntent.ISSUE.value
            print(f"--- [TECH FOLLOW-UP] Detected as follow-up to {state.last_ai_question_type}")
    
    dont_repeat = brain_result.get("dont_repeat", [])
    
    # Update Category & State
    if intent == UserIntent.SALES.value:
        state.category = "Sales"
    elif intent == UserIntent.INFO.value:
        state.category = "General"
    elif intent == UserIntent.ISSUE.value:
        state.category = "Tech"
    
    # 🔒 STICKY TECH MODE: Prevent premature breakout when troubleshooting
    if state.status in ["diagnosing", "solution_offered"]:
        # (is_feedback already detected proactively at the top)
        
        # Stay in ISSUE mode if feedback or forced ISSUE
        if is_feedback or forced_intent == UserIntent.ISSUE.value or intent == UserIntent.ISSUE.value:
            intent = UserIntent.ISSUE.value
            state.category = "Tech"
            if is_feedback:
                print(f"--- [STICKY TECH] Detected feedback, maintaining ISSUE mode")
        elif intent not in [UserIntent.INFO.value, UserIntent.SALES.value, UserIntent.OFF_TOPIC.value, UserIntent.GREETING.value]:
            intent = UserIntent.ISSUE.value
            state.category = "Tech"
        else:
            print(f"--- [BREAKOUT] User intent {intent} broke Sticky Tech Mode")

    # Status Sync
    state.status = brain_result.get("status", state.status)

    # (tech_keywords and is_technical_content are now defined at the top)

    # 🎯 SMART DISCOVERY PHASE: **DISABLED**
    # ============================================================
    # User requested to remove the numbered menu (1-6 options)
    # Users should describe their problem directly without seeing a checklist
    # The system will process raw input and provide solutions or ask clarifying questions
    should_show_discovery = False
    # Discovery phase is now completely disabled
    
    # If user responds to Discovery Menu, exit Discovery Phase
    if state.is_discovery_phase:
        state.is_discovery_phase = False


    # Merge Entities & Smart Lead Capture
    new_ents = brain_result.get("entities", {})
    if isinstance(new_ents, dict):
        # 0.6 AI-DRIVEN LEAD CAPTURE: If guest didn't provide email in payload, 
        # but AI found it in natural message, capture it now!
        if not user_email_for_session and new_ents.get("email"):
            extracted_email = str(new_ents.get("email"))
            if "@" in extracted_email:
                user_email_for_session = extracted_email
                SupabaseService.ensure_user_exists(user_email_for_session, role="Guest")
                print(f"--- [LEAD CAPTURED] Extracted email from talk: {user_email_for_session}")

        for k, v in new_ents.items():
            if v and v != "null" and hasattr(state.entities, k):
                setattr(state.entities, k, str(v))
    
    # ============================================================
    # RAG SEARCH: Unified knowledge retrieval
    # ============================================================
    rag_context = []
    context_str = ""
    
    # 🚨 CRITICAL: Check for LOCAL TECHNICAL SOLUTIONS first for high-intent keywords
    # (tech_keywords and is_technical_content are now defined above)
    
    # (Handled by proactive check at the top)
    if intent == "ISSUE":
        print(f"--- [TECH PATH] Confirmed ISSUE flow.")
    
    
    # ============================================================
    # 5. RAG RETRIEVAL (Intelligent Context)
    # ============================================================
    context_str = ""
    chunk_limit = 4 # Default
    # helper for dynamic chunk count
    def get_optimal_chunk_count(user_message: str) -> int:
        word_count = len(user_message.split())
        if word_count <= 5: return 2
        elif word_count <= 10: return 3
        return 4

    # ============================================================
    # 5. KNOWLEDGE RETRIEVAL (RAG)
    # ============================================================
    rag_context = []
    chunk_limit = 4
    context_str = ""

    # 🎯 RAG SCOPE: Include General intent to catch factual queries classified as General
    if intent in [UserIntent.INFO.value, UserIntent.SALES.value, "General"]:
        # 🚀 Apply RAG BOOST for factual queries (companies, clients, etc.)
        factual_keywords = ["شركات", "عملاء", "قطاعات", "sectors", "clients", "companies", "names", "اسماء"]
        active_threshold = 0.35 # Default
        
        # 🛡️ ROBUST MATCHING: Support both prefix and suffix variations (الشركات vs شركات)
        has_factual_intent = any(normalize_arabic(k) in normalized_msg for k in factual_keywords)
        
        if has_factual_intent:
            chunk_limit = 8
            active_threshold = 0.25 # 🎯 EVEN MORE AGGRESSIVE: Lower threshold for list-based factual queries
            print(f"--- [RAG BOOST] Factual query detected. Limit: {chunk_limit}, Threshold: {active_threshold}")

        # 🎯 Execute Search with the calculated limit and threshold
        rag_context = RagService.search_knowledge_base(optimized_query, limit=chunk_limit, threshold=active_threshold)
        
        if rag_context:
            context_str = "\n---\n".join(rag_context)
            print(f"\n🔥🔥🔥 [RAG HIT] Found {len(rag_context)} chunks for query!")
            print(f"--- [DEBUG] Intent: {intent}")
            print(f"--- [DEBUG] Optimized Query: {optimized_query}\n")
        else:
            print(f"\n💀💀💀 [RAG MISS] No context found for query: {optimized_query}")
            print(f"--- [DEBUG] Intent: {intent}\n")

    # ============================================================
    # 6. SYSTEM PROMPT PREPARATION (Non-Technical Trajectories)
    # ============================================================
    system_prompt = ""
    if intent in [UserIntent.SALES.value, UserIntent.INFO.value, UserIntent.GREETING.value]:
        # Greeting specific RAG override: Don't let greetings trigger generic "Who is Zedny" RAG
        if intent == UserIntent.GREETING.value:
            context_str = ""
            print("--- [RAG OMITTED] Clearing context for GREETING intent.")

        pivot_rule = ""
        if is_competitor:
            pivot_rule = f"\n!!! CRITICAL: User asked about COMPETITORS. Focus on Zedny's ROI and Arabic Excellence. Do not list other platforms.\n"

        # CONDITIONAL GREETING: Only mention the loyalty instructions if it's the very first message
        current_loyalty = BRAND_LOYALTY_INSTRUCTIONS if not state.history else "Skip all greetings. Start directly."

        # Language Rule Enforcement
        lang_name = "English" if detected_lang == "en" else "Modern Standard Arabic"
        language_rule = f"### 🌍 LANGUAGE RULE:\n- Respond ONLY in {lang_name}.\n- If context is in another language, translate the key info to {lang_name}."

        system_prompt = SALES_INFO_PROMPT.format(
            user_name=user_mem.get("name", "Guest"),
            company_name=user_mem.get("company", "Visitor"),
            user_type=user_mem.get("user_type", "Guest"),
            courses=user_mem.get("enrolled_courses", []),
            BRAND_LOYALTY_INSTRUCTIONS=current_loyalty,
            OUTPUT_SANITIZATION_RULES=OUTPUT_SANITIZATION_RULES,
            LANGUAGE_RULE=language_rule,
            pending_topic_context=state.pending_topic or "None",
            session_summary=state.summary or "New Interaction"
        ) + pivot_rule + f"\nSTRICT VARIETY: Do not repeat these points: {dont_repeat}\n"


    # 7. Trajectories: 🚨 COMPETITOR BLOCKING (Hard-Coded Defense)
    # If a competitor is detected, force the refusal path UNLESS it is a SALES comparison.
    if (is_competitor and intent != UserIntent.SALES.value) or "OFF_TOPIC" in intent:
        # 🔒 Use LOCKED language for refusal
        lang_instruction = "English" if detected_lang == "en" else "Modern Standard Arabic"
        
        # Determine specific refusal type
        refusal_type = "COMPETITOR_MENTION" if is_competitor else "STRICT_SCOPE_REFUSAL"
        
        refusal_prompt = f"""{refusal_type}: Speak as the Zedny Assistant. 
        {"NEVER mention other platforms like Udemy, Coursera, or Edraak. Stay loyal to Zedny." if is_competitor else "Politely refuse to answer anything unrelated to Zedny or corporate training."}
        ⚠️ MANDATORY: Respond ONLY in {lang_instruction}.
        Use this instruction from loyalty rules: {BRAND_LOYALTY_INSTRUCTIONS}"""
        
        answer = AIService.run_llm(refusal_prompt, user_msg)
        state.history.append(f"User: {user_msg}")
        state.history.append(f"AI: {answer}")
        SupabaseService.save_session(state, user_email_for_session)
        return ChatResponse(answer=answer, incident_state=state)

    # TRAJECTORY: SALES
    if intent == UserIntent.SALES.value:
        # 🏢 B2B Check: Immediate form for corporate leads
        b2b_keywords = ["موظفين", "موظف", "شركة", "شركات", "تعاقد", "employee", "corporate", "business", "company", "staff", "training for teams"]
        is_b2b = any(k in user_msg.lower() for k in b2b_keywords)
        
        print(f"--- [ROUTING] SALES Intent detected (B2B: {is_b2b})")
        
        if USE_MULTI_AGENT:
            answer = brain_result.get("answer", "أهلاً بك! كيف أقدر أساعدك النهادرى؟")
        else:
            # 🧠 INTELLIGENT RAG USAGE: Add explicit instruction when factual info is requested
            rag_instruction = ""
            factual_keywords = ["شركات", "companies", "اسماء", "names", "عملاء", "clients", "قطاعات", "sectors"]
            if any(k in user_msg.lower() for k in factual_keywords):
                rag_instruction = f"""
🚨 CRITICAL INSTRUCTION:
The user is asking for FACTUAL INFORMATION (companies, names, clients, etc.).
You MUST extract this information ONLY from the 'Context' provided below.
DO NOT hallucinate or make up names. If the Context has company names, list them.
If the Context doesn't have this info, say: "للحصول على القائمة الكاملة، يسعدنا تواصلك مع فريقنا."

Context from Knowledge Base:
{context_str}
---
"""
            # RESTORED: Use intent="Sales" to leverage the dynamic priority list in AIService
            # Claude 3.5 remains the lead in that list, but now we have failover
            user_prompt = f"User: {user_msg}\n{rag_instruction}\nContext: {context_str}"
            answer = AIService.run_llm(system_prompt, user_prompt, intent="Sales")
        
        # 🚨 AI-DRIVEN FALLBACK DETECTION: Detect NO_DIRECT_ANSWER tag before cleaning
        no_answer_signal = "[[NO_DIRECT_ANSWER]]" in answer or "NO_DIRECT_ANSWER" in answer
        answer = re.sub(r'\[\[\s*NO_DIRECT_ANSWER\s*\]\]', '', answer).strip()
        answer = clean_ai_response(answer)

        
        # 2. Generate Professional Executive Summary for Sales Team
        report_id = str(uuid.uuid4())
        user_email = request.user_email or "Guest (Waiting for registration)"
        
        # AI-Generated Professional Summary
        summary_prompt = """أنت الآن **محلل ذكاء المبيعات (Sales Intelligence Analyst)**. 
        مهمتك هي صياغة ملخص تنفيذي (Executive Summary) احترافي جداً ومقنع لفريق المبيعات بناءً على محادثة العميل.
        
        استخدم الهيكل التالي وmarkdown حصراً:
        
        📋 **تحليل الفرصة البيعية**
        [وصف دقيق في جملتين لما يبحث عنه العميل وما هي "نقطة الألم" التي لديه]
        
        🎯 **التصنيف النوعي**:
        - **مستوى الاهتمام**: [عالي جداً / متوسط / استكشافي]
        - **فئة العميل**: [B2B - مؤسسة كبيرة / شركة ناشئة / فرد]
        - **المنتج المستهدف**: [ذكر الكورسات أو الحلول المحددة]
        
        🚀 **خطة المتابعة المقترحة**:
        1. [توصية محددة لمندوب المبيعات ليبدأ بها كلامه]
        2. [ما هو العرض أو الحل الأنسب لهذا العميل]
        
        ⚠️ **ملاحظات استراتيجية**:
        - [أي ملاحظة عن تردده، ميزانيته، أو اهتمامه بميزة معينة]
        
        **القواعد:**
        - اللغة: عربية فصحى مهنية.
        - الطول: مختصر ومركز (أقل من 150 كلمة).
        - التنسيق: Markdown فقط."""

        customer_context = f"""
Customer Question: {user_msg}
Customer Profile: {json.dumps(user_mem, ensure_ascii=False)}
AI Response Given: {answer[:500]}...
Conversation History: {state.history[-4:] if state.history else 'New conversation'}
"""
        
        professional_summary = AIService.run_llm(summary_prompt, customer_context, model="gemini", intent="Sales")
        
        # Fallback if AI fails
        if not professional_summary or len(professional_summary) < 50:
            professional_summary = f"""📋 **ملخص تنفيذي**
استفسار مبيعات جديد من عميل محتمل.

🎯 **الاستفسار**: {user_msg}
💼 **نوع العميل**: {user_mem.get('user_type', 'Guest')}
📧 **البريد الإلكتروني**: {user_email}

✅ **الإجراء المطلوب**: التواصل مع العميل للمتابعة وتقديم عرض مخصص."""

        sales_report = EscalationReport(
            id=report_id, 
            category="Sales", 
            service="Sales Inquiry",
            urgency="Medium", 
            summary=professional_summary, 
            history=state.history + [f"User: {user_msg}", f"AI: {answer}"],
            timestamp=datetime.datetime.now().isoformat(), 
            assigned_to="sales_manager@zedny.ai", 
            user_email=user_email
        )
        SupabaseService.save_report(sales_report)
        
        # DO NOT send email here - Wait for form submission like Technical reports
        # This ensures we capture accurate customer details from the form
        print(f"--- [SALES ESCALATION] Report {report_id} saved, waiting for form submission ---")
        
        state.status = "escalated_sales"
        state.history.append(f"User: {user_msg}")
        state.history.append(f"AI: {answer}")
        SupabaseService.save_session(state, user_email_for_session)
        
        # 🚨 FINAL DECISION: Check if we have RAG info for B2C
        # If is_b2b or is_global_b2b is True OR AI signaled no answer -> Force form
        
        final_action = "force_form"
        if not is_b2b and not is_global_b2b and not no_answer_signal:
            final_action = None # Stay in chat, we have an answer
            print(f"--- [SALES B2C] Answer found. Keeping in chat.")
        else:
            reason = "B2B_Keywords" if is_b2b else ("B2B_Radar" if is_global_b2b else "AI Signal")
            print(f"--- [SALES ESCALATION] Forcing lead form. Reason: {reason}")

        return ChatResponse(
            answer=answer, 
            should_escalate=True if final_action == "force_form" else False, 
            incident_state=state,
            context_used=professional_summary if final_action == "force_form" else context_str,
            action_required=final_action
        )

    # 5.5 SMART DEVICE TRIGGER: Only request if specific conditions met
    if ConversationService.needs_device_info(state.device_info, intent, is_media_issue, len(state.solutions_tried)):
        # AI-driven instruction for the final answer phase
        soft_device_prompt = f"\nUSER CONTEXT: {ConversationService.generate_device_question('ar')}\nINSTRUCTION: Add this soft request optionally to your response only if relevant to the technical nature of the issue."
    else:
        soft_device_prompt = ""

    # 5.6 DEVICE EXTRACTION: (Transient - Only extract if user actually provided it)
    if len(state.history) > 0 and ("جهاز" in state.history[-1] or "device" in state.history[-1].lower()):
        extracted = ConversationService.extract_device_info_from_response(user_msg)
        if extracted.is_collected:
            # We store it in session state, but we'll flag it as 'not for DB' if not escalated
            state.device_info = extracted
            print(f"--- [DEVICE INFO EXTRACTED] Transient storage active.")

    # 6. Trajectories
    if "OFF_TOPIC" in intent:
        refusal_prompt = f"STRICT_SCOPE_REFUSAL: Speak as the Zedny Assistant. Politely refuse to answer anything unrelated to Zedny or corporate training. Use this instruction from loyalty rules: {BRAND_LOYALTY_INSTRUCTIONS}"
        answer = AIService.run_llm(refusal_prompt, user_msg)
        state.history.append(f"User: {user_msg}")
        state.history.append(f"AI: {answer}")
        SupabaseService.save_session(state, user_email_for_session)
        return ChatResponse(answer=answer, incident_state=state)


    # TRAJECTORY: INFO / GREETING
    if intent in [UserIntent.INFO.value, UserIntent.GREETING.value]:
        # 🔄 CONTINUATION LOGIC: Check if this is a follow-up to a pending info topic
        if is_follow_up and state.pending_topic and state.current_phase == "awaiting_confirmation":
             print(f"--- [INFO CONTINUATION] Providing details for: {state.pending_topic}")
             # Reset context after handling
             state.current_phase = "discovery"
             state.pending_topic = None

        # Include Summary in Context
        full_history_context = f"Previous Summary: {state.summary}\nRecent History: {state.history}" if state.summary else f"History: {state.history}"
        
        # 🧠 INTELLIGENT RAG USAGE: Add explicit instruction when factual info is requested
        rag_instruction = ""
        factual_keywords = ["شركات", "عملاء", "قطاعات", "sectors", "clients", "companies", "names", "اسماء"]
        if any(normalize_arabic(k) in normalized_msg for k in factual_keywords):
            rag_instruction = f"""
🚨 CRITICAL INSTRUCTION:
The user is asking for FACTUAL INFORMATION (companies, names, clients, etc.).
You MUST extract this information ONLY from the 'Context' provided below.
Provide as much detail as found in the Context. If company names are listed, list them clearly.

Important: If the Context contains examples but not a full list, provide the examples and mention that these are some of our partners.
Only if NO information is found in the Context should you say: "للحصول على تفاصيل دقيقة، يسعدنا تواصلك مع فريقنا المختص."

---
"""
        
        if USE_MULTI_AGENT:
            answer = brain_result.get("answer", "أهلاً بك! كيف أقدر أساعدك النهاردة؟")
        else:
            # RESTORED: Use intent="General" for dynamic expert selection with failover
            user_prompt = f"User: {user_msg}\n{full_history_context}\n{rag_instruction}\nContext: {context_str}"
            answer = AIService.run_llm(system_prompt, user_prompt, intent="General")
        
        # Sales Radar check for Info/Greeting path
        action_req = "force_form" if is_global_b2b else None
        should_esc = True if is_global_b2b else False

        state.history.append(f"User: {user_msg}")
        state.history.append(f"AI: {answer}")
        SupabaseService.save_session(state, user_email_for_session)
        return ChatResponse(
            answer=answer, 
            context_used=context_str, 
            incident_state=state,
            action_required=action_req,
            should_escalate=should_esc
        )

    # TRAJECTORY: SUPPORT/ISSUE - Unified Technical Orchestrator
    if intent == UserIntent.ISSUE.value:
        return await TechnicalOrchestrator.process_request(
            message=user_msg,
            state=state,
            user_mem=user_mem,
            detected_lang=detected_lang,
            user_email=user_email_for_session
        )

    # 8. Final Fallback (Should not be reached with proper intent classification)
    state.history.append(f"User: {user_msg}")
    state.history.append(f"AI: أهلاً بك! كيف أقدر أساعدك؟")
    SupabaseService.save_session(state, user_email_for_session)
    return ChatResponse(answer="أهلاً بك! كيف أقدر أساعدك؟", incident_state=state)
