"""
Test Script: Verify RAG and Issue Diagnostic Flow
=================================================
This script tests:
1. INFO query → Should hit RAG and return chunks
2. ISSUE query → Should NOT hit RAG, should diagnose with prompting
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
import time

API_URL = "http://localhost:8000/chat"

def test_query(message, description):
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"[USER]: {message}")
    
    payload = {
        "message": message,
        "user_email": "test@test.com",
        "session_id": f"test_{int(time.time())}"  # Fresh session each time
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        answer = data.get("answer", "No answer")
        context_used = data.get("context_used", "None")
        
        print(f"\n[AI RESPONSE]:\n{answer[:500]}...")  # First 500 chars
        print(f"\n[CONTEXT USED]: {context_used[:200] if context_used else 'None'}...")
        
        # Check if RAG was used
        if context_used and context_used != "None" and len(context_used) > 10:
            print(f"\n✅ RAG WAS USED (Chunks returned)")
        else:
            print(f"\n❌ RAG NOT USED (Pure LLM)")
            
        return data
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "="*60)
    print("STARTING RAG & ISSUE FLOW TESTS")
    print("="*60)
    
    # Test 1: INFO query (should use RAG)
    test_query(
        "ما هي الكورسات المتاحة؟",
        "INFO Query - Should use RAG"
    )
    
    time.sleep(2)
    
    # Test 2: ISSUE query (should NOT use RAG)
    test_query(
        "الفيديو مش شغال عندي وبيعلق",
        "ISSUE Query - Should NOT use RAG, Should Diagnose"
    )
    
    print("\n" + "="*60)
    print("TESTS COMPLETED")
    print("="*60)
