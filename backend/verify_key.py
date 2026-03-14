import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('COHERE_API_KEY')
if key:
    print(f"Key loaded: {key[:4]}...{key[-4:]}")
else:
    print("Key NOT found in .env")
