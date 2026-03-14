"""
Re-index knowledge_chunks with Hybrid Embedding Strategy
"""
from app.core.config import supabase
from app.services.rag_service import get_embedding_hybrid
import time

print("🚀 Starting Re-indexing Process...\n")
print("=" * 60)

# Step 1: Get all records
print("\n📊 Step 1: Fetching all knowledge_chunks...")
res = supabase.table('knowledge_chunks').select('id, content').execute()

if not res.data:
    print("❌ No data found!")
    exit()

total_records = len(res.data)
print(f"✅ Found {total_records} records to re-index")

# Step 2: Detect language for each chunk
print("\n🔍 Step 2: Analyzing language distribution...")
import re

def detect_language(text: str) -> str:
    """Simple Arabic detection"""
    has_arabic = bool(re.search(r'[\u0600-\u06FF]', text))
    return "ar" if has_arabic else "en"

ar_count = 0
en_count = 0

for record in res.data:
    lang = detect_language(record['content'])  # Always detect from content
    if lang == 'ar':
        ar_count += 1
    else:
        en_count += 1

print(f"   Arabic chunks: {ar_count}")
print(f"   English chunks: {en_count}")

# Step 3: Re-embed with hybrid strategy
print("\n🎯 Step 3: Re-embedding with Hybrid Strategy...")
print("   (This will take a few minutes...)\n")

success_count = 0
error_count = 0

for i, record in enumerate(res.data, 1):
    try:
        record_id = record['id']
        content = record['content']
        
        # Detect language from content
        lang = detect_language(content)
        
        # Generate new embedding using hybrid strategy
        new_embedding = get_embedding_hybrid(content, detected_lang=lang)
        
        # Update in Supabase
        supabase.table('knowledge_chunks').update({
            'embedding': new_embedding
        }).eq('id', record_id).execute()
        
        success_count += 1
        
        # Progress indicator
        if i % 5 == 0 or i == total_records:
            progress = (i / total_records) * 100
            print(f"   Progress: {i}/{total_records} ({progress:.1f}%) - {success_count} ✅")
        
        # Rate limit (to avoid overwhelming Cohere API if many Arabic)
        if lang == 'ar':
            time.sleep(0.5)  # 2 requests/sec for Cohere
            
    except Exception as e:
        error_count += 1
        print(f"   ❌ Error on record {record_id}: {str(e)[:50]}")

# Step 4: Summary
print("\n" + "=" * 60)
print("🎉 RE-INDEXING COMPLETE!")
print("=" * 60)
print(f"✅ Successfully re-indexed: {success_count}/{total_records}")
print(f"❌ Errors: {error_count}")

if error_count > 0:
    print(f"\n⚠️  Some records failed. Check logs above.")
else:
    print(f"\n✅ All records successfully re-indexed!")
    
print(f"\n📊 New embedding dimensions:")
print(f"   English → MiniLM: 384 dims")
print(f"   Arabic → Cohere: 1024 dims")
print(f"\n💰 Estimated Cohere API calls: {ar_count}")
print(f"   (Within free tier: {ar_count <= 1000} ✅)")
