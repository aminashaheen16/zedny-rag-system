import resend
import logging
from typing import Optional, Any
from app.core.config import RESEND_API_KEY, SUPPORT_EMAIL

logger = logging.getLogger("Zedny.EmailService")

# Initialize Resend
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

class EmailService:
    @staticmethod
    def send_html_email(subject: str, recipient: str, html_content: str) -> bool:
        """
        Sends an HTML email using Resend API.
        """
        if not RESEND_API_KEY:
            logger.error("--- [RESEND ERROR] API Key missing in .env ---")
            return False

        try:
            params = {
                "from": "Zedny Support <onboarding@resend.dev>", # Default for sandbox, update if verified domain
                "to": [recipient],
                "subject": subject,
                "html": html_content,
            }

            # Update specialized sender if domain is available later
            # params["from"] = "Zedny Support <support@zedny.ai>"

            response = resend.Emails.send(params)
            
            logger.info(f"--- [EMAIL SENT] Resend ID: {response.get('id')} to {recipient} ---")
            return True

        except Exception as e:
            logger.error(f"--- [EMAIL FAILED] Resend Error: {e}")
            return False

    @staticmethod
    def format_escalation_html(report: Any) -> str:
        """
        Formats an ultra-premium, card-based HTML report.
        """
        # Logic to extract metadata safely
        meta = getattr(report, 'metadata', {})
        phone = meta.get('user_phone', '—') or '—'
        company = meta.get('company_name', '—') or '—'
        ai_summary = meta.get('ai_summary', report.summary)
        
        # Format history as a conversation bubble flow
        history_bubbles = ""
        for line in report.history[-10:]:
            is_ai = "AI:" in line or "Bot:" in line
            bg = "#f1f2f6" if is_ai else "#e3f2fd"
            align = "left" if is_ai else "right"
            history_bubbles += f"""
            <div style="background: {bg}; padding: 12px 16px; border-radius: 12px; margin-bottom: 8px; font-size: 13px; text-align: {align}; border-left: 4px solid {'#0984e3' if not is_ai else '#b2bec3'};">
                {line.replace('AI:', '<b>🤖 Support:</b>').replace('User:', '<b>👤 Customer:</b>')}
            </div>
            """

        urgency_color = "#d63031" if report.urgency.lower() == "high" else "#fdcb6e"
        dept_icon = "💼" if "Sales" in report.category else "🛠️"

        # Specialized Dashboard Link with Auto-Login for Mock QA
        from app.core.config import FRONTEND_URL
        is_sales = "Sales" in report.category
        # Specialized Dashboard Link with Auto-Login for Mock QA
        from app.core.config import FRONTEND_URL
        is_sales = "Sales" in report.category
        mock_email = "sales_manager@zedny.ai" if is_sales else "mohammedrawan653@gmail.com"
        
        # We point to /employee and force login as the relevant mock user
        dashboard_url = f"{FRONTEND_URL}/employee?id={report.id}&autoLogin={mock_email}"

        category_ar = "مبيعات" if is_sales else "دعم فني"
        category_en = "Sales" if is_sales else "Technical"

        return f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&family=Inter:wght@400;600;700&display=swap');
                body {{ font-family: 'Tajawal', 'Inter', system-ui, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; color: #1e293b; text-align: right; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
                .hero {{ background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 40px 30px; text-align: center; color: white; }}
                .hero h1 {{ margin: 0; font-size: 24px; font-weight: 800; text-transform: uppercase; }}
                .hero p {{ margin-top: 10px; font-size: 14px; opacity: 0.8; }}
                .badge {{ display: inline-block; padding: 6px 14px; border-radius: 30px; font-size: 11px; font-weight: 700; color: white; margin-bottom: 25px; }}
                .content {{ padding: 30px; }}
                .card {{ background: #ffffff; border: 1px solid #f1f5f9; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }}
                .card-title {{ font-size: 13px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; }}
                .grid {{ display: grid; gap: 12px; }}
                .label {{ color: #94a3b8; font-size: 12px; font-weight: 600; }}
                .value {{ font-size: 15px; font-weight: 700; color: #0f172a; }}
                .summary-text {{ font-size: 15px; line-height: 1.8; color: #334155; white-space: pre-wrap; }}
                .history-container {{ background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px inset #f1f5f9; }}
                .footer {{ background: #f1f5f9; padding: 25px; text-align: center; font-size: 11px; color: #94a3b8; line-height: 1.6; direction: ltr; }}
                .btn {{ background: #1e3a8a; color: white !important; padding: 14px 28px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 14px; display: inline-block; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <h1>{dept_icon} تصعيد جديد: {category_ar}</h1>
                    <p>{category_en} Department Escalation • Level 2</p>
                </div>
                
                <div class="content">
                    <div style="text-align: center;">
                        <span class="badge" style="background: {urgency_color};">⚡ درجة الأهمية: {report.urgency.upper()}</span>
                    </div>

                    <div class="card">
                        <div class="card-title">👤 بيانات العميل</div>
                        <div class="grid">
                            <div><span class="label">البريد:</span> <span class="value">{report.user_email}</span></div>
                            <div><span class="label">الشركة:</span> <span class="value">{company}</span></div>
                            <div><span class="label">الهاتف:</span> <span class="value">{phone}</span></div>
                        </div>
                    </div>

                    <div class="card" style="border-right: 5px solid #3b82f6;">
                        <div class="card-title">📝 ملخص التحليل الذكي</div>
                        <div class="summary-text">
                            {ai_summary}
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-title">💬 سياق المحادثة الأخيرة</div>
                        <div class="history-container">
                            {history_bubbles}
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <a href="{dashboard_url}" class="btn">فتح في لوحة التحكم (Dashboard)</a>
                    </div>
                </div>
                
                <div class="footer">
                    Zedny AI Agentic Infrastructure • Technical Service Unit<br>
                    CONFIDENTIAL INFORMATION • FOR AUTHORIZED PERSONNEL ONLY<br>
                    REF: {report.id} • Generated on {report.timestamp}
                </div>
            </div>
        </body>
        </html>
        """
