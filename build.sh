#!/bin/bash
# Build script for Render - Install system dependencies

set -e  # Exit on error

echo "🔧 Installing system dependencies for OCR..."

# Update package list
apt-get update

# Install Tesseract OCR and dependencies
echo "📦 Installing Tesseract OCR..."
apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libpq-dev \
    gcc \
    libgl1 \
    libglib2.0-0

# Verify tesseract installation
echo "✅ Verifying Tesseract installation..."
tesseract --version

echo "🎉 System dependencies installed successfully!"
