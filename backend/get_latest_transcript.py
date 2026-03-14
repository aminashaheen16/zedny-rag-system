from app.core.config import supabase
import json

def get_mohamed_data():
    try:
        print("\n--- [SEARCHING FOR MOHAMMED DATA] ---")
        
        # 1. Search users for anything matching 'mohamed' or 'mohammed'
        res_users = supabase.table("users").select("*").or_("name.ilike.%mohamed%,name.ilike.%mohammed%,email.ilike.%mohamed%,email.ilike.%mohammed%").execute()
        
        emails = [u.get('email', '').lower() for u in res_users.data if u.get('email')]
        print(f"Matched Emails: {emails}")

        # 2. Check Recent Sessions
        print("\n--- [RELEVANT SESSIONS] ---")
        res_sessions = supabase.table("chat_sessions").select("*").order("updated_at", desc=True).limit(20).execute()
        for sess in res_sessions.data:
            history = sess.get("history", []) or []
            history_str = " ".join([str(m) for m in history]).lower()
            user_email = (sess.get("user_email") or "").lower()
            
            is_mohamed = any(e in user_email for e in emails if e) or "mohamed" in history_str or "mohammed" in history_str
            
            if is_mohamed:
                print(f"\nSession ID: {sess['id']} | User: {sess.get('user_email')} | Status: {sess.get('status')}")
                for msg in history:
                    print(f"  {msg}")

        # 3. Check Recent Reports
        print("\n--- [RELEVANT REPORTS] ---")
        res_reports = supabase.table("reports").select("*").order("timestamp", desc=True).limit(20).execute()
        for rep in res_reports.data:
            history = rep.get("history", []) or []
            history_str = " ".join([str(m) for m in history]).lower()
            user_email = (rep.get("user_email") or "").lower()
            customer_name = (rep.get("customer_name") or "").lower()
            
            is_mohamed = any(e in user_email for e in emails if e) or "mohamed" in history_str or "mohammed" in history_str or "mohamed" in customer_name
            
            if is_mohamed:
                print(f"\nReport ID: {rep['id']} | Cat: {rep['category']} | User: {rep['user_email']}")
                for msg in history:
                    print(f"  {msg}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_mohamed_data()
