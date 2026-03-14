# 🚀 Production Deployment Checklist - Zedny Elite

> **Pre-Launch Validation & Deployment Guide**

---

## 📋 Pre-Deployment Checklist

### 1. Environment Configuration ✅

- [ ] **Backend `.env` file configured**
  ```bash
  OPENROUTER_API_KEY=sk-or-v1-xxxxx
  COHERE_API_KEY=xxxxx
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_SERVICE_ROLE_KEY=xxxxx
  RESEND_API_KEY=re_xxxxx
  ```

- [ ] **Frontend environment variables**
  ```bash
  VITE_API_URL=https://api.zedny.ai
  ```

- [ ] **API Keys validated** (test with minimal requests)

- [ ] **Database migrations applied**
  ```sql
  -- Run in Supabase SQL Editor
  CREATE EXTENSION IF NOT EXISTS vector;
  -- (See ZEDNY_DOCUMENTATION.md for full schema)
  ```

---

### 2. Code Quality ⚠️

- [ ] **Linting passed**
  ```bash
  # Backend
  cd backend
  pylint app/

  # Frontend
  npm run lint
  ```

- [ ] **Type checking passed**
  ```bash
  # Frontend
  npm run type-check
  ```

- [ ] **No hardcoded secrets** (scan with `git-secrets`)

- [ ] **Remove debug logs** (search for `console.log`, `print()`)

---

### 3. Testing 🔴 CRITICAL GAP

**Current Status:** ❌ No automated tests

**Minimum Required:**
- [ ] **RAG Service Tests**
  ```python
  # backend/tests/test_rag_service.py
  def test_search_knowledge_base_valid_query():
      results = RagService.search_knowledge_base("test", 0.5, 4)
      assert len(results) <= 4
  ```

- [ ] **API Endpoint Tests**
  ```python
  # backend/tests/test_chat_api.py
  def test_chat_endpoint_returns_200():
      response = client.post("/chat", json={"message": "مرحبا"})
      assert response.status_code == 200
  ```

- [ ] **Frontend Component Tests**
  ```tsx
  // src/__tests__/MessageBubble.test.tsx
  test('renders user message correctly', () => {
    render(<MessageBubble message="Hello" isUser={true} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
  ```

**Recommendation:** Deploy with manual QA, add tests post-launch.

---

### 4. Security 🔒

- [ ] **CORS configured** (whitelist production domains)
  ```python
  # backend/app/main.py
  allow_origins=[
      "https://zedny.ai",
      "https://www.zedny.ai"
  ]
  ```

- [ ] **Rate limiting enabled**
  ```python
  # Add to chat.py
  @limiter.limit("60/minute")
  async def chat_endpoint():
      pass
  ```

- [ ] **Input validation** (Pydantic models enforced)

- [ ] **HTTPS enforced** (redirect HTTP → HTTPS)

- [ ] **Secrets rotation plan** (quarterly API key updates)

---

### 5. Performance ⚡

- [ ] **Load testing completed**
  ```bash
  # Using Locust
  locust -f tests/load_test.py --host=https://api.zedny.ai
  ```

- [ ] **Target metrics validated**
  - P95 response time < 3s
  - 100+ concurrent users supported
  - RAG accuracy > 85%

- [ ] **Database indexes created**
  ```sql
  CREATE INDEX idx_sessions_id ON sessions(session_id);
  CREATE INDEX idx_kb_embedding ON knowledge_base USING ivfflat(embedding);
  ```

- [ ] **CDN configured** (for frontend static assets)

---

### 6. Monitoring & Observability 📊

- [ ] **Error tracking** (Sentry integration)
  ```python
  import sentry_sdk
  sentry_sdk.init(dsn="https://xxxxx@sentry.io/xxxxx")
  ```

- [ ] **Structured logging**
  ```python
  import structlog
  logger = structlog.get_logger()
  logger.info("chat_request", session_id=session_id, intent=intent)
  ```

- [ ] **Health check endpoint**
  ```python
  @app.get("/health")
  async def health_check():
      return {
          "status": "healthy",
          "database": check_db_connection(),
          "cohere": check_cohere_api(),
          "openrouter": check_openrouter_api()
      }
  ```

- [ ] **Uptime monitoring** (UptimeRobot, Pingdom)

- [ ] **Metrics dashboard** (Grafana, Datadog)

---

### 7. Backup & Disaster Recovery 💾

- [ ] **Database backups enabled** (Supabase auto-backup)

- [ ] **Knowledge base exported**
  ```bash
  # Export to JSON
  supabase db dump > backup_$(date +%Y%m%d).sql
  ```

- [ ] **Environment variables documented** (secure vault)

- [ ] **Rollback plan documented**
  ```bash
  # Quick rollback
  git revert HEAD
  git push origin main
  vercel --prod  # Redeploy previous version
  ```

---

## 🌐 Deployment Steps

### Backend (Railway / Render)

1. **Create New Project**
   ```bash
   railway login
   railway init
   ```

2. **Set Environment Variables**
   ```bash
   railway variables set OPENROUTER_API_KEY=xxxxx
   railway variables set COHERE_API_KEY=xxxxx
   railway variables set SUPABASE_URL=xxxxx
   railway variables set SUPABASE_SERVICE_ROLE_KEY=xxxxx
   ```

3. **Deploy**
   ```bash
   railway up
   ```

4. **Verify Deployment**
   ```bash
   curl https://zedny-backend.railway.app/health
   ```

---

### Frontend (Vercel / Netlify)

1. **Connect GitHub Repository**
   - Go to Vercel Dashboard
   - Import project from GitHub

2. **Configure Build Settings**
   ```
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

3. **Set Environment Variables**
   ```
   VITE_API_URL=https://zedny-backend.railway.app
   ```

4. **Deploy**
   - Push to `main` branch
   - Vercel auto-deploys

5. **Verify Deployment**
   - Visit https://zedny.ai
   - Test chat functionality

---

### Database (Supabase)

1. **Run Migrations**
   ```sql
   -- In Supabase SQL Editor
   CREATE EXTENSION IF NOT EXISTS vector;
   
   CREATE TABLE knowledge_base (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     title TEXT,
     content TEXT,
     language TEXT,
     category TEXT,
     embedding vector(1024),
     metadata JSONB,
     created_at TIMESTAMPTZ DEFAULT NOW()
   );
   
   CREATE INDEX ON knowledge_base 
   USING ivfflat (embedding vector_cosine_ops)
   WITH (lists = 100);
   ```

2. **Import Knowledge Base**
   ```bash
   # Upload ZEDNY_RAG_Optimized.json via Supabase dashboard
   # Or use Python script
   python scripts/import_knowledge_base.py
   ```

3. **Verify Data**
   ```sql
   SELECT COUNT(*) FROM knowledge_base;
   -- Expected: 663 records
   ```

---

## 🧪 Post-Deployment Validation

### Smoke Tests

- [ ] **Health Check**
  ```bash
  curl https://api.zedny.ai/health
  # Expected: {"status": "healthy"}
  ```

- [ ] **Chat Endpoint**
  ```bash
  curl -X POST https://api.zedny.ai/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "مرحبا", "department": "tech"}'
  # Expected: 200 OK with AI response
  ```

- [ ] **RAG Retrieval**
  ```bash
  curl -X POST https://api.zedny.ai/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "ما هي الشركات التي اشتغلت معاها؟", "department": "sales"}'
  # Expected: Response with company list
  ```

- [ ] **Frontend Load**
  ```bash
  curl https://zedny.ai
  # Expected: 200 OK, HTML content
  ```

---

### User Acceptance Testing (UAT)

**Test Scenarios:**

1. **Greeting Flow**
   - User: "مرحبا"
   - Expected: Welcoming response in Arabic

2. **Info Query**
   - User: "What is Zedny?"
   - Expected: RAG-powered answer about Zedny

3. **Sales Query**
   - User: "كم سعر الباقة الاحترافية؟"
   - Expected: Pricing info + optional lead form

4. **Technical Issue**
   - User: "مشكلة في تسجيل الدخول"
   - Expected: Diagnostic questions → Solutions → Escalation

5. **Escalation**
   - User: Fails 3 solutions
   - Expected: Form displayed, email sent to support

---

## 📈 Monitoring Metrics

### Key Performance Indicators (KPIs)

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Uptime | 99.5% | <99% |
| P95 Response Time | <3s | >5s |
| Error Rate | <1% | >5% |
| RAG Hit Rate | >85% | <70% |
| Escalation Rate | <15% | >25% |
| User Satisfaction | >4.0/5 | <3.5/5 |

### Alerting Rules

```yaml
# alerts.yml (for Prometheus/Grafana)
alerts:
  - name: HighErrorRate
    condition: error_rate > 0.05
    action: notify_slack
  
  - name: SlowResponses
    condition: p95_latency > 5000ms
    action: notify_pagerduty
  
  - name: DatabaseDown
    condition: db_connection_failed
    action: notify_pagerduty_urgent
```

---

## 🔄 Rollback Procedure

**If deployment fails:**

1. **Identify Issue**
   ```bash
   # Check logs
   railway logs
   vercel logs
   ```

2. **Rollback Backend**
   ```bash
   railway rollback
   ```

3. **Rollback Frontend**
   ```bash
   vercel rollback
   ```

4. **Verify Rollback**
   ```bash
   curl https://api.zedny.ai/health
   ```

5. **Post-Mortem**
   - Document what went wrong
   - Update checklist to prevent recurrence

---

## 📞 Support Contacts

| Role | Contact | Escalation |
|------|---------|------------|
| **DevOps** | devops@zedny.ai | Slack: #incidents |
| **Backend** | backend@zedny.ai | On-call: +20-xxx-xxxx |
| **Frontend** | frontend@zedny.ai | Slack: #frontend |
| **Database** | Supabase Support | support@supabase.com |

---

## ✅ Final Sign-Off

**Deployment Approved By:**

- [ ] **Tech Lead** - Architecture validated
- [ ] **QA Lead** - Manual testing passed
- [ ] **Security Lead** - Security review completed
- [ ] **Product Owner** - Business requirements met

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Rollback Plan Confirmed:** _______________

---

**Last Updated:** February 3, 2026  
**Version:** 1.0.0
