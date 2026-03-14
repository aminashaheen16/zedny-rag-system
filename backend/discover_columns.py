import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import supabase

def discover_columns():
    test_columns = ["embedding", "vector", "content_vector", "embeddings", "content_embedding"]
    
    print("Attempting to discover embedding column name...")
    for col in test_columns:
        try:
            # Try to insert a dummy row (will fail if col doesn't exist)
            # Use data that satisfies other constraints if any (content is likely required)
            supabase.table("knowledge_chunks").insert({"content": "test", col: [0.1]*1024}).execute()
            print(f"✅ SUCCESS: Column '{col}' exists and accepts 1024-dim vectors!")
            return col
        except Exception as e:
            error_msg = str(e)
            if "Could not find the" in error_msg:
                print(f"❌ '{col}' not found.")
            elif "dimensions" in error_msg:
                print(f"⚠️ '{col}' exists BUT dimension mismatch: {error_msg}")
                return col
            else:
                print(f"❓ '{col}' error: {error_msg}")

    # If all fail, try to just select the first row and print keys again but more robustly
    try:
        res = supabase.table("knowledge_chunks").select("*").limit(1).execute()
        if res.data:
            print(f"Columns in first row: {list(res.data[0].keys())}")
        else:
            print("Table empty, no rows to inspect.")
    except Exception as e:
        print(f"Final select error: {e}")

if __name__ == "__main__":
    discover_columns()
