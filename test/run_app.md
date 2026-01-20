# Running and Testing PDF OCR Extractor Locally

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Running the Application](#running-the-application)
4. [Testing Guide](#testing-guide)
5. [What Can Be Tested Locally](#what-can-be-tested-locally)
6. [What Cannot Be Tested Locally](#what-cannot-be-tested-locally)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 2GB (4GB recommended for OCR processing)
- **Disk Space**: 500MB for dependencies and test files

### Required External Tools
- **Tesseract OCR**: Must be installed separately
  - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
  - **macOS**: `brew install tesseract`
  - **Windows**: Download installer from [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Optional - For Full OAuth Testing
- **Google OAuth Credentials**: Not required for local testing (can be mocked)
- **Docker**: For containerized deployment (optional)

---

## Setup Instructions

### 1. Clone/Navigate to Project Directory
```bash
cd /home/joseph/Desktop/pdf-ocr-extractor
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - ORM
- Authlib - OAuth
- pytesseract - OCR wrapper
- python-multipart - File uploads
- python-dotenv - Environment variables

### 4. Create Environment File
```bash
# Create .env file in project root
cat > .env << 'EOF'
# Database
DATABASE_URL=sqlite:///./ocr_app.db

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth (Optional - for local testing with mock)
GOOGLE_CLIENT_ID=mock_client_id
GOOGLE_CLIENT_SECRET=mock_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# Email (Optional - for local testing)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# OCR
TESSERACT_PATH=/usr/bin/tesseract  # Adjust based on your OS
EOF
```

### 5. Initialize Database
```bash
# Database will auto-create on first run, but you can manually initialize:
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

---

## Running the Application

### Start the Backend Server
```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode (no auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Access the Application

1. **Frontend (Home Page)**: http://localhost:8000
2. **Swagger API Docs**: http://localhost:8000/docs
3. **ReDoc API Docs**: http://localhost:8000/redoc

### Default Navigation
- **Home/Hero**: http://localhost:8000/
- **Login**: http://localhost:8000/login
- **Register**: http://localhost:8000/register
- **Dashboard** (requires login): http://localhost:8000/dashboard
- **Settings** (requires login): http://localhost:8000/settings

---

## Testing Guide

### Manual Testing Workflow

#### 1. Test User Registration (✅ Fully Testable Locally)
```
Step 1: Navigate to http://localhost:8000/register
Step 2: Fill in form:
  - First Name: John
  - Last Name: Doe
  - Email: test@example.com
  - Password: TestPassword123!
  - Confirm Password: TestPassword123!
Step 3: Click "Create Account"
Expected: Success page or redirect to login
Step 4: Check SQLite database for new user
  sqlite3 ocr_app.db "SELECT * FROM user;"
```

#### 2. Test User Login (✅ Fully Testable Locally)
```
Step 1: Navigate to http://localhost:8000/login
Step 2: Enter credentials:
  - Email: test@example.com
  - Password: TestPassword123!
Step 3: Click "Sign In"
Expected: Redirect to /dashboard with session cookie
Step 4: Verify cookie in browser DevTools (Application > Cookies)
```

#### 3. Test File Upload (✅ Partially Testable Locally)
```
Step 1: Login and navigate to /dashboard
Step 2: Select language (English)
Step 3: Drag & drop PDF file OR click "Choose Files"
Step 4: Select sample PDF file
Expected: 
  - File validation passes (size < 25MB, type = pdf/image)
  - Loading indicator shows
  - API call to POST /api/ocr/upload
  - Response contains job_id
  - Recent documents update
```

#### 4. Test OCR Processing (✅ Partially Testable Locally - Requires Tesseract)
```
Prerequisites: Tesseract installed and configured
Step 1: Upload PDF/image file
Step 2: Monitor console output for OCR processing
Step 3: Wait for processing completion
Expected:
  - Tesseract processes image
  - Text extracted and saved to database
  - Results page displays extracted text
```

#### 5. Test Results Viewer (✅ Fully Testable Locally)
```
Step 1: From dashboard, click recent document OR access:
  http://localhost:8000/results/job_id_here
Step 2: Verify page displays:
  - Extracted text in viewer
  - Page selector (if multi-page)
  - Copy button functionality
  - Download as TXT button
Step 3: Test copy: Select text, click "Copy", paste elsewhere
Step 4: Test download: Click download, verify file saved
```

#### 6. Test Settings Page (✅ Fully Testable Locally)
```
Step 1: Login and navigate to /settings
Step 2: Test Profile Tab:
  - Edit name, click Save
  - Verify changes persist (refresh page)
Step 3: Test Security Tab:
  - Change password
  - Logout and login with new password
Step 4: Test Notifications Tab:
  - Toggle notification preferences
  - Save and verify
Step 5: Test Account Tab:
  - Verify account info displays correctly
```

#### 7. Test Password Reset (✅ Partially Testable Locally - Email Limitations)
```
Step 1: Click "Forgot Password" on login page
Step 2: Enter registered email: test@example.com
Step 3: In console, you'll see verification code (instead of email)
Step 4: Enter code in verification field
Step 5: Set new password and confirm
Expected: Password changes successfully
Limitation: No actual email sent locally
Workaround: Check console logs for verification code
```

#### 8. Test Responsive Design (✅ Fully Testable Locally)
```
Chrome DevTools Method:
Step 1: Open any page
Step 2: Press F12 to open DevTools
Step 3: Click device icon (top-left)
Step 4: Select device preset:
  - iPhone 12 (375px width)
  - iPad (768px width)
  - Desktop (1024px+ width)
Step 5: Verify layout adjusts properly
Expected:
  - Mobile: Single column, stacked elements
  - Tablet: 2-column grid where applicable
  - Desktop: Full layout with sidebars
```

#### 9. Test Browser Compatibility (✅ Fully Testable Locally)
```
Test in multiple browsers:
  - Chrome/Chromium
  - Firefox
  - Safari (macOS)
  - Edge
Expected: All pages render correctly, no JS errors
```

#### 10. Test API Rate Limiting (✅ Testable with Rate Limit Middleware)
```
Prerequisites: Rate limit middleware enabled in main.py
Step 1: Send rapid requests (>100/minute to same endpoint)
Step 2: Observe 429 Too Many Requests response
```

---

## What Can Be Tested Locally

### ✅ Full Local Testing (No External Services Needed)

#### Frontend/UI Testing
- [x] Page load and rendering
- [x] Responsive design (mobile/tablet/desktop)
- [x] CSS animations and transitions
- [x] Form validation
- [x] Button interactions
- [x] Navigation between pages
- [x] Local storage persistence (JavaScript)
- [x] Loading states and spinners
- [x] Error message display
- [x] Success notifications

#### Authentication
- [x] User registration
- [x] User login/logout
- [x] Session management (local)
- [x] Password validation rules
- [x] Form field validation
- [x] User profile viewing
- [x] Profile editing
- [x] Account deletion confirmation

#### File Handling
- [x] File selection (browser file picker)
- [x] Drag & drop upload UI
- [x] File type validation (PDF/Image)
- [x] File size validation (<25MB)
- [x] Error messages for invalid files

#### OCR (Local Processing)
- [x] OCR text extraction (if Tesseract installed)
- [x] Results display
- [x] Text copy functionality
- [x] Text download as .txt file
- [x] Multi-page navigation
- [x] Text statistics calculation
- [x] Page count display

#### Settings Management
- [x] Profile information display
- [x] Profile information update
- [x] Password change
- [x] Notification preference toggles
- [x] Account information viewing

#### API (Backend)
- [x] User registration endpoint
- [x] User login endpoint
- [x] User profile endpoint
- [x] Profile update endpoint
- [x] Password change endpoint
- [x] OCR upload endpoint (local processing)
- [x] OCR result retrieval endpoint
- [x] Database operations (SQLite)

#### Database
- [x] User creation
- [x] User profile updates
- [x] OCR job storage
- [x] Results persistence
- [x] Transaction integrity
- [x] Data deletion

#### Security (Local)
- [x] Password hashing verification (bcrypt)
- [x] CORS configuration
- [x] Session cookie security (HTTP-only)
- [x] CSRF protection
- [x] Input validation
- [x] SQL injection prevention (SQLAlchemy ORM)

---

## What Cannot Be Tested Locally

### ❌ Requires External Services

#### Email Services
```
❌ Cannot send actual emails without:
  - SMTP server credentials (Gmail, SendGrid, etc.)
  - Real email account
  
Limitations:
  - Email verification cannot send actual verification codes
  - Password reset emails won't be sent
  - Account confirmation emails won't be sent
  
Workarounds:
  - Check console logs for generated codes/links
  - Use MailHog or similar local email testing tool
  - Mock email service in testing
```

#### Google OAuth
```
❌ Cannot complete Google OAuth flow without:
  - Valid Google OAuth credentials
  - Google Cloud project setup
  - Verified redirect URI with Google
  - Real Google user account for testing
  
Limitations:
  - OAuth callback won't work with production Google account
  - Cannot test "Sign in with Google" button functionality
  - Callback redirect won't complete
  
Workarounds:
  - Set up local Google OAuth app in Google Cloud Console
  - Use mock OAuth for development
  - Test OAuth integration manually in staging environment
  - Implement OAuth testing with fake credentials
```

#### Production Database
```
❌ SQLite limitations:
  - Not suitable for concurrent requests (production bottleneck)
  - Not multi-user concurrent safe
  - Limited scalability testing
  
Cannot test:
  - High concurrency scenarios
  - Database sharding
  - Replication
  
Workarounds:
  - Use PostgreSQL locally with Docker:
    docker run --name postgres -e POSTGRES_PASSWORD=password \
    -p 5432:5432 -d postgres
  - Update DATABASE_URL in .env to:
    postgresql://postgres:password@localhost/ocr_db
```

#### Cloud Storage
```
❌ Cannot test without cloud provider setup:
  - AWS S3 bucket configuration
  - Google Cloud Storage access
  - Azure Blob Storage setup
  
Currently testing with:
  - Local file uploads (uploads/ directory)
  - Not production-ready for scale
  
Workarounds:
  - Set up moto (AWS mocking library) for S3 testing
  - Use LocalStack for cloud service emulation
  - Mock storage service in development
```

#### SMS/Two-Factor Authentication
```
❌ Not implemented in current version
  - Cannot test 2FA functionality
  - Cannot test SMS notifications
  - Cannot test backup codes
```

#### Advanced OCR Features
```
⚠️ Limited testing capability:
  - OCR language packs (can test installed languages only)
  - Complex document types (forms, tables, handwriting)
  - Batch processing at scale
  - OCR with GPU acceleration
  
Testable locally:
  - Basic text extraction with English/installed languages
  - Single document processing
  - API response format
```

#### Deployment & Infrastructure
```
❌ Cannot test without deployment:
  - Docker containerization
  - Kubernetes orchestration
  - CI/CD pipeline
  - Load balancing
  - Reverse proxy configuration
  - SSL/HTTPS certificate handling
```

#### Analytics & Monitoring
```
❌ Cannot test without external services:
  - Google Analytics
  - Error tracking (Sentry)
  - Performance monitoring
  - User behavior analytics
```

#### Payment Processing
```
❌ Not implemented in current version
  - No payment gateway integration
  - No subscription management
  - No Stripe/PayPal testing
```

---

## Testing Checklist

### Quick Test (5 minutes)
```
[ ] Backend server starts: uvicorn main:app --reload
[ ] Frontend loads: http://localhost:8000
[ ] Swagger docs accessible: http://localhost:8000/docs
[ ] Database initializes without errors
[ ] No console errors in browser
```

### Basic Functionality Test (30 minutes)
```
[ ] Register new user account
[ ] Login with created credentials
[ ] View profile on dashboard
[ ] Access settings page
[ ] Update profile information
[ ] Change password
[ ] Logout and login with new password
[ ] View responsive design on mobile viewport
```

### File Upload & OCR Test (15 minutes)
```
[ ] Upload sample PDF file
[ ] File validation works (rejects invalid files)
[ ] OCR processing starts
[ ] Results page displays extracted text
[ ] Copy text button works
[ ] Download as TXT button works
[ ] Navigate between pages (if multi-page)
```

### API Testing (20 minutes)
```
[ ] Test endpoints in Swagger UI:
    - POST /api/auth/register
    - POST /api/auth/login
    - GET /api/users/profile
    - PUT /api/users/profile
    - POST /api/ocr/upload
    - GET /api/ocr/result/{job_id}
[ ] Verify response formats
[ ] Check error responses
[ ] Validate status codes
```

### Security Test (10 minutes)
```
[ ] Try accessing /dashboard without login (should redirect to login)
[ ] Try accessing /settings without login (should redirect to login)
[ ] Verify session cookie is HTTP-only (DevTools)
[ ] Try submitting form with malicious input (should be sanitized)
[ ] Verify CORS headers in responses
```

---

## Troubleshooting

### Server Won't Start
```bash
# Error: Address already in use
# Solution: Use different port
uvicorn main:app --reload --port 8001

# Error: Module not found
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# Error: Database locked
# Solution: Remove old database and restart
rm ocr_app.db
uvicorn main:app --reload
```

### Tesseract Not Found
```bash
# Error: pytesseract.TesseractNotFoundError
# Solution: Install and configure Tesseract

# Linux/Debian
sudo apt-get install tesseract-ocr
# Update .env: TESSERACT_PATH=/usr/bin/tesseract

# macOS
brew install tesseract
# Update .env: TESSERACT_PATH=/usr/local/bin/tesseract

# Windows
# Download installer: https://github.com/UB-Mannheim/tesseract/wiki
# Update .env: TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### File Upload Not Working
```bash
# Ensure uploads directory exists
mkdir -p uploads/

# Check permissions
chmod 755 uploads/

# Verify file size limits in config
# Max upload: 25MB (configurable in core/config.py)
```

### Database Errors
```bash
# Reset database
rm ocr_app.db

# Reinitialize
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Check database contents
sqlite3 ocr_app.db ".tables"
sqlite3 ocr_app.db "SELECT * FROM user;"
```

### CORS Errors in Browser
```bash
# Error: Access to XMLHttpRequest blocked by CORS policy
# Cause: Frontend making requests to different origin
# Solution: Check CORS configuration in main.py
# Ensure frontend and backend on same origin (localhost:8000)
```

### Session Cookie Not Persisting
```bash
# Issue: Login succeeds but cookie lost on refresh
# Check: Browser DevTools > Application > Cookies
# Verify: Session cookie is HTTP-only, Secure=false (local), SameSite=Lax
# Solution: Check session middleware configuration in main.py
```

### Slow OCR Processing
```bash
# Issue: OCR takes too long
# Causes:
  1. Large image resolution (reduce image size)
  2. Multiple languages enabled (use single language)
  3. Complex document (preprocessing might help)
# Solution: Optimize image before upload or use image preprocessing
```

---

## Docker Testing (Optional)

### Run with Docker Compose
```bash
cd docker/
docker-compose up -d

# Access application at http://localhost:8000
# View logs: docker-compose logs -f app
# Stop: docker-compose down
```

### Run with Docker Only
```bash
# Build image
docker build -t pdf-ocr-extractor .

# Run container
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads pdf-ocr-extractor

# Access at http://localhost:8000
```

---

## Performance Testing (Load Testing)

### Using Apache Bench
```bash
# Install
sudo apt-get install apache2-utils

# Test homepage (10 requests, 5 concurrent)
ab -n 10 -c 5 http://localhost:8000/

# Test login endpoint
ab -n 10 -c 5 -p data.json -T application/json \
  http://localhost:8000/api/auth/login
```

### Using Locust
```bash
# Install
pip install locust

# Create locustfile.py with test scenarios
# Run
locust -f locustfile.py --host=http://localhost:8000
```

---

## Next Steps After Local Testing

1. **Deploy to Staging**
   - Configure PostgreSQL database
   - Set up Google OAuth credentials
   - Configure email service (SendGrid/Gmail)
   - Set up error tracking (Sentry)

2. **Integration Testing**
   - Test with real Google OAuth
   - Test email sending
   - Test with production-like database

3. **User Acceptance Testing**
   - Have users test workflows
   - Gather feedback on UX
   - Test on real devices

4. **Performance Testing**
   - Load testing with concurrent users
   - Database optimization
   - CDN configuration

5. **Security Testing**
   - Penetration testing
   - OWASP vulnerability scanning
   - SSL/TLS certificate setup

---

## Quick Reference - Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload

# Access application
open http://localhost:8000

# Check database
sqlite3 ocr_app.db "SELECT * FROM user;"

# Reset database
rm ocr_app.db

# Run tests (if test suite exists)
pytest tests/

# Format code
black app/

# Lint code
pylint app/

# Type check
mypy app/
```

---

## Summary

| Feature | Local | Notes |
|---------|-------|-------|
| Frontend UI | ✅ | Fully testable |
| User Auth | ✅ | Works locally |
| File Upload | ✅ | Works with local storage |
| OCR Processing | ✅ | If Tesseract installed |
| Email | ❌ | Needs SMTP setup |
| Google OAuth | ❌ | Needs Google credentials |
| SMS/2FA | ❌ | Not implemented |
| Cloud Storage | ❌ | Needs AWS/GCP setup |
| Database Scale | ⚠️ | SQLite limited |
| Load Testing | ✅ | With tools like Locust |

---

**Happy Testing! 🚀**
