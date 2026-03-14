import os
from dotenv import load_dotenv
import requests

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
if not supabase_url:
    print("SUPABASE_URL not found in .env")
else:
    print(f"Testing connectivity to: {supabase_url}")
    try:
        response = requests.get(supabase_url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print("Successfully connected to Supabase URL.")
    except Exception as e:
        print(f"Failed to connect: {e}")
