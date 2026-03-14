# 📡 Zedny Elite - API Reference

> **Version:** 2.0.0  
> **Base URL:** `http://localhost:8000` (Development)  
> **Authentication:** Session-based (future: JWT)

---

## Table of Contents

1. [Chat Endpoints](#chat-endpoints)
2. [Admin Endpoints](#admin-endpoints)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)

---

## Chat Endpoints

### POST `/chat`
**Primary conversation endpoint for customer interactions**

#### Headers
```http
Content-Type: application/json
```

#### Request Body
```typescript
interface ChatRequest {
  message: string;              // User's message (Arabic or English)
  department: "tech" | "sales"; // Routing hint
  session_id?: string;          // UUID v4 (auto-generated if missing)
  incident_state?: IncidentState; // Conversation state (optional)
}
```

#### Response
```typescript
interface ChatResponse {
  answer: string;               // AI-generated response
  should_escalate: boolean;     // True if human intervention needed
  context_used: string;         // RAG context (for debugging)
  incident_state: IncidentState; // Updated conversation state
  action_required?: "show_escalation_form" | "force_form" | null;
}
```

#### Example Request
```json
{
  "message": "ما هي الشركات التي اشتغلت معاها زدني؟",
  "department": "sales",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Example Response
```json
{
  "answer": "اشتغلنا مع جهات كبرى في قطاعات مختلفة بنسبة نجاح 95%، منها:\n- قطاع البنوك والتمويل\n- قطاع التكنولوجيا\n- قطاع الرعاية الصحية",
  "should_escalate": false,
  "context_used": "**السؤال:** اشتغلتوا مع مين قبل كده؟\n\n**الإجابة:**\n\nاشتغلنا مع **جهات كبرى في قطاعات مختلفة**...",
  "incident_state": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "step": 0,
    "category": "SALES",
    "status": "active",
    "history": [
      "User: ما هي الشركات التي اشتغلت معاها زدني؟",
      "AI: اشتغلنا مع جهات كبرى..."
    ],
    "language": "ar"
  },
  "action_required": null
}
```

#### Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid request body |
| 500 | Internal server error |

---

### POST `/rate`
**Submit user feedback on AI response quality**

#### Request Body
```typescript
interface RatingRequest {
  session_id: string;    // UUID of the conversation
  rating: 1 | 2 | 3 | 4 | 5; // Star rating
  feedback?: string;     // Optional text feedback
}
```

#### Response
```json
{
  "status": "success",
  "message": "Feedback recorded"
}
```

---

## Admin Endpoints

### GET `/reports`
**Retrieve escalation reports (requires admin auth)**

#### Query Parameters
```typescript
interface ReportsQuery {
  status?: "pending" | "resolved" | "all";
  limit?: number;  // Default: 50
  offset?: number; // For pagination
}
```

#### Response
```typescript
interface Report {
  id: string;
  category: "Sales" | "Tech";
  service: string;
  urgency: "Low" | "Medium" | "High";
  summary: string;
  history: string[];
  timestamp: string; // ISO 8601
  assigned_to: string;
  user_email: string;
}

interface ReportsResponse {
  reports: Report[];
  total: number;
  page: number;
}
```

---

### GET `/stats`
**Analytics dashboard metrics**

#### Response
```json
{
  "total_conversations": 1250,
  "escalation_rate": 0.12,
  "avg_resolution_time_seconds": 180,
  "top_intents": [
    {"intent": "INFO", "count": 450},
    {"intent": "SALES", "count": 380},
    {"intent": "ISSUE", "count": 280}
  ],
  "satisfaction_score": 4.3,
  "rag_hit_rate": 0.89
}
```

---

## Data Models

### IncidentState
**Conversation state tracking**

```typescript
interface IncidentState {
  session_id: string;           // UUID v4
  step: number;                 // Conversation turn count
  category: "INFO" | "SALES" | "ISSUE" | "GREETING" | "General";
  status: "new" | "diagnosing" | "active" | "escalated" | "resolved";
  history: string[];            // Full conversation log
  entities: {
    course_name?: string;
    payment_status?: string;
    platform_feature?: string;
    dates?: string;
    user_type?: string;
  };
  summary: string;              // AI-generated summary
  turn_count: number;
  diagnostic_turns: number;     // For technical support
  device_info: {
    device_type?: string;
    browser?: string;
    os?: string;
    is_collected: boolean;
  };
  language: "ar" | "en";
  current_phase: "discovery" | "awaiting_confirmation";
  pending_topic?: string;
  awaiting_clarification: boolean;
  last_ai_question_type: string;
  session_metadata: Record<string, any>;
  problem_description: string;
  solutions_tried: string[];
  tried_solution_ids: string[];
  awaiting_solution_feedback: boolean;
  max_solutions_before_escalation: number;
  clarification_count: number;
  solutions_count: number;
  is_discovery_phase: boolean;
}
```

### UserIntent (Enum)
```python
class UserIntent(str, Enum):
    GREETING = "GREETING"
    INFO = "INFO"
    SALES = "SALES"
    ISSUE = "ISSUE"
    OFF_TOPIC = "OFF_TOPIC"
```

---

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error message here",
  "error_code": "RAG_SERVICE_UNAVAILABLE",
  "timestamp": "2026-02-03T02:00:00Z"
}
```

### Common Error Codes
| Code | Description | Solution |
|------|-------------|----------|
| `COHERE_RATE_LIMIT` | Embedding API quota exceeded | Upgrade Cohere key or wait for reset |
| `SUPABASE_CONNECTION_ERROR` | Database unreachable | Check Supabase status |
| `INVALID_SESSION_ID` | Malformed UUID | Regenerate session ID |
| `RAG_SERVICE_UNAVAILABLE` | Knowledge base search failed | Check Cohere API key |

---

## Rate Limiting

### Current Limits (Development)
- **Chat Endpoint**: No limit
- **Reports Endpoint**: 100 requests/minute
- **Stats Endpoint**: 10 requests/minute

### Production Limits (Future)
- **Chat Endpoint**: 60 requests/minute per IP
- **Reports Endpoint**: 30 requests/minute
- **Stats Endpoint**: 5 requests/minute

### Rate Limit Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1675430400
```

---

## Webhooks (Future)

### POST `/webhooks/escalation`
**Triggered when a conversation is escalated**

```json
{
  "event": "escalation.created",
  "data": {
    "report_id": "uuid",
    "category": "Tech",
    "urgency": "High",
    "user_email": "customer@example.com"
  },
  "timestamp": "2026-02-03T02:00:00Z"
}
```

---

## Testing

### Using cURL
```bash
# Health check
curl http://localhost:8000

# Send chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "مرحباً",
    "department": "tech"
  }'

# Submit rating
curl -X POST http://localhost:8000/rate \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "rating": 5,
    "feedback": "ممتاز"
  }'
```

### Using Python
```python
import requests

# Chat request
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "ما هي الدورات المتاحة؟",
        "department": "sales"
    }
)
print(response.json())
```

### Using JavaScript (Frontend)
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What is Zedny?',
    department: 'sales'
  })
});

const data = await response.json();
console.log(data.answer);
```

---

## Interactive Documentation

For live API testing, visit:
**http://localhost:8000/docs** (Swagger UI)

---

**Last Updated:** February 3, 2026
