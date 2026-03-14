import os
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI
from google import genai

# Load environment variables
load_dotenv()

# --- System Flags ---
USE_MULTI_AGENT = False  # Set to True to enable specialized agent orchestration

# --- OpenRouter Configuration (Primary Engine) ---
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize OpenRouter Client
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- Legacy/Direct Fallbacks (Optional) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

genai_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
ai_client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1") if GROQ_API_KEY else None

# --- Supabase Configuration ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN")

# --- Email Configuration (Resend Agent) ---
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL") or "mohammedrawan653@gmail.com"

# --- WhatsApp Configuration (Twilio Agent) ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER") or "+14155238886"  # Twilio Sandbox Default
MOHAMED_WHATSAPP = os.getenv("MOHAMED_WHATSAPP") or "+201234567890" # Example Recipient

# --- Frontend Configuration ---
FRONTEND_URL = os.getenv("FRONTEND_URL") or "http://localhost:5173"

if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ Warning: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def get_supabase() -> Client:
    return supabase

def get_ai_client() -> OpenAI:
    return ai_client
