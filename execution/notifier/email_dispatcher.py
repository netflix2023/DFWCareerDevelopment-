"""
Daily Morning Email Dispatcher for Career Surge Engine.
Formats a clean, responsive HTML summary of the Top 10 qualifying positions
with 1-click direct apply buttons and dispatches via Resend API (or local HTML preview).
"""

import sys
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request
import urllib.error
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from execution.storage.database import get_top_active_jobs, get_market_telemetry, DEFAULT_DB_PATH


RESEND_API_URL = "https://api.resend.com/emails"


def generate_email_html(jobs: List[Dict[str, Any]], telemetry: Dict[str, Any]) -> str:
    """Renders a modern, responsive HTML email template for the morning job digest."""
    total_active = telemetry.get("total_active_positions", len(jobs))
    date_str = datetime.now().strftime("%B %d, %Y")
    
    rows_html = ""
    for idx, j in enumerate(jobs, 1):
        score_pct = int(j.get("match_score", 0.5) * 100)
        age = j.get("age_days")
        age_str = f"{age}d ago" if age is not None else "Active"
        skills = j.get("matching_skills", "")
        skills_badge = f'<span style="font-size: 11px; color: #64748b; display: block; margin-top: 3px;">Matched: {skills}</span>' if skills else ""
        
        # Color badge for score
        score_color = "#10b981" if score_pct >= 70 else "#f59e0b"
        
        rows_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 12px 8px; font-weight: bold; color: #1e293b; vertical-align: middle;">{idx}</td>
            <td style="padding: 12px 8px; vertical-align: middle;">
                <div style="font-weight: 600; color: #0f172a; font-size: 14px;">{j['company']}</div>
                <div style="color: #334155; font-size: 13px;">{j['title']}</div>
                {skills_badge}
            </td>
            <td style="padding: 12px 8px; font-size: 12px; color: #475569; vertical-align: middle;">{j['location']}</td>
            <td style="padding: 12px 8px; font-size: 12px; color: #64748b; vertical-align: middle; text-align: center;">{age_str}</td>
            <td style="padding: 12px 8px; vertical-align: middle; text-align: center;">
                <span style="background-color: {score_color}15; color: {score_color}; padding: 4px 8px; border-radius: 9999px; font-size: 11px; font-weight: bold;">
                    {score_pct}%
                </span>
            </td>
            <td style="padding: 12px 8px; vertical-align: middle; text-align: right;">
                <a href="{j['apply_url']}" target="_blank" style="background-color: #2563eb; color: #ffffff; padding: 6px 14px; text-decoration: none; border-radius: 6px; font-size: 12px; font-weight: 600; display: inline-block;">
                    Apply &rarr;
                </a>
            </td>
        </tr>
        """
        
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Tech Internship Digest</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px;">
        <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 24px; color: #ffffff;">
                <h1 style="margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px;">Career Surge Engine &bull; Top 10 Opportunities</h1>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: #94a3b8;">{date_str} &bull; {len(jobs)} High-Velocity Positions Selected from {total_active} Live Listings</p>
            </div>
            
            <!-- Content -->
            <div style="padding: 20px;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 2px solid #cbd5e1; font-size: 11px; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px;">
                            <th style="padding: 8px;">#</th>
                            <th style="padding: 8px;">Role & Company</th>
                            <th style="padding: 8px;">Location</th>
                            <th style="padding: 8px; text-align: center;">Age</th>
                            <th style="padding: 8px; text-align: center;">Match</th>
                            <th style="padding: 8px; text-align: right;">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f1f5f9; padding: 16px 20px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; text-align: center;">
                <p style="margin: 0;">Automated by <strong>Career Surge Engine</strong> &bull; Validated with 5-second live link checks.</p>
                <p style="margin: 4px 0 0 0;">Inspect complete dataset in <code style="background: #e2e8f0; padding: 2px 4px; border-radius: 4px;">output/clean_csvs/dfw_qualifying_jobs.csv</code></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_via_gmail_smtp(
    html_content: str,
    recipient: str,
    sender: str,
    app_password: str,
    subject: str
) -> bool:
    """Sends email directly via Google's free Gmail SMTP server (smtp.gmail.com:587)."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        
        part = MIMEText(html_content, "html", "utf-8")
        msg.attach(part)
        
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, [recipient], msg.as_string())
            
        print(f"[+] Email successfully delivered directly to {recipient} via Gmail SMTP!")
        return True
    except Exception as e:
        print(f"[-] Gmail SMTP delivery failed: {e}")
        return False


def dispatch_top_jobs_email(db_path: str = DEFAULT_DB_PATH) -> bool:
    """Dispatches the daily top 10 email via Gmail SMTP or Resend API or writes local preview."""
    jobs = get_top_active_jobs(limit=10, max_age_days=7, db_path=db_path)
    telemetry = get_market_telemetry(db_path)
    
    if not jobs:
        print("[!] No active jobs found meeting criteria for daily email.")
        return False
        
    html_content = generate_email_html(jobs, telemetry)
    
    # Save local preview file
    preview_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output", "daily_email_preview.html")
    os.makedirs(os.path.dirname(preview_path), exist_ok=True)
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Saved rendered email digest preview: {preview_path}")
    
    recipient = os.getenv("NOTIFICATION_EMAIL", "candidate@example.com")
    subject = f"🚀 Top 10 Tech Internships Digest ({datetime.now().strftime('%b %d')})"
    gmail_app_pw = os.getenv("GMAIL_APP_PASSWORD", "").strip()
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    
    # Priority 1: Free Native Gmail SMTP (zero external services needed)
    if gmail_app_pw:
        sender = os.getenv("GMAIL_SENDER", recipient)
        print(f"[*] Dispatching Top 10 email directly to {recipient} via Gmail SMTP...")
        return send_via_gmail_smtp(html_content, recipient, sender, gmail_app_pw, subject)
        
    # Priority 2: Resend API
    if api_key:
        sender = os.getenv("SENDER_EMAIL", "onboarding@resend.dev")
        print(f"[*] Dispatching Top 10 email to {recipient} via Resend API...")
        payload = {
            "from": sender,
            "to": [recipient],
            "subject": subject,
            "html": html_content
        }
        try:
            req = urllib.request.Request(
                RESEND_API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.getcode()
                print(f"[+] Email successfully dispatched via Resend API (HTTP {status})!")
                return True
        except Exception as e:
            print(f"[-] Failed to dispatch email via Resend API: {e}")
            return False

    print(f"[*] Neither GMAIL_APP_PASSWORD nor RESEND_API_KEY is configured in .env.")
    print(f"    Saved local HTML preview at {preview_path}.")
    print(f"    To receive live emails directly in Gmail: add GMAIL_APP_PASSWORD to .env (generate at myaccount.google.com/apppasswords).")
    return True


if __name__ == "__main__":
    dispatch_top_jobs_email()
