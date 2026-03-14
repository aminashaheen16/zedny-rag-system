import json
import os
import sys
import cohere
from typing import List

# Add parent directory to path to access app modules if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import COHERE_API_KEY

# Source and Target Paths
SOURCE_KB_PATH = r"d:\New folder (33) - copy\ZEDNY_Technical_Troubleshooting_KB.json"
TARGET_INDEX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TARGET_INDEX_PATH = os.path.join(TARGET_INDEX_DIR, "tech_kb_index.json")

def get_embedding(text: str, client: cohere.Client) -> List[float]:
    """Generate embedding using Cohere"""
    try:
        response = client.embed(
            texts=[text],
            model="embed-multilingual-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"[ERROR] Error generating embedding: {e}")
        return []

def build_index():
    print("[INFO] Starting Isolated Tech Index Build...")

    # 1. Setup Environment
    if not COHERE_API_KEY:
        print("[ERROR] COHERE_API_KEY not found in environment variables!")
        return

    client = cohere.Client(COHERE_API_KEY)
    
    if not os.path.exists(TARGET_INDEX_DIR):
        os.makedirs(TARGET_INDEX_DIR)
        print(f"[INFO] Created directory: {TARGET_INDEX_DIR}")

    # 2. Load Source Data
    try:
        with open(SOURCE_KB_PATH, "r", encoding="utf-8") as f:
            kb_data = json.load(f)
            chunks = kb_data.get("chunks", [])
            print(f"[INFO] Loaded {len(chunks)} chunks from source KB.")
    except Exception as e:
        print(f"[ERROR] Failed to read source file: {e}")
        return

    # 3. Process & Embed
    indexed_chunks = []
    print("[INFO] Generating Embeddings (Cohere Multilingual v3.0)...")
    
    for i, chunk in enumerate(chunks):
        # Create a rich representation for embedding
        # Title + Content is usually sufficient for semantic matching
        text_to_embed = f"{chunk['title']}\n{chunk['content']}"
        
        embedding = get_embedding(text_to_embed, client)
        
        if embedding:
            chunk["embedding"] = embedding
            indexed_chunks.append(chunk)
            print(f"   [INDEXED] Chunk #{i+1}")
        else:
            print(f"   [SKIPPED] Chunk #{i+1} (No embedding)")

    # 4. Save Index
    try:
        with open(TARGET_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(indexed_chunks, f, ensure_ascii=False, indent=2)
        print(f"\n[SUCCESS] Index saved successfully to: {TARGET_INDEX_PATH}")
        print(f"[INFO] Total Indexed Documents: {len(indexed_chunks)}")
    except Exception as e:
        print(f"[ERROR] Failed to save index file: {e}")

if __name__ == "__main__":
    build_index()
