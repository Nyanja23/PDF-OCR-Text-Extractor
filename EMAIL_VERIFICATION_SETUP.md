`# Email Verification Setup Guide

## Overview
Your app is configured to send real emails for:
- Email verification during signup
- Password reset codes
- OTP (One-Time Password) verification

## Current Configuration
The email service uses **Gmail SMTP** by default (can be changed to any provider).

## Step 1: Configure Environment Variables on Render

You need to set these environment variables in your Render dashboard:

### Required Variables:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_FROM_NAME=PDF OCR Extractor
```

## Step 2: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** (left sidebar)
3. Enable **2-Step Verification** if not already enabled
4. Search for **App passwords**
5. Select **Mail** and **Windows Computer** (or your device)
6. Google will generate a 16-character password
7. Copy this password (remove spaces)

## Step 3: Set Environment Variables on Render

1. Go to your Render dashboard
2. Select your PDF OCR Extractor service
3. Go to **Environment** tab
4. Add the variables from Step 1:
   - `SMTP_HOST=smtp.gmail.com`
   - `SMTP_PORT=587`
   - `SMTP_USER=your_email@gmail.com`
   - `SMTP_PASSWORD=<16-char password from Step 2>`
   - `EMAIL_FROM=your_email@gmail.com`
   - `EMAIL_FROM_NAME=PDF OCR Extractor`

5. Click **Save**
6. Service will automatically redeploy

## Step 4: Test Email Verification

Once deployed:

1. **Register a new account:**
   - Go to: `https://pdf-ocr-text-extractor-kqk7.onrender.com/register`
   - Fill in: email, password, full name
   - Click Register

2. **Check your email:**
   - You should receive an email with a verification code
   - Subject: "Verify Your Email - PDF OCR Extractor"

3. **Verify your email:**
   - Go to: `https://pdf-ocr-text-extractor-kqk7.onrender.com/verify-email`
   - Enter your email and the code from the email
   - Click Verify

4. **Login:**
   - Go to: `https://pdf-ocr-text-extractor-kqk7.onrender.com/login`
   - Use your credentials to login

## Alternative Email Providers

### SendGrid (Recommended for Production)
```
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your_sendgrid_api_key
EMAIL_FROM=your_verified_email@yourdomain.com
```

### AWS SES
```
SMTP_HOST=email-smtp.region.amazonaws.com
SMTP_PORT=587
SMTP_USER=your_aws_username
SMTP_PASSWORD=your_aws_password
EMAIL_FROM=verified_email@yourdomain.com
```

### Mailgun
```
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your_domain.com
SMTP_PASSWORD=your_mailgun_password
EMAIL_FROM=noreply@your_domain.com
```

## Testing Without Real Email

For testing, you can leave SMTP credentials empty and emails will be logged to your Render logs instead:
- The OTP code will be visible in the logs
- No actual emails will be sent

## Troubleshooting

### "Email not received"
- Check spam/junk folder
- Verify SMTP credentials are correct
- Check Render logs for errors

### "SMTP connection failed"
- Verify SMTP_HOST and SMTP_PORT are correct
- Ensure your email provider allows less secure app connections
- For Gmail: Make sure App Password was generated (not regular password)

### "Invalid verification code"
- Code is case-sensitive
- Code expires after 15 minutes (configurable in config.py)
- Each code can only be used once

## Production Recommendations

1. Use a dedicated email service (SendGrid, AWS SES, Mailgun)
2. Configure domain verification for better deliverability
3. Implement email retry logic
4. Monitor email delivery rates
5. Add email templates for branding
