# OCR Upload Error - Solution

## Problem
You're getting a 500 error when uploading files to `/api/ocr/upload` because:

**The OCR endpoint requires email verification!**

The endpoint uses `get_verified_user` dependency which checks:
```python
if not current_user.is_verified:
    raise HTTPException(status_code=403, detail="Please verify your email address")
```

## Solution

### Step 1: Verify Your Email First
1. Go to `/register` → Create account
2. Check **Render logs** for OTP code:
   ```
   🔐 OTP FOR your_email@gmail.com
   Code: 794751
   ```
3. Go to `/verify-email?email=your_email@gmail.com`
4. Enter the 6-digit code
5. Click **Verify**

### Step 2: Login
After verification:
1. Go to `/login`
2. Enter your email and password
3. Login to access dashboard

### Step 3: Upload File
Now that you're verified and logged in:
1. Go to `/dashboard` or `/upload`
2. Upload a PDF or image
3. Click **Process File**
4. OCR should work! ✅

---

## Why This Requirement?

- **Security**: Prevents spam/abuse
- **Email Delivery**: Ensures real users
- **Features**: Some future features may need email contact

---

## Testing OCR

### Option A: Via Web UI
1. Register → Verify email → Login → Upload file

### Option B: Via API (requires valid session)
```bash
# 1. First, verify your email (see above)
# 2. Get session cookie from login
# 3. Upload file with session cookie:

curl -X POST https://pdf-ocr-text-extractor-kqk7.onrender.com/api/ocr/upload \
  -H "Cookie: session_id=YOUR_SESSION_ID" \
  -F "file=@path/to/file.pdf" \
  -F "language=eng"
```

---

## Expected Response

```json
{
  "job_id": "abc123",
  "filename": "document.pdf",
  "total_pages": 5,
  "results": [
    {
      "page_number": 1,
      "text": "Extracted text here...",
      "confidence": 0.95,
      "processing_time": 2.5
    }
  ],
  "total_processing_time": 12.5,
  "created_at": "2026-01-23T12:00:00"
}
```

---

## Debug Tips

If OCR still fails after verification, check:
1. **File size**: Max 10MB (change in `config.py` if needed)
2. **File format**: .pdf, .jpg, .png, .tiff supported
3. **Render logs**: Look for OCR error messages
4. **Language**: Default is 'eng', can specify others

---

## Next Steps

1. ✅ Register and verify email (use OTP from logs)
2. ✅ Login with your credentials
3. ✅ Test OCR upload on dashboard
4. ✅ Check Render logs for any errors

Let me know when you've verified your email and I can help debug any OCR issues!
