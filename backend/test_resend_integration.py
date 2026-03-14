import asyncio
import sys
import os
from unittest.mock import MagicMock

# Mocking env dependencies
sys.modules['app.core.config'] = MagicMock()
import app.core.config as config
config.RESEND_API_KEY = os.getenv("RESEND_API_KEY", "re_mock_key")
config.SUPPORT_EMAIL = "mohammedrawan653@gmail.com"

from app.services.ai_service import AIService
from app.models.schemas import EscalationReport

async def test_resend_escalation():
    print("\n--- 📧 RESEND INTEGRATION TEST ---")
    
    # Create a dummy report with rich details
    report = EscalationReport(
        id="resend-test-001",
        category="Technical Support",
        service="Mobile App",
        urgency="High",
        summary="Critical crash loop reported on Android 14. Customer is unable to open the login screen.",
        history=["User: The app keeps closing.", "AI: Did you clear cache?", "User: Yes, I also reinstalled it."],
        timestamp="2026-01-27T23:15:00",
        assigned_to="mohammedrawan653@gmail.com",
        user_email="premium_user@company.com",
        user_phone="+20123456789",
        company_name="Global Education Corp"
    )

    print(f"Triggering Resend email to: {report.assigned_to}")
    await AIService.send_escalation_email(report)
    print("\nCheck the console output for Resend ID or Error message.")

if __name__ == "__main__":
    asyncio.run(test_resend_escalation())
