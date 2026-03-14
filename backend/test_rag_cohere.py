"""
Quick test: Verify RAG works with new Cohere embeddings
"""
from app.services.rag_service import RagService

print("🧪 Testing RAG with Cohere embeddings...\n")

# Test 1: Arabic query
print("--- Test 1: Arabic Query ---")
query_ar = "ايه هي زدني؟"
results_ar = RagService.search_knowledge_base(query_ar, detected_lang="ar")
print(f"Query: {query_ar}")
print(f"Results: {len(results_ar)} chunks found")
if results_ar:
    print(f"Sample: {results_ar[0][:100]}...")
print()

# Test 2: English query
print("--- Test 2: English Query ---")
query_en = "What is ZEDNY?"
results_en = RagService.search_knowledge_base(query_en, detected_lang="en")
print(f"Query: {query_en}")
print(f"Results: {len(results_en)} chunks found")
if results_en:
    print(f"Sample: {results_en[0][:100]}...")
print()

if results_ar and results_en:
    print("✅ RAG is working with Cohere embeddings!")
    print("🚀 Ready for deployment!")
else:
    print("⚠️  RAG not returning results - check embeddings")
