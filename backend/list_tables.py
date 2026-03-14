from app.core.config import supabase

def list_tables():
    print("--- [LISTING TABLES] ---")
    try:
        # Standard Postgres query for table names
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        # Supabase client doesn't support raw SQL easily unless there's an RPC
        # But we can try to guess or use RPC if it exists
        
        # Let's try to query a common hidden table or just list what we know
        tables = ["knowledge_chunks", "chat_sessions", "users", "reports", "ratings", "local_solutions"]
        for t in tables:
            try:
                res = supabase.table(t).select("count", count="exact").limit(1).execute()
                print(f"✅ Table '{t}' exists. Rows: {res.count}")
            except:
                print(f"❌ Table '{t}' does not exist or access denied.")
                
    except Exception as e:
        print(f"❌ Error listing tables: {e}")

if __name__ == "__main__":
    list_tables()
