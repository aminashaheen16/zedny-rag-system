import asyncio
import os
import sys

# Add the current directory to sys.path to allow imports from app
sys.path.append(os.getcwd())

from app.services.rag_service import RagService
from app.utils.arabic_helper import normalize_arabic

async def sanity_check():
    query = "اي الشركات الي اشتغلتوا معاها"
    # Testing with various thresholds
    thresholds = [0.45, 0.35, 0.25, 0.20, 0.15]
    
    print(f"🔍 RAG SANITY CHECK")
    print(f"Query: {query}")
    print(f"Normalized: {normalize_arabic(query)}")
    print("-" * 30)
    
    import time
    from app.services.rag_service import COHERE_API_KEY
    
    print(f"📡 Using Key: {COHERE_API_KEY[:4]}...{COHERE_API_KEY[-4:] if COHERE_API_KEY else 'NONE'}")
    
    for t in thresholds:
        print(f"\n📡 Testing Threshold: {t}")
        results = RagService.search_knowledge_base(query, threshold=t, limit=5)
        time.sleep(2) # Avoid 5/min rate limit
        if results:
            print(f"✅ FOUND {len(results)} results!")
            for i, res in enumerate(results):
                print(f"  [{i+1}] {res[:100]}...")
        else:
            print(f"❌ RAG MISS")

if __name__ == "__main__":
    asyncio.run(sanity_check())
