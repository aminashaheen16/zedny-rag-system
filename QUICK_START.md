# 📘 Zedny Elite - Quick Start Guide

## 🚀 How to Run the Application

### Option 1: Automated Startup (Recommended)

```powershell
# From project root
.\START_ZEDNY.ps1
```

This script will:
1. ✅ Kill any old backend instances
2. ✅ Verify your `.env` configuration
3. ✅ Start the backend on port 8000
4. ✅ Provide instructions for the frontend

After the script runs, **open a new terminal** and run:
```bash
npm run dev
```

### Option 2: Manual Startup

#### Backend
```powershell
cd backend
py -m uvicorn app.main:app --reload --port 8000
```

#### Frontend (in a separate terminal)
```powershell
# From project root
npm run dev
```

---

## 🔗 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Customer chat interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |

---

## ⚙️ Configuration Checklist

Before running, ensure you have:

- [x] **Node.js** 18+ installed
- [x] **Python** 3.11+ installed
- [x] **`.env` file** in `backend/` with:
  - `COHERE_API_KEY` (for RAG embeddings)
  - `OPENROUTER_API_KEY` (for AI models)
  - `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`
  - `RESEND_API_KEY` (for email notifications)

---

## 🐛 Troubleshooting

### Frontend can't connect to backend

**Symptom:** `Failed to fetch` or `ERR_CONNECTION_REFUSED`

**Solution:**
1. Verify backend is running: http://localhost:8000
2. Check for multiple backend instances:
   ```powershell
   Get-Process python | Where-Object {$_.CommandLine -like "*uvicorn*"}
   ```
3. Kill duplicates and restart with `START_ZEDNY.ps1`

### RAG MISS errors in backend logs

**Symptom:** `💀💀💀 [RAG MISS] No context found`

**Solution:**
1. Check Cohere API key quota (1000 calls/month for trial)
2. Verify key in `.env`: `COHERE_API_KEY=xxxxx`
3. Restart backend to reload environment variables

### Port 8000 already in use

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

---

## 📚 Full Documentation

For comprehensive technical documentation, see:
- **[ZEDNY_DOCUMENTATION.md](./ZEDNY_DOCUMENTATION.md)** - Complete architecture, API reference, and deployment guide

---

## 🎯 Quick Test

After starting both services, test the connection:

```bash
# Test backend health
curl http://localhost:8000

# Expected response:
# {
#   "status": "Zedny Backend is Running",
#   "architecture": "Modular Micro-services",
#   "cloud": "Supabase Enabled",
#   "ai": "Gemini/Groq Hybrid"
# }
```

Then open http://localhost:5173 and send a test message like:
- "مرحباً" (Arabic greeting)
- "What is Zedny?" (English info query)

---

**Last Updated:** February 3, 2026
