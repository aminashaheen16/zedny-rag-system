import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/chat"
TEST_QUERY = "إيه هو التعليم الترفيهي (Edutainment)؟"

def verify_sync():
    print(f"🚀 --- STARTING SYNC VERIFICATION --- 🚀")
    print(f"Query: {TEST_QUERY}\n")
    
    payload = {
        "message": TEST_QUERY,
        "user_email": "tester@zedny.ai",
        "session_id": f"sync_test_{int(time.time())}",
        "incident_state": None
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload, headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            context = data.get("context_used", "None")
            
            print(f"⏱️ Response Time: {end_time - start_time:.2f}s")
            print(f"\n[RAW RAG CONTEXT (FROM BACKEND)]:")
            print("-" * 30)
            print(context)
            print("-" * 30)
            
            print(f"\n[FINAL AI ANSWER (AS SENT TO FRONTEND)]:")
            print("=" * 60)
            print(answer)
            print("=" * 60)
            
            # Simple check
            if len(context) > 50 and len(answer) > 50:
                print("\n✅ BOTH Context and Answer are present.")
                # Basic detail check (Look for keywords from context in the answer)
                # Note: This depends on the specific RAG data
                keywords = ["زدني", "Zedny", "التعلم", "التفاعل"]
                found_keywords = [k for k in keywords if k in answer]
                print(f"   Found keywords in answer: {found_keywords}")
            else:
                print("\n❌ DATA MISMATCH: One of them is empty or too short.")
                
        else:
            print(f"❌ API ERROR: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    verify_sync()
