
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ai_service import AIService

def test_gemini():
    print("🚀 Testing Gemini with NEW SDK...")
    # Explicitly request a gemini model to force use of the new SDK logic
    res = AIService.run_llm("You are a helpful assistant.", "Hello, who are you?", model="gemini-1.5-flash")
    print(f"\n🤖 AI Response: {res}")
    
    if "gemini" in res.lower() or "assistant" in res.lower() or len(res) > 5:
        print("\n✅ SUCCESS: Gemini responded via new SDK!")
    else:
        print("\n❌ FAILURE: Response seems empty or corrupted.")

if __name__ == "__main__":
    test_gemini()
