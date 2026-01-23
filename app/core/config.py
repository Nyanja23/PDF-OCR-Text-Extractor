"""
app/core/config.py
Configuration management using environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "PDF OCR Text Extractor"
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.onrender.com"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://*.onrender.com"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./ocr_app.db"
    
    # Security
    BCRYPT_ROUNDS: int = 12
    SESSION_DURATION_DAYS: int = 7
    OTP_EXPIRY_MINUTES: int = 15
    MAX_LOGIN_ATTEMPTS: int = 5
    RATE_LIMIT_WINDOW: int = 900  # 15 minutes in seconds
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".jpg", ".jpeg", ".png", ".tiff"]
    UPLOAD_DIR: str = "uploads"
    FILE_CLEANUP_HOURS: int = 1
    
    # Email Configuration (MailerSend HTTP API)
    MAILERSEND_API_KEY: str = ""  # MailerSend API token
    EMAIL_FROM: str = ""  # Must be verified domain email in MailerSend
    EMAIL_FROM_NAME: str = "PDF OCR Extractor"
    
    # OAuth (Google)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"
    
    # OCR Settings
    TESSERACT_CMD: str = "/usr/bin/tesseract"  # Path to tesseract binary
    DEFAULT_LANGUAGE: str = "eng"
    OCR_TIMEOUT_SECONDS: int = 30
    
    # Redis (for session storage - optional for MVP)
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
