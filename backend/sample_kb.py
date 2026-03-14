import os
import json
from app.core.config import supabase

def sample_knowledge_base():
    print("--- [SAMPLING KNOWLEDGE BASE] ---")
    try:
        # Fetch first 20 records from knowledge_chunks
        res = supabase.table("knowledge_chunks").select("content, metadata").limit(20).execute()
        
        if not res.data:
            print("❌ No data found in knowledge_base table.")
            return
            
        print(f"✅ Found {len(res.data)} sample records.")
        for i, row in enumerate(res.data):
            print(f"\n--- Record #{i+1} ---")
            print(f"Content Sample: {row['content'][:200]}...")
            print(f"Metadata: {row['metadata']}")
            
    except Exception as e:
        print(f"❌ Error sampling knowledge base: {e}")

if __name__ == "__main__":
    sample_knowledge_base()
