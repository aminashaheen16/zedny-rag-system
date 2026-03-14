"""
🔍 SUPABASE LAST MESSAGE VIEWER
Queries the latest chat session to see what happened.
"""

from app.core.config import supabase
import json

def view_last_interaction():
    print("\n" + "="*80)
    print("👀 FETCHING LAST MESSAGE FROM DATABASE")
    print("="*80)
    
    try:
        # Get the most recently updated session
        res = supabase.table("chat_sessions").select("*").order("updated_at", desc=True).limit(1).execute()
        
        if res.data:
            session = res.data[0]
            history = session.get("history", [])
            
            print(f"📍 Session ID: {session.get('id')}")
            print(f"⏰ Updated At: {session.get('updated_at')}")
            print(f"📊 Intent: {session.get('category')}")
            print(f"🔢 Progress: Step {session.get('step')}")
            
            print("\n💬 Last 4 Messages in History:")
            print("-" * 40)
            
            # Show the last few messages for context
            last_msgs = history[-4:] if len(history) >= 4 else history
            for msg in last_msgs:
                print(msg)
                
            print("-" * 40)
            
        else:
            print("❌ No sessions found in chat_sessions table.")
            
    except Exception as e:
        print(f"❌ SUPABASE ERROR: {e}")

if __name__ == "__main__":
    view_last_interaction()
