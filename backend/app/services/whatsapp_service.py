from twilio.rest import Client
import logging
from typing import Any
from app.core.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, MOHAMED_WHATSAPP

logger = logging.getLogger("Zedny.WhatsAppService")

class WhatsAppService:
    @staticmethod
    def send_alert(message_body: str) -> bool:
        """
        Sends a WhatsApp message via Twilio.
        """
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, MOHAMED_WHATSAPP]):
            logger.error("--- [WHATSAPP ERROR] Twilio Credentials or Recipient missing in .env ---")
            return False

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            # Ensure numbers use the 'whatsapp:+...' format
            from_number = f"whatsapp:{TWILIO_WHATSAPP_NUMBER.replace('whatsapp:', '')}"
            to_number = f"whatsapp:{MOHAMED_WHATSAPP.replace('whatsapp:', '')}"

            message = client.messages.create(
                body=message_body,
                from_=from_number,
                to=to_number
            )
            
            logger.info(f"--- [WHATSAPP SENT] SID: {message.sid} to {MOHAMED_WHATSAPP} ---")
            return True

        except Exception as e:
            logger.error(f"--- [WHATSAPP FAILED] Twilio Error: {e}")
            return False

    @staticmethod
    def format_escalation_alert(report: Any) -> str:
        """
        Formats a concise, actionable WhatsApp alert.
        """
        severity_emoji = "🚨" if report.urgency.lower() == "high" else "⚠️"
        
        return (
            f"{severity_emoji} *Zedny Escalation Alert*\n\n"
            f"👤 *Customer:* {report.user_email}\n"
            f"🏢 *Company:* {getattr(report, 'company_name', 'N/A') or 'N/A'}\n"
            f"📞 *Phone:* {getattr(report, 'user_phone', 'N/A') or 'N/A'}\n"
            f"📂 *Dept:* {report.category}\n"
            f"📝 *Issue:* {report.summary[:100]}...\n\n"
            f"🔗 *Action:* Check the Admin Dashboard for details."
        )
