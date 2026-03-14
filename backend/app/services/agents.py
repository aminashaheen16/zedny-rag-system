import json
import logging
from typing import Dict, Any, List, Optional
from app.services.ai_service import AIService
from app.core.prompts import BRAND_LOYALTY_INSTRUCTIONS

logger = logging.getLogger("Zedny.Agents")

class ClassificationAgent:
    """Specialized Agent for intent, language, and entity extraction."""
    
    @staticmethod
    def analyze(user_msg: str, history: List[str], summary: str, entities: Dict[str, Any], status: str) -> Dict[str, Any]:
        prompt = f"""You are the **Zedny Classification Agent**. 
Your sole purpose is to analyze the user's intent and extract metadata.

**INPUT DATA:**
User Message: "{user_msg}"
Summary: {summary}
Status: {status}
History: {history[-5:]}

**YOUR TASKS:**
1. **Intent**: GREETING, INFO, ISSUE, SALES, COMPLAINT, OFF_TOPIC.
2. **Media Detection**: Is this about video/audio problems? (true/false)
3. **Optimized Query**: Create a clean search query for the database.
4. **Entities**: Extract email, product, or specific error messages.
5. **Intent Priority**: If the user asks about Zedny's identity (Who is Zedny?), it is ALWAYS **INFO** or **SALES**.

**OUTPUT SCHEMA (JSON ONLY):**
{{
  "intent": "...",
  "is_media": true/false,
  "optimized_query": "...",
  "entities": {{"email": "...", "product": "..."}},
  "detected_language": "ar/en"
}}
Return ONLY valid JSON."""
        
        raw = AIService.run_llm(prompt, "Classify now.", model="llama-3.3-70b-versatile")
        from app.services.conversation_service import ConversationService
        return ConversationService.safe_json_extract(raw) or {"intent": "INFO", "optimized_query": user_msg}

class SynthesisAgent:
    """Specialized Agent for crafting the final conversational response."""
    
    @staticmethod
    def craft_response(user_msg: str, context: str, intent: str, user_mem: Dict[str, Any], system_prompt: str) -> str:
        """
        Synthesizes the final response using provided context and brand voice.
        """
        # We use the existing SALES/INFO/SUPPORT prompts but with a cleaner mission
        # since classification/RAG-optimization are already done.
        
        full_context = f"Context: {context}\n\nUser Question: {user_msg}"
        return AIService.run_llm(system_prompt, full_context, model="llama-3.3-70b-versatile")

class RAGAgent:
    """Specialized Agent for retrieval optimization and ranking (Phase 2)."""
    
    @staticmethod
    def optimize_and_search(query: str, limit: int = 4, threshold: float = 0.35) -> List[str]:
        from app.services.rag_service import RagService
        # For now, we use the standard search, but we can add re-ranking logic here later.
        return RagService.search_knowledge_base(query, limit=limit, threshold=threshold)
