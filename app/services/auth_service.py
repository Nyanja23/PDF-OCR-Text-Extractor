"""
app/services/auth_service.py
Authentication business logic
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Tuple

from app.models.user import User, Session as UserSession, OTP
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password, verify_password, generate_session_id,
    generate_otp, get_session_expiry, get_otp_expiry,
    constant_time_compare
)
from app.core.exceptions import (
    BadRequestException, UnauthorizedException,
    ConflictException, NotFoundException
)


class AuthService:
    """Authentication service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: UserCreate) -> Tuple[User, str]:
        """
        Register a new user and generate verification email OTP
        Note: Email sending is handled separately in the router (background task)
        Returns (user, otp_code)
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_user:
            raise ConflictException("Email already registered")
        
        # Create new user with email verification required
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name,
            is_verified=False  # Email verification required
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Generate OTP for email verification (email sent in background by router)
        otp_code = self._create_otp(user.id, "email_verification")
        
        return user, otp_code
    
    def verify_email(self, email: str, code: str) -> User:
        """Verify user email with OTP"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            raise NotFoundException("User not found")
        
        if user.is_verified:
            raise BadRequestException("Email already verified")
        
        # Find valid OTP
        otp = self.db.query(OTP).filter(
            OTP.user_id == user.id,
            OTP.purpose == "email_verification",
            OTP.is_used == False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            raise BadRequestException("No verification code found")
        
        if otp.is_expired():
            raise BadRequestException("Verification code expired")
        
        if not constant_time_compare(otp.code, code):
            raise BadRequestException("Invalid verification code")
        
        # Mark OTP as used
        otp.is_used = True
        
        # Verify user
        user.is_verified = True
        user.reset_failed_login()
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def login(self, email: str, password: str, ip_address: str, user_agent: str) -> Tuple[User, str]:
        """
        Authenticate user and create session
        Returns (user, session_id)
        """
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            raise UnauthorizedException("Invalid credentials")
        
        # Check if email is verified
        if not user.is_verified:
            raise UnauthorizedException("Please verify your email before logging in. Check your inbox for the verification code.")
        
        # Check if account is locked
        if user.is_locked():
            raise UnauthorizedException("Account is temporarily locked. Try again later.")
        
        # Verify password
        if not user.hashed_password or not verify_password(password, user.hashed_password):
            user.increment_failed_login()
            self.db.commit()
            raise UnauthorizedException("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise UnauthorizedException("Account is inactive")
        
        # Reset failed login attempts
        user.reset_failed_login()
        
        # Create session
        session_id = generate_session_id()
        session = UserSession(
            session_id=session_id,
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=get_session_expiry()
        )
        
        self.db.add(session)
        self.db.commit()
        
        return user, session_id
    
    def logout(self, session_id: str) -> bool:
        """Logout user by deleting session"""
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        
        return False
    
    def request_password_reset(self, email: str) -> str:
        """Request password reset and send OTP"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            # Don't reveal if user exists
            return "If the email exists, a reset code has been sent"
        
        if user.is_oauth:
            raise BadRequestException("OAuth users cannot reset password")
        
        # Generate and send OTP
        otp_code = self._create_otp(user.id, "password_reset")
        send_otp_email(user.email, otp_code, "password_reset")
        
        return "Password reset code sent to email"
    
    def reset_password(self, email: str, code: str, new_password: str) -> User:
        """Reset password with OTP"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user:
            raise NotFoundException("User not found")
        
        if user.is_oauth:
            raise BadRequestException("OAuth users cannot reset password")
        
        # Find valid OTP
        otp = self.db.query(OTP).filter(
            OTP.user_id == user.id,
            OTP.purpose == "password_reset",
            OTP.is_used == False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            raise BadRequestException("No reset code found")
        
        if otp.is_expired():
            raise BadRequestException("Reset code expired")
        
        if not constant_time_compare(otp.code, code):
            raise BadRequestException("Invalid reset code")
        
        # Mark OTP as used
        otp.is_used = True
        
        # Update password
        user.hashed_password = hash_password(new_password)
        user.reset_failed_login()
        
        # Invalidate all sessions
        self.db.query(UserSession).filter(
            UserSession.user_id == user.id
        ).delete()
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def create_oauth_user(self, email: str, full_name: str, provider: str) -> User:
        """Create or get OAuth user"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if user:
            # User exists, update OAuth info if needed
            if not user.is_oauth:
                user.is_oauth = True
                user.oauth_provider = provider
            user.is_verified = True  # OAuth users are pre-verified
            self.db.commit()
            self.db.refresh(user)
            return user
        
        # Create new OAuth user
        user = User(
            email=email,
            full_name=full_name,
            is_verified=True,
            is_oauth=True,
            oauth_provider=provider
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def _create_otp(self, user_id: int, purpose: str) -> str:
        """Create OTP for user"""
        # Invalidate previous OTPs of same purpose
        self.db.query(OTP).filter(
            OTP.user_id == user_id,
            OTP.purpose == purpose,
            OTP.is_used == False
        ).update({"is_used": True})
        
        # Create new OTP
        code = generate_otp()
        otp = OTP(
            user_id=user_id,
            code=code,
            purpose=purpose,
            expires_at=get_otp_expiry()
        )
        
        self.db.add(otp)
        self.db.commit()
        
        return code
