import datetime
import uuid
from typing import Optional, List, Dict, Any
from app.core.config import supabase
from app.models.schemas import IncidentState, EscalationReport

class SupabaseService:
    @staticmethod
    def save_report(report: EscalationReport):
        try:
            data = report.dict()
            supabase.table("reports").insert(data).execute()
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to save report: {e}")

    @staticmethod
    def update_report(report: EscalationReport):
        try:
            data = report.dict()
            report_id = data.pop("id")
            supabase.table("reports").update(data).eq("id", report_id).execute()
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to update report: {e}")

    @staticmethod
    def save_rating(rating: int, session_id: str, user_email: Optional[str] = None, message: str = "", history: List[str] = None):
        if history is None:
            history = []
        try:
            new_rating = {
                "id": str(uuid.uuid4()),
                "rating": rating,
                "session_id": session_id,
                "user_email": user_email,
                "message": message,
                "history": (history or [])[-5:], # Store last 5 messages for context
                "created_at": datetime.datetime.now().isoformat()
            }
            # Insert into dedicated 'ratings' table
            # Note: Ensure columns session_id and user_email exist in your Supabase table
            supabase.table("ratings").insert(new_rating).execute()
            print(f"--- [RATING SAVED] {rating} stars | User: {user_email or 'Guest'} | Session: {session_id}")
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to save rating: {e}")

    @staticmethod
    def save_session(state: IncidentState, user_email: str = None):
        try:
            # 1. Prepare base data matching table columns
            data = {
                "id": state.session_id,
                "category": state.category,
                "step": state.step,
                "turn_count": state.turn_count,
                "diagnostic_turns": state.diagnostic_turns,
                "summary": state.summary,
                "status": state.status,
                "history": state.history,
                "updated_at": datetime.datetime.now().isoformat()
            }
            
            # 2. Serialize Entities
            if hasattr(state.entities, "dict"):
                data["entities"] = state.entities.dict()
            else:
                data["entities"] = state.entities
            
            # 3. Pack flexible fields into metadata JSONB column
            metadata = {
                "problem_description": state.problem_description,
                "solutions_tried": state.solutions_tried,
                "awaiting_solution_feedback": state.awaiting_solution_feedback,
                "max_solutions_before_escalation": state.max_solutions_before_escalation
            }
            
            # Senior Rule: Only store device info in DB if escalated (Step 2) 
            # or if it was previously committed (to avoid data loss)
            if state.step == 2 or (state.device_info and state.device_info.is_collected and state.step == 2):
                if hasattr(state.device_info, "dict"):
                    metadata["device_info"] = state.device_info.dict()
                else:
                    metadata["device_info"] = state.device_info
            
            data["metadata"] = metadata

            # 4. Link User Email
            if user_email:
                data["user_email"] = user_email
            
            supabase.table("chat_sessions").upsert(data).execute()
            print(f"--- [SESSION SAVED] {data['id']} with {len(data.get('history', []))} messages")
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to save session: {e}")

    @staticmethod
    def load_session(session_id: str) -> Optional[IncidentState]:
        try:
            res = supabase.table("chat_sessions").select("*").eq("id", session_id).execute()
            if res.data:
                data = res.data[0]
                data["session_id"] = data.pop("id")
                
                # Unpack metadata
                metadata = data.get("metadata", {}) or {}
                
                # Handle nested objects
                if "device_info" in metadata:
                    from app.models.schemas import DeviceInfo
                    data["device_info"] = DeviceInfo(**metadata["device_info"])
                
                # Map metadata fields back to state
                data["problem_description"] = metadata.get("problem_description", "")
                data["solutions_tried"] = metadata.get("solutions_tried", [])
                data["awaiting_solution_feedback"] = metadata.get("awaiting_solution_feedback", False)
                data["max_solutions_before_escalation"] = metadata.get("max_solutions_before_escalation", 3)
                
                # Handle entities
                if "entities" in data and isinstance(data["entities"], dict):
                    from app.models.schemas import EntityState
                    data["entities"] = EntityState(**data["entities"])
                
                return IncidentState(**data)
            return None
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to load session {session_id}: {e}")
            return None

    @staticmethod
    def save_user_memory(email: str, data: Dict[str, Any]):
        try:
            supabase.table("users").update({"metadata": data}).eq("email", email).execute()
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to save user memory: {e}")

    @staticmethod
    def get_user_profile(email: str) -> Dict[str, Any]:
        try:
            res = supabase.table("users").select("name, metadata").eq("email", email).execute()
            if res.data:
                profile = res.data[0].get("metadata", {})
                profile["name"] = res.data[0].get("name", "Guest")
                return profile
            return {"user_type": "Guest", "name": "Guest", "company": "Visitor"}
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Failed to load user profile for {email}: {e}")
            return {"user_type": "Guest", "name": "Guest", "company": "Visitor"}

    @staticmethod
    def ensure_user_exists(email: str, name: Optional[str] = None, role: str = "Guest"):
        try:
            res = supabase.table("users").select("id").eq("email", email).execute()
            if not res.data:
                user_data = {
                    "name": name or email.split("@")[0].capitalize(),
                    "email": email,
                    "metadata": {
                        "role": role,
                        "user_type": "Guest" if role == "Guest" else "Registered",
                        "department": "External",
                        "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={email}"
                    }
                }
                supabase.table("users").insert(user_data).execute()
        except Exception as e:
            print(f"--- [SUPABASE ERROR] Error in ensure_user_exists: {e}")


