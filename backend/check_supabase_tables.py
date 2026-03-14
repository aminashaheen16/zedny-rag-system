"""
Comprehensive Supabase database check
"""
from app.core.config import supabase

print("🔍 Scanning Supabase database...\n")

# List of tables to check
tables_to_check = [
    "knowledge_base",
    "knowledge", 
    "embeddings",
    "documents",
    "users",
    "sessions",
    "ratings"
]

found_tables = []

for table_name in tables_to_check:
    try:
        res = supabase.table(table_name).select("*").limit(1).execute()
        if res.data:
            first_row = res.data[0]
            columns = list(first_row.keys())
            
            # Check for embedding column
            has_embedding = any("embed" in col.lower() for col in columns)
            embedding_dims = None
            
            if has_embedding:
                for col in columns:
                    if "embed" in col.lower() and first_row.get(col):
                        embedding_dims = len(first_row[col])
                        break
            
            print(f"✅ Table '{table_name}' found!")
            print(f"   Columns: {columns[:5]}{'...' if len(columns) > 5 else ''}")
            print(f"   Has embeddings: {has_embedding}")
            if embedding_dims:
                print(f"   Embedding dimensions: {embedding_dims}")
                if embedding_dims == 1024:
                    print(f"   → Looks like BGE-M3 or Cohere embeddings")
                elif embedding_dims == 384:
                    print(f"   → Looks like MiniLM embeddings")
                elif embedding_dims == 2048:
                    print(f"   → Old BGE-M3 embeddings - NEEDS RE-INDEX!")
            print()
            found_tables.append(table_name)
        else:
            print(f"ℹ️  Table '{table_name}' exists but is empty")
    except Exception as e:
        if "does not exist" in str(e).lower() or "404" in str(e):
            pass  # Table doesn't exist, skip silently
        else:
            print(f"⚠️  Error checking '{table_name}': {str(e)[:50]}")

print(f"\n📊 Summary: Found {len(found_tables)} tables with data")

# Count total records in key tables
try:
    sessions_count = supabase.table("sessions").select("id", count="exact").execute()
    print(f"   → Sessions: {sessions_count.count if hasattr(sessions_count, 'count') else 'N/A'}")
except:
    pass

try:
    users_count = supabase.table("users").select("id", count="exact").execute()
    print(f"   → Users: {users_count.count if hasattr(users_count, 'count') else 'N/A'}")
except:
    pass
