# Email Verification Testing Guide

## Complete Test Flow

### Step 1: Go to Registration Page
```
https://pdf-ocr-text-extractor-kqk7.onrender.com/register
```

### Step 2: Register with a NEW Email
Use a unique email each time (not one you've registered before):
- **Email**: `test.user+$(date +%s)@gmail.com` (generates unique emails)
- **Password**: Must include:
  - At least 1 UPPERCASE letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character (!@#$%^&*(),.?":{}|<>)
  
  Example: `MyPassword123!`
  
- **Full Name**: Your name

### Step 3: After Registration
You'll see: `"Registration successful. Please check your email for verification code."`

The page will **automatically redirect** you to:
```
https://pdf-ocr-text-extractor-kqk7.onrender.com/verify-email?email=your.email@gmail.com
```

### Step 4: Check Your Email
Look for an email with:
- **Subject**: `Verify Your Email - PDF OCR Extractor`
- **Contains**: A 6-digit code

Check spam/promotions folder if not in inbox!

### Step 5: Enter Verification Code
Back on the verification page, enter the 6 digits and click **Verify Email**

### Step 6: Success!
You'll be redirected to login page, now you can log in with your credentials.

---

## Quick Email Examples for Testing

Here are some unique test emails you can use:

```
test.user.1@gmail.com
test.user.2@gmail.com
test.jan22a@gmail.com
test.jan22b@gmail.com
test.dev001@gmail.com
```

Or generate unique ones with timestamps:
```bash
# Generate a unique test email
echo "test.user+$(date +%s)@gmail.com"
# Output: test.user+1705948325@gmail.com
```

---

## Troubleshooting

### ❌ "Email already registered"
- Use a different email address
- Database still has your old email

### ❌ "Verification code not working"
- Make sure you entered the EXACT code from email
- Code is case-sensitive
- Code expires after 15 minutes
- Each code can only be used once

### ❌ "Email not received"
- Check spam/promotions/other folders
- Wait 1-2 minutes
- Gmail takes time to deliver
- Check if SMTP credentials are set correctly in Render

### ❌ "Can't see my email in database"
This is normal! Emails are only visible if:
- Registration succeeded
- Email was actually sent (if configured)

---

## Direct API Testing

If you want to test the API directly:

### 1. Register via API
```bash
curl -X POST https://pdf-ocr-text-extractor-kqk7.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test'$(date +%s)'@gmail.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'
```

Response:
```json
{
  "message": "Registration successful. Please check your email for verification code.",
  "email": "test@gmail.com",
  "user_id": 1
}
```

### 2. Verify Email via API
```bash
curl -X POST https://pdf-ocr-text-extractor-kqk7.onrender.com/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@gmail.com",
    "code": "123456"
  }'
```

### 3. Login via API
```bash
curl -X POST https://pdf-ocr-text-extractor-kqk7.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@gmail.com",
    "password": "TestPassword123!"
  }'
```

---

## Email Configuration Check

To verify email is working:

1. Go to Render dashboard
2. Select your PDF OCR service
3. Check **Logs** tab for:
   - `✉️ Email sent to test@gmail.com` = Email sent successfully
   - `❌ Failed to send email` = SMTP configuration issue

4. Check **Environment** tab for:
   - `SMTP_HOST` = smtp.gmail.com
   - `SMTP_PORT` = 587
   - `SMTP_USER` = your_email@gmail.com
   - `SMTP_PASSWORD` = app_password (not regular password)
   - `EMAIL_FROM` = your_email@gmail.com

---

## Expected Timeline

1. **Click Register** → Instant response
2. **Check Email** → 1-2 minutes
3. **Enter Code** → Instant response
4. **Login** → Instant response

If no email after 5 minutes, check Render logs!
