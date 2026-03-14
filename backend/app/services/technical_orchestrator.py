import json
import uuid
import datetime
import logging
from typing import Dict, Any, List, Optional
from app.models.schemas import IncidentState, ChatResponse, EscalationReport
from app.services.ai_service import AIService
from app.services.tech_service import TechService
from app.services.supabase_service import SupabaseService

logger = logging.getLogger("Zedny.TechnicalOrchestrator")

class TechnicalOrchestrator:
    """
    Orchestrates the technical support diagnostic flow using a state-machine approach.
    States: discovery, diagnosing, solution_feedback, escalated, resolved.
    """

    @staticmethod
    async def process_request(
        message: str, 
        state: IncidentState, 
        user_mem: Dict[str, Any], 
        detected_lang: str,
        user_email: Optional[str] = None
    ) -> ChatResponse:
        """
        Main entry point for handling technical inquiries.
        """
        logger.info(f"--- [TECH ORCHESTRATOR] Processing State: {state.status} | Lang: {detected_lang}")
        
        # 1. Intent/Sentiment Interpretation for Context
        history_snippet = state.history[-10:] if state.history else []
        interpretation = AIService.interpret_tech_intent(message, history_snippet)
        intent_type = interpretation.get("intent", "FOLLOW_UP")
        extracted_problem = interpretation.get("core_problem_extraction")

        # 2. State Transitions & Logic
        if intent_type == "ESCALATION_AGREEMENT":
             return await TechnicalOrchestrator._handle_escalation_request(message, state, detected_lang, user_email)

        if state.status in ["new", "discovery", "collecting_info"]:
            return await TechnicalOrchestrator._handle_discovery(message, state, detected_lang, user_email, extracted_problem)
        
        if state.status == "diagnosing" or state.status == "solution_offered":
            return await TechnicalOrchestrator._handle_diagnostic_loop(message, state, detected_lang, user_email, intent_type, extracted_problem)

        # Fallback
        return await TechnicalOrchestrator._handle_discovery(message, state, detected_lang, user_email)

    @staticmethod
    async def _handle_discovery(message: str, state: IncidentState, lang: str, email: str, extracted: str = None) -> ChatResponse:
        """Handles initial problem identification phase."""
        state.status = "diagnosing"
        problem = extracted or message
        state.problem_description = problem
        
        logger.info(f"--- [TECH ORCH] Transitioned to DIAGNOSING. Problem: {problem}")
        
        # Immediately try to find first solution
        return await TechnicalOrchestrator._propose_next_solution(state, lang, email)

    @staticmethod
    async def _handle_diagnostic_loop(message: str, state: IncidentState, lang: str, email: str, intent: str, extracted: str) -> ChatResponse:
        """Handles the feedback loop and multiple solution attempts."""
        
        # If user says it worked
        if intent == "POSITIVE_FEEDBACK" or any(w in message.lower() for w in ["اشتغل", "تمام", "fixed", "worked"]):
            state.status = "resolved"
            ans = "الحمد لله! سعيد إن المشكلة اتحلت. 🙏 لو محتاج أي حاجة تانية أنا هنا." if lang == "ar" else "Great! I'm glad the issue is resolved. 🙏 Let me know if you need anything else."
            return TechnicalOrchestrator._finalize_response(ans, state, email)

        # If user says didn't work or asks for next
        if intent in ["REJECTION", "NEGATIVE_FEEDBACK", "REQUEST_NEXT_SOLUTION"]:
            state.diagnostic_turns += 1
            state.solutions_count += 1 # Syncing counters
            
            if state.solutions_count >= state.max_solutions_before_escalation:
                return await TechnicalOrchestrator._handle_escalation(message, state, lang, email)
            
            # Try to refine problem if extracted
            if extracted and len(extracted) > 10:
                state.problem_description = extracted
            
            return await TechnicalOrchestrator._propose_next_solution(state, lang, email)

        # If user is just asking a follow-up question about the CURRENT solution
        if intent == "FOLLOW_UP":
            prompt = f"The user is asking a follow-up question about the technical solution we just provided.\nContext: {state.history[-2:]}\nSolution: {state.solutions_tried[-1] if state.solutions_tried else 'N/A'}\nUser Msg: {message}\nAnswer in {lang}."
            ans = AIService.run_llm(prompt, message, intent="ISSUE")
            return TechnicalOrchestrator._finalize_response(ans, state, email)

        # Default: try to find a solution or ask for clarity
        return await TechnicalOrchestrator._propose_next_solution(state, lang, email)

    @staticmethod
    async def _propose_next_solution(state: IncidentState, lang: str, email: str) -> ChatResponse:
        """Searches KB and returns the best matching solution."""
        query = state.problem_description
        
        # High-confidence search
        solution = TechService.search(query, threshold=0.7, exclude_ids=state.tried_solution_ids)
        
        if solution:
            state.tried_solution_ids.append(solution["chunk_id"])
            state.solutions_tried.append(solution["title"])
            state.status = "solution_offered"
            
            prompt = f"""You are a helpful Tech Support Agent.
            Problem: {state.problem_description}
            Solution to propose: {solution['content']}
            Respond in {lang}. Be direct and professional."""
            
            ans = AIService.run_llm(prompt, query, intent="ISSUE")
            return TechnicalOrchestrator._finalize_response(ans, state, email)
        
        # If no solution found and we've tried before, escalate
        if state.solutions_count > 0:
            return await TechnicalOrchestrator._handle_escalation("No more solutions found.", state, lang, email)
        
        # If no solution found at all (vague input)
        ans = "ممكن توضح المشكلة أكتر؟ مش قادر ألاقي حل دقيق حالياً." if lang == "ar" else "Could you explain the problem in more detail? I couldn't find a precise match."
        return TechnicalOrchestrator._finalize_response(ans, state, email)

    @staticmethod
    async def _handle_escalation(message: str, state: IncidentState, lang: str, email: str) -> ChatResponse:
        """Prepares for human handoff."""
        state.status = "escalated"
        state.step = 2
        
        tried = "\n".join(state.solutions_tried)
        if lang == "ar":
            ans = f"بعتذر جداً، جربنا كذا حاجة ومنفعتش. هحولك دلوقتي لمهندس دعم بشري هيتابع معاك.\n\nالحلول اللي جربناها:\n{tried}\n\nمن فضلك سجل بياناتك هنا:"
        else:
            ans = f"I apologize, we've tried several solutions but the issue persists. I'm escalating this to a human engineer.\n\nSolutions tried:\n{tried}\n\nPlease register your details:"
            
        return ChatResponse(
            answer=ans,
            should_escalate=True,
            action_required="show_escalation_form",
            incident_state=state
        )

    @staticmethod
    async def _handle_escalation_request(message: str, state: IncidentState, lang: str, email: str) -> ChatResponse:
        """User explicitly asked for human."""
        if state.solutions_count >= 1: # If we tried at least one thing, allow direct escalation
            return await TechnicalOrchestrator._handle_escalation(message, state, lang, email)
        
        # Otherwise, try to persuade to try at least one AI solution
        ans = "أنا معاك وهساعدك، بس خليني أحاول أحلك المشكلة دي فوراً الأول؟ لو مانفعش هحولك فوراً." if lang == "ar" else "I'm here to help! Let me try to solve this for you instantly first? If it doesn't work, I'll connect you to an engineer right away."
        return TechnicalOrchestrator._finalize_response(ans, state, email)

    @staticmethod
    def _finalize_response(answer: str, state: IncidentState, email: str) -> ChatResponse:
        """Helper to save state and wrap response."""
        state.history.append(f"AI: {answer}")
        SupabaseService.save_session(state, email)
        return ChatResponse(answer=answer, incident_state=state)
