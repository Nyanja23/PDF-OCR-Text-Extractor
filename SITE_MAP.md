# 🗺️ PDF OCR Application - Site Map & Navigation Structure

## Application Navigation Tree

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PDF OCR EXTRACTOR APP                               │
│                     Complete Navigation Structure                            │
└─────────────────────────────────────────────────────────────────────────────┘


                           🏠 ENTRY POINTS
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
            hero.html         Direct Link      Deep Link
            Landing Page      Port 8000        API Docs
                 │                │                │
                 │                │                │
    ┌────────────┴────────────┐   │   ┌──────────┴─────────────┐
    │                         │   │   │                        │
    ▼                         ▼   │   ▼                        ▼
┌─────────┐             ┌─────────────┐                    /docs
│  Login  │◄───────────►│   Signup    │
│ /login  │             │ /register   │
└────┬────┘             └──────┬──────┘
     │                         │
     │  ┌─────────────────────┬─┴──────────────┐
     │  │                     │                │
     │  ▼                     ▼                ▼
     │ Forgot         Email          Register
     │ Password      Verification      Verify
     │ /forgot-   /verify-email    /set-new-
     │ password               password
     │  │                     ▲                ▲
     │  └────────────┬────────┘                │
     │               │                         │
     │               ▼                         │
     │        ┌──────────────┐                 │
     │        │ OTP Code     │                 │
     │        │ Entry Form   │                 │
     │        └──────────────┘                 │
     │                                         │
     │      /api/auth/verify-email────────────┘
     │                                         
     │  ┌────────────────────────────────────┐  
     │  │  Google OAuth Button               │  
     │  │  ────────────────────────────      │  
     │  │  Initiates /api/auth/google        │  
     │  │  Redirects to Google OAuth         │  
     │  │  Google returns to:                │  
     │  │  /api/auth/google/callback         │  
     │  │  Backend creates session ✅        │  
     │  │  Redirects to /auth/callback       │  
     │  └──────────────────────────────────┬─┘  
     │                                    │
     │  ┌────────────────────────────────┴──┐
     │  │                                   │
     ▼  ▼                                   ▼
┌────────────────┐                  ┌─────────────────┐
│     Email &    │              ✨  │  OAuth Callback │ ✨ NEW
│   Password     │                  │  /auth/callback │
│   Authentication                  │                 │
│   /api/auth/login                 │ • Processing    │
│                                    │   State         │
│ Returns:                           │ • Success State │
│ • access_token                     │ • Error State   │
│ • session_id (cookie)              │ • Auto Redirect │
└────────┬───────┘                  └────────┬────────┘
         │                                   │
         │  ┌──────────────────────────────┬┘
         │  │                              │
         ▼  ▼                              ▼
      ┌──────────────────────────────────────┐
      │                                      │
      │        🎯 MAIN APPLICATION          │
      │                                      │
      │  /dashboard                         │
      │  Dashboard (Authenticated)      ✨ NEW
      │                                      │
      │  Features:                           │
      │  • File Upload (Drag & Drop)         │
      │  • Language Selection                │
      │  • Recent Documents                  │
      │  • User Profile Header               │
      │  • Logout Button                     │
      │                                      │
      └──────────┬──────────────┬───────────┘
                 │              │
    ┌────────────┴──┐   ┌───────┴──────────┐
    │               │   │                  │
    ▼               ▼   ▼                  ▼
 Upload          Settings        View Results
 File           /settings    /results/{job_id}
    │              ✨ NEW          ✨ NEW
    │               │               │
    │  Process      │               │
    │  Document     │               │
    │    │          │               │
    │    ▼          │               │
    │ /api/ocr/     │               │
    │ upload        │               │
    │    │          │               │
    │    ├─────────►│   ┌───────────┤
    │    │          │   │           │
    │    ▼          ▼   ▼           ▼
    │ Get Job    Profile    Extract Text
    │ Results    Security   • Copy Text
    └──────────► Settings   • Download
       │        Notifications• Statistics
       │        Account     • Metadata
       │        Danger Zone • Share
       ▼
    /api/ocr/
    result/
    {job_id}
       │
       ▼
   Display in
   Results Page
```

---

## Page Connectivity Map

### 1️⃣ **Landing Page** (hero.html)
```
hero.html (/")
├── Navigation to /login
├── Navigation to /register  
└── Features overview
```

### 2️⃣ **Authentication Hub**
```
login.html (/login)
├── Email/Password Form
│   └── POST /api/auth/login
│       └── Redirect to /dashboard ✅
├── Google OAuth Button
│   └── GET /api/auth/google
│       └── Google Consent
│           └── GET /api/auth/google/callback (Backend)
│               └── Redirect to /auth/callback
│                   └── callback.html
├── Link to signup.html
└── Link to forgot_password.html


signup.html (/register)
├── Registration Form
│   └── POST /api/auth/register
│       └── Redirect to /verify-email
├── Link to login.html
└── Google Sign-up Option


email_verification.html (/verify-email)
├── OTP Input Form
│   └── POST /api/auth/verify-email
│       └── Redirect to login.html (success)
└── Resend Option


forgot_password.html (/forgot-password)
├── Email Entry
│   └── POST /api/auth/password-reset/request
├── OTP Input
└── New Password Form
    └── POST /api/auth/password-reset/confirm
        └── Redirect to login.html


set_new_password.html (/reset-password)
└── Password Reset Completion
    └── Link back to /login
```

### 3️⃣ **OAuth Callback Flow**
```
callback.html (/auth/callback) ✨ NEW
├── URL Parameters
│   ├── code=oauth_success (success case)
│   ├── error=... (error case)
│   └── error_description=... (error details)
│
├── Processing State
│   └── Show loading animation
│
├── Check Session
│   └── GET /api/users/profile (verify authenticated)
│
├── Success State
│   ├── Display user info
│   ├── Show checkmark
│   └── Countdown Timer (3 seconds)
│
├── Error State
│   ├── Show error message
│   └── Retry button → back to login.html
│
└── Auto-Redirect
    └── window.location = '/dashboard' ✅
```

### 4️⃣ **Main Application**
```
dashboard.html (/dashboard) ✨ NEW
├── Header
│   ├── User Profile Card
│   │   └── Avatar, Name, Email
│   └── Logout Button
│       └── POST /api/auth/logout
│
├── Upload Section
│   ├── Drag & Drop Zone
│   ├── File Input
│   ├── Language Selector
│   └── Process Button
│       └── POST /api/ocr/upload
│           └── Redirect to /results/{job_id}
│
├── Quick Start Guide
│   └── Tips for best OCR results
│
├── Recent Documents Section
│   ├── Job Cards Grid
│   │   ├── View Button → /results/{job_id}
│   │   └── Delete Button
│   └── Empty State (if no jobs)
│
└── Navigation
    ├── Link to /settings
    └── Logout option


results.html (/results/{job_id}) ✨ NEW
├── Header
│   ├── Document Name
│   ├── Metadata (Date, Pages, Time)
│   └── Back to Dashboard Link
│
├── Actions
│   ├── Download Text Button
│   │   └── Downloads .txt file
│   └── Copy All Button
│       └── Navigator.clipboard.writeText()
│
├── Main Content
│   ├── Page Selector Dropdown
│   ├── Extracted Text Viewer
│   │   ├── Copy Button (per page)
│   │   └── Scrollable text area
│   └── Loading State (simulation)
│       └── GET /api/ocr/result/{job_id}
│
└── Sidebar
    ├── Statistics
    │   ├── Character Count
    │   ├── Word Count
    │   └── Confidence Score
    ├── OCR Info
    │   ├── Language Used
    │   ├── Status
    │   └── Engine Version
    └── Actions
        ├── Download as TXT
        ├── Share Results
        └── Process Again → /dashboard


settings.html (/settings) ✨ NEW
├── Header
│   └── Back to Dashboard Link
│
├── Sidebar Navigation
│   ├── Profile Tab
│   ├── Security Tab
│   ├── Notifications Tab
│   └── Account Tab
│
├── Profile Tab
│   ├── Avatar Display
│   ├── User Info
│   ├── Edit Form
│   │   ├── Name Input
│   │   ├── Email Input
│   │   └── Bio Input
│   └── Save Button
│       └── PUT /api/users/profile
│           └── Success Notification
│
├── Security Tab
│   ├── Change Password
│   │   ├── Current Password Input
│   │   ├── New Password Input
│   │   ├── Confirm Input
│   │   └── Submit
│   │       └── POST /api/users/change-password
│   │           └── Success Notification
│   └── Sessions
│       ├── Active Sessions List
│       └── Logout All Devices
│           └── Redirect to /login
│
├── Notifications Tab
│   ├── Email Notifications Toggle
│   ├── Processing Alerts Toggle
│   ├── Feature News Toggle
│   └── Security Alerts Toggle
│       └── Save Button
│
└── Account Tab
    ├── Account Info Display
    │   ├── Created Date
    │   ├── Last Login
    │   ├── Status
    │   └── Auth Method
    └── Danger Zone
        ├── Delete Account Button
        │   └── Confirmation Dialog
        │       └── DELETE /api/users/account
        │           └── Redirect to /hero
        └── Warning Message
```

---

## API Endpoint Map

```
Authentication API
├── POST /api/auth/register
├── POST /api/auth/verify-email
├── POST /api/auth/login
├── POST /api/auth/logout
├── GET /api/auth/google              (Initiate OAuth)
├── GET /api/auth/google/callback     (OAuth response - backend)
├── POST /api/auth/password-reset/request
├── POST /api/auth/password-reset/confirm
└── GET /api/auth/me                  (Get current user)

User Management API
├── GET /api/users/profile
├── PUT /api/users/profile
├── POST /api/users/change-password
└── DELETE /api/users/account

OCR Processing API
├── POST /api/ocr/upload              (Process document)
└── GET /api/ocr/result/{job_id}      (Get results)

Health & Info
├── GET /health                       (Health check)
└── GET /docs                         (API Documentation)
```

---

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────┐
│                    USER ACTION FLOW                         │
└────────────────────────────────────────────────────────────┘

NEW USER JOURNEY:
─────────────────
hero.html
    ↓ (Click "Sign Up")
signup.html (enter details) 
    ↓ POST /api/auth/register
email_verification.html (enter OTP)
    ↓ POST /api/auth/verify-email
login.html (success message)
    ↓ (Re-login)
login.html (enter credentials)
    ↓ POST /api/auth/login
dashboard.html ✅


EXISTING USER JOURNEY:
─────────────────────
login.html (email + password)
    ↓ POST /api/auth/login
dashboard.html ✅


GOOGLE OAUTH JOURNEY:
───────────────────
login.html (click "Google")
    ↓ GET /api/auth/google
[Google Consent Screen]
    ↓ (User approves)
/api/auth/google/callback (backend)
    ↓ POST /api/auth/google/callback (backend logic)
[Backend creates session]
    ↓ Redirect to /auth/callback?code=oauth_success
callback.html (process & display)
    ↓ (3 second countdown)
dashboard.html ✅


OCR PROCESSING JOURNEY:
──────────────────────
dashboard.html (upload file)
    ↓ Drag & drop file
Select language → Click "Process"
    ↓ POST /api/ocr/upload (with file)
[Backend processes with OCR]
    ↓ Returns job_id + results
results.html (/results/{job_id})
    ↓ GET /api/ocr/result/{job_id}
Display extracted text
    ↓ [Copy / Download / Share / Process Again]
    └─► back to dashboard.html


ACCOUNT MANAGEMENT JOURNEY:
──────────────────────────
dashboard.html (user profile menu)
    ↓ Click "Settings"
settings.html
    ├─► Profile Tab
    │   ├─ Edit profile
    │   └─ PUT /api/users/profile
    │
    ├─► Security Tab
    │   ├─ Change password
    │   └─ POST /api/users/change-password
    │
    ├─► Notifications Tab
    │   └─ Update preferences (local)
    │
    └─► Account Tab
        └─ Delete account
            └─ DELETE /api/users/account
                └─ Redirect to hero.html
```

---

## Component Reusability

### Shared Components (Used Across Pages)

#### Header Pattern
```
header {
  ├─ Logo/Brand (click to go home)
  ├─ Navigation Links
  └─ User Action Buttons
}
Used in: dashboard.html, settings.html, results.html, callback.html
```

#### Card Component
```
.card {
  ├─ Glassmorphism background
  ├─ Gradient top border
  ├─ Smooth shadow
  └─ Hover effects
}
Used in: All pages
```

#### Button Styles
```
Gradient Primary:  #667eea → #764ba2
Secondary:        Light purple tint
Danger:           Red tint
Download/Success: Green tint
```

#### Form Pattern
```
form {
  ├─ Input field with focus state
  ├─ Label
  ├─ Help text
  └─ Validation feedback
}
Used in: login, signup, settings
```

#### Animation Set
```
slideInDown    - Header animations
slideInLeft    - Left sections
slideInUp      - Main content
fadeIn         - Opacity transitions
pulse          - Loading indicators
float          - Background orbs
```

---

## Mobile Responsive Breakpoints

```
Desktop  (1024px+)  → Full layouts with sidebars
Tablet   (768-1023) → Adjusted grid columns, hidden sidebars
Mobile   (<768px)   → Single column, hamburger nav, touch-friendly
```

---

## Summary Statistics

```
Total HTML Pages:     12
├─ Created (New):      4 ✨
│  ├─ dashboard.html
│  ├─ callback.html
│  ├─ results.html
│  └─ settings.html
│
└─ Existing:           8
   ├─ hero.html
   ├─ login.html
   ├─ signup.html
   ├─ email_verification.html
   ├─ forgot_password.html
   ├─ set_new_password.html
   ├─ features.html
   └─ startup.html

API Routes Created:   12 (in pages.py)
Components Unified:   6 (cards, buttons, forms, animations, etc.)
Total Navigation Links: 40+
User Flows Supported: 5 (Registration, Login, OAuth, OCR, Settings)
```

---

This map shows every page connection, data flow, and navigation path in the complete PDF OCR application!
