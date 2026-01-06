"""
app/core/security.py
Security utilities for password hashing and token generation
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets
import random
import string

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS
)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def generate_session_id() -> str:
    """Generate a secure random session ID"""
    return secrets.token_urlsafe(32)


def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def get_session_expiry() -> datetime:
    """Get session expiry datetime"""
    return datetime.utcnow() + timedelta(days=settings.SESSION_DURATION_DAYS)


def get_otp_expiry() -> datetime:
    """Get OTP expiry datetime"""
    return datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)


def constant_time_compare(val1: str, val2: str) -> bool:
    """
    Constant time string comparison to prevent timing attacks
    """
    if len(val1) != len(val2):
        return False
    
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    
    return result == 0
