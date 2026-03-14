import cohere
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('COHERE_API_KEY')
co = cohere.Client(key)

try:
    print(f"Testing key: {key[:4]}...{key[-4:]}")
    response = co.embed(
        texts=["test"],
        model="embed-multilingual-v3.0",
        input_type="search_query"
    )
    print("✅ Success! Embedding generated.")
    print(f"Dimensions: {len(response.embeddings[0])}")
except Exception as e:
    print(f"❌ Failed: {e}")
