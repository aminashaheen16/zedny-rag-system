
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def audit_latest_messages():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    supabase: Client = create_client(url, key)
    
    print("\n" + "="*60)
    print("📜 AUDITING LATEST 10 CHAT SESSIONS")
    print("="*60)
    
    # Get latest sessions
    sessions = supabase.table("chat_sessions").select("*").order("updated_at", desc=True).limit(10).execute()
    
    for session in sessions.data:
        print(f"\n🔹 Session: {session['id']} | Language: {session.get('language')} | Updated: {session['updated_at']}")
        history = session.get("history", [])
        if history:
            print(f"   Last 4 Messages:")
            for msg in history[-4:]:
                print(f"   - {msg[:200]}...")
        else:
            print("   (Empty History)")
            
if __name__ == "__main__":
    audit_latest_messages()
