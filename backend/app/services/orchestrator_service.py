import logging
import asyncio
from typing import Dict, Any, List, Optional
from app.services.agents import ClassificationAgent, SynthesisAgent, RAGAgent
from app.services.ai_service import AIService
from app.core.prompts import SALES_INFO_PROMPT, SUPPORT_ENGINEER_V2_PROMPT, BRAND_LOYALTY_INSTRUCTIONS
from app.core.config import USE_MULTI_AGENT

logger = logging.getLogger("Zedny.Orchestrator")

class OrchestratorService:
    """The central brain that coordinates specialized agents."""
    
    @staticmethod
    async def process_interaction(
        user_msg: str, 
        history: List[str], 
        summary: str, 
        entities: Dict[str, Any], 
        status: str,
        user_mem: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinates the agent pipeline.
        """
        logger.info(f"--- [ORCHESTRATOR] Processing msg: {user_msg[:50]}...")
        
        # 1. CLASSIFICATION (Llama 70B Focused)
        # We run this first as it determines the trajectory
        brain_result = ClassificationAgent.analyze(user_msg, history, summary, entities, status)
        
        intent = brain_result.get("intent", "INFO").upper()
        optimized_query = brain_result.get("optimized_query", user_msg)
        is_media = brain_result.get("is_media", False)
        
        # 🚀 RAG BOOST LOGIC: Calculate dynamic search parameters
        from app.utils.arabic_helper import normalize_arabic
        normalized_msg = normalize_arabic(user_msg)
        factual_keywords = ["شركات", "عملاء", "قطاعات", "sectors", "clients", "companies", "names", "اسماء"]
        
        active_limit = 4
        active_threshold = 0.35 # Default
        
        if any(normalize_arabic(k) in normalized_msg for k in factual_keywords):
            active_limit = 8
            active_threshold = 0.25 # AGGRESSIVE retrieval for factual lists
            logger.info(f"--- [ORCHESTRATOR RAG BOOST] Limit: {active_limit}, Threshold: {active_threshold}")

        # 2. RAG RETRIEVAL (Parallel to other prep logic if needed)
        context_chunks = RAGAgent.optimize_and_search(optimized_query, limit=active_limit, threshold=active_threshold)
        context_str = "\n---\n".join(context_chunks[:5]) if context_chunks else ""
        
        # 3. SELECT SYSTEM PROMPT based on Intent/Category
        # (This logic mirror chat.py but modularized)
        from app.models.schemas import UserIntent
        
        system_prompt = ""
        category = "General"
        
        if intent == UserIntent.SALES.value:
            category = "Sales"
            current_loyalty = BRAND_LOYALTY_INSTRUCTIONS if not history else "Skip all greetings. Start directly."
            system_prompt = SALES_INFO_PROMPT.format(
                user_name=user_mem.get("name", "Guest"),
                company_name=user_mem.get("company", "Visitor"),
                user_type=user_mem.get("user_type", "Guest"),
                courses=user_mem.get("enrolled_courses", []),
                BRAND_LOYALTY_INSTRUCTIONS=current_loyalty
            )
        elif intent == UserIntent.ISSUE.value:
            category = "Tech"
            # Support prompt requires more fields (mocking defaults for now)
            current_loyalty = BRAND_LOYALTY_INSTRUCTIONS if not history else "Skip all greetings. Start directly."
            system_prompt = SUPPORT_ENGINEER_V2_PROMPT.format(
                user_name=user_mem.get("name", "Guest"),
                company_name=user_mem.get("company", "Visitor"),
                tech_profile=user_mem.get("technical_profile", {}),
                courses=user_mem.get("enrolled_courses", []),
                problem_description="Troubleshooting",
                solutions_tried="",
                solution_attempt_count=1,
                max_attempts=3,
                awaiting_feedback="No",
                BRAND_LOYALTY_INSTRUCTIONS=current_loyalty
            )
        else:
            # Default INFO
            category = "General"
            current_loyalty = BRAND_LOYALTY_INSTRUCTIONS if not history else "Skip all greetings. Start directly."
            system_prompt = SALES_INFO_PROMPT.format(
                user_name=user_mem.get("name", "Guest"),
                company_name=user_mem.get("company", "Visitor"),
                user_type=user_mem.get("user_type", "Guest"),
                courses=user_mem.get("enrolled_courses", []),
                BRAND_LOYALTY_INSTRUCTIONS=current_loyalty
            )

        # 4. FINAL SYNTHESIS (Synthesis Agent)
        answer = SynthesisAgent.craft_response(user_msg, context_str, intent, user_mem, system_prompt)
        
        return {
            "answer": answer,
            "intent": intent,
            "category": category,
            "context_used": context_str,
            "entities": brain_result.get("entities", {}),
            "is_media": is_media,
            "optimized_query": optimized_query
        }
