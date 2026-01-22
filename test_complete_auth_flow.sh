#!/bin/bash
# Complete registration, email verification, and login test

set -e  # Exit on error

RENDER_URL="https://pdf-ocr-text-extractor-kqk7.onrender.com"
TIMESTAMP=$(date +%s)
TEST_EMAIL="test.user.${TIMESTAMP}@gmail.com"
TEST_PASSWORD="TestPassword123!"
TEST_NAME="Test User ${TIMESTAMP}"

echo "============================================"
echo "📋 Complete Auth Flow Test"
echo "============================================"
echo ""

# Step 1: Register
echo "Step 1️⃣  REGISTER"
echo "━━━━━━━━━━━━━━━━━━"
echo "Email: $TEST_EMAIL"
echo "Password: $TEST_PASSWORD"
echo "Name: $TEST_NAME"
echo ""

REGISTER_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"full_name\": \"$TEST_NAME\"
  }")

echo "Response:"
echo "$REGISTER_RESPONSE" | jq . 2>/dev/null || echo "$REGISTER_RESPONSE"
echo ""

# Extract info
USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.user_id' 2>/dev/null)
if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
    echo "❌ Registration failed!"
    exit 1
fi

echo "✅ Registration successful!"
echo "User ID: $USER_ID"
echo ""

# Step 2: Check for OTP in logs (simulated)
echo "Step 2️⃣  EMAIL VERIFICATION CODE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⏳ In production, check email: $TEST_EMAIL"
echo "🔍 Look for 6-digit code in email subject: 'Verify Your Email - PDF OCR Extractor'"
echo ""
echo "For local testing with development mode:"
echo "📋 Check Render logs for line: '✉️ Email sent to $TEST_EMAIL'"
echo "📋 Extract the OTP code from the email content"
echo ""
read -p "Enter the 6-digit OTP code (or press Enter to skip verification test): " OTP_CODE

if [ ! -z "$OTP_CODE" ]; then
    echo ""
    echo "Step 3️⃣  VERIFY EMAIL"
    echo "━━━━━━━━━━━━━━━━━━━"
    echo "Email: $TEST_EMAIL"
    echo "Code: $OTP_CODE"
    echo ""
    
    VERIFY_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/auth/verify-email" \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"$TEST_EMAIL\",
        \"code\": \"$OTP_CODE\"
      }")
    
    echo "Response:"
    echo "$VERIFY_RESPONSE" | jq . 2>/dev/null || echo "$VERIFY_RESPONSE"
    echo ""
    
    VERIFIED=$(echo "$VERIFY_RESPONSE" | jq -r '.message' 2>/dev/null | grep -i "success" || echo "")
    if [ -z "$VERIFIED" ]; then
        echo "❌ Email verification failed!"
        echo "Make sure the code is correct and not expired (15 min timeout)"
        exit 1
    fi
    
    echo "✅ Email verified successfully!"
    echo ""
    
    # Step 4: Login
    echo "Step 4️⃣  LOGIN"
    echo "━━━━━━━━━━━"
    echo "Email: $TEST_EMAIL"
    echo "Password: $TEST_PASSWORD"
    echo ""
    
    LOGIN_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/auth/login" \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"$TEST_EMAIL\",
        \"password\": \"$TEST_PASSWORD\"
      }")
    
    echo "Response:"
    echo "$LOGIN_RESPONSE" | jq . 2>/dev/null || echo "$LOGIN_RESPONSE"
    echo ""
    
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token' 2>/dev/null)
    if [ ! -z "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
        echo "✅ Login successful!"
        echo "Access Token: ${ACCESS_TOKEN:0:20}..."
        echo ""
        echo "============================================"
        echo "🎉 ALL TESTS PASSED!"
        echo "============================================"
        echo ""
        echo "✅ Registration works"
        echo "✅ Email verification works"
        echo "✅ Login works"
    else
        echo "❌ Login failed!"
        exit 1
    fi
else
    echo "⏭️  Skipping email verification test"
    echo ""
    echo "To test the complete flow:"
    echo "1. Run this script again"
    echo "2. When prompted, enter the 6-digit code from email"
fi

echo ""
echo "Test email: $TEST_EMAIL"
echo "For future reference, you can use this email to test login"
