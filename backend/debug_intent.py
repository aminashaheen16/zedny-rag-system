from app.services.ai_service import AIService
import asyncio

async def debug_intent():
    history = [
        "User: نسيت كلمة المرور",
        "AI: يمكنك محاولة استعادة كلمة المرور عبر الايميل..."
    ]
    msg = "حولني لمهندس مش عايز ذكاء اصطناعي"
    
    print(f"--- [DEBUG] Testing Intent for: '{msg}'")
    result = AIService.interpret_tech_intent(msg, history)
    print(f"--- [RESULT] {result}")

if __name__ == "__main__":
    asyncio.run(debug_intent())
