"""
Re-index knowledge_chunks with COHERE-ONLY Strategy (1024 dims)
"""
from app.core.config import supabase
from app.services.rag_service import get_embedding_cohere
import time

print("🚀 Starting Re-indexing Process (COHERE-ONLY)...\n")
print("=" * 60)

# Step 1: Get all records
print("\n📊 Step 1: Fetching all knowledge_chunks...")
res = supabase.table('knowledge_chunks').select('id, content').execute()

if not res.data:
    print("❌ No data found!")
    exit()

total_records = len(res.data)
print(f"✅ Found {total_records} records to re-index")
print(f"   Strategy: Cohere-only (1024 dims)")
print(f"   Free tier limit: 1000 calls/month")
print(f"   Status: {'✅ Within limit!' if total_records <= 1000 else '⚠️ Exceeds free tier'}")

# Step 2: Re-embed with Cohere
print("\n🎯 Step 2: Re-embedding ALL records with Cohere...")
print("   (This will take a few minutes...)\n")

success_count = 0
error_count = 0

for i, record in enumerate(res.data, 1):
    try:
        record_id = record['id']
        content = record['content']
        
        # Generate embedding using Cohere (1024 dims)
        new_embedding = get_embedding_cohere(content, input_type="search_document")
        
        # Update in Supabase
        supabase.table('knowledge_chunks').update({
            'embedding': new_embedding
        }).eq('id', record_id).execute()
        
        success_count += 1
        
        # Progress indicator
        if i % 10 == 0 or i == total_records:
            progress = (i / total_records) * 100
            print(f"   Progress: {i}/{total_records} ({progress:.1f}%) - {success_count} ✅")
        
        # Rate limit (to avoid overwhelming Cohere API)
        time.sleep(0.3)  # ~3 requests/sec
            
    except Exception as e:
        error_count += 1
        print(f"   ❌ Error on record {record_id}: {str(e)[:80]}")
        time.sleep(1)  # Longer pause on error

# Step 3: Summary
print("\n" + "=" * 60)
print("🎉 RE-INDEXING COMPLETE!")
print("=" * 60)
print(f"✅ Successfully re-indexed: {success_count}/{total_records}")
print(f"❌ Errors: {error_count}")

if error_count > 0:
    print(f"\n⚠️  {error_count} records failed. Check logs above.")
else:
    print(f"\n✅ All records successfully re-indexed!")
    
print(f"\n📊 New embedding dimensions: 1024 (Cohere)")
print(f"💰 Cohere API calls used: {success_count}")
print(f"   Remaining in free tier: {1000 - success_count}")
print(f"\n🚀 Ready for deployment on Railway!")
print(f"   RAM usage: ~200MB (no local model) ✅")
