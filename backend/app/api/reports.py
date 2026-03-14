from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Header
from app.core.config import supabase, ADMIN_API_TOKEN
from app.models.schemas import EscalationReport

router = APIRouter()

def require_admin_token(x_admin_token: Optional[str] = Header(default=None)) -> None:
    """
    Lightweight protection for admin endpoints.
    - If ADMIN_API_TOKEN is not set (dev mode), allow requests.
    - If set, require matching `X-Admin-Token` header.
    """
    if not ADMIN_API_TOKEN:
        return
    if not x_admin_token or x_admin_token != ADMIN_API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/reports")
async def get_reports(role: Optional[str] = "admin", department: Optional[str] = None, _: None = Depends(require_admin_token)):
    try:
        query = supabase.table("reports").select("*")
        
        # Admin sees everything. Employees see their department reports.
        # Use fuzzy matching (ilike) so 'tech' matches 'Technical Support'
        if role and role.lower() != "admin" and department:
            query = query.ilike("category", f"%{department}%")
        
        res = query.order("timestamp", desc=True).execute()
        return res.data
    except Exception as e:
        print(f"--- [SUPABASE ERROR] Failed to fetch reports: {e}")
        return []

@router.get("/users")
async def get_users(_: None = Depends(require_admin_token)):
    try:
        res = supabase.table("users").select("*").execute()
        return res.data
    except Exception as e:
        print(f"--- [SUPABASE ERROR] Failed to fetch users: {e}")
        return []

@router.get("/ratings")
async def get_ratings(_: None = Depends(require_admin_token)):
    try:
        res = supabase.table("ratings").select("*").order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        print(f"--- [SUPABASE ERROR] Failed to fetch ratings: {e}")
        return []

@router.post("/reports")
async def create_report(report_data: Dict[str, Any], background_tasks: BackgroundTasks):
    from app.services.ai_service import AIService
    from app.services.supabase_service import SupabaseService
    import uuid
    import datetime

    # DEBUG: See what the frontend is actually sending
    print(f"--- [CREATE REPORT PAYLOAD] {report_data}")

    # Logic to prioritize explicit customer email (from form) over logged-in user email
    # Frontend might send 'customerEmail', 'contact_email', or 'user_email'
    customer_email = (
        report_data.get("customerEmail") or 
        report_data.get("contact_email") or 
        report_data.get("metadata", {}).get("email") or
        report_data.get("user_email") or
        "Unregistered Guest"
    )

    # Create internal model with metadata
    report = EscalationReport(
        id=str(uuid.uuid4()),
        category=report_data.get("category", "General"),
        service=report_data.get("service", "Unknown"),
        urgency=report_data.get("urgency", "Normal"),
        summary=report_data.get("summary", ""),
        history=report_data.get("history", []),
        timestamp=datetime.datetime.now().isoformat(),
        assigned_to=report_data.get("assigned_to", "mohammedrawan653@gmail.com"),
        user_email=customer_email,
        metadata={
            "user_phone": report_data.get("user_phone") or report_data.get("contactPhone"),
            "company_name": report_data.get("company_name") or report_data.get("company"),
            **report_data.get("metadata", {})
        }
    )
    
    # Auto-Register Guest as Lead
    user_email = report_data.get("user_email")
    if user_email and "@" in user_email:
        SupabaseService.ensure_user_exists(user_email, name=report_data.get("customerName"), role="Lead")

    # Save to DB
    SupabaseService.save_report(report)
    
    # Trigger Async Email
    background_tasks.add_task(AIService.send_escalation_email, report)
    
    return {"status": "Escalated Successfully", "report_id": report.id}

@router.get("/reports/{report_id}")
async def get_report_details(report_id: str, role: str, department: Optional[str] = None, _: None = Depends(require_admin_token)):
    try:
        res = supabase.table("reports").select("*").eq("id", report_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Report not found")
            
        report = res.data[0]
        if role.lower() == "admin":
            return report
            
        # Flexible department check: Allow if user's dept is a substring of report category
        # e.g., User Dept 'tech' allowed for Category 'Technical Support'
        report_cat = report.get("category", "").lower()
        user_dept = (department or "").lower()
        
        if not user_dept or (user_dept not in report_cat and report_cat not in user_dept):
            raise HTTPException(status_code=403, detail=f"Unauthorized: Department mismatch ({user_dept} vs {report_cat})")
            
        return report
    except HTTPException:
        raise
    except Exception as e:
        print(f"--- [SUPABASE ERROR] Failed to fetch report details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/reports/{report_id}/status")
async def update_report_status(report_id: str, status_data: Dict[str, Any], _: None = Depends(require_admin_token)):
    """
    Update the status of a report.
    Valid statuses: pending, in_progress, solved
    """
    try:
        new_status = status_data.get("status", "").lower()
        valid_statuses = ["pending", "in_progress", "solved"]
        
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        # Update in Supabase
        res = supabase.table("reports").update({"status": new_status}).eq("id", report_id).execute()
        
        if not res.data:
            raise HTTPException(status_code=404, detail="Report not found")
        
        print(f"--- [STATUS UPDATE] Report {report_id} -> {new_status}")
        return {"status": "success", "report_id": report_id, "new_status": new_status}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"--- [SUPABASE ERROR] Failed to update report status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update status")

@router.get("/stats")
async def get_stats(_: None = Depends(require_admin_token)):
    try:
        # 1. Reports Stats
        res_reports = supabase.table("reports").select("category, status, timestamp, assigned_to").execute()
        all_reports = res_reports.data if res_reports.data else []
        total_reports = len(all_reports)
        
        # 2. Users Stats
        res_users = supabase.table("users").select("id").execute()
        total_users = len(res_users.data) if res_users.data else 0

        # 3. Sessions Stats (Interactions)
        res_sessions = supabase.table("chat_sessions").select("id, updated_at, created_at").execute()
        sessions_data = res_sessions.data if res_sessions.data else []
        total_sessions = len(sessions_data)
        
        # 4. Success Rate from real ratings
        res_ratings = supabase.table("ratings").select("rating").execute()
        all_ratings = [r['rating'] for r in res_ratings.data] if res_ratings.data else []
        success_rate = round((sum(all_ratings) / (len(all_ratings) * 5)) * 100, 1) if all_ratings else 95.0
        
        # 5. DYNAMIC: Escalation Rate (% of reports that were escalated to humans)
        escalated_reports = [r for r in all_reports if r.get("assigned_to")]
        escalation_rate = round((len(escalated_reports) / total_reports) * 100, 1) if total_reports > 0 else 0.0
        
        # 6. DYNAMIC: Average Response Time (from session duration)
        response_times = []
        for s in sessions_data:
            if s.get("created_at") and s.get("updated_at"):
                try:
                    from datetime import datetime
                    created = datetime.fromisoformat(s["created_at"].replace("Z", "+00:00"))
                    updated = datetime.fromisoformat(s["updated_at"].replace("Z", "+00:00"))
                    duration = (updated - created).total_seconds()
                    if 0 < duration < 3600:  # Only count sessions < 1 hour
                        response_times.append(duration)
                except:
                    pass
        avg_response = round(sum(response_times) / len(response_times), 1) if response_times else 2.0
        avg_response_str = f"{avg_response:.1f}s" if avg_response < 60 else f"{round(avg_response/60, 1)}m"
        
        # 7. DYNAMIC: Average Wait Time (pending reports age)
        pending_reports = [r for r in all_reports if r.get("status") == "pending"]
        wait_times = []
        for p in pending_reports:
            if p.get("timestamp"):
                try:
                    from datetime import datetime, timezone
                    created = datetime.fromisoformat(p["timestamp"].replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    wait_min = (now - created).total_seconds() / 60
                    wait_times.append(wait_min)
                except:
                    pass
        avg_wait = round(sum(wait_times) / len(wait_times), 1) if wait_times else 0.0
        avg_wait_str = f"{avg_wait:.1f}m" if avg_wait < 60 else f"{round(avg_wait/60, 1)}h"
        
        # 8. Department Distribution
        depts = ["Tech", "Media", "Content", "Sales"]
        dept_data = []
        for d in depts:
            dept_reports = [r for r in all_reports if r.get("category", "").lower() == d.lower()]
            count = len(dept_reports)
            solved = len([r for r in dept_reports if r.get("status") == "solved"])
            health = 100 if count == 0 else round((solved / count) * 100, 1)
            dept_data.append({"name": d, "health": health, "load": count, "solved": solved, "pending": count - solved})

        return {
            "kpis": [
                {"label": "Total Interactions", "value": f"{total_sessions}+", "trend": "up", "change": 5.2},
                {"label": "AI Success Rate", "value": f"{success_rate}%", "trend": "up", "change": 1.1},
                {"label": "Active Users", "value": str(total_users), "trend": "up", "change": 12.4},
                {"label": "Total Reports", "value": str(total_reports), "trend": "up", "change": 2.5},
                {"label": "Avg. Response", "value": avg_response_str, "trend": "stable", "change": 0.0}
            ],
            "departments": dept_data,
            "escalation_rate": escalation_rate,
            "avg_wait_time": avg_wait_str
        }
    except Exception as e:
        print(f"--- [STATS ERROR] {e}")
        return {"error": str(e)}

@router.get("/analysis")
async def get_smart_analysis(_: None = Depends(require_admin_token)):
    try:
        from app.services.ai_service import AIService
        # Fetch last 30 reports for analysis
        res = supabase.table("reports").select("category, summary, timestamp").order("timestamp", desc=True).limit(30).execute()
        analysis = AIService.perform_smart_analysis(res.data)
        return {"analysis": analysis}
    except Exception as e:
        print(f"--- [ANALYSIS ERROR] {e}")
        return {"analysis": "عذراً، فشلت عملية التحليل الذكي للبيانات حالياً."}
