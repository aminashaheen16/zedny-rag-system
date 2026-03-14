"""
Re-Index Supabase Knowledge Base with New Embedding Model

This script:
1. Loads the RAG data from JSON
2. Generates new embeddings using the updated model (text-multilingual-embedding-002)
3. Updates Supabase knowledge_chunks table with new vectors
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import supabase, genai_client, EMBED_MODEL
from google.genai import types

def load_rag_data():
    """Load RAG data from JSON file"""
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ZEDNY_RAG_Optimized.json")
    print(f"Loading from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

from sentence_transformers import SentenceTransformer

# Load the local model
# BGE-M3 is SOTA for Multilingual RAG (Arabic support is excellent)
print("[0/3] Initializing SOTA embedding model (BAAI/bge-m3)...")
local_model = SentenceTransformer('BAAI/bge-m3')

def generate_embedding(text: str):
    """Generate embedding using local Sentence-Transformers model"""
    try:
        # Generate embedding locally
        embedding = local_model.encode(text).tolist()
        return embedding
    except Exception as e:
        print(f"Local Embedding Error: {e}")
        raise

def re_index():
    """Re-index all chunks with new embeddings"""
    print("=" * 60)
    print(f"🚀 Re-Indexing Knowledge Base with {EMBED_MODEL}")
    print("=" * 60)
    
    # Load data
    print("\n[1/3] Loading RAG data...")
    data = load_rag_data()
    chunks = data.get("chunks", [])
    print(f"✅ Loaded {len(chunks)} chunks")
    
    # Clear existing data (Ensuring clean state)
    print("\n[2/3] Clearing old embeddings...")
    try:
        # Use a numeric condition for bigint IDs
        supabase.table("knowledge_chunks").delete().gt("id", 0).execute()
        print("✅ Old data cleared")
    except Exception as e:
        print(f"⚠️ Could not clear old data: {e}")
    
    # Re-index with Batch Processing (Speed Optimization)
    BATCH_SIZE = 32
    print(f"\n[3/3] Generating embeddings and uploading (Batch Size: {BATCH_SIZE})...")
    success_count = 0
    error_count = 0
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_contents = [c["content"] for c in batch]
        
        try:
            # Batch generate embeddings (VECTORIZED - much faster)
            embeddings = local_model.encode(batch_contents, normalize_embeddings=True).tolist()
            
            # Prepare batch data for Supabase
            batch_data = []
            for idx, chunk in enumerate(batch):
                batch_data.append({
                    "content": chunk["content"],
                    "embedding": embeddings[idx],
                    "metadata": chunk.get("metadata", {}),
                    "title": chunk.get("title", "")
                })
            
            # Batch Insert into Supabase (REDUCES ROUND-TRIPS)
            supabase.table("knowledge_chunks").insert(batch_data).execute()
            
            success_count += len(batch)
            print(f"   Progress: {min(i + BATCH_SIZE, len(chunks))}/{len(chunks)} chunks processed...")
                
        except Exception as e:
            error_count += len(batch)
            print(f"❌ Error in batch {i//BATCH_SIZE + 1}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ RE-INDEXING COMPLETE")
    print("=" * 60)
    print(f"Total Chunks: {len(chunks)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"Model Used: {EMBED_MODEL}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        re_index()
    except KeyboardInterrupt:
        print("\n\n⚠️ Re-indexing cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        sys.exit(1)
