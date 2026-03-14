from typing import List, Dict, Any, Optional
from app.core.config import supabase
from app.core.solutions_db import SOLUTIONS_DB
import cohere
import os

# Initialize Cohere client for ALL queries (English + Arabic)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None

def get_embedding_cohere(text: str, input_type: str = "search_query") -> List[float]:
    """
    🎯 COHERE-ONLY STRATEGY (1024 dims for ALL languages)
    - Works with existing Supabase column (1024 dims)
    - Excellent quality for both Arabic & English
    - Free tier: 1000 calls/month (663 records = ✅ fits!)
    """
    if not co:
        raise ValueError("COHERE_API_KEY not set!")
    
    try:
        response = co.embed(
            texts=[text],
            model="embed-multilingual-v3.0",
            input_type=input_type
        )
        print(f"--- [COHERE API] Embedding generated (1024 dims) ---")
        return response.embeddings[0]
    except Exception as e:
        print(f"--- [COHERE ERROR] {e}")
        raise

class RagService:
    @staticmethod
    def search_knowledge_base(
        query: str, 
        threshold: float = 0.35,  # 🎯 REFINED: Lowered from 0.45 for better recall
        detected_lang: str = "en",  # For logging only
        limit: int = 4
    ) -> List[str]:
        """
        UPDATED: Search knowledge base using COHERE-ONLY strategy.
        Accepts a dynamic 'limit' (default 4) for flexible context retrieval.
        """
        try:
            # Get embedding using Cohere
            query_embedding = get_embedding_cohere(query)
            
            # Search Supabase via match_knowledge RPC
            res = supabase.rpc("match_knowledge", {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }).execute()
            
            if res.data:
                print(f"--- [RAG HIT] Found {len(res.data)} results (Limit: {limit}) ---")
                for i, r in enumerate(res.data):
                    print(f"      [{i+1}] Score: {r.get('similarity', 'N/A')} | Title: {r.get('title', 'N/A')}")
                return [r["content"][:1500] for r in res.data]
            else:
                print(f"--- [RAG MISS] No results above threshold ({threshold}) ---")
                
        except Exception as e:
            print(f"--- [RAG ERROR] {e}")
            
        return []

    @staticmethod
    def search_local_solutions(
        problem_description: str, 
        exclude_ids: List[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        🚀 HYBRID APPROACH: Search local solutions with scoring, whole-word matching,
        synonym expansion, and Egyptian slang normalization.
        """
        import re
        from app.core.solutions_db import normalize_egyptian_slang, expand_with_synonyms
        
        if exclude_ids is None:
            exclude_ids = []
        
        # Step 0: Normalize and expand the problem description
        from app.utils.arabic_helper import normalize_arabic
        
        # 🛡️ NORMALIZATION: Standardize Arabic variations (ه vs ة, etc.)
        problem_norm_ar = normalize_arabic(problem_description)
        
        # 🗣️ SLANG & SYNONYMS: Use original + slang + synonyms
        problem_normalized = normalize_egyptian_slang(problem_norm_ar)
        problem_expanded = expand_with_synonyms(problem_normalized)
        problem_lower = problem_expanded.lower()
        
        print(f"--- [LOCAL RAG] Original: {problem_description}")
        print(f"--- [LOCAL RAG] Normalized: {problem_norm_ar}")
        print(f"--- [LOCAL RAG] Expanded: {problem_lower[:100]}...")
        
        candidates = []
        
        # Step 1: Score all solutions
        for solution in SOLUTIONS_DB:
            if solution["solution_id"] in exclude_ids:
                continue
                
            score = 0
            for keyword in solution["symptom_keywords"]:
                # 🛡️ KEYWORD NORMALIZATION: Normalize the keyword itself for robust matching
                k_norm = normalize_arabic(keyword)
                
                # 🧲 ROBUST ARABIC MATCHING: Allow optional 'ال' prefix for each word in the keyword
                parts = k_norm.split()
                flex_pattern = r'\s+'.join([rf'(?:ال)?{re.escape(p)}' for p in parts])
                
                # Full pattern allowing for Arabic prefixes
                pattern = rf"(?:^|\s|[بلوفك])?{flex_pattern}(?:\s|$)"
                
                if re.search(pattern, problem_lower):
                    # Give higher weight to matches in specific categories vs Universal
                    weight = 2 if solution["category"] != "UNIVERSAL" else 1
                    score += weight
            
            if score > 0:
                candidates.append({
                    "solution": solution,
                    "score": score,
                    "priority": solution.get("priority", 99)
                })
        
        # Step 2: Sort by Score (DESC) then Priority (ASC)
        # Higher score wins. If same score, lower priority (more important) wins.
        candidates.sort(key=lambda x: (-x["score"], x["priority"]))
        
        if candidates:
            selected = candidates[0]["solution"]
            print(f"--- [LOCAL RAG] Selected: {selected['solution_id']} (Score: {candidates[0]['score']}, Priority: {selected['priority']}) ---")
            return selected
        
        return None


