"""
Detailed check of knowledge_chunks table
"""
from app.core.config import supabase

print("🔍 Checking 'knowledge_chunks' table...\n")

try:
    # Get first few records
    res = supabase.table('knowledge_chunks').select('*').limit(3).execute()
    
    if res.data:
        first_record = res.data[0]
        
        print(f"✅ Table 'knowledge_chunks' found!")
        print(f"   Total records: {len(res.data)} (showing first 3)")
        print(f"\n📋 Columns: {list(first_record.keys())}")
        
        # Check for embedding column
        embedding_col = None
        for col in first_record.keys():
            if 'embed' in col.lower():
                embedding_col = col
                break
        
        if embedding_col:
            embedding = first_record[embedding_col]
            if embedding:
                dims = len(embedding)
                print(f"\n✅ Embeddings found!")
                print(f"   Column name: '{embedding_col}'")
                print(f"   Dimensions: {dims}")
                print(f"   Sample (first 5): {embedding[:5]}")
                
                # Determine model type
                if dims == 1024:
                    print(f"\n🎯 Model Type: BGE-M3 (1024 dims)")
                    print(f"   ⚠️  RE-INDEX NEEDED!")
                    print(f"   → Switch to: MiniLM (384) + Cohere (1024)")
                elif dims == 384:
                    print(f"\n🎯 Model Type: MiniLM-L6 (384 dims)")
                    print(f"   ✅ Already optimized for English!")
                elif dims == 2048:
                    print(f"\n🎯 Model Type: Old BGE-M3 (2048 dims)")
                    print(f"   ⚠️  DEFINITELY RE-INDEX NEEDED!")
                else:
                    print(f"\n🤔 Unknown model ({dims} dimensions)")
            else:
                print(f"\n⚠️  Embedding column exists but is NULL")
        else:
            print(f"\n❌ No embedding column found")
        
        # Show sample content
        if 'content' in first_record:
            content = first_record['content']
            print(f"\n📄 Sample content: {content[:100]}...")
        
        # Check language
        if 'language' in first_record:
            print(f"   Language: {first_record['language']}")
            
    else:
        print("ℹ️  Table exists but is empty")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print(f"\n💡 Table might not exist or permission issue")

print("\n" + "="*50)
print("🎯 RECOMMENDATION:")
print("="*50)
