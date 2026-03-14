"""
Check if Supabase knowledge base needs re-indexing
"""
from app.core.config import supabase

print("🔍 Checking Supabase knowledge base...\n")

try:
    # Check if knowledge_base table exists
    res = supabase.table("knowledge_base").select("*").limit(1).execute()
    
    if res.data:
        # Table exists, check embedding dimensions
        first_entry = res.data[0]
        
        if "embedding" in first_entry:
            embedding_dims = len(first_entry["embedding"])
            print(f"✅ Knowledge base found!")
            print(f"   Current embedding dimensions: {embedding_dims}")
            
            if embedding_dims == 2048:
                print(f"\n⚠️  OLD BGE-M3 embeddings detected!")
                print(f"   → You NEED to re-index with hybrid strategy")
            elif embedding_dims == 384:
                print(f"\n✅ MiniLM embeddings (English) - OK")
            elif embedding_dims == 1024:
                print(f"\n✅ Cohere embeddings (Arabic) - OK")
            else:
                print(f"\n🤔 Unknown embedding model ({embedding_dims} dims)")
        else:
            print("⚠️  No embeddings found in knowledge base")
    else:
        print("ℹ️  No knowledge base found in Supabase")
        print("   → Using only solutions_db.py (keyword matching)")
        print("   → No re-indexing needed! ✅")
        
except Exception as e:
    print(f"ℹ️  Table 'knowledge_base' doesn't exist")
    print(f"   → Using only solutions_db.py")
    print(f"   → No re-indexing needed! ✅")
