import os
import sys

# Add parent directory to sys.path to import app modules
# C:\Users\COMPUTER   ONE\Desktop\source\repos\New folder (7)\backend
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Also ensure we can find 'app'
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.services.ai_service import AIService
from app.services.rag_service import RagService

def test_deepseek_rag():
    print("--- [TEST] Testing DeepSeek with Optimized RAG ---")
    
    query = "مين زدني واية الي بيميزها؟"
    print(f"User Query: {query}")
    
    # 1. Test RAG Retrieval
    chunks = RagService.search_knowledge_base(query)
    print(f"Retrieved Chunks: {len(chunks)}")
    
    context = "\n---\n".join(chunks)
    
    # 2. Test DeepSeek Synthesis (via OpenRouter)
    system_prompt = "أنت مساعد ذكي لشركة زدني. استخدم المعلومات المتاحة لتقديم إجابة احترافية ومقنعة."
    user_message = f"المعلومات المتاحة:\n{context}\n\nسؤال المستخدم: {query}"
    
    print("\n--- [Calling DeepSeek via OpenRouter] ---")
    # Using the first in the list we added to Priority in AIService
    response = AIService.run_llm(system_prompt, user_message, model="deepseek/deepseek-chat")
    
    print("\n--- [DeepSeek Response] ---")
    print(response)
    print("\n" + "="*50)

if __name__ == "__main__":
    test_deepseek_rag()
