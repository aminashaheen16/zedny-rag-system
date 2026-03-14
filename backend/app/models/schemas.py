from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

class EntityState(BaseModel):
    course_name: Optional[str] = None
    payment_status: Optional[str] = None
    platform_feature: Optional[str] = None
    dates: Optional[str] = None
    user_type: Optional[str] = None # student, instructor, company

class DeviceInfo(BaseModel):
    """Device information collected during conversation (not stored in DB)"""
    device_type: Optional[str] = None  # desktop, laptop, mobile, tablet
    browser: Optional[str] = None      # chrome, safari, firefox, edge
    os: Optional[str] = None           # windows, macos, linux, ios, android
    is_collected: bool = False         # True when user provided all needed info

class IncidentState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step: int = 0
    category: str = "General"
    status: str = "new"  # new, collecting_info, diagnosing, solution_offered, resolved, escalated
    history: List[str] = Field(default_factory=list)
    entities: EntityState = Field(default_factory=EntityState)
    summary: str = ""
    turn_count: int = 0 
    diagnostic_turns: int = 0
    device_info: DeviceInfo = Field(default_factory=DeviceInfo)
    
    # 🔒 LANGUAGE LOCKING: Set on first message, used for all subsequent responses
    language: str = ""  # "en" or "ar" - locked after first user message
    
    # 🔄 DIALOGUE STATE TRACKING: Professional Context Management
    current_phase: str = "discovery"  # discovery, diagnosing, solution_feedback, awaiting_confirmation
    pending_topic: Optional[str] = None  # The topic we asked the user about (e.g., "ROI", "Pricing")
    awaiting_clarification: bool = False  
    last_ai_question_type: str = ""  # "discovery_options", "solution_verification", etc.
    session_metadata: Dict[str, Any] = Field(default_factory=dict) # For storing transient flow data
    
    # Smart Diagnostic Tracking
    problem_description: str = ""                    # AI's understanding of the issue
    solutions_tried: List[str] = Field(default_factory=list)  # List of solutions attempted
    tried_solution_ids: List[str] = Field(default_factory=list)  # NEW: Track solution IDs for exclusion logic
    awaiting_solution_feedback: bool = False         # True when waiting for "did this work?"
    max_solutions_before_escalation: int = 3         # Escalate after this many failed attempts 
    
    # Granular Turn Tracking (Diagnostic Intelligence)
    clarification_count: int = 0  # Number of clarifying questions asked
    solutions_count: int = 0      # Number of actual solutions offered
    diagnostic_turns: int = 0     # Deprecated: use clarification_count and solutions_count instead
    is_discovery_phase: bool = False  # True when user is in initial Discovery Menu
class ChatRequest(BaseModel):
    message: str
    department: Optional[str] = "general"
    incident_state: Optional[IncidentState] = None
    rating: Optional[int] = None
    user_email: Optional[str] = None 
    technical_profile: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None  # For loading existing sessions from DB

class ChatResponse(BaseModel):
    answer: str
    should_escalate: bool = False
    context_used: Optional[str] = None
    incident_state: Optional[IncidentState] = None
    action_required: Optional[str] = None  # e.g., "register_details"

class EscalationReport(BaseModel):
    id: str
    category: str
    service: str
    urgency: str
    summary: str
    history: List[str]
    timestamp: str
    status: str = "pending"
    user_email: Optional[str] = None
    assigned_to: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Employee(BaseModel):
    name: str
    email: str
    role: str # Admin, Tech, Media, Content, Sales
    department: Optional[str] = None

class RateRequest(BaseModel):
    rating: int
    message: Optional[str] = ""
    history: List[str] = Field(default_factory=list)
