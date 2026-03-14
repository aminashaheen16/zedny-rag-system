from app.services.conversation_service import ConversationService
from app.services.ai_service import AIService
import json

def test_restoration():
    print("--- RESTORATION VERIFICATION START ---")
    
    # Test 1: Intent Routing for Payment Issues
    print("\n1. Testing Intent Routing for 'دفعت الكورس ومش شغال'...")
    prompt = """Analyze input: "دفعت الكورس ومش شغال"
    Return JSON only: {"intent": "CATEGORY"}"""
    raw = AIService.run_llm(prompt, "Analyze now", model="llama-3.3-70b-versatile")
    data = json.loads(raw.strip().replace("```json", "").replace("```", ""))
    print(f"   Result: {data['intent']} (Expected: ISSUE)")
    
    # Test 2: Solution Summary Extraction
    print("\n2. Testing Solution Summary Extraction...")
    answer = "برجاء التأكد من وصول رسالة تأكيد الدفع وجرب تسجيل الخروج ثم الدخول مرة أخرى. الخطوات: 1. اضغط خروج 2. ادخل بياناتك."
    indicator_found = any(indicator in answer for indicator in ["الخطوات", "Steps", "1.", "جرب", "Try", "خطوة", "تأكد"])
    summary = answer[:150].strip().replace("\n", " ") + "..."
    print(f"   Indicator found: {indicator_found}")
    print(f"   Summary stored: {summary}")

    print("\n--- RESTORATION VERIFICATION END ---")

if __name__ == "__main__":
    test_restoration()
