#!/bin/bash
# Test script for email verification on Render

RENDER_URL="https://pdf-ocr-text-extractor-kqk7.onrender.com"

echo "🧪 PDF OCR Email Verification Test"
echo "===================================="
echo ""

# Generate test email with timestamp
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123!"
TEST_NAME="Test User"

echo "📧 Step 1: Creating test account..."
echo "Email: $TEST_EMAIL"
echo "Password: $TEST_PASSWORD"
echo ""

# Register
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

# Extract user_id if available
USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.user_id' 2>/dev/null)
if [ ! -z "$USER_ID" ] && [ "$USER_ID" != "null" ]; then
    echo "✅ Account created with ID: $USER_ID"
    echo ""
    echo "📧 Step 2: Check your email for verification code"
    echo "Email: $TEST_EMAIL"
    echo "Check inbox/spam folder for: 'Verify Your Email - PDF OCR Extractor'"
    echo ""
    echo "🔐 Step 3: To complete verification, use this endpoint:"
    echo "POST $RENDER_URL/api/auth/verify-email"
    echo "Body:"
    echo "{"
    echo "  \"email\": \"$TEST_EMAIL\","
    echo "  \"code\": \"XXXXXX\"  (6-digit code from email)"
    echo "}"
else
    echo "❌ Registration failed"
fi
