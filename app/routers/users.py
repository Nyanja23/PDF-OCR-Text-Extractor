"""
app/routers/users.py
User management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, PasswordChange
from app.core.security import hash_password, verify_password
from app.core.exceptions import BadRequestException, UnauthorizedException


router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Get user profile"""
    return UserResponse.from_orm(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # Update full name
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    
    # Update email only if it's different from current email
    if update_data.email is not None and update_data.email != current_user.email:
        # Check if email already exists
        existing = db.query(User).filter(
            User.email == update_data.email,
            User.id != current_user.id
        ).first()
        
        if existing:
            raise BadRequestException("Email already in use")
        
        # In production, this should trigger email verification
        current_user.email = update_data.email
        current_user.is_verified = False  # Require re-verification only for actual email change
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # OAuth users cannot change password
    if current_user.is_oauth:
        raise BadRequestException("OAuth users cannot change password")
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise UnauthorizedException("Current password is incorrect")
    
    # Update password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    # Delete user (cascades to sessions and OTPs)
    db.delete(current_user)
    db.commit()
    
    return {"message": "Account deleted successfully"}
