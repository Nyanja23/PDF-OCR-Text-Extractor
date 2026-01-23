#!/bin/bash
# Complete OCR test flow for verified user

set -e

RENDER_URL="https://pdf-ocr-text-extractor-kqk7.onrender.com"
EMAIL="nyanja.joseph@student.utamu.ac.ug"
PASSWORD="YourPassword123!"  # Change this to your actual password

echo "============================================"
echo "🔍 Complete OCR Test Flow"
echo "============================================"
echo ""

# Step 1: Login to get session
echo "Step 1️⃣  LOGIN"
echo "━━━━━━━━━━━━"
echo "Email: $EMAIL"
echo ""

LOGIN_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

echo "Response:"
echo "$LOGIN_RESPONSE" | jq . 2>/dev/null || echo "$LOGIN_RESPONSE"
echo ""

# Extract session from response or cookies
SESSION_ID=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token' 2>/dev/null)
if [ -z "$SESSION_ID" ] || [ "$SESSION_ID" = "null" ]; then
    echo "❌ Login failed!"
    echo "Make sure your password is correct"
    exit 1
fi

echo "✅ Login successful!"
echo "Session Token: ${SESSION_ID:0:20}..."
echo ""

# Step 2: Test OCR with sample file
echo "Step 2️⃣  TEST OCR UPLOAD"
echo "━━━━━━━━━━━━━━━━━━"

# Create a simple test image (1x1 pixel PNG with text)
TEST_FILE="/tmp/test_ocr.txt"
echo "Hello World OCR Test" > "$TEST_FILE"

# Try uploading
echo "Uploading test file: $TEST_FILE"
echo ""

OCR_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/ocr/upload" \
  -H "Cookie: session_id=$SESSION_ID" \
  -F "file=@$TEST_FILE" \
  -F "language=eng")

echo "Response:"
echo "$OCR_RESPONSE" | jq . 2>/dev/null || echo "$OCR_RESPONSE"
echo ""

# Check if successful
JOB_ID=$(echo "$OCR_RESPONSE" | jq -r '.job_id' 2>/dev/null)
if [ ! -z "$JOB_ID" ] && [ "$JOB_ID" != "null" ]; then
    echo "✅ OCR upload successful!"
    echo "Job ID: $JOB_ID"
    echo ""
    
    # Step 3: Get result
    echo "Step 3️⃣  GET OCR RESULTS"
    echo "━━━━━━━━━━━━━━━━━━━"
    echo "Job ID: $JOB_ID"
    echo ""
    
    RESULT_RESPONSE=$(curl -s -X GET "$RENDER_URL/api/ocr/result/$JOB_ID" \
      -H "Cookie: session_id=$SESSION_ID")
    
    echo "Response:"
    echo "$RESULT_RESPONSE" | jq . 2>/dev/null || echo "$RESULT_RESPONSE"
    echo ""
    
    echo "============================================"
    echo "🎉 OCR TEST COMPLETE!"
    echo "============================================"
else
    echo "❌ OCR upload failed!"
    echo "Response:"
    echo "$OCR_RESPONSE"
    echo ""
    echo "Check Render logs for detailed error:"
    echo "1. Go to Render dashboard"
    echo "2. Select your service"
    echo "3. Go to Logs tab"
    echo "4. Look for error messages"
fi

# Cleanup
rm -f "$TEST_FILE"
