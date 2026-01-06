"""
app/core/security.py
Security utilities for password hashing and token generation
(with heavy debugging prints)
"""
import bcrypt
# from passlib.context import CryptContext  Removed during debugging
from datetime import datetime, timedelta
import secrets
import random
import string
import traceback

from app.core.config import settings

print("[security.py] Loading security module...")

# Fake the missing attribute so passlib's version check doesn't crash
if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('About', (), {'__version__': bcrypt.__version__})()



# Password hashing context
try:
    print("[security.py] Creating CryptContext with bcrypt...")
  
    print(f"[security.py] CryptContext created successfully. Rounds: {settings.BCRYPT_ROUNDS}")
except Exception as e:
    print("[security.py] FAILED to create CryptContext!")
    print(traceback.format_exc())
    raise

def hash_password(password: str) -> str:
    """Hash a password using bcrypt with safe truncation"""
    print("\n[hash_password] ENTERED (direct bcrypt)")
    print(f"  Input length: {len(password)} chars")

    pw_bytes = _truncate_password(password).encode('utf-8')
    print(f"  Bytes to hash: {len(pw_bytes)}")

    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS))
    return hashed.decode('utf-8')  # store as string in DB

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    print("[verify_password] ENTERED (direct bcrypt)")
    pw_bytes = _truncate_password(plain_password).encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pw_bytes, hashed_bytes)

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """Truncate a unicode string so its UTF-8 encoding is at most `max_bytes` bytes."""
    print("[_truncate_password] ENTERED")
    print(f"  Original length: {len(password)} chars")

    if not isinstance(password, str):
        print("  Converting non-string to str")
        password = str(password)

    try:
        encoded = password.encode("utf-8")
        print(f"  Original UTF-8 length: {len(encoded)} bytes")
    except Exception as e:
        print(f"  Encoding failed: {e}")
        raise

    if len(encoded) <= max_bytes:
        print("  No truncation needed")
        return password

    print(f"  Truncation required! Max allowed: {max_bytes} bytes")

    acc = bytearray()
    for ch in password:
        try:
            b = ch.encode("utf-8")
        except Exception as e:
            print(f"  Failed to encode char {repr(ch)}: {e}")
            continue

        if len(acc) + len(b) > max_bytes:
            print(f"  Stopped at char {repr(ch)} - would exceed limit")
            break
        acc.extend(b)

    result = acc.decode("utf-8", errors="ignore")
    print(f"  Truncated result length: {len(result)} chars")
    print(f"  Truncated UTF-8 length: {len(result.encode('utf-8'))} bytes")

    return result


def generate_session_id() -> str:
    """Generate a secure random session ID"""
    sid = secrets.token_urlsafe(32)
    print(f"[generate_session_id] Generated: {sid[:12]}...{sid[-12:]}")
    return sid


def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    code = ''.join(random.choices(string.digits, k=6))
    print(f"[generate_otp] Generated: {code}")
    return code


def get_session_expiry() -> datetime:
    """Get session expiry datetime"""
    expiry = datetime.utcnow() + timedelta(days=settings.SESSION_DURATION_DAYS)
    print(f"[get_session_expiry] Expiry set to: {expiry}")
    return expiry


def get_otp_expiry() -> datetime:
    """Get OTP expiry datetime"""
    expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    print(f"[get_otp_expiry] OTP expiry: {expiry}")
    return expiry


def constant_time_compare(val1: str, val2: str) -> bool:
    """Constant time string comparison to prevent timing attacks"""
    print(f"[constant_time_compare] Comparing lengths: {len(val1)} vs {len(val2)}")
    if len(val1) != len(val2):
        print("  Length mismatch → False")
        return False
    
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    
    equal = result == 0
    print(f"  Comparison result: {'equal' if equal else 'NOT equal'}")
    return equal


print("[security.py] Module loaded successfully")