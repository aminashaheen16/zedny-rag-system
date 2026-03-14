from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api import chat, reports
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- ZEDNY BACKEND: Starting Up ---")
    yield
    print("--- ZEDNY BACKEND: Shutting Down ---")

app = FastAPI(
    title="Zedny Elite Support API",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://0.0.0.0:8000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, tags=["Conversation"])
app.include_router(reports.router, tags=["Admin & Stats"])

@app.get("/")
async def root():
    return {
        "status": "Zedny Backend is Running",
        "architecture": "Modular Micro-services",
        "cloud": "Supabase Enabled",
        "ai": "Gemini/Groq Hybrid"
    }
