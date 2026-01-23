# Render Deployment Fix - Tesseract Installation

## Problem
Tesseract OCR is not installed on Render because:
- ❌ Render is running as **native Python**, not Docker
- ❌ The Dockerfile dependencies aren't used in native deployment
- ❌ System packages need to be installed via build script

## Solution

### Option 1: Use `render.yaml` (Recommended)
This tells Render to run the `build.sh` script before installing Python packages.

**Steps:**
1. A `render.yaml` file has been created in your repo root
2. Push to GitHub:
   ```bash
   git add . && git commit -m "Add Render build configuration for Tesseract" && git push
   ```
3. Redeploy on Render:
   - Go to Render dashboard
   - Select your service
   - Click **Redeploy** (or wait for auto-redeploy)
   - Wait 3-5 minutes for build to complete
   - Check Logs to verify Tesseract installed

### Option 2: Manual Configuration in Render Dashboard
If Option 1 doesn't work:

1. Go to Render Dashboard
2. Select **pdf-ocr-extractor** service
3. Go to **Settings** tab
4. Find **Build Command**
5. Set to:
   ```bash
   bash build.sh && pip install -r requirements.txt
   ```
6. Save and **Redeploy**

### Option 3: Switch to Docker Deployment
If you want to use your Dockerfile instead:

1. In Render dashboard
2. Delete current service
3. Create **New Web Service**
4. Select **Docker** as environment
5. Connect your GitHub repo
6. Build should use your Dockerfile automatically

---

## What the Build Script Does

```bash
# Update package manager
apt-get update

# Install Tesseract and dependencies
apt-get install -y \
    tesseract-ocr \        # Main OCR engine
    libtesseract-dev \     # Development files
    poppler-utils \        # PDF processing
    libpq-dev \            # PostgreSQL
    gcc \                  # C compiler
    libgl1 \               # OpenGL
    libglib2.0-0           # GLib

# Verify installation
tesseract --version        # Should show version info
```

---

## Verification

After deployment, check Render logs:

**Expected Success Output:**
```
🔧 Installing system dependencies for OCR...
📦 Installing Tesseract OCR...
Processing triggers for hicolor-icon-theme...
✅ Verifying Tesseract installation...
tesseract 4.1.1
OCR Engine modes:
  0 Legacy engine only.
  1 Neural nets LSTM engine only.
  2 Legacy + LSTM engines.
🎉 System dependencies installed successfully!
```

**Then your app deploys normally:**
```
Building Python environment...
Installing dependencies from requirements.txt...
Running start command...
INFO: Uvicorn running on http://0.0.0.0:10000
```

---

## Testing After Deployment

1. **Login** with your verified email
2. **Upload a PDF or image**
3. **Click Process**
4. **Should now work!** ✅

---

## If Still Not Working

### Check 1: Build Script Ran?
Look in Render logs for:
- `🔧 Installing system dependencies`
- `tesseract --version` output

If not there, build script didn't run.

### Check 2: Tesseract Version
Should output something like:
```
tesseract 4.1.1
```

If you see `tesseract: command not found`, installation failed.

### Check 3: Python Dependencies
Make sure `requirements.txt` has:
```
pytesseract==0.3.10
pdf2image==1.16.3
opencv-python==4.8.1.78
```

---

## Files Added

1. **`build.sh`** - Build script to install Tesseract
2. **`render.yaml`** - Configuration file telling Render how to build

---

## Next Steps

1. **Push changes:**
   ```bash
   git add . && git commit -m "Add Render build configuration" && git push
   ```

2. **Redeploy on Render:**
   - Go to dashboard
   - Click **Redeploy** on your service
   - Wait for build (check logs)

3. **Test OCR:**
   - Login to app
   - Upload file
   - Should work now!

---

## Troubleshooting

| Issue | Check | Fix |
|-------|-------|-----|
| Build script not running | Render logs | Use Option 2: manual config |
| Tesseract not found | OCR upload error | Try full redeploy (not just restart) |
| Build takes long | Normal | First build takes 3-5 min |
| Still 500 error | Render logs | Check for other errors |

---

Let me know once you've pushed and redeployed, then test the OCR upload! 🚀
