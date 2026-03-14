
from app.api.chat import is_pure_english
from app.services.conversation_service import ConversationService, FirstMessageGuard, UserIntent
from app.models.schemas import IncidentState
import json

def test_language_and_intent():
    test_cases = [
        "مين زدني",
        "Who is Zedny?",
        "مين Zedny",
        "مشكلة",
        "I have a problem",
        "hello",
        "اهلاً"
    ]
    
    state = IncidentState(session_id="test_session", user_email="test@test.com")
    
    print(f"{'Text':<20} | {'Pure EN':<7} | {'FM Guard Intent':<15} | {'Brain Intent':<12} | {'Brain Lang':<10}")
    print("-" * 75)
    
    for text in test_cases:
        pure_en = is_pure_english(text)
        fm_guard = FirstMessageGuard.protect_first_message(text)
        
        # Note: unified_strategic_brain hits the AI, let's see what it says
        try:
            brain = ConversationService.unified_strategic_brain(text, [], "", {}, "NEW")
            brain_intent = brain.get("intent", "N/A")
            brain_lang = brain.get("detected_language", "N/A")
        except Exception as e:
            brain_intent = f"Error: {e}"
            brain_lang = "N/A"
            
        print(f"{text:<20} | {str(pure_en):<7} | {str(fm_guard['intent']):<15} | {brain_intent:<12} | {brain_lang:<10}")

if __name__ == "__main__":
    test_language_and_intent()
