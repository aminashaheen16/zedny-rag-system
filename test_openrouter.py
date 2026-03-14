"""
🚀 OPENROUTER INTEGRATION TEST
Verifies that the new OpenRouter-first strategy in AIService works correctly.
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from backend.app.services.ai_service import AIService
import logging

# Setup logging to see the flow
logging.basicConfig(level=logging.INFO)

def test_openrouter():
    print("\n" + "="*60)
    print("🚀 TESTING OPENROUTER INTEGRATION")
    print("="*60)
    
    system_prompt = "You are a helpful assistant for Zedny.ai (An Arabic Enterprise Training Platform). Respond briefly."
    user_message = "What is Zedny?"
    
    print(f"\n📡 Sending request to AIService (Default should be Claude 3.5 Sonnet via OpenRouter)...")
    
    start_time = 1706825400 # Mock start time for logic
    import time
    start = time.time()
    
    response = AIService.run_llm(system_prompt, user_message)
    
    end = time.time()
    duration = end - start
    
    print(f"\n⏱️ Response Time: {duration:.2f} seconds")
    print(f"\n🤖 AI Response:")
    print("-" * 30)
    print(response)
    print("-" * 30)
    
    if "Zedny" in response or "زدني" in response or "training" in response.lower():
        print("\n✅ SUCCESS: LLM integration is working and context-aware.")
    else:
        print("\n⚠️ WARNING: Response seems generic. Check if fallback occurred.")

def test_specific_model():
    print("\n" + "="*60)
    print("🧪 TESTING SPECIFIC MODEL (DeepSeek V3)")
    print("="*60)
    
    response = AIService.run_llm(
        "You are a logic expert.", 
        "Write a 1-sentence logic puzzle.", 
        model="deepseek/deepseek-chat"
    )
    
    print(f"\n🤖 DeepSeek Response:")
    print("-" * 30)
    print(response)
    print("-" * 30)

if __name__ == "__main__":
    try:
        test_openrouter()
        test_specific_model()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
