"""
🧪 DIRECT LLM TEST
Tests AIService.run_llm directly to see internal errors.
"""

from app.services.ai_service import AIService
import logging

# Enable logging to console
logging.basicConfig(level=logging.INFO)

def test_direct():
    print("\nStarting Direct LLM Test...")
    prompt = "You are a helpful assistant."
    msg = "Say 'Hello Zedny' if you can hear me."
    
    # Test for OpenRouter specific model
    print("\n--- Testing OpenRouter (Gemini 2.0 Flash) ---")
    res1 = AIService.run_llm(prompt, msg, model="google/gemini-2.0-flash-001")
    print(f"Result: {res1}")
    
    # Test for Tech Intent (Should use DeepSeek Free)
    print("\n--- Testing Tech Intent (DeepSeek) ---")
    res2 = AIService.run_llm(prompt, msg, intent="Tech")
    print(f"Result: {res2}")

if __name__ == "__main__":
    test_direct()
