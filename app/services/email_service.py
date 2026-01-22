"""
app/services/email_service.py
Email sending service for OTP and notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.config import settings


def send_email(to_email: str, subject: str, html_content: str, text_content: Optional[str] = None):
    """Send email via SMTP"""
    # For development/testing: if no SMTP credentials, log to console instead
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD or not settings.EMAIL_FROM:
        print(f"\n{'='*80}")
        print(f"📧 EMAIL (Development Mode - Not Actually Sent)")
        print(f"{'='*80}")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"{'─'*80}")
        print(text_content if text_content else "[HTML content only - see terminal for HTML]")
        print(f"{'='*80}\n")
        return True
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # Add plain text version
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        
        # Add HTML version
        msg.attach(MIMEText(html_content, "html"))
        
        # Connect to SMTP server
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✉️ Email sent to {to_email}")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False


def send_otp_email(to_email: str, otp_code: str, purpose: str):
    """Send OTP email for verification or password reset"""
    
    if purpose == "email_verification":
        subject = "Verify Your Email - PDF OCR Extractor"
        heading = "Verify Your Email Address"
        message = "Thank you for signing up! Please use the code below to verify your email address:"
    elif purpose == "password_reset":
        subject = "Reset Your Password - PDF OCR Extractor"
        heading = "Reset Your Password"
        message = "You requested to reset your password. Use the code below to proceed:"
    else:
        subject = "Your Verification Code - PDF OCR Extractor"
        heading = "Verification Code"
        message = "Your verification code is:"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 40px 30px;
            }}
            .content p {{
                margin: 0 0 20px 0;
                font-size: 16px;
                color: #555;
            }}
            .otp-box {{
                background-color: #f8f9fa;
                border: 2px dashed #667eea;
                border-radius: 8px;
                padding: 30px;
                text-align: center;
                margin: 30px 0;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #667eea;
                font-family: 'Courier New', monospace;
            }}
            .warning {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .warning p {{
                margin: 0;
                font-size: 14px;
                color: #856404;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 14px;
                color: #6c757d;
                border-top: 1px solid #e9ecef;
            }}
            .footer a {{
                color: #667eea;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 {heading}</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>{message}</p>
                
                <div class="otp-box">
                    <div class="otp-code">{otp_code}</div>
                </div>
                
                <div class="warning">
                    <p><strong>⚠️ Important:</strong> This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes. Do not share this code with anyone.</p>
                </div>
                
                <p>If you didn't request this code, please ignore this email or contact support if you have concerns.</p>
            </div>
            <div class="footer">
                <p>© 2026 PDF OCR Text Extractor. All rights reserved.</p>
                <p>Need help? <a href="mailto:support@pdfocr.com">Contact Support</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    {heading}
    
    {message}
    
    Your verification code is: {otp_code}
    
    This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
    
    If you didn't request this code, please ignore this email.
    
    © 2026 PDF OCR Text Extractor
    """
    
    return send_email(to_email, subject, html_content, text_content)


def send_welcome_email(to_email: str, user_name: str):
    """Send welcome email after successful registration"""
    subject = "Welcome to PDF OCR Extractor!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome!</title>
    </head>
    <body>
        <h2>Welcome{' ' + user_name if user_name else ''}! 🎉</h2>
        <p>Your account has been successfully created and verified.</p>
        <p>You can now start extracting text from your PDFs and images.</p>
        <p>Happy extracting!</p>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)
