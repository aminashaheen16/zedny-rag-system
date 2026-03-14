import sys
import os
import asyncio

# Fix Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.tech_service import TechService

# Mock Objects
tech_service = TechService
tech_service.load_index()

async def test_search():
    print("\n[TEST] TEST 1: Semantic Search Accuracy")
    queries = [
        ("الفيديو بيقطع والنت سريع", "Video Buffering"),
        ("Cert download failed", "Certificate Issue"), 
        ("My employees need training", "None") 
    ]
    
    for i, (q, expected) in enumerate(queries):
        # Don't print the query if it has Arabic, just print ID
        res = tech_service.search(q)
        match_found = "YES" if res else "NO"
        print(f"   Query #{i+1}: Match Found? {match_found}")

if __name__ == "__main__":
    asyncio.run(test_search())
