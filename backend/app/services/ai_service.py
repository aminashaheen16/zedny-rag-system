import time
import os
import logging
import concurrent.futures
from typing import List, Dict, Any, Optional
from app.core.config import ai_client, openrouter_client, GOOGLE_API_KEY, genai_client

class AIService:
    logger = logging.getLogger("Zedny.AIService")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    @staticmethod
    def run_llm(system_prompt: str, user_message: str, model: str = None, timeout: int = 30, intent: str = "General") -> str:
        """
        Standard LLM wrapper using OpenRouter FREE models exclusively.
        """
        # 🏆 FREE MODEL PRIORITY LIST (Verified Stability)
        priority_list = [
            "google/gemini-2.0-flash-001",           # Fast & High Quality
            "meta-llama/llama-3.3-70b-instruct",     # Powerhouse
            "deepseek/deepseek-chat",                # Reliable Fallback
            "openrouter/auto",                       # Best Free Router
        ]
        
        # 🧠 INTENT-BASED REORDERING (Optimization)
        if intent == "ISSUE":
            # Technical: prioritize larger reasoning models
            priority_list = ["meta-llama/llama-3.3-70b-instruct", "google/gemini-2.0-flash-001", "deepseek/deepseek-chat"]
        elif intent in ["Sales", "INFO"]:
            # Info: prioritize eloquence and facts
            priority_list = ["google/gemini-2.0-flash-001", "meta-llama/llama-3.3-70b-instruct", "deepseek/deepseek-chat"]

        AIService.logger.info(f"--- [OPENROUTER FREE] Using unified priority for intent: {intent}")

        if model:
            requested = model.lower()
            matched = [m for m in priority_list if requested in m.lower()]
            if matched:
                priority_list = matched + [m for m in priority_list if m not in matched]
            else:
                priority_list = [model] + priority_list

        for current_model in priority_list:
            future = AIService.executor.submit(AIService._run_single_call, current_model, system_prompt, user_message)
            try:
                # ⚡ FAILOVER OPTIMIZATION: Wait max 15s per model to avoid massive hangs
                result = future.result(timeout=15)
                if result: 
                    AIService.logger.info(f"LLM SUCCESS: {current_model} (OpenRouter Free) for Intent: {intent}")
                    return result
            except Exception as e:
                AIService.logger.error(f"LLM Error: {current_model} | {e}")
                continue
        
        return "عذراً، نواجه ضغطاً تقنياً بسيطاً في محرك الذكاء الاصطناعي الخاص بزدني. يرجى المحاولة مرة أخرى خلال لحظات. 🚀"

    @staticmethod
    def _run_single_call(current_model: str, system_prompt: str, user_message: str) -> Optional[str]:
        """Internal worker for LLM execution logic."""
        try:
            # A. GEMINI LOGIC (Direct SDK)
            if "gemini" in current_model.lower() and "/" not in current_model:
                if not genai_client: return None
                from google.genai import types
                
                # Use stable ID for SDK
                sdk_model = "gemini-1.5-flash" 
                
                response = genai_client.models.generate_content(
                    model=sdk_model,
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.2,
                        max_output_tokens=1000
                    )
                )
                
                if not response or not response.text:
                    return None
                return response.text.strip()

            # B. OPENROUTER LOGIC
            if "/" in current_model:  # OpenRouter models use "provider/model" format
                if not openrouter_client: return None
                
                # Extra headers for OpenRouter visibility & priority
                extra_headers = {
                    "HTTP-Referer": "https://zedny.ai", 
                    "X-Title": "Zedny AI Intelligent Assistant"
                }

                completion = openrouter_client.chat.completions.create(
                    model=current_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3, # Balanced for Enterprise Logic
                    max_tokens=1500,
                    extra_headers=extra_headers
                )
                if not completion or not completion.choices:
                    return None
                return completion.choices[0].message.content.strip()

            # C. DIRECT GROQ / OPENAI LOGIC (Fallback)
            if not ai_client:
                AIService.logger.warning(f"Direct AI client not available for fallback to {current_model}")
                return None
            
            temperature = 0.2 
            completion = ai_client.chat.completions.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=1000
            )
            if not completion or not completion.choices:
                return None
            return completion.choices[0].message.content.strip()
        except Exception as e:
            AIService.logger.debug(f"Direct LLM call failed for {current_model}: {e}")
            return None

    @staticmethod
    def generate_conversation_summary(history: List[str], current_summary: str = "") -> str:
        if not history: return ""
        combined_history = "\n".join(history[-20:])
        prompt = f"""Summarize this support conversation concisely for a human agent.
        Current Summary: {current_summary}
        New History: {combined_history}
        
        Format:
        Main Problem: <...>
        Entities: <...>
        Status: <...>
        """
        return AIService.run_llm(prompt, "Summarize now.", model="gemini")

    @staticmethod
    def detect_b2b_intent(message: str) -> bool:
        """
        Passively detects if the user represents a business interest (B2B) vs an individual user.
        Uses semantic context to filter out general mentions of "company" in support or casual contexts.
        Returns True if high confidence B2B intent (Buying, Training, Bulk accounts).
        """
        # 1. Fast Keyword Check (Low Latency)
        # Added singular "موظف" and "اشتراك"
        keywords = ["company", "corporate", "employee", "team", "training my", "business", "staff", "bulk", "enterprise", "شركة", "موظف", "موظفين", "فريق", "تدريب", "بزنس", "مؤسسة", "عدد كبير", "اشتراك", "خطة"]
        if not any(k in message.lower() for k in keywords):
            return False

        # 2. Semantic Verification (High Accuracy Response)
        system_prompt = """You are a High-Precision B2B Sales Intent Classifier for Zedny.ai.
Your goal is to distinguish between a "Potential Corporate Customer" (B2B Lead) and an "Individual Support User".

CLASSIFICATION RULES:
- YES (B2B): Message implies buying services, training teams, BULK SUBSCRIPTIONS (اشتراكات جماعية), or representing a company seeking business partnership.
- NO (Support): Message is about individual tech issues, personal accounts, or mentions a company incidentally while asking for support.

EXAMPLES OF NO:
- "أنا موظف في شركة X ومش عارف أدخل" (Individual support)
- "عايز أكلم المدير بخصوص الباسورد" (Support)
- "شركة فودافون مش شغالة عندي" (External service)

EXAMPLES OF YES:
- "عايز اشتراك لـ 50 موظف في شركتي" (Bulk Sale/Subscription)
- "عندي شركة وعايز أدرب فريقي" (Company Training)
- "Corporate rates for 50+ users?" (Bulk Sale)
- "نحن شركة تدريب ونريد التعاون معكم" (Partnership)

Reply strictly with: YES or NO"""
        
        try:
            # Using Gemini 2.0 or Llama 70B for high-quality semantic reasoning
            res = AIService.run_llm(system_prompt, message, model="google/gemini-2.0-flash-001")
            
            # Robust check: look for "YES" as a word
            is_b2b = "YES" in res.upper()
            AIService.logger.info(f"--- [B2B RADAR DEBUG] Msg: {message[:30]} | LLM Raw: {res} | Final: {is_b2b}")
            return is_b2b
        except Exception as e:
            AIService.logger.error(f"B2B Radar Error: {e}")
            return False

    @staticmethod
    def perform_smart_analysis(reports: List[Dict[str, Any]]) -> str:
        if not reports: return "لا توجد بيانات كافية للتحليل الاستراتيجي حالياً. يرجى انتظار استقبال المزيد من البلاغات."
        
        # Prepare structured context
        report_snippets = []
        for r in reports[:30]:
            cat = r.get('category', 'General')
            sum_text = r.get('summary', 'No summary')
            time = r.get('timestamp', 'N/A')
            report_snippets.append(f"[{time}] [{cat}] {sum_text}")
        
        context = "\n".join(report_snippets)
        
        prompt = f"""أنت الآن **المحلل الاستراتيجي الأول ورئيس العمليات في منصة زدني (Zedny.ai)**.
        مهمتك هي تحليل بلاغات التصعيد الأخيرة وتقديم تقرير تنفيذي رفيع المستوى لصناع القرار.
        
        يجب أن يكون التقرير باللغة العربية، مهنياً للغاية، ومبنياً على البيانات المتاحة.
        
        **بيانات البلاغات الأخيرة**:
        {context}
        
        **مطلوب التقرير بالهيكل التالي (استخدم Markdown):**
        
        ### 📊 ملخص الحالة الراهنة (Executive Overview)
        - نظرة عامة على حجم التصعيدات والاتجاه العام (هل الوضع مستقر أم متأزم؟).
        - تحديد القسم الأكثر ضغطاً (Sales, Tech, etc.).
        
        ### 🔍 تحليل الأنماط المتكررة (Pattern Recognition)
        - استخرج أهم مشكلتين تقنيتين أو عقبتين في المبيعات يتكرر حدوثهما.
        - ما هو "جذر المشكلة" (Root Cause) المحتمل بناءً على وصف البلاغات؟
        
        ### 💡 التوصيات الاستراتيجية (Strategic Roadmap)
        - قدم توصيتين عمليتين لتقليل العبء على الفريق البشري (مثلاً: تحديث في واجهة المستخدم، إضافة محتوى للـ RAG، أو تغيير في سياسة المبيعات).
        - وضح العائد المتوقع (ROI) من تنفيذ هذه التوصيات.
        
        ### 📈 مؤشر الأداء المتوقع
        - توقع كيف سيتأثر معدل ذكاء النظام (AI Success Rate) في حال تنفيذ التوصيات.
        
        **قواعد هامة:**
        - النبرة: احترافية، تحليلية، ومباشرة.
        - تجنب العبارات العامة، كن محدداً بناءً على البيانات.
        - استخدم تنسيق Markdown (عناوين، نقاط، جداول إن لزم الأمر).
        """
        return AIService.run_llm(prompt, "فريق العمليات يحتاج لتحليلك الآن.", model="gemini")

    @staticmethod
    async def send_escalation_email(report: Any):
        """
        Sends a professional escalation email to the support team or specific agent.
        Uses EmailService for SMTP delivery and formatting.
        """
        from app.services.email_service import EmailService
        from app.core.config import SUPPORT_EMAIL

        try:
            # 1. Generate professional content via AI
            history_text = "\n".join(report.history)
            prompt = f"""أنت الآن **رئيس فريق التحليل الاستراتيجي (Head of Strategic Analytics)** في زدني. 
            مهمتك هي كتابة "موجز الاستخبارات الفنية" (Technical Intelligence Brief) لمهندس الدعم المختص.
            
            القسم: {report.category}
            بريد العميل: {report.user_email}
            
            سجل المحادثة الكامل:
            {history_text}
            
            **مطلوب منك كتابة فقرتين إلى ثلاث فقرات (بدون نقاط):**
            1. **تشخيص الموقف**: لخص باختصار وعمق ماذا يريد العميل بالضبط وما هي الحالة النفسية التي يتحدث بها (غاضب، مستعجل، مهتم بالشراء).
            2. **تحليل العوائق**: بناءً على المحادثة، أين تكمن المشكلة الحقيقية (هل هي تقنية بحتة أم سوء فهم من العميل)؟
            3. **التوصية الحاسمة**: ما هي أفضل طريقة للتعامل مع هذا العميل لإرضائه وحل مشكلته في المكالمة أو الإيميل القادم؟
            
            **القواعد:**
            - اللغة: عربية فصحى احترافية جداً.
            - النبرة: استخباراتية، تحليلية، وهادئة.
            - لا تستخدم قوائم نقطية، اكتب نصاً انسيابياً رفيع المستوى."""
            email_body = AIService.run_llm(prompt, "توليد موجز تحليلي رفيع المستوى للموظف.", model="gemini")
            
            # 2. Add description to report object (inside metadata for persistence)
            report.metadata["ai_summary"] = email_body
            
            # Persist to DB so the Dashboard reflects the email content
            from app.services.supabase_service import SupabaseService
            SupabaseService.update_report(report)
            
            # 3. Format as HTML
            html_content = EmailService.format_escalation_html(report)
            
            # 4. Route to Department Recipients
            department = report.category.lower()
            recipients = []

            # A. Add the Assigned Specialist (Direct Routing)
            if report.assigned_to and "@" in report.assigned_to:
                recipients.append(report.assigned_to.strip())

            # B. Add Departmental Groups (Dual Oversight)
            if any(key in department for key in ["sales", "commercial", "partnership"]):
                sales_email = os.getenv("SALES_EMAIL") or "mohammedrawan653@gmail.com"
                recipients.append(sales_email)
            else:
                # Tech / Support
                tech_email = os.getenv("SUPPORT_EMAIL") or "mohammedrawan653@gmail.com"
                recipients.append(tech_email)
                # Backup/Oversight
                # recipients.append("support@zedny.ai") # Disabled for sandbox safety

            # 5. Send to all unique, valid recipients
            subject = f"🚨 {report.urgency.upper()} {report.category.upper()} ESCALATION"
            final_targets = list(set([r for r in recipients if "@" in r]))
            
            for target in final_targets:
                success = EmailService.send_html_email(subject, target, html_content)
                if success:
                    print(f"--- [ROUTING SUCCESS] {report.category} escalation dispatched to {target} ---")
                else:
                    print(f"--- [ROUTING FAILED] Failed to reach {target} ---")

        except Exception as e:
            AIService.logger.error(f"--- [EMAIL SERVICE ERROR] Critical failure in dispatcher: {e}")
    @staticmethod
    def interpret_tech_intent(message: str, history: List[str]) -> Dict[str, Any]:
        """
        Interprets the user's intent within a technical diagnostic flow using conversational history.
        Specifically handles feedback loops and topic rejections.
        """
        # Format recent history for context
        history_context = "\n".join(history[-5:]) if history else "New Conversation"
        
        system_prompt = """You are a Technical Support Intent Analyst.
Analyze the user's latest message in context of the recent conversation to determine their intent.

INTENT CATEGORIES:
1. "REJECTION": User explicitly says the proposed solution is WRONG, UNRELATED, or for a DIFFERENT TOPIC entirely.
2. "ESCALATION_AGREEMENT": User says "كمل" or "حولني" in response to an AI escalation offer, or asks for a human.
3. "REQUEST_NEXT_SOLUTION": User wants ANOTHER troubleshooting step because the current one didn't work.
4. "NEGATIVE_FEEDBACK": User says the solution was correct for the topic but IT DIDN'T WORK.
5. "FOLLOW_UP": User is asking a question about the current solution/steps.
6. "NEW_PROBLEM": User starts a completely new and different technical issue.

YOUR TASK:
- Return a JSON object with:
  - "intent": One of the 6 categories above.
  - "core_problem_extraction": For REJECTION, REQUEST_NEXT_SOLUTION or NEW_PROBLEM, extract the REAL problem.
  - "explanation": Brief reasoning.

Reply strictly in JSON format. """

        user_input = f"History:\n{history_context}\n\nLatest User Message: {message}"
        
        try:
            # Using Llama 70B for high-quality reasoning
            raw_response = AIService.run_llm(system_prompt, user_input, model="meta-llama/llama-3.3-70b-instruct:free", intent="ISSUE")
            
            # Extract JSON from potential markdown markers
            json_text = raw_response.strip()
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0].strip()
            
            import json
            return json.loads(json_text)
        except Exception as e:
            AIService.logger.error(f"Error interpreting tech intent: {e}")
            return {"intent": "OTHER", "core_problem_extraction": message, "explanation": "Fallback due to error"}
