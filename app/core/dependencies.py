"""
app/core/dependencies.py
FastAPI dependency injection utilities
"""

from fastapi import Cookie, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User, Session as UserSession
from app.core.exceptions import UnauthorizedException


async def get_current_user(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from session cookie
    """
    if not session_id:
        raise UnauthorizedException("Not authenticated")
    
    # Get session from database
    session = db.query(UserSession).filter(
        UserSession.session_id == session_id
    ).first()
    
    if not session:
        raise UnauthorizedException("Invalid session")
    
    # Check if session is expired
    if session.is_expired():
        db.delete(session)
        db.commit()
        raise UnauthorizedException("Session expired")
    
    # Get user
    user = db.query(User).filter(User.id == session.user_id).first()
    
    if not user:
        raise UnauthorizedException("User not found")
    
    if not user.is_active:
        raise UnauthorizedException("Account is inactive")
    
    return user


async def get_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email address"
        )
    return current_user


async def get_optional_user(
    session_id: Optional[str] = Cookie(None, alias="session_id"),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to get current user if authenticated, None otherwise
    """
    try:
        return await get_current_user(session_id, db)
    except:
        return None
