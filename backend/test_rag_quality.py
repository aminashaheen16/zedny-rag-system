import requests
import json
import time

API_URL = "http://localhost:8000/chat"

TEST_CASES = [
    {
        "query": "إيه هي زدني؟",
        "description": "Short General Info"
    },
    {
        "query": "التعليم الترفيهي",
        "description": "Specific Keyword (Edutainment)"
    },
    {
        "query": "Micro-learning",
        "description": "Technical Term"
    },
    {
        "query": "لوحات التحكم (Dashboards)",
        "description": "Feature Specific Query"
    },
    {
        "query": "مين المدربين؟",
        "description": "Granular Info Request"
    }
]

def run_quality_test():
    print(f"\n{'='*70}")
    print(f"🚀 RAG PRECISION TEST: Granular Arabic Queries")
    print(f"{'='*70}\n")
    
    for test in TEST_CASES:
        print(f"TEST: {test['description']}")
        print(f"USER: {test['query']}")
        
        payload = {
            "message": test["query"],
            "user_email": "tester@zedny.ai"
        }
        
        try:
            start_time = time.time()
            # Test with a slightly lower threshold for granular info
            payload["threshold"] = 0.35
            response = requests.post(API_URL, json=payload, timeout=60)
            latency = time.time() - start_time
            
            data = response.json()
            answer = data.get("answer", "No answer")
            context = data.get("context_used", "")
            
            print(f"Latency: {latency:.2f}s")
            print(f"AI: {answer[:400]}...")
            
            if context and len(context) > 100:
                print(f"✅ RAG MATCHED (Context Length: {len(context)})")
            else:
                print(f"❌ NO RAG CONTEXT (Fallback to LLM memory)")
                
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
        time.sleep(1)

if __name__ == "__main__":
    run_quality_test()
