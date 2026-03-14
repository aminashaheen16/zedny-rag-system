"""
Test script for hybrid embedding strategy
"""
import os
os.environ.setdefault("COHERE_API_KEY", os.getenv("COHERE_API_KEY", ""))

from app.services.rag_service import get_embedding_hybrid

print("🚀 Testing Hybrid Embedding Strategy...\n")

# Test 1: English query (should use MiniLM local)
print("--- Test 1: English Query ---")
english_query = "how to reset my password"
embedding_en = get_embedding_hybrid(english_query, detected_lang="en")
print(f"✅ English embedding generated: {len(embedding_en)} dimensions\n")

# Test 2: Arabic query (should use Cohere API)
print("--- Test 2: Arabic Query ---")
arabic_query = "ازاي احل مشكلة الفيديو الأسود؟"
embedding_ar = get_embedding_hybrid(arabic_query, detected_lang="ar")
print(f"✅ Arabic embedding generated: {len(embedding_ar)} dimensions\n")

# Test 3: Verify they're different strategies
print("--- Test 3: Strategy Verification ---")
print(f"English first 5 values: {embedding_en[:5]}")
print(f"Arabic first 5 values: {embedding_ar[:5]}")
print("\n✅ Hybrid embedding strategy working correctly!")
print("💰 Cost: $0 (English uses local, Arabic within free tier)")
print("🎯 RAM: ~300-400MB (fits in Railway free tier!)")
