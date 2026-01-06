"""
app/schemas/__init__.py
Package initialization for schemas
"""

# User schemas
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordChange
)

# Auth schemas
from app.schemas.auth import (
    OTPVerify,
    PasswordResetRequest,
    PasswordReset,
    TokenResponse
)

# OCR schemas
from app.schemas.ocr import (
    OCRResult,
    OCRResponse,
    OCRStatus
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "PasswordChange",
    # Auth
    "OTPVerify",
    "PasswordResetRequest",
    "PasswordReset",
    "TokenResponse",
    # OCR
    "OCRResult",
    "OCRResponse",
    "OCRStatus",
]