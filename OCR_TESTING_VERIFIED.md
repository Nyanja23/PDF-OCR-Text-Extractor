services:
  - type: web
    name: pdf-ocr-extractor
    dockerfilePath: ./docker/Dockerfile
    plan: free
    healthCheckPath: /
    healthCheckInterval: 30
    autoDeploy: true
    envVars:
      - key: PORT
        value: 10000# OCR Upload Troubleshooting Guide

## Status: Email Verified ✅

Your email `nyanja.joseph@student.utamu.ac.ug` is now verified and ready to use OCR!

---

## Quick Test

### Option 1: Web UI Test (Easiest)
1. Go to: `https://pdf-ocr-text-extractor-kqk7.onrender.com/`
2. Click **Login** (top right)
3. Enter: `nyanja.joseph@student.utamu.ac.ug` + your password
4. Click **Dashboard** (after login)
5. Upload a PDF or image
6. Click **Process File**
7. Wait for results ✅

### Option 2: CLI Test
```bash
cd /home/joseph/Desktop/pdf-ocr-extractor
chmod +x test_ocr_flow.sh
./test_ocr_flow.sh
```

Note: Edit the script first to set your actual password.

---

## What Should Happen

### Before Upload (Verified User)
```
User Email: nyanja.joseph@student.utamu.ac.ug ✅
User Verified: Yes ✅
Can Access OCR: YES ✅
```

### During Upload
1. File is validated (extension, size)
2. File is saved to `/uploads/` directory
3. OCR processes the file
4. Results returned with job_id

### Expected Response
```json
{
  "job_id": "abc123-def456",
  "filename": "document.pdf",
  "total_pages": 1,
  "results": [
    {
      "page_number": 1,
      "text": "Extracted text from the image...",
      "confidence": 0.92,
      "processing_time": 2.5
    }
  ],
  "total_processing_time": 3.2,
  "created_at": "2026-01-23T10:30:00"
}
```

---

## Supported File Formats

- **Images**: `.jpg`, `.jpeg`, `.png`, `.tiff`
- **Documents**: `.pdf`
- **Max Size**: 10MB (can be changed)
- **Languages**: eng, fra, deu, spa, ita, por, rus, jpn, kor, chi_sim, chi_tra

---

## Debugging if it Fails

### Check 1: Are you logged in?
```bash
# Your session should be valid for 7 days
# Cookie name: session_id
# If expired, login again
```

### Check 2: Render Logs
```
1. Go to Render dashboard
2. Select "pdf-ocr-extractor" service
3. Click "Logs" tab
4. Look for errors like:
   - "Failed to process PDF"
   - "Tesseract command not found"
   - "Network is unreachable"
```

### Check 3: File Requirements
- File must be a real image/PDF (not corrupt)
- File extension must match content
- File size < 10MB
- File has readable content (for OCR)

### Check 4: Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "File type not allowed" | Wrong extension | Use .pdf, .jpg, .png, .tiff |
| "File too large" | Exceeds 10MB | Compress or split file |
| "Failed to process PDF" | Corrupt file | Try different PDF |
| "OCR failed" | Tesseract issue | Check Render environment |
| "403 Forbidden" | Not verified | Verify email first |
| "401 Unauthorized" | Not logged in | Login again |

---

## Test Files

### Create test PDF (Linux/Mac)
```bash
# Create simple text file
echo "Test OCR Document" > test.txt

# Or use ImageMagick
convert -size 300x100 xc:white -pointsize 20 \
  -fill black -annotate +50+50 "Test OCR" test.pdf
```

### Create test image
```bash
# Using ImageMagick
convert -size 400x300 xc:white -pointsize 24 \
  -fill black -annotate +50+100 "Hello World OCR" test.png
```

---

## API Endpoints

### Upload File
```
POST /api/ocr/upload
Headers: 
  - Cookie: session_id=YOUR_SESSION
  - Content-Type: multipart/form-data
Body:
  - file: <file>
  - language: eng (optional)
```

### Get Result
```
GET /api/ocr/result/{job_id}
Headers:
  - Cookie: session_id=YOUR_SESSION
```

---

## Next Steps

1. **Login** to the app
2. **Go to Dashboard**
3. **Upload a PDF or image**
4. **Click Process**
5. **View results**

If you get errors, check the **Render Logs** and share the error message!

---

## Performance Notes

- First OCR takes ~3-5 seconds (Tesseract initialization)
- Subsequent OCRs take ~1-3 seconds
- Large PDFs (50+ pages) may take 1-2 minutes
- Results are cached by job_id for 24 hours

Let me know if you encounter any issues! 🚀
