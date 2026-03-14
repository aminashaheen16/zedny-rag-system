import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import supabase

def check_schema():
    print("Checking 'knowledge_chunks' table schema...")
    try:
        # Try to get one result to see columns
        res = supabase.table("knowledge_chunks").select("*").limit(1).execute()
        if res.data:
            print(f"Columns found: {list(res.data[0].keys())}")
        else:
            print("Table is empty, checking column definitions via RPC or similar might be needed or just try a dummy insert.")
            # Alternatively, try to insert a dummy row with a wrong column to see the error message which lists valid columns
            try:
                supabase.table("knowledge_chunks").insert({"dummy_col": "val"}).execute()
            except Exception as e:
                print(f"Error (as expected, checking for column names): {e}")
    except Exception as e:
        print(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_schema()
