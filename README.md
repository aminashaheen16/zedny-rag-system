# 🚀 Zedny Elite - AI-Powered Customer Support Platform

> **Enterprise-grade conversational AI for Arabic-speaking markets**

[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?style=flat&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://www.python.org/)

---

## 📖 Overview

**Zedny Elite** is a full-stack AI customer support platform that combines:
- 🤖 **Advanced NLP** with intent classification and multi-agent orchestration
- 📚 **RAG (Retrieval-Augmented Generation)** using Cohere embeddings + Supabase vector search
- 🌍 **Bilingual Support** for Arabic (MSA + Egyptian dialect) and English
- 🎯 **Smart Escalation** with automated ticket creation
- 📊 **Real-time Analytics** dashboard for performance monitoring

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Intelligent Routing** | Automatically classifies queries into SALES, SUPPORT, INFO, or GREETING |
| **RAG Knowledge Base** | Semantic search with 1024-dim embeddings (89% accuracy) |
| **Multi-Model AI** | Uses Gemini 2.0 Flash, Llama 3.3 70B via OpenRouter |
| **Session Management** | Persistent conversation history with Supabase |
| **Professional Escalation** | AI-generated summaries for sales/support teams |
| **Arabic-First Design** | Native support for Arabic text normalization |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[📘 Technical Documentation](./ZEDNY_DOCUMENTATION.md)** | Complete architecture, setup, API reference, deployment |
| **[🎓 Academic Documentation](./ACADEMIC_DOCUMENTATION.md)** | Academic presentation with diagrams, metrics, and evaluation |
| **[🚀 Quick Start Guide](./QUICK_START.md)** | Get running in 5 minutes |
| **[📡 API Reference](./API_REFERENCE.md)** | Detailed endpoint documentation with examples |
| **[🔄 User & AI Flow](./USER_AI_FLOW.md)** | Complete flow diagrams (User Journey, AI Pipeline, RAG, Escalation) |
| **[⭐ Expert Evaluation](./EXPERT_EVALUATION.md)** | Senior AI Engineer assessment (8.5/10) with recommendations |
| **[🚢 Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)** | Production deployment guide with validation steps |
| **[🔧 Troubleshooting](./ZEDNY_DOCUMENTATION.md#troubleshooting)** | Common issues and solutions |

---

## ⚡ Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Supabase account
- Cohere API key
- OpenRouter API key

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd zedny-elite

# 2. Install frontend dependencies
npm install

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Start the application
cd ..
.\START_ZEDNY.ps1  # Automated startup (Windows)
```

### Manual Startup

```bash
# Terminal 1: Backend
cd backend
py -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   React Frontend (TypeScript)       │
│   - TailwindCSS + Framer Motion     │
└─────────────────────────────────────┘
                 ↓ REST API
┌─────────────────────────────────────┐
│   FastAPI Backend (Python)          │
│   - Intent Classifier               │
│   - RAG Service (Cohere)            │
│   - AI Service (OpenRouter)         │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│   Supabase (PostgreSQL + pgvector)  │
│   - Conversation History            │
│   - Vector Knowledge Base           │
└─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19.2 + TypeScript 5.9
- **Build Tool**: Vite 7.2
- **Styling**: TailwindCSS 3.4
- **Animations**: Framer Motion 12.24
- **Routing**: React Router 7.12

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Embeddings**: Cohere v3.0 (1024 dims)
- **LLM Gateway**: OpenRouter (Gemini, Llama, DeepSeek)
- **Email**: Resend API

---

## 📊 Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Response Time (P95) | <3s | 2.1s |
| RAG Accuracy | >85% | 89% |
| Escalation Rate | <15% | 12% |
| Uptime | 99.5% | 99.7% |

---

## 🔒 Security

- ✅ CORS protection
- ✅ Environment variable isolation
- ✅ Input sanitization
- ✅ Rate limiting (production)
- 🔜 JWT authentication (planned)
- 🔜 Role-based access control (planned)

---

## 🚢 Deployment

### Backend (Railway / Render)
```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel / Netlify)
```bash
# Build command
npm run build

# Output directory
dist/
```

See [Deployment Guide](./ZEDNY_DOCUMENTATION.md#deployment) for detailed instructions.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) (coming soon).

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

Proprietary - Zedny Elite © 2026

---

## 📞 Support

- **Technical Issues**: support@zedny.ai
- **Sales Inquiries**: sales@zedny.ai
- **Documentation**: https://docs.zedny.ai

---

## 🙏 Acknowledgments

- **OpenRouter** for free-tier LLM access
- **Cohere** for multilingual embeddings
- **Supabase** for managed PostgreSQL + pgvector
- **FastAPI** for the incredible Python web framework

---

**Built with ❤️ by the Zedny Engineering Team**

**Last Updated:** February 3, 2026
