import json
import os
import math
import cohere
from typing import List, Dict, Optional
from app.core.config import COHERE_API_KEY

# Path to the isolated index
INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "tech_kb_index.json")

class TechService:
    _index: List[Dict] = []
    _cohere_client: Optional[cohere.Client] = None

    @classmethod
    def load_index(cls):
        """Load the JSON index into memory on startup"""
        if cls._index:
            return  # Already loaded

        if not os.path.exists(INDEX_PATH):
            print(f"[WARN] Tech Index not found at {INDEX_PATH}. Please run build_tech_index.py")
            return

        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                cls._index = json.load(f)
            print(f"[INFO] TechService: Loaded {len(cls._index)} solutions from isolated index.")
            
            if COHERE_API_KEY:
                cls._cohere_client = cohere.Client(COHERE_API_KEY)
            else:
                print("[WARN] TechService: COHERE_API_KEY missing. Search will fail.")
                
        except Exception as e:
            print(f"[ERROR] TechService: Failed to load index: {e}")

    @classmethod
    def cosine_similarity(cls, v1: List[float], v2: List[float]) -> float:
        """Compute cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a * a for a in v1))
        magnitude2 = math.sqrt(sum(b * b for b in v2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    @classmethod
    def search(cls, query: str, threshold: float = 0.4, exclude_ids: List[str] = None) -> Optional[Dict]:
        """
        Semantic search for the best technical solution.
        1. Embed the query.
        2. Compare against in-memory index.
        3. Return the best match if score > threshold.
        """
        if exclude_ids is None:
            exclude_ids = []
            
        if not cls._index:
            cls.load_index()
        
        if not cls._index or not cls._cohere_client:
            return None

        try:
            # 1. Embed Query
            response = cls._cohere_client.embed(
                texts=[query],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            )
            query_embedding = response.embeddings[0]

            # 2. Find Best Match
            best_score = -1
            best_doc = None

            for doc in cls._index:
                # 🛑 EXCLUSION CHECK
                doc_id = doc.get("chunk_id")
                if doc_id in exclude_ids:
                    continue

                doc_embedding = doc.get("embedding")
                if not doc_embedding: 
                    continue
                
                score = cls.cosine_similarity(query_embedding, doc_embedding)
                if score > best_score:
                    best_score = score
                    best_doc = doc

            # Safe logging
            print(f"--- [TECH SEMANTIC MATCH] Best Score: {best_score:.4f} | Excluded: {len(exclude_ids)}")

            # 3. Return if above threshold
            if best_score >= threshold and best_doc:
                best_doc["score"] = best_score
                return best_doc
                
            return None

        except Exception as e:
            print(f"[ERROR] TechService Search Error: {e}")
            return None
